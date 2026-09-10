import os
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-summarizer-key")

UPLOAD_FOLDER = "/tmp"
ALLOWED_EXTENSIONS = {"pdf", "txt"}
DRIVE_INPUT_FOLDER_ID = os.environ.get("GDRIVE_INPUT_FOLDER_ID", "YOUR_INPUT_FOLDER_ID")
SERVICE_ACCOUNT_FILE = "service_account.json"

SCOPES = ["https://www.googleapis.com/auth/drive"]

def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "document" not in request.files:
        flash("No file part in request.")
        return redirect(url_for("index"))
        
    file = request.files["document"]
    if file.filename == "" or not allowed_file(file.filename):
        flash("Please upload a valid .pdf or .txt file.")
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        service = get_drive_service()
        file_metadata = {
            "name": filename,
            "parents": [DRIVE_INPUT_FOLDER_ID]
        }
        media = MediaFileUpload(filepath, resumable=True)
        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, name"
        ).execute()

        flash(f"'{filename}' uploaded successfully! Processing initiated.")
    except Exception as e:
        flash(f"Upload failed. Ensure service_account.json is valid and Drive API is enabled. Error: {str(e)}")
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
