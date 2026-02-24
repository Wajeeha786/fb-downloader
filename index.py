from flask import Flask, render_template_string, request
import yt_dlp

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ExtremeWrites Downloader</title>
    <style>
        body { background: radial-gradient(circle, #1e293b 0%, #0f172a 100%); color: #f8fafc; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); padding: 40px; border-radius: 30px; box-shadow: 0 25px 50px rgba(0,0,0,0.5); width: 90%; max-width: 420px; border: 1px solid rgba(255,255,255,0.1); text-align: center; }
        h2 { color: #38bdf8; font-size: 26px; margin-bottom: 5px; }
        input { width: 100%; padding: 16px; background: #0f172a; border: 2px solid #334155; border-radius: 15px; color: white; margin-bottom: 20px; box-sizing: border-box; outline: none; transition: 0.4s; }
        input:focus { border-color: #38bdf8; }
        .btn { width: 100%; padding: 16px; background: linear-gradient(135deg, #38bdf8 0%, #1d4ed8 100%); color: white; border: none; border-radius: 15px; font-weight: 800; cursor: pointer; transition: 0.3s; }
        .btn:hover { transform: scale(1.02); }
    </style>
</head>
<body>
    <div class="card">
        <h2>ExtremeWrites</h2>
        <p style="color:#94a3b8; font-size:13px;">Universal Video Downloader</p>
        <form method="POST" action="/download">
            <input type="text" name="url" placeholder="Paste link here..." required>
            <button type="submit" class="btn">GENERATE LINK</button>
        </form>
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
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url', None)
        return f'''
            <body style="background:#0f172a; color:white; display:flex; justify-content:center; align-items:center; height:100vh; font-family:sans-serif;">
                <div style="background:#1e293b; padding:40px; border-radius:30px; text-align:center; border:1px solid #334155; width:350px;">
                    <h3 style="color:#38bdf8;">Download Ready!</h3>
                    <a href="{video_url}" target="_blank" style="display:inline-block; padding:18px 35px; background:#10b981; color:white; text-decoration:none; border-radius:15px; font-weight:bold; margin-top:10px; width:80%;">DOWNLOAD NOW</a>
                    <br><br><a href="/" style="color:#64748b; text-decoration:none;">← Back</a>
                </div>
            </body>
        '''
    except Exception:
        return f'<body style="background:#0f172a; color:white; text-align:center; padding-top:100px;"><h3>Invalid or Private Link</h3><a href="/" style="color:#38bdf8;">Try Again</a></body>'

if __name__ == '__main__':
    app.run()
