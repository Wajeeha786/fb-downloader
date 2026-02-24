from flask import Flask, render_template_string, request
import yt_dlp

app = Flask(__name__)

# نیا ڈارک اور جدید ڈیزائن
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FB Downloader | Dark Edition</title>
    <style>
        body { 
            background-color: #0f172a; 
            color: #f8fafc; 
            font-family: 'Inter', sans-serif; 
            display: flex; justify-content: center; align-items: center; 
            height: 100vh; margin: 0;
        }
        .container { 
            background: #1e293b; 
            padding: 40px; 
            border-radius: 24px; 
            box-shadow: 0 20px 50px rgba(0,0,0,0.5); 
            width: 100%; max-width: 450px; 
            border: 1px solid #334155;
        }
        h2 { color: #38bdf8; margin-bottom: 10px; font-size: 28px; }
        p { color: #94a3b8; margin-bottom: 30px; font-size: 14px; }
        input { 
            width: 100%; padding: 15px; 
            background: #0f172a; border: 1px solid #334155; 
            border-radius: 12px; color: white; 
            margin-bottom: 20px; box-sizing: border-box;
            outline: none; transition: 0.3s;
        }
        input:focus { border-color: #38bdf8; box-shadow: 0 0 10px rgba(56, 189, 248, 0.2); }
        button { 
            width: 100%; padding: 15px; 
            background: linear-gradient(135deg, #38bdf8 0%, #1d4ed8 100%); 
            color: white; border: none; border-radius: 12px; 
            font-weight: bold; cursor: pointer; font-size: 16px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover { 
            transform: translateY(-2px); 
            box-shadow: 0 10px 20px rgba(29, 78, 216, 0.4); 
        }
        .footer { margin-top: 25px; font-size: 11px; color: #64748b; letter-spacing: 1px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>FB Downloader</h2>
        <p>Premium Video Downloading Tool</p>
        <form method="POST" action="/download">
            <input type="text" name="url" placeholder="Paste video link here..." required>
            <button type="submit">GENERATE LINK</button>
        </form>
        <div class="footer">POWERED BY EXTREMEWRITES AI</div>
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
    try:
        ydl_opts = {'format': 'best', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url', None)
            title = info.get('title', 'Video')

        return f'''
            <body style="background:#0f172a; color:white; font-family:sans-serif; display:flex; justify-content:center; align-items:center; height:100vh;">
                <div style="background:#1e293b; padding:40px; border-radius:24px; text-align:center; border:1px solid #334155; max-width:400px;">
                    <h2 style="color:#10b981;">Video Found!</h2>
                    <p style="color:#94a3b8; font-size:14px;">{title[:60]}...</p>
                    <a href="{video_url}" target="_blank" style="display:inline-block; padding:15px 30px; background:#10b981; color:white; text-decoration:none; border-radius:12px; font-weight:bold; margin-top:20px;">
                        DOWNLOAD NOW
                    </a>
                    <br><br>
                    <a href="/" style="color:#38bdf8; text-decoration:none; font-size:13px;">← Go Back</a>
                </div>
            </body>
        '''
    except Exception as e:
        return f'<body style="background:#0f172a; color:white; text-align:center; padding-top:100px;"><h3>Error: Link is private or invalid</h3><a href="/" style="color:#38bdf8;">Back</a></body>'

if __name__ == '__main__':
    app.run()
