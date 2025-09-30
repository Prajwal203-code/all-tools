from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
import json
import time
import uuid
from werkzeug.utils import secure_filename
import threading
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'xlsx', 'xls', 'csv', 'txt', 'jpg', 'jpeg', 'png', 'gif', 'html', 'md', 'json'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Create directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Processing status tracking
processing_status = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_processing_time(tool_id):
    """Get estimated processing time for each tool"""
    processing_times = {
        # PDF & Document Tools (1-20)
        'pdf_to_word': 15, 'pdf_to_excel': 20, 'word_to_pdf': 10, 'excel_to_pdf': 12,
        'pdf_merger': 8, 'pdf_splitter': 10, 'pdf_editor': 25, 'pdf_compressor': 15,
        'pdf_ocr': 30, 'pdf_form_filler': 20, 'pdf_to_image': 12, 'image_to_pdf': 8,
        'pdf_watermark': 10, 'pdf_password': 5, 'pdf_metadata': 3, 'table_extractor': 25,
        'pdf_summary': 45, 'pdf_annotation': 20, 'pdf_reorder': 8, 'pdf_template': 15,
        
        # Excel & CSV Tools (21-30)
        'excel_to_csv': 5, 'csv_to_excel': 8, 'excel_deduplicator': 12, 'excel_cleaner': 15,
        'csv_validator': 8, 'csv_to_sql': 10, 'csv_json_converter': 6, 'excel_merger': 15,
        'pivot_table': 20, 'chart_generator': 18,
        
        # Image & Media Tools (31-45)
        'image_resizer': 8, 'image_compressor': 10, 'background_remover': 25, 'meme_generator': 5,
        'watermark_tool': 12, 'thumbnail_generator': 8, 'format_converter': 6, 'collage_maker': 15,
        'color_extractor': 8, 'ai_enhancer': 30, 'caption_generator': 20, 'image_ocr': 15,
        'gif_maker': 20, 'video_to_gif': 25, 'meme_template': 3,
        
        # Website & URL Tools (46-60)
        'url_summarizer': 30, 'keyword_scraper': 20, 'meta_extractor': 8, 'link_checker': 25,
        'sitemap_generator': 15, 'speed_analyzer': 30, 'link_visualizer': 20, 'share_preview': 10,
        'html_to_pdf': 12, 'screenshot_generator': 20, 'robots_validator': 8, 'redirect_checker': 15,
        'competitor_analyzer': 35, 'text_extractor': 10, 'web_archive': 18,
        
        # SEO & Marketing Tools (61-70)
        'keyword_suggestion': 15, 'backlink_analyzer': 45, 'keyword_gap': 30, 'seo_audit': 60,
        'meta_generator': 20, 'hashtag_generator': 10, 'post_scheduler': 5, 'email_extractor': 15,
        'email_validator': 25, 'meta_analyzer': 12,
        
        # AI & Automation Tools (71-80)
        'content_summarizer': 30, 'content_rewriter': 25, 'faq_generator': 35, 'product_description': 20,
        'subject_generator': 8, 'post_optimizer': 15, 'sentiment_analyzer': 20, 'competitor_report': 45,
        'table_extractor_ai': 30, 'text_translator': 25,
        
        # Developer & Code Tools (81-90)
        'html_pdf_converter': 10, 'markdown_converter': 8, 'css_js_minifier': 5, 'json_converter': 6,
        'api_tester': 20, 'url_cleaner': 3, 'content_downloader': 25, 'response_checker': 15,
        'structured_data': 8, 'multi_screenshot': 30,
        
        # Productivity & Miscellaneous Tools (91-105)
        'document_renamer': 5, 'format_converter': 8, 'signature_generator': 3, 'certificate_generator': 12,
        'badge_generator': 8, 'calendar_generator': 5, 'qr_generator': 2, 'password_generator': 1,
        'ascii_art': 8, 'template_generator': 15, 'resume_builder': 10, 'email_template': 8,
        'text_replacer': 10, 'metadata_editor': 8, 'version_tracker': 5
    }
    return processing_times.get(tool_id, 10)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tools')
