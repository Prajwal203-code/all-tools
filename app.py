import os
import json
import time
from typing import Dict, Any, List
from flask import Flask, render_template, jsonify, request, Response, abort
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MANIFEST_PATH = os.path.join(BASE_DIR, 'tools_manifest.json')
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'), static_folder=os.path.join(BASE_DIR, 'static'))
CORS(app)

_manifest_cache: Dict[str, Any] = {"data": None, "mtime": None}


def _load_manifest() -> List[Dict[str, Any]]:
    global _manifest_cache
    try:
        mtime = os.path.getmtime(MANIFEST_PATH)
    except FileNotFoundError:
        return []
    if _manifest_cache["data"] is not None and _manifest_cache["mtime"] == mtime:
        return _manifest_cache["data"]
    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    _manifest_cache = {"data": data, "mtime": mtime}
    return data


def _group_by_category(tools: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for tool in tools:
        cat = tool.get('category', 'Other')
        grouped.setdefault(cat, []).append(tool)
    # Keep deterministic ordering by tool index if present
    for cat in grouped:
        grouped[cat].sort(key=lambda t: t.get('index', 9999))
    return grouped


@app.route('/')
def index():
    tools = _load_manifest()
    grouped = _group_by_category(tools)
    return render_template('index.html', grouped_tools=grouped)


@app.route('/tools/<slug>')
def tool_page(slug: str):
    tools = _load_manifest()
    tool = next((t for t in tools if t.get('slug') == slug), None)
    if tool is None:
        abort(404)
    return render_template('tool.html', tool=tool)


@app.route('/api/tools')
def api_tools():
    return jsonify(_load_manifest())


@app.route('/api/tools/<slug>/upload', methods=['POST'])
def upload_files(slug: str):
    # Accept multiple files; save to uploads for demo purposes
    if 'files' not in request.files:
        return jsonify({"error": "No files part in request"}), 400
    files = request.files.getlist('files')
    saved: List[str] = []
    for storage in files:
        if not storage or storage.filename == '':
            continue
        safe_name = storage.filename.replace('..', '_')
        dst = os.path.join(UPLOAD_DIR, safe_name)
        storage.save(dst)
        saved.append(safe_name)
    return jsonify({"ok": True, "files": saved})


@app.route('/api/tools/<slug>/progress')
def sse_progress(slug: str):
    tools = _load_manifest()
    tool = next((t for t in tools if t.get('slug') == slug), None)
    if tool is None:
        return Response('data: {"error": "Unknown tool"}\n\n', mimetype='text/event-stream')

    # Estimate duration in seconds based on manifest
    est = tool.get('processing_time', {}).get('avg_seconds', 15)
    # Allow override via query param
    try:
        est = int(request.args.get('estimate', est))
    except ValueError:
        pass

    def generate():
        steps = max(10, min(50, est // 1))  # between 10 and 50 steps
        sleep_per_step = max(0.1, est / steps)
        # Start event
        start_payload = {"status": "started", "progress": 0, "message": "Queued and starting..."}
        yield f"data: {json.dumps(start_payload)}\n\n"
        progress = 0
        for i in range(int(steps)):
            time.sleep(min(sleep_per_step, 1.0))
            progress = int(((i + 1) / steps) * 100)
            stage_msg = "Processing..." if progress < 80 else "Finalizing..."
            payload = {"status": "running", "progress": progress, "message": stage_msg}
            yield f"data: {json.dumps(payload)}\n\n"
        done = {"status": "completed", "progress": 100, "message": "Done", "download_url": "#"}
        yield f"data: {json.dumps(done)}\n\n"

    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '8000'))
    app.run(host='0.0.0.0', port=port, debug=True)