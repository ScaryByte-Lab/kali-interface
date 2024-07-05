from flask import Flask, request, render_template, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_command', methods=['POST'])
def run_command():
    command = request.form.get('command')

    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return jsonify({'result': result})
    except subprocess.CalledProcessError as e:
        return jsonify({'result': e.output}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
