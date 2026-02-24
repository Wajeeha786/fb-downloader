from flask import Flask, render_template_string, request
import yt_dlp

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ExtremeWrites Universal Downloader</title>
    <style>
        body { 
            background: radial-gradient(circle, #1e293b 0%, #0f172a 100%); 
            color: #f8fafc; font-family: 'Segoe UI', sans-serif; 
            display: flex; justify-content: center; align-items: center; 
            height: 100vh; margin: 0;
        }
        .card { 
            background: rgba(30, 41, 59, 0.7); 
            backdrop-filter: blur(10px);
            padding: 40px; border-radius: 30px; 
            box-shadow: 0 25px 50px rgba(0,0,0,0.5); 
            width: 90%; max-width: 420px; 
            border: 1px solid rgba(255,255,255,0.1);
            text-align: center;
        }
        h2 { color: #38bdf8; font-size: 26px; margin-bottom: 5px; }
        .sub { color: #94a3b8; margin-bottom: 25px; font-size: 13px; }
        input { 
            width: 100%; padding: 16px; 
            background: #0f172a; border: 2px solid #334155; 
            border-radius: 15px; color: white; 
            margin-bottom: 20px; box-sizing: border-box;
            outline: none; transition: 0.4s;
        }
        input:focus { border-color: #38bdf8; }
        .btn { 
            width: 100%; padding: 16px; 
            background: linear-gradient(135deg, #38bdf8 0%, #1d4ed8 100%);
            color: white; border: none; border-radius: 15px; 
            font-weight: 800; cursor: pointer; font-size: 15px;
            text-transform: uppercase; transition: 0.3s;
        }
        .btn:hover { transform: scale(1.02); box-shadow: 0 0 20px rgba(56, 189, 248, 0.4); }
        .footer { margin-top: 25px; font-size: 10px; color: #475569; letter-spacing: 1px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>ExtremeWrites</h2>
        <div class="sub">Universal Video Downloader</div>
        <form method="POST" action="/download">
            <input type="text" name="url" placeholder="Paste link here..." required>
            <button type="submit" class="btn">Extract Media</button>
        </form>
        <div class="footer">AI POWERED TECHNOLOGY</div>
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
    # یوٹیوب اور انسٹاگرام کے لیے اضافی سیٹنگز
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url', None)
            title = info.get('title', 'Your Content')
            
        return f'''
            <body style="background:#0f172a; color:white; display:flex; justify-content:center; align-items:center; height:100vh; font-family:sans-serif;">
                <div style="background:#1e293b; padding:40px; border-radius:30px; text-align:center; border:1px solid #334155; width:350px;">
                    <h3 style="color:#38bdf8; margin-top:0;">Download Ready</h3>
                    <p style="color:#94a3b8; font-size:12px;">{title[:50]}...</p>
                    <a href="{video_url}" target="_blank" style="display:inline-block; padding:18px 35px; background:#10b981; color:white; text-decoration:none; border-radius:15px; font-weight:bold; margin-top:10px; width:80%;">
                        DOWNLOAD NOW
                    </a>
                    <br><br>
                    <a href="/" style="color:#64748b; text-decoration:none; font-size:13px;">← Back</a>
                </div>
            </body>
        '''
    except Exception as e:
        # یہاں اصل ایرر دیکھنے کے لیے آپ اسے پرنٹ بھی کر سکتے ہیں
        return f'<body style="background:#0f172a; color:white; text-align:center; padding-top:100px; font-family:sans-serif;"><div style="background:#1e293b; display:inline-block; padding:30px; border-radius:20px;"><h3>Error Fetching Video</h3><p style="color:#94a3b8;">Make sure the link is public.</p><a href="/" style="color:#38bdf8; text-decoration:none;">Try Another Link</a></div></body>'

if __name__ == '__main__':
    app.run()
    