def get_tools():
    """Get all available tools organized by category"""
    tools = {
        "PDF & Document Tools": {
            "Converters": [
                {"id": "pdf_to_word", "name": "PDF → Word Converter", "time": "15s", "description": "Convert PDFs into editable Word documents"},
                {"id": "pdf_to_excel", "name": "PDF → Excel Converter", "time": "20s", "description": "Extract tables from PDF to structured Excel"},
                {"id": "word_to_pdf", "name": "Word → PDF Converter", "time": "10s", "description": "Convert Word files to PDF format"},
                {"id": "excel_to_pdf", "name": "Excel → PDF Converter", "time": "12s", "description": "Convert Excel sheets into formatted PDF"},
                {"id": "pdf_to_image", "name": "PDF → Image Converter", "time": "12s", "description": "Convert each PDF page into image files"},
                {"id": "image_to_pdf", "name": "Image → PDF Converter", "time": "8s", "description": "Combine multiple images into a single PDF"}
            ],
            "PDF Manipulation": [
                {"id": "pdf_merger", "name": "PDF Merger", "time": "8s", "description": "Combine multiple PDFs into one"},
                {"id": "pdf_splitter", "name": "PDF Splitter", "time": "10s", "description": "Split PDF into single pages or selected ranges"},
                {"id": "pdf_editor", "name": "PDF Editor", "time": "25s", "description": "Add/remove text, images, pages; annotate PDF"},
                {"id": "pdf_compressor", "name": "PDF Compressor", "time": "15s", "description": "Reduce PDF size without quality loss"},
                {"id": "pdf_watermark", "name": "PDF Watermark Tool", "time": "10s", "description": "Add watermark to multiple PDFs"},
                {"id": "pdf_password", "name": "PDF Password Remover/Encryptor", "time": "5s", "description": "Encrypt or decrypt PDF files"},
                {"id": "pdf_metadata", "name": "PDF Metadata Editor", "time": "3s", "description": "View & modify PDF metadata"},
                {"id": "pdf_reorder", "name": "PDF Page Reorder Tool", "time": "8s", "description": "Rearrange PDF pages"}
            ],
            "Advanced PDF": [
                {"id": "pdf_ocr", "name": "PDF OCR", "time": "30s", "description": "Convert scanned PDFs to searchable text"},
                {"id": "pdf_form_filler", "name": "PDF Form Filler", "time": "20s", "description": "Fill PDF forms in bulk from CSV/Excel"},
                {"id": "table_extractor", "name": "Table Extractor", "time": "25s", "description": "Extract tables from PDFs to structured Excel/CSV"},
                {"id": "pdf_summary", "name": "PDF Summary Generator", "time": "45s", "description": "Generate key points from PDF content"},
                {"id": "pdf_annotation", "name": "PDF Annotation Tool", "time": "20s", "description": "Highlight, comment, and draw on PDFs"},
                {"id": "pdf_template", "name": "PDF Template Generator", "time": "15s", "description": "Create reusable PDF templates"}
            ]
        },
        "Excel & CSV Tools": {
            "Converters": [
                {"id": "excel_to_csv", "name": "Excel → CSV Converter", "time": "5s", "description": "Convert Excel files to CSV"},
                {"id": "csv_to_excel", "name": "CSV → Excel Converter", "time": "8s", "description": "Convert CSV to Excel"},
                {"id": "csv_json_converter", "name": "CSV ↔ JSON Converter", "time": "6s", "description": "Convert CSV to JSON or JSON to CSV"}
            ],
            "Data Processing": [
                {"id": "excel_deduplicator", "name": "Excel Deduplicator", "time": "12s", "description": "Remove duplicate rows/columns"},
                {"id": "excel_cleaner", "name": "Excel Cleaner", "time": "15s", "description": "Remove empty cells, standardize formatting"},
                {"id": "csv_validator", "name": "CSV Validator", "time": "8s", "description": "Check for errors in CSV files"},
                {"id": "excel_merger", "name": "Excel/CSV Merger", "time": "15s", "description": "Combine multiple Excel or CSV files"}
            ],
            "Advanced Features": [
                {"id": "csv_to_sql", "name": "Bulk CSV → SQL Generator", "time": "10s", "description": "Convert CSV to SQL insert statements"},
                {"id": "pivot_table", "name": "Excel Pivot Table Generator", "time": "20s", "description": "Generate pivot tables from raw data"},
                {"id": "chart_generator", "name": "Excel Chart Generator", "time": "18s", "description": "Create charts from Excel/CSV data"}
            ]
        },
        "Image & Media Tools": {
            "Image Processing": [
                {"id": "image_resizer", "name": "Bulk Image Resizer", "time": "8s", "description": "Resize multiple images to specified dimensions"},
                {"id": "image_compressor", "name": "Image Compressor", "time": "10s", "description": "Reduce image file size without quality loss"},
                {"id": "background_remover", "name": "Image Background Remover", "time": "25s", "description": "Automatically remove image backgrounds"},
                {"id": "format_converter", "name": "Image Format Converter", "time": "6s", "description": "Convert images between JPG, PNG, WebP"}
            ],
            "Creative Tools": [
                {"id": "meme_generator", "name": "Meme Generator", "time": "5s", "description": "Add text to images to create memes"},
                {"id": "watermark_tool", "name": "Bulk Watermark Tool", "time": "12s", "description": "Add logos or text to multiple images"},
                {"id": "thumbnail_generator", "name": "Social Media Thumbnail Generator", "time": "8s", "description": "Generate ready-to-post social media thumbnails"},
                {"id": "collage_maker", "name": "Photo Collage Maker", "time": "15s", "description": "Merge multiple images into a single collage"},
                {"id": "meme_template", "name": "Meme Template Generator", "time": "3s", "description": "Predefined meme templates for easy creation"}
            ],
            "AI & Analysis": [
                {"id": "color_extractor", "name": "Color Palette Extractor", "time": "8s", "description": "Extract dominant colors from images"},
                {"id": "ai_enhancer", "name": "AI Image Enhancer", "time": "30s", "description": "Enhance image quality using AI"},
                {"id": "caption_generator", "name": "AI Image Caption Generator", "time": "20s", "description": "Generate descriptive captions for images"},
                {"id": "image_ocr", "name": "Image OCR → Text", "time": "15s", "description": "Extract text from images"},
                {"id": "gif_maker", "name": "Animated GIF Maker", "time": "20s", "description": "Create GIFs from multiple images"},
                {"id": "video_to_gif", "name": "Video → GIF Converter", "time": "25s", "description": "Convert short video clips to GIFs"}
            ]
        },
        "Website & URL Tools": {
            "Content Analysis": [
                {"id": "url_summarizer", "name": "URL Summarizer", "time": "30s", "description": "Summarize website content using AI"},
                {"id": "keyword_scraper", "name": "Keyword Scraper", "time": "20s", "description": "Extract top keywords from any page"},
                {"id": "meta_extractor", "name": "Meta Tag Extractor", "time": "8s", "description": "Extract meta title, description, keywords"},
                {"id": "text_extractor", "name": "Website Text Extractor", "time": "10s", "description": "Extract all visible text from webpage"}
            ],
            "Technical Analysis": [
                {"id": "link_checker", "name": "Broken Link Checker", "time": "25s", "description": "Scan website for dead links"},
                {"id": "sitemap_generator", "name": "Sitemap Generator", "time": "15s", "description": "Generate XML sitemap from website"},
                {"id": "speed_analyzer", "name": "Page Speed Analyzer", "time": "30s", "description": "Website performance report"},
                {"id": "link_visualizer", "name": "Internal Link Visualizer", "time": "20s", "description": "Map internal links of a website"},
                {"id": "robots_validator", "name": "Robots.txt Validator", "time": "8s", "description": "Check robots.txt rules for URL accessibility"},
                {"id": "redirect_checker", "name": "Redirect Checker", "time": "15s", "description": "Track URL redirects"}
            ],
            "Visual Tools": [
                {"id": "share_preview", "name": "Social Media Share Preview", "time": "10s", "description": "Preview how link appears on social media"},
                {"id": "html_to_pdf", "name": "HTML → PDF Generator", "time": "12s", "description": "Convert webpage HTML to PDF"},
                {"id": "screenshot_generator", "name": "Bulk Screenshot Generator", "time": "20s", "description": "Capture screenshots of multiple URLs"},
                {"id": "competitor_analyzer", "name": "Competitor Content Analyzer", "time": "35s", "description": "Extract headings, meta, keywords from competitor sites"},
                {"id": "web_archive", "name": "Web Archive Generator", "time": "18s", "description": "Capture website as PDF/HTML snapshot"}
            ]
        },
        "SEO & Marketing Tools": {
            "Keyword Research": [
                {"id": "keyword_suggestion", "name": "Keyword Suggestion Tool", "time": "15s", "description": "Generate relevant keywords based on topic/content"},
                {"id": "keyword_gap", "name": "Competitor Keyword Gap Analysis", "time": "30s", "description": "Compare keywords between two domains"},
                {"id": "hashtag_generator", "name": "Hashtag Generator", "time": "10s", "description": "Generate trending hashtags for social posts"}
            ],
            "Link Analysis": [
                {"id": "backlink_analyzer", "name": "Backlink Analyzer", "time": "45s", "description": "Analyze backlinks of a website/domain"},
                {"id": "seo_audit", "name": "SEO Audit Report Generator", "time": "60s", "description": "Generate full SEO audit for a website"},
                {"id": "meta_analyzer", "name": "Bulk URL Meta Tag Analyzer", "time": "12s", "description": "Analyze meta tags for multiple URLs"}
            ],
            "Content & Social": [
                {"id": "meta_generator", "name": "Meta Description Generator", "time": "20s", "description": "Auto-generate SEO-optimized meta descriptions"},
                {"id": "post_scheduler", "name": "Social Media Post Scheduler", "time": "5s", "description": "Schedule posts to multiple platforms"},
                {"id": "email_extractor", "name": "Email List Extractor", "time": "15s", "description": "Extract emails from URL or uploaded file"},
                {"id": "email_validator", "name": "Email Validator", "time": "25s", "description": "Validate email list for syntax & deliverability"}
            ]
        },
        "AI & Automation Tools": {
            "Content Generation": [
                {"id": "content_summarizer", "name": "AI Content Summarizer", "time": "30s", "description": "Summarize PDF, Word, or website content using AI"},
                {"id": "content_rewriter", "name": "AI Content Rewriter", "time": "25s", "description": "Paraphrase text content"},
                {"id": "faq_generator", "name": "AI FAQ Generator", "time": "35s", "description": "Generate FAQs from website or document"},
                {"id": "product_description", "name": "AI Product Description Generator", "time": "20s", "description": "Generate product descriptions from CSV/website"}
            ],
            "Marketing AI": [
                {"id": "subject_generator", "name": "AI Email Subject Line Generator", "time": "8s", "description": "Suggest engaging subject lines"},
                {"id": "post_optimizer", "name": "AI Social Media Post Optimizer", "time": "15s", "description": "Improve social post content for engagement"},
                {"id": "sentiment_analyzer", "name": "AI Sentiment Analyzer", "time": "20s", "description": "Analyze sentiment of reviews/texts"},
                {"id": "competitor_report", "name": "AI Competitor Report Generator", "time": "45s", "description": "Generate insights on competitor websites"}
            ],
            "Data Processing": [
                {"id": "table_extractor_ai", "name": "AI Table Extractor", "time": "30s", "description": "Extract tables from PDF/images into Excel"},
                {"id": "text_translator", "name": "AI Text Translator", "time": "25s", "description": "Translate text/files to multiple languages"}
            ]
        },
        "Developer & Code Tools": {
            "File Converters": [
                {"id": "html_pdf_converter", "name": "HTML → PDF Converter", "time": "10s", "description": "Convert HTML files or webpages into PDF"},
                {"id": "markdown_converter", "name": "Markdown → HTML/PDF", "time": "8s", "description": "Convert Markdown (.md) to HTML or PDF"},
                {"id": "json_converter", "name": "JSON → CSV/Excel", "time": "6s", "description": "Convert JSON files to Excel/CSV"}
            ],
            "Code Optimization": [
                {"id": "css_js_minifier", "name": "CSS/JS Minifier & Optimizer", "time": "5s", "description": "Minify and optimize CSS/JS files"},
                {"id": "url_cleaner", "name": "URL Parameter Cleaner", "time": "3s", "description": "Clean URLs by removing unnecessary tracking/query parameters"},
                {"id": "structured_data", "name": "Structured Data Generator", "time": "8s", "description": "Generate JSON-LD structured data for products/events"}
            ],
            "Testing & Analysis": [
                {"id": "api_tester", "name": "Bulk API Response Tester", "time": "20s", "description": "Test multiple API endpoints and record response"},
                {"id": "content_downloader", "name": "Website Content Downloader", "time": "25s", "description": "Download all visible text/images from a website"},
                {"id": "response_checker", "name": "Bulk URL Response Checker", "time": "15s", "description": "Check HTTP response codes of multiple URLs"},
                {"id": "multi_screenshot", "name": "Multi-Page Website Screenshot → PDF", "time": "30s", "description": "Capture screenshots of multiple pages and merge into PDF"}
            ]
        },
        "Productivity & Miscellaneous Tools": {
            "File Management": [
                {"id": "document_renamer", "name": "Bulk Document Renamer", "time": "5s", "description": "Rename multiple documents with a pattern"},
                {"id": "format_converter", "name": "File Format Converter", "time": "8s", "description": "Convert between DOCX ↔ ODT, XLSX ↔ ODS, etc."},
                {"id": "text_replacer", "name": "Bulk Text Replacer in Files", "time": "10s", "description": "Search & replace text in multiple files"},
                {"id": "metadata_editor", "name": "File Metadata Editor", "time": "8s", "description": "View & edit metadata of PDFs, images, Word files"},
                {"id": "version_tracker", "name": "File Version Tracker", "time": "5s", "description": "Track changes/versions of uploaded files"}
            ],
            "Generators": [
                {"id": "signature_generator", "name": "Digital Signature Generator", "time": "3s", "description": "Create reusable digital signature stamps"},
                {"id": "certificate_generator", "name": "Certificate Generator", "time": "12s", "description": "Bulk generate certificates from names list"},
                {"id": "badge_generator", "name": "Badge Generator", "time": "8s", "description": "Generate badges for events/teams"},
                {"id": "calendar_generator", "name": "Calendar Generator", "time": "5s", "description": "Generate printable monthly/annual calendars"},
                {"id": "qr_generator", "name": "QR Code Generator", "time": "2s", "description": "Create QR codes for URL, text, or contact info"},
                {"id": "password_generator", "name": "Random Password Generator", "time": "1s", "description": "Generate secure random passwords"},
                {"id": "ascii_art", "name": "ASCII Art Generator", "time": "8s", "description": "Convert text/images into ASCII art"}
            ],
            "Templates & Documents": [
                {"id": "template_generator", "name": "Template Generator", "time": "15s", "description": "Generate templates for invoices, proposals, flyers"},
                {"id": "resume_builder", "name": "Markdown Resume Builder", "time": "10s", "description": "Create resumes from Markdown input"},
                {"id": "email_template", "name": "Email Template Generator", "time": "8s", "description": "Create reusable HTML email templates"}
            ]
        }
    }
    return jsonify(tools)

