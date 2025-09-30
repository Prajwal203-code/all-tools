import os
import time
import pandas as pd
import qrcode
from PIL import Image, ImageDraw, ImageFont
import zipfile
import json
import re
import secrets
import string
from datetime import datetime, timedelta
import calendar

class ProductivityProcessor:
    def __init__(self):
        self.output_dir = 'output'
        os.makedirs(self.output_dir, exist_ok=True)
    
    def process(self, tool_name, data, task_id):
        """Main processing method that routes to specific tool handlers"""
        
        time.sleep(1)  # Initial setup time
        
        method_map = {
            'bulk_renamer': self.rename_files,
            'file_format_converter': self.convert_file_formats,
            'signature_generator': self.generate_signature,
            'certificate_generator': self.generate_certificates,
            'badge_generator': self.generate_badges,
            'calendar_generator': self.generate_calendar,
            'qr_generator': self.generate_qr_codes,
            'password_generator': self.generate_passwords,
            'ascii_generator': self.generate_ascii_art,
            'template_generator': self.generate_templates,
            'resume_builder': self.build_resume,
            'email_template_generator': self.generate_email_templates,
            'bulk_text_replacer': self.replace_text_bulk,
            'metadata_editor': self.edit_metadata,
            'version_tracker': self.track_versions
        }
        
        handler = method_map.get(tool_name)
        if not handler:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        return handler(data, task_id)
    
    def update_progress(self, task_id, progress):
        """Update task progress"""
        from app import TaskManager
        TaskManager.update_progress(task_id, progress)
    
    def rename_files(self, data, task_id):
        """Rename multiple files with a pattern"""
        self.update_progress(task_id, 20)
        
        files = data.get('files', [])
        pattern = data.get('pattern', 'file_{index}')
        
        renamed_files = []
        
        for i, file_info in enumerate(files):
            original_path = file_info['filepath']
            original_name = os.path.basename(original_path)
            file_ext = os.path.splitext(original_name)[1]
            
            # Generate new name
            new_name = pattern.replace('{index}', str(i + 1).zfill(3))
            new_name = new_name.replace('{original}', os.path.splitext(original_name)[0])
            new_name = new_name.replace('{date}', datetime.now().strftime('%Y%m%d'))
            
            if not new_name.endswith(file_ext):
                new_name += file_ext
            
            # Copy file with new name
            new_path = os.path.join(self.output_dir, f"{task_id}_{new_name}")
            
            try:
                import shutil
                shutil.copy2(original_path, new_path)
                
                renamed_files.append({
                    'original_name': original_name,
                    'new_name': new_name,
                    'status': 'Success'
                })
                
            except Exception as e:
                renamed_files.append({
                    'original_name': original_name,
                    'new_name': new_name,
                    'status': f'Error: {str(e)}'
                })
            
            progress = 20 + (60 * (i + 1) / len(files))
            self.update_progress(task_id, progress)
        
        # Create report
        df = pd.DataFrame(renamed_files)
        report_path = os.path.join(self.output_dir, f"{task_id}_rename_report.xlsx")
        df.to_excel(report_path, index=False)
        
        # Create ZIP with renamed files and report
        zip_path = os.path.join(self.output_dir, f"{task_id}_renamed_files.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(report_path, os.path.basename(report_path))
            
            # Add renamed files to ZIP
            for file_data in renamed_files:
                if file_data['status'] == 'Success':
                    file_path = os.path.join(self.output_dir, f"{task_id}_{file_data['new_name']}")
                    if os.path.exists(file_path):
                        zipf.write(file_path, file_data['new_name'])
                        os.remove(file_path)
            
            os.remove(report_path)
        
        self.update_progress(task_id, 100)
        return {'output_path': zip_path, 'filename': os.path.basename(zip_path)}
    
    def convert_file_formats(self, data, task_id):
        """Convert between different file formats"""
        self.update_progress(task_id, 30)
        
        files = data.get('files', [])
        target_format = data.get('target_format', 'txt')
        
        converted_files = []
        
        for i, file_info in enumerate(files):
            input_path = file_info['filepath']
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            
            try:
                if target_format.lower() == 'txt':
                    # Convert to text
                    output_path = os.path.join(self.output_dir, f"{task_id}_{base_name}.txt")
                    
                    # Simple conversion based on file type
                    if input_path.endswith('.csv'):
                        df = pd.read_csv(input_path)
                        df.to_string(output_path, index=False)
                    elif input_path.endswith(('.xlsx', '.xls')):
                        df = pd.read_excel(input_path)
                        df.to_string(output_path, index=False)
                    else:
                        # Copy as text
                        with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        with open(output_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                    
                    converted_files.append(output_path)
                    
                elif target_format.lower() == 'json':
                    # Convert to JSON
                    output_path = os.path.join(self.output_dir, f"{task_id}_{base_name}.json")
                    
                    if input_path.endswith('.csv'):
                        df = pd.read_csv(input_path)
                        df.to_json(output_path, orient='records', indent=2)
                    elif input_path.endswith(('.xlsx', '.xls')):
                        df = pd.read_excel(input_path)
                        df.to_json(output_path, orient='records', indent=2)
                    else:
                        # Create simple JSON structure
                        with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        
                        json_data = {
                            'filename': os.path.basename(input_path),
                            'content': content,
                            'converted_at': datetime.now().isoformat()
                        }
                        
                        with open(output_path, 'w') as f:
                            json.dump(json_data, f, indent=2)
                    
                    converted_files.append(output_path)
                
            except Exception as e:
                # Create error file
                error_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_error.txt")
                with open(error_path, 'w') as f:
                    f.write(f"Error converting {base_name}: {str(e)}")
                converted_files.append(error_path)
            
            progress = 30 + (60 * (i + 1) / len(files))
            self.update_progress(task_id, progress)
        
        # Create ZIP
        zip_path = os.path.join(self.output_dir, f"{task_id}_converted_files.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_path in converted_files:
                zipf.write(file_path, os.path.basename(file_path))
                os.remove(file_path)
        
        self.update_progress(task_id, 100)
        return {'output_path': zip_path, 'filename': os.path.basename(zip_path)}
    
    def generate_signature(self, data, task_id):
        """Generate digital signature"""
        self.update_progress(task_id, 30)
        
        signature_text = data.get('signature_text', 'John Doe')
        font_size = int(data.get('font_size', 50))
        
        # Create signature image
        img_width, img_height = 400, 150
        img = Image.new('RGBA', (img_width, img_height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Get text dimensions
        bbox = draw.textbbox((0, 0), signature_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center text
        x = (img_width - text_width) // 2
        y = (img_height - text_height) // 2
        
        # Draw signature in cursive style (simulated with italic-like effect)
        draw.text((x, y), signature_text, font=font, fill=(0, 0, 0, 255))
        
        # Add underline
        underline_y = y + text_height + 5
        draw.line([(x, underline_y), (x + text_width, underline_y)], fill=(0, 0, 0, 255), width=2)
        
        # Save signature
        output_path = os.path.join(self.output_dir, f"{task_id}_signature.png")
        img.save(output_path, 'PNG')
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def generate_certificates(self, data, task_id):
        """Generate certificates from names list"""
        self.update_progress(task_id, 20)
        
        files = data.get('files', [])
        certificate_title = data.get('title', 'Certificate of Achievement')
        
        if not files:
            raise ValueError("No names file provided")
        
        # Read names
        input_path = files[0]['filepath']
        try:
            if input_path.endswith('.csv'):
                df = pd.read_csv(input_path)
                names = df.iloc[:, 0].tolist()  # First column
            else:
                df = pd.read_excel(input_path)
                names = df.iloc[:, 0].tolist()  # First column
        except Exception as e:
            raise ValueError(f"Error reading names file: {str(e)}")
        
        certificate_files = []
        
        for i, name in enumerate(names[:50]):  # Limit to 50 certificates
            # Create certificate
            cert_width, cert_height = 800, 600
            cert = Image.new('RGB', (cert_width, cert_height), (255, 255, 255))
            draw = ImageDraw.Draw(cert)
            
            # Draw border
            border_margin = 20
            draw.rectangle([border_margin, border_margin, cert_width - border_margin, cert_height - border_margin], 
                          outline=(0, 0, 0), width=3)
            
            # Certificate content
            try:
                title_font = ImageFont.truetype("arial.ttf", 36)
                name_font = ImageFont.truetype("arial.ttf", 48)
                text_font = ImageFont.truetype("arial.ttf", 20)
            except:
                title_font = ImageFont.load_default()
                name_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
            
            # Title
            title_bbox = draw.textbbox((0, 0), certificate_title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            draw.text(((cert_width - title_width) // 2, 100), certificate_title, font=title_font, fill=(0, 0, 0))
            
            # "This is to certify that"
            certify_text = "This is to certify that"
            certify_bbox = draw.textbbox((0, 0), certify_text, font=text_font)
            certify_width = certify_bbox[2] - certify_bbox[0]
            draw.text(((cert_width - certify_width) // 2, 200), certify_text, font=text_font, fill=(0, 0, 0))
            
            # Name
            name_bbox = draw.textbbox((0, 0), str(name), font=name_font)
            name_width = name_bbox[2] - name_bbox[0]
            draw.text(((cert_width - name_width) // 2, 250), str(name), font=name_font, fill=(0, 0, 0))
            
            # Achievement text
            achievement_text = "has successfully completed the requirements"
            achievement_bbox = draw.textbbox((0, 0), achievement_text, font=text_font)
            achievement_width = achievement_bbox[2] - achievement_bbox[0]
            draw.text(((cert_width - achievement_width) // 2, 350), achievement_text, font=text_font, fill=(0, 0, 0))
            
            # Date
            date_text = f"Date: {datetime.now().strftime('%B %d, %Y')}"
            date_bbox = draw.textbbox((0, 0), date_text, font=text_font)
            draw.text((100, 450), date_text, font=text_font, fill=(0, 0, 0))
            
            # Signature line
            draw.text((500, 450), "Signature: ___________________", font=text_font, fill=(0, 0, 0))
            
            # Save certificate
            safe_name = re.sub(r'[^\w\s-]', '', str(name)).strip().replace(' ', '_')
            cert_path = os.path.join(self.output_dir, f"{task_id}_certificate_{safe_name}.png")
            cert.save(cert_path, 'PNG')
            certificate_files.append(cert_path)
            
            # Update progress
            progress = 20 + (70 * (i + 1) / len(names))
            self.update_progress(task_id, progress)
        
        # Create ZIP
        zip_path = os.path.join(self.output_dir, f"{task_id}_certificates.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for cert_path in certificate_files:
                zipf.write(cert_path, os.path.basename(cert_path))
                os.remove(cert_path)
        
        self.update_progress(task_id, 100)
        return {'output_path': zip_path, 'filename': os.path.basename(zip_path)}
    
    def generate_badges(self, data, task_id):
        """Generate badges for events/teams"""
        self.update_progress(task_id, 30)
        
        files = data.get('files', [])
        event_name = data.get('event_name', 'Conference 2024')
        
        if not files:
            raise ValueError("No names file provided")
        
        # Read names and info
        input_path = files[0]['filepath']
        try:
            if input_path.endswith('.csv'):
                df = pd.read_csv(input_path)
            else:
                df = pd.read_excel(input_path)
        except Exception as e:
            raise ValueError(f"Error reading file: {str(e)}")
        
        badge_files = []
        
        for i, row in df.iterrows():
            name = str(row.iloc[0])  # First column as name
            company = str(row.iloc[1]) if len(row) > 1 else ""
            
            # Create badge
            badge_width, badge_height = 400, 300
            badge = Image.new('RGB', (badge_width, badge_height), (255, 255, 255))
            draw = ImageDraw.Draw(badge)
            
            # Draw border
            draw.rectangle([5, 5, badge_width - 5, badge_height - 5], outline=(0, 0, 0), width=2)
            
            # Event name header
            header_rect = [10, 10, badge_width - 10, 60]
            draw.rectangle(header_rect, fill=(70, 130, 180))
            
            try:
                event_font = ImageFont.truetype("arial.ttf", 20)
                name_font = ImageFont.truetype("arial.ttf", 24)
                company_font = ImageFont.truetype("arial.ttf", 16)
            except:
                event_font = ImageFont.load_default()
                name_font = ImageFont.load_default()
                company_font = ImageFont.load_default()
            
            # Event name
            event_bbox = draw.textbbox((0, 0), event_name, font=event_font)
            event_width = event_bbox[2] - event_bbox[0]
            draw.text(((badge_width - event_width) // 2, 25), event_name, font=event_font, fill=(255, 255, 255))
            
            # Name
            name_bbox = draw.textbbox((0, 0), name, font=name_font)
            name_width = name_bbox[2] - name_bbox[0]
            draw.text(((badge_width - name_width) // 2, 120), name, font=name_font, fill=(0, 0, 0))
            
            # Company
            if company and company != 'nan':
                company_bbox = draw.textbbox((0, 0), company, font=company_font)
                company_width = company_bbox[2] - company_bbox[0]
                draw.text(((badge_width - company_width) // 2, 160), company, font=company_font, fill=(100, 100, 100))
            
            # Save badge
            safe_name = re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')
            badge_path = os.path.join(self.output_dir, f"{task_id}_badge_{safe_name}.png")
            badge.save(badge_path, 'PNG')
            badge_files.append(badge_path)
            
            # Update progress
            progress = 30 + (60 * (i + 1) / len(df))
            self.update_progress(task_id, progress)
        
        # Create ZIP
        zip_path = os.path.join(self.output_dir, f"{task_id}_badges.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for badge_path in badge_files:
                zipf.write(badge_path, os.path.basename(badge_path))
                os.remove(badge_path)
        
        self.update_progress(task_id, 100)
        return {'output_path': zip_path, 'filename': os.path.basename(zip_path)}
    
    def generate_calendar(self, data, task_id):
        """Generate printable calendar"""
        self.update_progress(task_id, 30)
        
        year = int(data.get('year', datetime.now().year))
        month = int(data.get('month', datetime.now().month)) if data.get('month') else None
        
        if month:
            # Generate single month calendar
            cal = calendar.monthcalendar(year, month)
            month_name = calendar.month_name[month]
            
            calendar_data = {
                'year': year,
                'month': month_name,
                'weeks': []
            }
            
            # Add week headers
            headers = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            
            for week in cal:
                week_data = []
                for day in week:
                    week_data.append(day if day != 0 else '')
                calendar_data['weeks'].append(week_data)
            
            # Create DataFrame for Excel export
            df_data = []
            df_data.append(headers)
            for week in calendar_data['weeks']:
                df_data.append([str(day) if day else '' for day in week])
            
            df = pd.DataFrame(df_data)
            output_path = os.path.join(self.output_dir, f"{task_id}_calendar_{year}_{month:02d}.xlsx")
            df.to_excel(output_path, index=False, header=False)
            
        else:
            # Generate full year calendar
            year_cal = calendar.calendar(year, w=2, l=1, c=6, m=3)
            
            output_path = os.path.join(self.output_dir, f"{task_id}_calendar_{year}.txt")
            with open(output_path, 'w') as f:
                f.write(f"Calendar for {year}\n")
                f.write("=" * 50 + "\n\n")
                f.write(year_cal)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def generate_qr_codes(self, data, task_id):
        """Generate QR codes"""
        self.update_progress(task_id, 30)
        
        urls = data.get('urls', [])
        texts = data.get('texts', [])
        
        if not urls and not texts:
            raise ValueError("No URLs or texts provided")
        
        qr_files = []
        items_to_process = urls + texts
        
        for i, item in enumerate(items_to_process):
            try:
                # Create QR code
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(item)
                qr.make(fit=True)
                
                # Create QR code image
                img = qr.make_image(fill_color="black", back_color="white")
                
                # Save QR code
                safe_name = re.sub(r'[^\w\s-]', '', str(item)[:20]).strip().replace(' ', '_')
                qr_path = os.path.join(self.output_dir, f"{task_id}_qr_{i+1}_{safe_name}.png")
                img.save(qr_path)
                qr_files.append(qr_path)
                
            except Exception as e:
                # Create error file
                error_path = os.path.join(self.output_dir, f"{task_id}_qr_{i+1}_error.txt")
                with open(error_path, 'w') as f:
                    f.write(f"Error creating QR code for: {item}\nError: {str(e)}")
                qr_files.append(error_path)
            
            # Update progress
            progress = 30 + (60 * (i + 1) / len(items_to_process))
            self.update_progress(task_id, progress)
        
        # Create ZIP if multiple files
        if len(qr_files) > 1:
            zip_path = os.path.join(self.output_dir, f"{task_id}_qr_codes.zip")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for qr_path in qr_files:
                    zipf.write(qr_path, os.path.basename(qr_path))
                    os.remove(qr_path)
            final_output = zip_path
        else:
            final_output = qr_files[0]
        
        self.update_progress(task_id, 100)
        return {'output_path': final_output, 'filename': os.path.basename(final_output)}
    
    def generate_passwords(self, data, task_id):
        """Generate secure random passwords"""
        self.update_progress(task_id, 30)
        
        count = int(data.get('count', 10))
        length = int(data.get('length', 12))
        include_symbols = data.get('include_symbols', True)
        include_numbers = data.get('include_numbers', True)
        
        # Character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        numbers = string.digits if include_numbers else ''
        symbols = '!@#$%^&*()_+-=[]{}|;:,.<>?' if include_symbols else ''
        
        all_chars = lowercase + uppercase + numbers + symbols
        
        passwords = []
        
        for i in range(count):
            # Ensure password has at least one character from each selected set
            password_chars = [
                secrets.choice(lowercase),
                secrets.choice(uppercase)
            ]
            
            if include_numbers:
                password_chars.append(secrets.choice(numbers))
            if include_symbols:
                password_chars.append(secrets.choice(symbols))
            
            # Fill remaining length
            remaining_length = length - len(password_chars)
            for _ in range(remaining_length):
                password_chars.append(secrets.choice(all_chars))
            
            # Shuffle the password
            secrets.SystemRandom().shuffle(password_chars)
            password = ''.join(password_chars)
            
            passwords.append({
                'password_id': i + 1,
                'password': password,
                'length': len(password),
                'strength': self.calculate_password_strength(password)
            })
            
            # Update progress
            progress = 30 + (60 * (i + 1) / count)
            self.update_progress(task_id, progress)
        
        # Create DataFrame and save
        df = pd.DataFrame(passwords)
        output_path = os.path.join(self.output_dir, f"{task_id}_passwords.xlsx")
        df.to_excel(output_path, index=False)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def calculate_password_strength(self, password):
        """Calculate password strength"""
        score = 0
        
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'[A-Z]', password):
            score += 1
        if re.search(r'\d', password):
            score += 1
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            score += 1
        
        if score <= 2:
            return 'Weak'
        elif score <= 4:
            return 'Medium'
        else:
            return 'Strong'
    
    # Simplified implementations for remaining methods
    def generate_ascii_art(self, data, task_id):
        self.update_progress(task_id, 50)
        text = data.get('text', 'ASCII ART')
        output_path = os.path.join(self.output_dir, f"{task_id}_ascii_art.txt")
        
        # Simple ASCII art generation
        ascii_art = f"""
  ___  _____ _____ _____ _____   ___  ____ _____ 
 / _ \/ ____/  ___/  ___/  ___| / _ \| __ \_   _|
/ /_\ \ (___\ `--.\ `--.\ `--. / /_\ \  \/  | |  
|  _  |\___ \`--. \`--. \`--. \|  _  | |\/| | |  
| | | |/\__/ /\__/ /\__/ /\__/ /| | | | |  | | |  
\_| |_/\____/\____/\____/\____/ \_| |_|_|  |_|_|  

Text: {text}
        """
        
        with open(output_path, 'w') as f:
            f.write(ascii_art)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def generate_templates(self, data, task_id):
        self.update_progress(task_id, 50)
        template_type = data.get('template_type', 'invoice')
        output_path = os.path.join(self.output_dir, f"{task_id}_{template_type}_template.html")
        
        template_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{template_type.title()} Template</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; }}
        .content {{ margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{template_type.title()} Template</h1>
    </div>
    <div class="content">
        <p>This is a basic {template_type} template.</p>
        <p>Customize this template according to your needs.</p>
    </div>
</body>
</html>
        """
        
        with open(output_path, 'w') as f:
            f.write(template_html)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def build_resume(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_resume.html")
        # Placeholder implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def generate_email_templates(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_email_template.html")
        # Placeholder implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def replace_text_bulk(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_text_replaced.zip")
        # Placeholder implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def edit_metadata(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_metadata_edited.zip")
        # Placeholder implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def track_versions(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_version_report.xlsx")
        # Placeholder implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}