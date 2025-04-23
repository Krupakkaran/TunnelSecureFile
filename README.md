# SecureFileShare

**SecureFileShare** is a Flask-based web application designed for secure file uploads and downloads. It supports AES encryption for file uploads and requires password protection for encrypted files during downloads. The application integrates with Cloudflare Tunnel to ensure secure and easy access.

## Features

- **File Uploads:** Allows users to upload files with optional password protection using AES encryption.
- **File Downloads:** Encrypted files require a password for decryption during download.
- **Cloudflare Tunnel Integration:** Exposes the app securely to the internet using Cloudflare Tunnel, providing a public URL for easy access.
- **Secure Communication:** Ensures data protection during file transfer with strong encryption protocols.

## Installation

### Prerequisites
Make sure you have the following installed:
- Python 3.8+  
- Flask  
- Cloudflare Tunnel

### Setting Up

1. Clone the repository:
    ```bash
    git clone https://github.com/Krupakkaran/TunnelSecureFile.git
    cd wget-share
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up Cloudflare Tunnel (refer to the Cloudflare Tunnel documentation for setup):
    ```bash
    cloudflared tunnel login
    cloudflared tunnel create <TUNNEL_NAME>
    cloudflared tunnel route dns <TUNNEL_NAME> your-tunnel.domain.com
    cloudflared tunnel run <TUNNEL_NAME>
    ```

4. Run the Flask application:
    ```bash
    python app.py
    ```

5. Access the app via the provided Cloudflare tunnel URL.

## Usage

1. **Upload Files:** Visit the main page and upload a file. Optionally, add a password for encryption.
2. **Download Files:** To download an encrypted file, provide the password used during the upload.

## Security

The application uses AES encryption to ensure file content remains private. All files are encrypted before being uploaded and decrypted upon download.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