@app.route('/api/process/<tool_id>', methods=['POST'])
def process_tool(tool_id):
    """Process a tool with uploaded files"""
    if 'files' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400
    
    files = request.files.getlist('files')
    if not files or all(file.filename == '' for file in files):
        return jsonify({'error': 'No files selected'}), 400
    
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    
    # Initialize processing status
    processing_status[job_id] = {
        'status': 'processing',
        'progress': 0,
        'tool_id': tool_id,
        'start_time': datetime.now().isoformat(),
        'estimated_time': get_processing_time(tool_id)
    }
    
    # Start processing in background thread
    thread = threading.Thread(target=process_files, args=(job_id, tool_id, files))
    thread.start()
    
    return jsonify({
        'job_id': job_id,
        'status': 'processing',
        'estimated_time': get_processing_time(tool_id)
    })

def process_files(job_id, tool_id, files):
    """Background processing function"""
    try:
        # Simulate processing time
        estimated_time = get_processing_time(tool_id)
        steps = 10
        
        for i in range(steps):
            time.sleep(estimated_time / steps)
            progress = int((i + 1) / steps * 100)
            processing_status[job_id]['progress'] = progress
            
            if progress >= 100:
                break
        
        # Simulate file processing based on tool type
        output_files = simulate_tool_processing(tool_id, files)
        
        processing_status[job_id].update({
            'status': 'completed',
            'progress': 100,
            'output_files': output_files,
            'end_time': datetime.now().isoformat()
        })
        
    except Exception as e:
        processing_status[job_id].update({
            'status': 'error',
            'error': str(e),
            'end_time': datetime.now().isoformat()
        })

