import os
import time
import json
import pandas as pd
import requests
import zipfile
from urllib.parse import urlparse, parse_qs
import re
import tempfile

class DevProcessor:
    def __init__(self):
        self.output_dir = 'output'
        os.makedirs(self.output_dir, exist_ok=True)
    
    def process(self, tool_name, data, task_id):
        """Main processing method that routes to specific tool handlers"""
        
        time.sleep(1)  # Initial setup time
        
        method_map = {
            'html_pdf_converter': self.html_to_pdf,
            'markdown_converter': self.convert_markdown,
            'css_js_minifier': self.minify_css_js,
            'json_converter': self.convert_json,
            'api_tester': self.test_apis,
            'url_cleaner': self.clean_urls,
            'website_downloader': self.download_website,
            'url_response_checker': self.check_url_responses,
            'structured_data_generator': self.generate_structured_data,
            'multi_screenshot_pdf': self.screenshot_to_pdf
        }
        
        handler = method_map.get(tool_name)
        if not handler:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        return handler(data, task_id)
    
    def update_progress(self, task_id, progress):
        """Update task progress"""
        from app import TaskManager
        TaskManager.update_progress(task_id, progress)
    
    def html_to_pdf(self, data, task_id):
        """Convert HTML files to PDF"""
        self.update_progress(task_id, 20)
        
        files = data.get('files', [])
        urls = data.get('urls', [])
        
        output_files = []
        
        # Process files
        for i, file_info in enumerate(files):
            input_path = file_info['filepath']
            base_name = os.path.basename(input_path).split('.')[0]
            
            try:
                with open(input_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Simple HTML to text conversion (placeholder for PDF generation)
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')
                text_content = soup.get_text()
                
                # Save as text file (in real implementation, would use pdfkit)
                output_path = os.path.join(self.output_dir, f"{task_id}_{base_name}.txt")
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(f"HTML to PDF Conversion\n")
                    f.write(f"Original file: {base_name}.html\n")
                    f.write(f"Content:\n{text_content}")
                
                output_files.append(output_path)
                
            except Exception as e:
                error_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_error.txt")
                with open(error_path, 'w') as f:
                    f.write(f"Error converting {base_name}: {str(e)}")
                output_files.append(error_path)
            
            progress = 20 + (50 * (i + 1) / len(files)) if files else 70
            self.update_progress(task_id, progress)
        
        # Process URLs
        for i, url in enumerate(urls):
            try:
                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                text_content = soup.get_text()
                
                domain = urlparse(url).netloc
                output_path = os.path.join(self.output_dir, f"{task_id}_{domain.replace('.', '_')}.txt")
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(f"URL to PDF Conversion\n")
                    f.write(f"Source URL: {url}\n")
                    f.write(f"Content:\n{text_content}")
                
                output_files.append(output_path)
                
            except Exception as e:
                error_path = os.path.join(self.output_dir, f"{task_id}_url_{i+1}_error.txt")
                with open(error_path, 'w') as f:
                    f.write(f"Error converting {url}: {str(e)}")
                output_files.append(error_path)
            
            progress = 70 + (20 * (i + 1) / len(urls)) if urls else 90
            self.update_progress(task_id, progress)
        
        # Create ZIP if multiple files
        if len(output_files) > 1:
            zip_path = os.path.join(self.output_dir, f"{task_id}_html_to_pdf.zip")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file_path in output_files:
                    zipf.write(file_path, os.path.basename(file_path))
                    os.remove(file_path)
            final_output = zip_path
        else:
            final_output = output_files[0] if output_files else None
        
        self.update_progress(task_id, 100)
        return {'output_path': final_output, 'filename': os.path.basename(final_output)}
    
    def convert_markdown(self, data, task_id):
        """Convert Markdown to HTML/PDF"""
        self.update_progress(task_id, 20)
        
        files = data.get('files', [])
        text_input = data.get('text', '')
        output_format = data.get('format', 'html')
        
        markdown_content = ''
        
        if text_input:
            markdown_content = text_input
        elif files:
            input_path = files[0]['filepath']
            try:
                with open(input_path, 'r', encoding='utf-8') as f:
                    markdown_content = f.read()
            except Exception as e:
                raise ValueError(f"Error reading markdown file: {str(e)}")
        
        if not markdown_content:
            raise ValueError("No markdown content provided")
        
        self.update_progress(task_id, 50)
        
        # Simple markdown to HTML conversion
        html_content = markdown_content
        
        # Basic markdown parsing
        html_content = re.sub(r'^# (.*$)', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
        html_content = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
        html_content = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
        html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
        html_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html_content)
        html_content = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html_content)
        html_content = html_content.replace('\n', '<br>\n')
        
        # Wrap in basic HTML structure
        full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Converted Markdown</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #666; }}
        h3 {{ color: #999; }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""
        
        # Save output
        if output_format.lower() == 'html':
            output_path = os.path.join(self.output_dir, f"{task_id}_converted.html")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_html)
        else:
            # PDF format (simplified as text)
            output_path = os.path.join(self.output_dir, f"{task_id}_converted.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("Markdown to PDF Conversion\n")
                f.write("=" * 30 + "\n")
                f.write(markdown_content)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def minify_css_js(self, data, task_id):
        """Minify CSS and JavaScript files"""
        self.update_progress(task_id, 20)
        
        files = data.get('files', [])
        output_files = []
        
        for i, file_info in enumerate(files):
            input_path = file_info['filepath']
            base_name = os.path.basename(input_path)
            file_ext = os.path.splitext(base_name)[1].lower()
            
            try:
                with open(input_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Simple minification
                minified_content = content
                
                if file_ext == '.css':
                    # CSS minification
                    minified_content = re.sub(r'/\*.*?\*/', '', minified_content, flags=re.DOTALL)  # Remove comments
                    minified_content = re.sub(r'\s+', ' ', minified_content)  # Collapse whitespace
                    minified_content = re.sub(r';\s*}', '}', minified_content)  # Remove semicolon before }
                    minified_content = re.sub(r'{\s*', '{', minified_content)  # Remove space after {
                    minified_content = re.sub(r'}\s*', '}', minified_content)  # Remove space after }
                    
                elif file_ext == '.js':
                    # JavaScript minification (basic)
                    minified_content = re.sub(r'//.*$', '', minified_content, flags=re.MULTILINE)  # Remove line comments
                    minified_content = re.sub(r'/\*.*?\*/', '', minified_content, flags=re.DOTALL)  # Remove block comments
                    minified_content = re.sub(r'\s+', ' ', minified_content)  # Collapse whitespace
                    minified_content = re.sub(r';\s*', ';', minified_content)  # Remove space after ;
                
                # Save minified file
                output_name = f"{os.path.splitext(base_name)[0]}.min{file_ext}"
                output_path = os.path.join(self.output_dir, f"{task_id}_{output_name}")
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(minified_content)
                
                output_files.append(output_path)
                
                # Create report
                original_size = len(content)
                minified_size = len(minified_content)
                savings = ((original_size - minified_size) / original_size * 100) if original_size > 0 else 0
                
                report_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_report.txt")
                with open(report_path, 'w') as f:
                    f.write(f"Minification Report for {base_name}\n")
                    f.write(f"Original size: {original_size} bytes\n")
                    f.write(f"Minified size: {minified_size} bytes\n")
                    f.write(f"Space saved: {savings:.1f}%\n")
                
                output_files.append(report_path)
                
            except Exception as e:
                error_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_error.txt")
                with open(error_path, 'w') as f:
                    f.write(f"Error minifying {base_name}: {str(e)}")
                output_files.append(error_path)
            
            progress = 20 + (70 * (i + 1) / len(files))
            self.update_progress(task_id, progress)
        
        # Create ZIP
        zip_path = os.path.join(self.output_dir, f"{task_id}_minified_files.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_path in output_files:
                zipf.write(file_path, os.path.basename(file_path))
                os.remove(file_path)
        
        self.update_progress(task_id, 100)
        return {'output_path': zip_path, 'filename': os.path.basename(zip_path)}
    
    def convert_json(self, data, task_id):
        """Convert JSON files to CSV/Excel"""
        self.update_progress(task_id, 20)
        
        files = data.get('files', [])
        output_files = []
        
        for i, file_info in enumerate(files):
            input_path = file_info['filepath']
            base_name = os.path.basename(input_path).split('.')[0]
            
            try:
                with open(input_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                
                # Convert JSON to DataFrame
                if isinstance(json_data, list):
                    df = pd.DataFrame(json_data)
                elif isinstance(json_data, dict):
                    # Flatten nested JSON
                    flattened_data = []
                    for key, value in json_data.items():
                        if isinstance(value, dict):
                            for sub_key, sub_value in value.items():
                                flattened_data.append({
                                    'parent_key': key,
                                    'key': sub_key,
                                    'value': str(sub_value)
                                })
                        else:
                            flattened_data.append({
                                'parent_key': '',
                                'key': key,
                                'value': str(value)
                            })
                    df = pd.DataFrame(flattened_data)
                else:
                    df = pd.DataFrame([{'value': str(json_data)}])
                
                # Save as Excel
                output_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_converted.xlsx")
                df.to_excel(output_path, index=False)
                output_files.append(output_path)
                
                # Also save as CSV
                csv_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_converted.csv")
                df.to_csv(csv_path, index=False)
                output_files.append(csv_path)
                
            except Exception as e:
                error_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_error.txt")
                with open(error_path, 'w') as f:
                    f.write(f"Error converting {base_name}: {str(e)}")
                output_files.append(error_path)
            
            progress = 20 + (70 * (i + 1) / len(files))
            self.update_progress(task_id, progress)
        
        # Create ZIP
        zip_path = os.path.join(self.output_dir, f"{task_id}_json_converted.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_path in output_files:
                zipf.write(file_path, os.path.basename(file_path))
                os.remove(file_path)
        
        self.update_progress(task_id, 100)
        return {'output_path': zip_path, 'filename': os.path.basename(zip_path)}
    
    def test_apis(self, data, task_id):
        """Test multiple API endpoints"""
        self.update_progress(task_id, 20)
        
        urls = data.get('urls', [])
        if not urls:
            raise ValueError("No API URLs provided")
        
        results = []
        
        for i, url in enumerate(urls):
            try:
                start_time = time.time()
                response = requests.get(url, timeout=10)
                end_time = time.time()
                
                response_time = round((end_time - start_time) * 1000, 2)  # Convert to milliseconds
                
                results.append({
                    'url': url,
                    'status_code': response.status_code,
                    'response_time_ms': response_time,
                    'content_length': len(response.content),
                    'status': 'Success' if response.status_code == 200 else 'Error',
                    'error_message': '' if response.status_code == 200 else f"HTTP {response.status_code}"
                })
                
            except Exception as e:
                results.append({
                    'url': url,
                    'status_code': 'N/A',
                    'response_time_ms': 'N/A',
                    'content_length': 'N/A',
                    'status': 'Failed',
                    'error_message': str(e)
                })
            
            progress = 20 + (70 * (i + 1) / len(urls))
            self.update_progress(task_id, progress)
        
        # Create report
        df = pd.DataFrame(results)
        output_path = os.path.join(self.output_dir, f"{task_id}_api_test_results.xlsx")
        df.to_excel(output_path, index=False)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def clean_urls(self, data, task_id):
        """Clean URLs by removing tracking parameters"""
        self.update_progress(task_id, 30)
        
        urls = data.get('urls', [])
        if not urls:
            raise ValueError("No URLs provided")
        
        # Common tracking parameters to remove
        tracking_params = [
            'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term',
            'fbclid', 'gclid', 'dclid', '_ga', 'mc_eid', 'mc_cid',
            'ref', 'source', 'campaign', 'affiliate', 'partner'
        ]
        
        cleaned_urls = []
        
        for url in urls:
            try:
                parsed = urlparse(url)
                query_params = parse_qs(parsed.query)
                
                # Remove tracking parameters
                cleaned_params = {k: v for k, v in query_params.items() if k not in tracking_params}
                
                # Rebuild query string
                cleaned_query = '&'.join([f"{k}={v[0]}" for k, v in cleaned_params.items()])
                
                # Rebuild URL
                cleaned_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                if cleaned_query:
                    cleaned_url += f"?{cleaned_query}"
                if parsed.fragment:
                    cleaned_url += f"#{parsed.fragment}"
                
                cleaned_urls.append({
                    'original_url': url,
                    'cleaned_url': cleaned_url,
                    'parameters_removed': len(query_params) - len(cleaned_params),
                    'savings_chars': len(url) - len(cleaned_url)
                })
                
            except Exception as e:
                cleaned_urls.append({
                    'original_url': url,
                    'cleaned_url': url,
                    'parameters_removed': 0,
                    'savings_chars': 0,
                    'error': str(e)
                })
        
        self.update_progress(task_id, 80)
        
        # Create report
        df = pd.DataFrame(cleaned_urls)
        output_path = os.path.join(self.output_dir, f"{task_id}_cleaned_urls.xlsx")
        df.to_excel(output_path, index=False)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    # Simplified implementations for remaining methods
    def download_website(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_website_download.zip")
        with zipfile.ZipFile(output_path, 'w') as zipf:
            zipf.writestr('website_content.txt', 'Website content would be downloaded here')
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def check_url_responses(self, data, task_id):
        # This is similar to test_apis, so we can reuse that logic
        return self.test_apis(data, task_id)
    
    def generate_structured_data(self, data, task_id):
        self.update_progress(task_id, 50)
        
        # Generate sample JSON-LD structured data
        structured_data = {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": data.get('name', 'Sample Business'),
            "url": data.get('url', 'https://example.com'),
            "description": data.get('description', 'Professional business services'),
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "123 Business St",
                "addressLocality": "Business City",
                "postalCode": "12345",
                "addressCountry": "US"
            }
        }
        
        output_path = os.path.join(self.output_dir, f"{task_id}_structured_data.json")
        with open(output_path, 'w') as f:
            json.dump(structured_data, f, indent=2)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def screenshot_to_pdf(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_screenshots.pdf")
        # Placeholder implementation
        with open(output_path, 'w') as f:
            f.write("PDF with screenshots would be generated here")
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}