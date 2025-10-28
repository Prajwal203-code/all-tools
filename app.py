from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import os
import time
import threading
import uuid
from datetime import datetime
import json

# Import tool processors
from tools.pdf_tools import PDFProcessor
from tools.excel_tools import ExcelProcessor
from tools.image_tools import ImageProcessor
from tools.url_tools import URLProcessor
from tools.seo_tools import SEOProcessor
from tools.ai_tools import AIProcessor
from tools.dev_tools import DevProcessor
from tools.productivity_tools import ProductivityProcessor

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Global task tracker for processing status
tasks = {}

class TaskManager:
    @staticmethod
    def create_task(task_id, tool_name, estimated_time=5):
        tasks[task_id] = {
            'status': 'processing',
            'progress': 0,
            'tool_name': tool_name,
            'start_time': datetime.now(),
            'estimated_time': estimated_time,
            'result': None,
            'error': None
        }
        return task_id
    
    @staticmethod
    def update_progress(task_id, progress, status='processing'):
        if task_id in tasks:
            tasks[task_id]['progress'] = progress
            tasks[task_id]['status'] = status
    
    @staticmethod
    def complete_task(task_id, result=None, error=None):
        if task_id in tasks:
            tasks[task_id]['status'] = 'completed' if not error else 'failed'
            tasks[task_id]['progress'] = 100
            tasks[task_id]['result'] = result
            tasks[task_id]['error'] = error

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tools/<category>')
def tools_category(category):
    return render_template('tools.html', category=category)

@app.route('/tool/<tool_name>')
def tool_page(tool_name):
    return render_template('tool.html', tool_name=tool_name)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        task_id = str(uuid.uuid4())
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{task_id}_{filename}")
        file.save(filepath)
        
        return jsonify({
            'task_id': task_id,
            'filename': filename,
            'filepath': filepath
        })

@app.route('/api/process', methods=['POST'])
def process_tool():
    data = request.get_json()
    tool_name = data.get('tool_name')
    task_id = data.get('task_id', str(uuid.uuid4()))
    
    # Route to appropriate processor
    processor_map = {
        'pdf': PDFProcessor,
        'excel': ExcelProcessor,
        'image': ImageProcessor,
        'url': URLProcessor,
        'seo': SEOProcessor,
        'ai': AIProcessor,
        'dev': DevProcessor,
        'productivity': ProductivityProcessor
    }
    
    # Determine processor based on tool name
    processor_class = None
    for key, proc in processor_map.items():
        if key in tool_name.lower():
            processor_class = proc
            break
    
    if not processor_class:
        return jsonify({'error': 'Tool not found'}), 404
    
    # Start processing in background
    def process_task():
        try:
            processor = processor_class()
            result = processor.process(tool_name, data, task_id)
            TaskManager.complete_task(task_id, result)
        except Exception as e:
            TaskManager.complete_task(task_id, error=str(e))
    
    # Create task and start processing
    estimated_time = get_estimated_time(tool_name)
    TaskManager.create_task(task_id, tool_name, estimated_time)
    
    thread = threading.Thread(target=process_task)
    thread.start()
    
    return jsonify({'task_id': task_id, 'estimated_time': estimated_time})

@app.route('/api/status/<task_id>')
def get_task_status(task_id):
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    task = tasks[task_id]
    elapsed_time = (datetime.now() - task['start_time']).seconds
    
    return jsonify({
        'status': task['status'],
        'progress': task['progress'],
        'elapsed_time': elapsed_time,
        'estimated_time': task['estimated_time'],
        'tool_name': task['tool_name'],
        'result': task['result'],
        'error': task['error']
    })

@app.route('/api/download/<task_id>')
def download_result(task_id):
    if task_id not in tasks or tasks[task_id]['status'] != 'completed':
        return jsonify({'error': 'Task not completed'}), 404
    
    result = tasks[task_id]['result']
    if not result or 'output_path' not in result:
        return jsonify({'error': 'No download available'}), 404
    
    return send_file(result['output_path'], as_attachment=True)

def get_estimated_time(tool_name):
    """Return estimated processing time in seconds based on tool complexity"""
    time_map = {
        'pdf_word_converter': 10,
        'pdf_excel_converter': 15,
        'word_pdf_converter': 8,
        'excel_pdf_converter': 8,
        'pdf_merger': 5,
        'pdf_splitter': 3,
        'pdf_editor': 20,
        'pdf_compressor': 12,
        'pdf_ocr': 25,
        'pdf_form_filler': 15,
        'pdf_image_converter': 8,
        'image_pdf_converter': 6,
        'pdf_watermark': 7,
        'pdf_password': 3,
        'pdf_metadata_editor': 2,
        'table_extractor': 15,
        'pdf_summary_generator': 20,
        'pdf_annotation': 10,
        'pdf_page_reorder': 4,
        'pdf_template_generator': 12,
        'excel_csv_converter': 3,
        'csv_excel_converter': 3,
        'excel_deduplicator': 8,
        'excel_cleaner': 6,
        'csv_validator': 5,
        'bulk_csv_sql': 7,
        'csv_json_converter': 4,
        'excel_merger': 6,
        'excel_pivot_generator': 10,
        'excel_chart_generator': 8,
        'bulk_image_resizer': 12,
        'image_compressor': 8,
        'image_background_remover': 15,
        'meme_generator': 5,
        'bulk_watermark': 10,
        'social_thumbnail_generator': 6,
        'image_format_converter': 6,
        'photo_collage_maker': 12,
        'color_palette_extractor': 3,
        'ai_image_enhancer': 25,
        'ai_image_caption': 15,
        'image_ocr_text': 12,
        'animated_gif_maker': 10,
        'video_gif_converter': 18,
        'meme_template_generator': 6
    }
    
    return time_map.get(tool_name, 10)  # Default 10 seconds

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)