def simulate_tool_processing(tool_id, files):
    """Simulate tool processing and return output files"""
    output_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            base_name = filename.rsplit('.', 1)[0]
            extension = filename.rsplit('.', 1)[1].lower()
            
            # Determine output format based on tool
            if 'pdf_to_word' in tool_id:
                output_files.append(f"{base_name}_converted.docx")
            elif 'pdf_to_excel' in tool_id:
                output_files.append(f"{base_name}_tables.xlsx")
            elif 'word_to_pdf' in tool_id:
                output_files.append(f"{base_name}_converted.pdf")
            elif 'excel_to_pdf' in tool_id:
                output_files.append(f"{base_name}_converted.pdf")
            elif 'image' in tool_id:
                output_files.append(f"{base_name}_processed.png")
            else:
                output_files.append(f"{base_name}_processed.{extension}")
    
    return output_files

@app.route('/api/status/<job_id>')
def get_status(job_id):
    """Get processing status for a job"""
    if job_id not in processing_status:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(processing_status[job_id])

@app.route('/api/download/<job_id>')
def download_result(job_id):
    """Download processed files"""
    if job_id not in processing_status:
        return jsonify({'error': 'Job not found'}), 404
    
    job = processing_status[job_id]
    if job['status'] != 'completed':
        return jsonify({'error': 'Job not completed'}), 400
    
    # In a real implementation, you would return the actual processed files
    # For now, return a placeholder response
    return jsonify({
        'message': 'Files ready for download',
        'output_files': job.get('output_files', [])
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)