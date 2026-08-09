from flask import Flask, render_template_string, request, Response
import yt_dlp
import requests
import os

app = Flask(__name__)

# آپ کا وہی خوبصورت ڈارک ڈیزائن
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ExtremeWrites Downloader</title>
    <style>
        body { background: radial-gradient(circle, #1e293b 0%, #0f172a 100%); color: #f8fafc; font-family: sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .card { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); padding: 40px; border-radius: 30px; box-shadow: 0 25px 50px rgba(0,0,0,0.5); width: 100%; max-width: 400px; border: 1px solid rgba(255,255,255,0.1); text-align: center; }
        input { width: 100%; padding: 15px; background: #0f172a; border: 2px solid #334155; border-radius: 12px; color: white; margin-bottom: 20px; box-sizing: border-box; outline: none; }
        .btn { width: 100%; padding: 15px; background: linear-gradient(135deg, #38bdf8 0%, #1d4ed8 100%); color: white; border: none; border-radius: 12px; font-weight: bold; cursor: pointer; }
        .dl-btn { display: inline-block; padding: 15px 30px; background: #10b981; color: white; text-decoration: none; border-radius: 12px; font-weight: bold; margin-top: 20px; width: 80%; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Downloader</h2>
        <p style="color: #94a3b8; font-size: 13px;">Paste link to download directly</p>
        <form method="POST" action="/get_video">
            <input type="text" name="url" placeholder="Paste link here..." required>
            <button type="submit" class="btn">GET VIDEO</button>
        </form>

        {% if download_url %}
        <div style="margin-top: 30px;">
            <p style="font-size: 12px; color: #94a3b8;">{{ title[:50] }}</p>
            <a href="/finish_download?link={{ download_url }}" class="dl-btn">📥 DOWNLOAD NOW</a>
        </div>
        {% endif %}
        
        {% if error %}
        <p style="color: #ef4444; margin-top: 20px;">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_video', methods=['POST'])
def get_video():
    url = request.form.get('url')
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return render_template_string(HTML_TEMPLATE, 
                                        download_url=info.get('url'), 
                                        title=info.get('title', 'Video Ready'))
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, error="Invalid Link or Private Video")

@app.route('/finish_download')
def finish_download():
    # یہ فنکشن کالی اسکرین کو ختم کرے گا
    video_link = request.args.get('link')
    req = requests.get(video_link, stream=True)
    
    # براؤزر کو بتانا کہ اسے فائل کے طور پر سیو کرے
    headers = {
        'Content-Disposition': 'attachment; filename="ExtremeWrites_Video.mp4"',
        'Content-Type': 'video/mp4'
    }
    
    return Response(req.iter_content(chunk_size=1024*1024), headers=headers)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # trigger deployment
