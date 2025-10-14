from flask import Flask, render_template, request, send_file, jsonify
from fpdf import FPDF
import os
from datetime import datetime
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize OpenAI (optional - only if API key is provided)
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    openai.api_key = openai_api_key

class ResumeTemplates:
    @staticmethod
    def praktikis_template(pdf, data):
        """Template matching your exact format"""
        # Name and Title - Centered at top
        pdf.set_font("Arial", 'B', 24)
        pdf.cell(0, 15, data['name'], ln=True, align='C')
        
        # Contact Information
        pdf.set_font("Arial", 'I', 10)
        contact_info = f"{data.get('email', '')} | {data.get('phone', '')}"
        if data.get('address'):
            contact_info += f" | {data['address']}"
        pdf.cell(0, 8, contact_info, ln=True, align='C')
        pdf.ln(5)
        
        # Cursor Objective
        if data.get('objective'):
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 12, "Cursor Objective", ln=True, align='L')
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 6, data['objective'])
            pdf.ln(5)
        
        # Education Section
        if data.get('education'):
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 12, "Education", ln=True, align='L')
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 6, data['education'])
            pdf.ln(3)
        
        # English Section
        if data.get('english'):
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 12, "English", ln=True, align='L')
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 6, data['english'])
            pdf.ln(3)
        
        # Technical Skills
        if data.get('skills'):
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 12, "Technical Skills", ln=True, align='L')
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 6, data['skills'])
            pdf.ln(3)
        
        # Area of Interest
        if data.get('interests'):
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 12, "Area of Interest", ln=True, align='L')
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 6, data['interests'])
            pdf.ln(3)
        
        # Certification
        if data.get('certifications'):
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 12, "Certification", ln=True, align='L')
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 6, data['certifications'])
            pdf.ln(3)
        
        # Application
        if data.get('applications'):
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 12, "Application", ln=True, align='L')
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 6, data['applications'])
            pdf.ln(3)
        
        # Events & Participation
        if data.get('events'):
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 12, "Events & Participation", ln=True, align='L')
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 6, data['events'])
        
        # Add template identifier
        pdf.set_y(270)
        pdf.set_font("Arial", 'I', 8)
        pdf.cell(0, 10, "Template: Professional Format", ln=True, align='C')

    @staticmethod
    def modern_template(pdf, data):
        """Modern clean template"""
        # Header with background
        pdf.set_fill_color(44, 62, 80)
        pdf.rect(0, 0, 210, 50, 'F')
        
        # Name
        pdf.set_font("Arial", 'B', 24)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 20, data['name'], ln=True, align='C')
        
        # Contact info
        pdf.set_font("Arial", '', 12)
        contact_info = f"{data.get('email','')} | {data.get('phone','')}"
        if data.get('address'):
            contact_info += f" | {data['address']}"
        pdf.cell(0, 8, contact_info, ln=True, align='C')
        
        pdf.ln(20)
        pdf.set_text_color(0, 0, 0)
        
        # Sections - ONLY show sections that have user content
        sections = [
            ('PROFESSIONAL OBJECTIVE', data.get('objective')),
            ('EDUCATION', data.get('education')),
            ('TECHNICAL SKILLS', data.get('skills')),
            ('LANGUAGE SKILLS', data.get('english')),
            ('CERTIFICATIONS', data.get('certifications')),
            ('PROJECTS', data.get('applications')),
            ('INTERESTS', data.get('interests')),
            ('EVENTS', data.get('events'))
        ]
        
        for title, content in sections:
            if content and content.strip():  # Only show if user provided content
                # Modern section styling
                pdf.set_font("Arial", 'B', 16)
                pdf.set_text_color(44, 62, 80)
                pdf.set_fill_color(240, 240, 240)
                pdf.cell(0, 10, f" {title} ", ln=True, fill=True)
                pdf.set_font("Arial", '', 11)
                pdf.set_text_color(0, 0, 0)
                pdf.multi_cell(0, 6, content)
                pdf.ln(5)
        
        # Add template identifier
        pdf.set_y(270)
        pdf.set_font("Arial", 'I', 8)
        pdf.cell(0, 10, "Template: Modern Style", ln=True, align='C')

    @staticmethod
    def professional_template(pdf, data):
        """Professional corporate template"""
        # Header with light gray background
        pdf.set_fill_color(240, 240, 240)
        pdf.rect(0, 0, 210, 35, 'F')
        
        # Name
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(0, 12, data['name'], ln=True, align='C')
        
        # Contact info
        pdf.set_font("Arial", 'I', 11)
        contact_lines = []
        if data.get('email'):
            contact_lines.append(data['email'])
        if data.get('phone'):
            contact_lines.append(data['phone'])
        if data.get('address'):
            contact_lines.append(data['address'])
        
        contact_info = " | ".join(contact_lines)
        pdf.cell(0, 8, contact_info, ln=True, align='C')
        
        pdf.ln(15)
        
        # Two column layout
        left_x = 15
        right_x = 115
        width = 80
        
        # Left column - Only include sections that have content
        y_start = pdf.get_y()
        left_sections = []
        
        if data.get('education'):
            left_sections.append(("EDUCATION", data['education']))
        if data.get('skills'):
            left_sections.append(("TECHNICAL SKILLS", data['skills']))
        if data.get('certifications'):
            left_sections.append(("CERTIFICATIONS", data['certifications']))
        
        # Render left sections
        pdf.set_x(left_x)
        for title, content in left_sections:
            pdf.set_font("Arial", 'B', 14)
            pdf.set_text_color(44, 62, 80)
            pdf.cell(width, 10, title, ln=True)
            pdf.set_font("Arial", '', 10)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(width, 5, content)
            pdf.ln(3)
        
        # Right column - Only include sections that have content
        pdf.set_xy(right_x, y_start)
        right_sections = []
        
        if data.get('objective'):
            right_sections.append(("PROFESSIONAL OBJECTIVE", data['objective']))
        if data.get('english'):
            right_sections.append(("LANGUAGE SKILLS", data['english']))
        if data.get('applications'):
            right_sections.append(("PROJECTS", data['applications']))
        if data.get('interests'):
            right_sections.append(("INTERESTS", data['interests']))
        if data.get('events'):
            right_sections.append(("EVENTS & PARTICIPATION", data['events']))
        
        # Render right sections
        for title, content in right_sections:
            pdf.set_font("Arial", 'B', 14)
            pdf.set_text_color(44, 62, 80)
            pdf.cell(width, 10, title, ln=True)
            pdf.set_font("Arial", '', 10)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(width, 5, content)
            pdf.ln(3)
        
        # Add template identifier
        pdf.set_y(270)
        pdf.set_font("Arial", 'I', 8)
        pdf.cell(0, 10, "Template: Corporate Style", ln=True, align='C')

