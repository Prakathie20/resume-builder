from flask import Flask, render_template, request, send_file, jsonify
from fpdf import FPDF
import os
from datetime import datetime
import re
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

print("🚀 Resume Builder Started - Using Local AI Improvements")

class PDF(FPDF):
    def header(self):
        # No header for professional template
        pass
    
    def footer(self):
        # Add page number
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

class ResumeTemplates:
    @staticmethod
    def professional_template(pdf, data):
        """Professional template matching your CV structure"""
        # Set Unicode font that supports bullet points
        pdf.add_page()
        
        # Name - Top Center
        pdf.set_font("Arial", 'B', 24)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 15, data['name'], ln=True, align='C')
        
        # Contact Information with LinkedIn and GitHub
        pdf.set_font("Arial", '', 11)
        pdf.set_text_color(100, 100, 100)
        
        contact_parts = []
        if data.get('phone'):
            contact_parts.append(data['phone'])
        if data.get('email'):
            contact_parts.append(data['email'])
        if data.get('linkedin'):
            contact_parts.append("LinkedIn")
        if data.get('github'):
            contact_parts.append("GitHub")
        if data.get('address'):
            contact_parts.append(data['address'])
        
        contact_info = " | ".join(contact_parts)
        pdf.cell(0, 8, contact_info, ln=True, align='C')
        pdf.ln(10)
        
        # Career Objective
        if data.get('objective'):
            pdf.set_font("Arial", 'B', 16)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, "Career Objective", ln=True, align='L')
            pdf.set_font("Arial", '', 11)
            pdf.set_text_color(80, 80, 80)
            pdf.multi_cell(0, 6, data['objective'])
            pdf.ln(8)
        
        # Education Section
        if data.get('education'):
            pdf.set_font("Arial", 'B', 16)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, "Education", ln=True, align='L')
            pdf.set_font("Arial", '', 11)
            pdf.set_text_color(80, 80, 80)
            pdf.multi_cell(0, 6, data['education'])
            pdf.ln(8)
        
        # Projects Section
        if data.get('applications'):
            pdf.set_font("Arial", 'B', 16)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, "Projects", ln=True, align='L')
            pdf.set_font("Arial", '', 11)
            pdf.set_text_color(80, 80, 80)
            pdf.multi_cell(0, 6, data['applications'])
            pdf.ln(8)
        
        # Internship Section
        if data.get('certifications'):  # Using certifications field for internship
            pdf.set_font("Arial", 'B', 16)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, "Internship", ln=True, align='L')
            pdf.set_font("Arial", '', 11)
            pdf.set_text_color(80, 80, 80)
            pdf.multi_cell(0, 6, data['certifications'])
            pdf.ln(8)
        
        # Technical Skills
        if data.get('skills'):
            pdf.set_font("Arial", 'B', 16)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, "Technical Skills", ln=True, align='L')
            pdf.set_font("Arial", '', 11)
            pdf.set_text_color(80, 80, 80)
            pdf.multi_cell(0, 6, data['skills'])
            pdf.ln(8)
        
        # Area of Interest
        if data.get('interests'):
            pdf.set_font("Arial", 'B', 16)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, "Area of Interest", ln=True, align='L')
            pdf.set_font("Arial", '', 11)
            pdf.set_text_color(80, 80, 80)
            pdf.multi_cell(0, 6, data['interests'])
            pdf.ln(8)
        
        # Certifications
        if data.get('events'):  # Using events field for certifications
            pdf.set_font("Arial", 'B', 16)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, "Certifications", ln=True, align='L')
            pdf.set_font("Arial", '', 11)
            pdf.set_text_color(80, 80, 80)
            pdf.multi_cell(0, 6, data['events'])
            pdf.ln(8)
        
        # Achievements
        if data.get('english'):  # Using english field for achievements
            pdf.set_font("Arial", 'B', 16)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, "Achievements", ln=True, align='L')
            pdf.set_font("Arial", '', 11)
            pdf.set_text_color(80, 80, 80)
            pdf.multi_cell(0, 6, data['english'])
            pdf.ln(8)

