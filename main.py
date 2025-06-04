# main.py
from flask import Flask, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route('/execute/python', methods=['POST'])
def execute_python():
    data = request.json
    code = data.get('code', '')
    
    try:
        # Write code to a temporary file
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as tmpfile:
            tmpfile.write(code.encode())
            tmpfile_path = tmpfile.name
        
        # Execute Python code
        result = subprocess.run(
            ['python3', tmpfile_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        os.remove(tmpfile_path)
        
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/execute/shell', methods=['POST'])
def execute_shell():
    data = request.json
    command = data.get('command', '')
    
    try:
        # Execute shell command
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            timeout=5
        )
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