def improve_with_ai(section, content):
    """Improve content with AI - ALWAYS improves when called"""
    if not openai_api_key or not content.strip():
        return content
    
    try:
        print(f"=== AI IMPROVEMENT REQUESTED ===")
        print(f"Section: {section}")
        print(f"Original: '{content}'")
        
        # Different prompts for different sections
        prompts = {
            'objective': f"""Improve this resume objective to make it professional and compelling:
            "{content}"
            
            Make it:
            - Professional and business-appropriate
            - Specific about career goals
            - Value-oriented for employers
            - 2-3 sentences maximum
            
            Improved version:""",
            
            'skills': f"""Organize and improve these technical skills for a professional resume:
            "{content}"
            
            Please:
            - Group related skills into categories
            - Use professional terminology
            - Make it well-organized and easy to read
            - Include relevant technical categories
            
            Organized skills:""",
            
            'education': f"""Improve this education section for a professional resume:
            "{content}"
            
            Make it:
            - Properly formatted
            - Include relevant details
            - Professional and clear
            - Well-structured
            
            Improved education:""",
            
            'english': f"""Improve this language skills description:
            "{content}"
            
            Make it professional and well-structured:"""
        }
        
        prompt = prompts.get(section, f"""Improve this resume content for the {section} section:
        "{content}"
        
        Make it professional and well-written:""")
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a professional resume writer. Always improve the given content to be more professional, well-structured, and suitable for a resume. Return only the improved content."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        improved_content = response.choices[0].message.content.strip()
        
        print(f"Improved: '{improved_content}'")
        print(f"Content changed: {improved_content != content}")
        print("==========================")
        
        return improved_content
        
    except Exception as e:
        print(f"AI Improvement Error: {e}")
        return content

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/improve-content", methods=["POST"])
def improve_content():
    """AI endpoint to improve specific sections"""
    if not openai_api_key:
        return jsonify({"error": "AI features not configured. Please add your OpenAI API key to use AI improvements."}), 400
    
    try:
        data = request.json
        section = data.get('section', '')
        content = data.get('content', '')
        
        print(f"=== AI IMPROVEMENT API CALL ===")
        print(f"Section: {section}")
        print(f"Content: '{content}'")
        
        if not content or not content.strip():
            return jsonify({"error": "Please enter some content to improve."}), 400
        
        if not section:
            return jsonify({"error": "Section not specified."}), 400
        
        # ALWAYS try to improve when this endpoint is called
        improved = improve_with_ai(section, content)
        
        return jsonify({
            "improved_content": improved,
            "section": section,
            "success": True
        })
        
    except Exception as e:
        print(f"AI Route Error: {e}")
        return jsonify({"error": f"AI service error: {str(e)}"}), 500