def improve_with_ai(section, content):
    """Local AI improvement - No API calls needed!"""
    print(f"=== 🤖 LOCAL AI IMPROVEMENT ===")
    print(f"Section: {section}")
    print(f"Original: '{content}'")
    
    if not content.strip():
        return content
    
    # Basic text improvements
    improved = content.strip()
    
    # Clean up formatting - replace bullet points with dashes
    improved = improved.replace('•', '-')
    improved = re.sub(r'\n\s*\n', '\n\n', improved)  # Remove extra blank lines
    improved = re.sub(r' +', ' ', improved)  # Remove extra spaces
    
    # Section-specific improvements
    if section == 'objective':
        # Make objective more professional
        improved = improved.capitalize()
        if not improved.endswith('.'):
            improved += '.'
        
        # Common objective improvements
        objective_keywords = {
            'become': 'pursue a position as',
            'want to': 'seeking to',
            'need to': 'aspiring to become',
            'like to': 'aiming to secure a role as',
            'get a job as': 'pursue a career as'
        }
        
        for old, new in objective_keywords.items():
            if old in improved.lower():
                improved = improved.lower().replace(old, new)
                improved = improved.capitalize()
        
        # Ensure it sounds professional
        if 'seeking' not in improved.lower() and 'aspiring' not in improved.lower() and 'pursuing' not in improved.lower():
            if improved.lower().startswith('to '):
                improved = 'Seeking ' + improved[3:]
            else:
                improved = 'Seeking to ' + improved.lower()
    
    elif section == 'skills':
        # Organize skills with categories and bullet points (using dashes)
        lines = improved.split('\n')
        organized_lines = []
        current_category = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if ':' in line and len(line) < 50:  # Likely a category
                current_category = line
                organized_lines.append(current_category)
            else:
                # Skill item - add dash point
                if not line.startswith('-'):
                    line = '- ' + line
                organized_lines.append(line)
        
        improved = '\n'.join(organized_lines)
        
        # Add common skill categories if missing
        if ':' not in improved:
            skill_categories = {
                'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby'],
                'web': ['html', 'css', 'react', 'angular', 'vue', 'django', 'flask'],
                'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'oracle'],
                'tools': ['git', 'docker', 'jenkins', 'aws', 'azure', 'linux']
            }
            
            categorized_skills = []
            uncategorized_skills = []
            
            for line in improved.split('\n'):
                line = line.strip()
                if line.startswith('-'):
                    skill = line[2:].strip().lower()
                    categorized = False
                    
                    for category, keywords in skill_categories.items():
                        if any(keyword in skill for keyword in keywords):
                            if category.capitalize() + ':' not in categorized_skills:
                                categorized_skills.append(category.capitalize() + ':')
                            categorized_skills.append('- ' + line[2:].strip())
                            categorized = True
                            break
                    
                    if not categorized:
                        uncategorized_skills.append(line)
            
            if categorized_skills:
                improved = '\n'.join(categorized_skills)
                if uncategorized_skills:
                    improved += '\nOther Skills:\n' + '\n'.join(uncategorized_skills)
    
    elif section == 'education':
        # Format education entries professionally
        lines = improved.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Add degree/duration if missing
            if ' - ' not in line and not any(word in line.lower() for word in ['bachelor', 'master', 'degree', 'diploma', 'certificate']):
                line += " - Course/Degree"
            
            formatted_lines.append(line)
        
        improved = '\n'.join(formatted_lines)
    
    elif section == 'english':
        # Format language skills or achievements
        if 'english' not in improved.lower():
            improved = f"Achievements: {improved}"
    
    elif section == 'interests':
        # Format interests professionally
        lines = improved.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('-'):
                formatted_lines.append('- ' + line)
            else:
                formatted_lines.append(line)
        
        improved = '\n'.join(formatted_lines)
    
    print(f"✅ Improved: '{improved}'")
    print("==========================")
    
    return improved

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/debug-ai")
def debug_ai():
    """Debug route to check AI configuration"""
    return """
    <h1>AI Debug Information</h1>
    <p>🤖 AI Status: <strong>Local AI Improvements Active</strong></p>
    <p>✅ No API keys required</p>
    <p>✅ No internet connection required</p>
    <p>✅ Instant improvements</p>
    <p><a href="/">← Back to Resume Builder</a></p>
    """

