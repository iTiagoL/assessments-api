from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "API is running"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    file_base64 = data.get('fileBase64', '')
    file_content = base64.b64decode(file_base64).decode('utf-8')
    assessment_type = data.get('assessment', 'Unknown')

    important_lines = "\n".join(
        line for line in file_content.splitlines()
        if "error" in line.lower() or "port" in line.lower() or "connection" in line.lower()
    )

    report_content = f"Assessment Type: {assessment_type}\n\nImportant Lines:\n{important_lines}"
    encoded_report = base64.b64encode(report_content.encode('utf-8')).decode('utf-8')

    return jsonify({
        "filename": "assessment_report.txt",
        "fileBase64": encoded_report
    })

if __name__ == "__main__":
    app.run()