@app.route("/build-resume", methods=["POST"])
def build_resume():
    try:
        # Get EXACT form data from user
        data = {
            'name': request.form.get('name', ''),
            'email': request.form.get('email', ''),
            'phone': request.form.get('phone', ''),
            'address': request.form.get('address', ''),
            'objective': request.form.get('objective', ''),
            'education': request.form.get('education', ''),
            'english': request.form.get('english', ''),
            'skills': request.form.get('skills', ''),
            'interests': request.form.get('interests', ''),
            'certifications': request.form.get('certifications', ''),
            'applications': request.form.get('applications', ''),
            'events': request.form.get('events', '')
        }
        
        template_choice = request.form.get('template', 'praktikis')
        
        print("=== USER PROVIDED DATA ===")
        for key, value in data.items():
            if value:
                print(f"{key}: {value}")
        print(f"Selected Template: {template_choice}")
        print("==========================")
        
        # Apply AI improvements ONLY if user enables the checkbox
        ai_enabled = request.form.get('ai_improvement') == 'on'
        
        if ai_enabled and openai_api_key:
            print("=== APPLYING AI IMPROVEMENTS ===")
            # Improve sections that commonly need enhancement
            sections_to_improve = ['objective', 'skills', 'education']
            
            for section in sections_to_improve:
                if data[section] and data[section].strip():
                    original = data[section]
                    data[section] = improve_with_ai(section, data[section])
                    if original != data[section]:
                        print(f"✅ Improved {section}")
                        print(f"   Before: {original}")
                        print(f"   After:  {data[section]}")
                    else:
                        print(f"⚠️  No changes for {section}")
        else:
            if not openai_api_key:
                print("❌ AI not configured - skipping improvements")
            else:
                print("❌ AI improvement not enabled by user")
        
        # Create PDF with chosen template
        pdf = FPDF()
        pdf.add_page()
        
        templates = {
            'praktikis': ResumeTemplates.praktikis_template,
            'modern': ResumeTemplates.modern_template,
            'professional': ResumeTemplates.professional_template
        }
        
        template_func = templates.get(template_choice, ResumeTemplates.praktikis_template)
        
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