@app.route("/improve-content", methods=["POST"])
def improve_content():
    """AI endpoint to improve specific sections"""
    try:
        data = request.json
        section = data.get('section', '')
        content = data.get('content', '')
        
        print(f"=== AI IMPROVEMENT REQUEST ===")
        print(f"Section: {section}")
        print(f"Content: '{content}'")
        
        if not content or not content.strip():
            return jsonify({"error": "Please enter some content to improve."}), 400
        
        if not section:
            return jsonify({"error": "Section not specified."}), 400
        
        # Use local AI improvements
        improved = improve_with_ai(section, content)
        
        return jsonify({
            "improved_content": improved,
            "section": section,
            "success": True,
            "ai_type": "local",
            "message": "Improved using local AI"
        })
        
    except Exception as e:
        print(f"❌ AI Route Error: {e}")
        return jsonify({"error": f"AI service error: {str(e)}"}), 500

@app.route("/build-resume", methods=["POST"])
def build_resume():
    try:
        # Get EXACT form data from user - including new LinkedIn and GitHub fields
        data = {
            'name': request.form.get('name', ''),
            'email': request.form.get('email', ''),
            'phone': request.form.get('phone', ''),
            'address': request.form.get('address', ''),
            'linkedin': request.form.get('linkedin', ''),
            'github': request.form.get('github', ''),
            'objective': request.form.get('objective', ''),
            'education': request.form.get('education', ''),
            'english': request.form.get('english', ''),
            'skills': request.form.get('skills', ''),
            'interests': request.form.get('interests', ''),
            'certifications': request.form.get('certifications', ''),
            'applications': request.form.get('applications', ''),
            'events': request.form.get('events', '')
        }
        
        template_choice = 'professional'  # Force professional template
        
        print("=== USER PROVIDED DATA ===")
        for key, value in data.items():
            if value:
                print(f"{key}: {value}")
        print(f"Selected Template: {template_choice}")
        print("==========================")
        
        # Apply AI improvements ONLY if user enables the checkbox
        ai_enabled = request.form.get('ai_improvement') == 'on'
        
        if ai_enabled:
            print("=== APPLYING LOCAL AI IMPROVEMENTS ===")
            # Improve sections that commonly need enhancement
            sections_to_improve = ['objective', 'skills', 'education', 'english', 'interests']
            
            for section in sections_to_improve:
                if data[section] and data[section].strip():
                    original = data[section]
                    data[section] = improve_with_ai(section, data[section])
                    if original != data[section]:
                        print(f"✅ Improved {section}")
                        print(f"   Before: {original}")
                        print(f"   After:  {data[section]}")
                    else:
                        print(f"✅ No changes needed for {section}")
        else:
            print("ℹ️  AI improvement not enabled by user")
        
        # Create PDF with chosen template
        pdf = PDF()
        
        templates = {
            'professional': ResumeTemplates.professional_template
        }
        
        template_func = templates.get(template_choice, ResumeTemplates.professional_template)
        
        print(f"=== USING TEMPLATE: {template_choice} ===")
        template_func(pdf, data)
        
        # Save PDF
        filename = f"resume_{data['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(filename)
        
        print(f"✅ PDF generated: {filename}")
        
        return send_file(filename, as_attachment=True, download_name=f"{data['name']}_Resume.pdf")
        
    except Exception as e:
        print(f"❌ Error generating resume: {e}")
        return f"Error generating resume: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)