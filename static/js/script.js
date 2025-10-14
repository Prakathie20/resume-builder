document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.resume-form');
    const aiImprovementToggle = document.getElementById('aiImprovement');
    const aiImproveBtns = document.querySelectorAll('.ai-improve-btn');
    const modal = document.getElementById('aiModal');
    const originalContent = document.getElementById('originalContent');
    const improvedContent = document.getElementById('improvedContent');
    const useImprovedBtn = document.getElementById('useImproved');
    const keepOriginalBtn = document.getElementById('keepOriginal');
    const warningMessage = document.getElementById('warningMessage');
    
    let currentTextarea = null;
    let currentSection = '';

    // Check if required fields are filled
    function checkRequiredFields() {
        const nameField = document.getElementById('name');
        const emailField = document.getElementById('email');
        const phoneField = document.getElementById('phone');
        
        return nameField.value.trim() !== '' && 
               emailField.value.trim() !== '' && 
               phoneField.value.trim() !== '';
    }

    // Show required fields warning
    function showRequiredFieldsWarning() {
        warningMessage.classList.add('show');
        
        // Highlight empty required fields
        const requiredFields = ['name', 'email', 'phone'];
        requiredFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (!field.value.trim()) {
                field.classList.add('field-error');
                
                // Remove highlighting after 3 seconds
                setTimeout(() => {
                    field.classList.remove('field-error');
                }, 3000);
            }
        });
        
        // Hide warning after 5 seconds
        setTimeout(() => {
            warningMessage.classList.remove('show');
        }, 5000);
    }

    // Form validation
    form.addEventListener('submit', function(e) {
        let isValid = true;
        const requiredFields = form.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add('field-error');
            } else {
                field.classList.remove('field-error');
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            alert('Please fill in all required fields (marked with *).');
        } else {
            // Show loading state
            const submitBtn = form.querySelector('.generate-btn');
            submitBtn.classList.add('loading');
        }
    });

    // Auto-resize textareas
    const textareas = form.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        
        // Trigger initial resize
        setTimeout(() => {
            textarea.style.height = 'auto';
            textarea.style.height = (textarea.scrollHeight) + 'px';
        }, 100);
    });

    // AI Improvement buttons with validation
    aiImproveBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const section = this.dataset.section;
            const textarea = document.getElementById(section);
            
            // Check if required fields are filled first
            if (!checkRequiredFields()) {
                showRequiredFieldsWarning();
                return;
            }
            
            if (!textarea.value.trim()) {
                alert('Please enter some content to improve in this section.');
                textarea.classList.add('field-error');
                
                // Remove highlighting after 2 seconds
                setTimeout(() => {
                    textarea.classList.remove('field-error');
                }, 2000);
                return;
            }
            
            currentTextarea = textarea;
            currentSection = section;
            
            showAIModal(textarea.value, section);
        });
    });

    // Toggle AI improvement availability
    aiImprovementToggle.addEventListener('change', function() {
        const isEnabled = this.checked;
        aiImproveBtns.forEach(btn => {
            if (isEnabled) {
                btn.style.display = 'block';
            } else {
                btn.style.display = 'none';
            }
        });
    });

    // Initially hide AI buttons if toggle is off
    if (!aiImprovementToggle.checked) {
        aiImproveBtns.forEach(btn => {
            btn.style.display = 'none';
        });
    }

    function showAIModal(content, section) {
        originalContent.textContent = content;
        improvedContent.textContent = 'Improving with AI...';
        
        modal.style.display = 'block';
        
        // Disable buttons during AI processing
        useImprovedBtn.disabled = true;
        keepOriginalBtn.disabled = true;
        
        // Call AI improvement
        fetch('/improve-content', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                section: section,
                content: content
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.improved_content) {
                improvedContent.textContent = data.improved_content;
            } else if (data.error) {
                improvedContent.textContent = 'Error: ' + data.error;
            } else {
                improvedContent.textContent = 'Error improving content. Please try again.';
            }
            
            useImprovedBtn.disabled = false;
            keepOriginalBtn.disabled = false;
        })
        .catch(error => {
            console.error('Error:', error);
            improvedContent.textContent = 'Error improving content. Please check your connection and make sure you have filled all required fields.';
            useImprovedBtn.disabled = false;
            keepOriginalBtn.disabled = false;
        });
    }

    // Modal actions
    useImprovedBtn.addEventListener('click', function() {
        if (currentTextarea) {
            currentTextarea.value = improvedContent.textContent;
            // Trigger resize
            currentTextarea.dispatchEvent(new Event('input'));
        }
        modal.style.display = 'none';
    });

    keepOriginalBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Real-time validation for required fields
    const requiredFields = ['name', 'email', 'phone'];
    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('input', function() {
                if (this.value.trim()) {
                    this.classList.remove('field-error');
                    this.classList.add('field-valid');
                    
                    // Remove green border after 1 second
                    setTimeout(() => {
                        this.classList.remove('field-valid');
                    }, 1000);
                }
            });
        }
    });

    // Auto-save form data
    function autoSaveForm() {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        localStorage.setItem('resumeBuilder_autosave', JSON.stringify(data));
    }

    function loadAutoSave() {
        const saved = localStorage.getItem('resumeBuilder_autosave');
        if (saved) {
            const data = JSON.parse(saved);
            Object.keys(data).forEach(key => {
                const element = form.querySelector(`[name="${key}"]`);
                if (element) {
                    element.value = data[key];
                    // Trigger resize for textareas
                    if (element.tagName === 'TEXTAREA') {
                        element.dispatchEvent(new Event('input'));
                    }
                }
            });
        }
    }

    // Initialize auto-save
    form.addEventListener('input', autoSaveForm);
    document.addEventListener('DOMContentLoaded', loadAutoSave);
});