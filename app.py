from flask import Flask, request, send_from_directory, render_template, redirect, url_for
import os
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)  # Sollte geheim gehalten werden in einer echten Anwendung

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def check_password(password):
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        return password == config['password']

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file:
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename))
        return 'Datei wurde hochgeladen.'

@app.route('/download', methods=['GET'])
def download_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    if not files:
        return 'Keine Dateien zum Herunterladen vorhanden.'
    
    zip_filename = 'uploaded_files.zip'
    with open(zip_filename, 'wb') as zip_file:
        for file in files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
            with open(file_path, 'rb') as f:
                zip_file.write(f.read())
    
    return send_from_directory(directory='.', filename=zip_filename, as_attachment=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if check_password(password):
            return redirect(url_for('index'))
        else:
            return 'Falsches Passwort. Bitte versuchen Sie es erneut.'
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
