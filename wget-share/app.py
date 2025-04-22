from flask import Flask, render_template, request, redirect, flash, send_file, url_for
import os, json, subprocess, re
from io import BytesIO
from crypto_utils import encrypt_file, decrypt_file

app = Flask(__name__)
app.secret_key = 'secret'
UPLOAD_FOLDER = 'uploads'
PASSWORDS_FILE = 'file_passwords.json'



os.makedirs(UPLOAD_FOLDER, exist_ok=True)
if not os.path.exists(PASSWORDS_FILE):
    with open(PASSWORDS_FILE, 'w') as f:
        json.dump({}, f)

with open(PASSWORDS_FILE, 'r') as f:
    file_passwords = json.load(f)

def save_passwords():
    with open(PASSWORDS_FILE, 'w') as f:
        json.dump(file_passwords, f)

def start_cloudflare_tunnel():
    try:
        proc = subprocess.Popen(
            ["cloudflared", "tunnel", "--no-chunked-encoding", "--url", "http://localhost:8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        tunnel_url = None
        for line in iter(proc.stdout.readline, ''):
            print("[Cloudflared]", line.strip())
            match = re.search(r"https://[a-z\-]+\.trycloudflare\.com", line)
            if match:
                tunnel_url = match.group(0)
                break

        return tunnel_url
    except Exception as e:
        print(f"❌ Cloudflare failed: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('❌ No file part in the request')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('❌ No file selected')
            return redirect(request.url)

        password = request.form.get('password')
        filename = file.filename
        data = file.read()

        if password:
            data = encrypt_file(data, password)
            filename += '.enc'
            file_passwords[filename] = password
            save_passwords()

        with open(os.path.join(UPLOAD_FOLDER, filename), 'wb') as f:
            f.write(data)

        flash(f'✅ Uploaded: {filename}')
        return redirect(url_for('index'))

    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files, tunnel_url=app.config.get('TUNNEL_URL'))

@app.route('/download/<filename>', methods=['POST'])
def download_file(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(path):
        flash('❌ File not found')
        return redirect(url_for('index'))

    password = request.form.get('password')
    if filename in file_passwords:
        if not password or password != file_passwords[filename]:
            flash('❌ Incorrect password')
            return redirect(url_for('index'))

        with open(path, 'rb') as f:
            decrypted = decrypt_file(f.read(), password)
        return send_file(BytesIO(decrypted), as_attachment=True, download_name=filename.replace('.enc', ''))

    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    tunnel_url = start_cloudflare_tunnel()
    print("✅ Tunnel URL:", tunnel_url)
    app.config['TUNNEL_URL'] = tunnel_url
    app.run(host='0.0.0.0', port=8000, debug=True)
