from flask import Flask, render_template_string, request
import yt_dlp

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FB Downloader</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; padding-top: 50px; background-color: #f0f2f5; }
        .container { background: white; padding: 40px; border-radius: 15px; display: inline-block; box-shadow: 0 10px 25px rgba(0,0,0,0.1); width: 90%; max-width: 400px; }
        h2 { color: #1877f2; margin-bottom: 20px; }
        input { padding: 12px; width: 100%; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 15px; box-sizing: border-box; }
        button { padding: 12px 25px; background-color: #1877f2; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%; transition: 0.3s; }
        button:hover { background-color: #166fe5; }
        .footer { margin-top: 20px; font-size: 12px; color: #777; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Facebook Downloader</h2>
        <form method="POST" action="/download">
            <input type="text" name="url" placeholder="Paste Facebook video link here..." required>
            <button type="submit">Get Download Link</button>
        </form>
        <div class="footer">Powered by ExtremeWrites AI Tools</div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    return f"Processing link: {url} (Functionality coming soon!)"

if __name__ == '__main__':
    app.run()
  
