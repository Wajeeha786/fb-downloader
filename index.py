from flask import Flask, render_template_string, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

# جدید ترین ڈیزائن جو اسی پیج پر رزلٹ دکھائے گا
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
            min-height: 100vh; margin: 0;
        }
        .card { 
            background: rgba(30, 41, 59, 0.7); 
            backdrop-filter: blur(10px);
            padding: 40px; border-radius: 30px; 
            box-shadow: 0 25px 50px rgba(0,0,0,0.5); 
            width: 100%; max-width: 420px; 
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
        .btn:disabled { background: #475569; cursor: not-allowed; }
        #result { margin-top: 25px; display: none; }
        .dl-btn {
            display: inline-block; padding: 15px 30px; 
            background: #10b981; color: white; 
            text-decoration: none; border-radius: 12px; 
            font-weight: bold; width: 80%;
        }
        .loader { color: #38bdf8; font-size: 14px; display: none; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Downloader Pro</h2>
        <div class="sub">Facebook, Insta, TikTok, YT & More</div>
        
        <input type="text" id="videoUrl" placeholder="Paste link here..." required>
        <button onclick="getDownloadLink()" id="mainBtn" class="btn">Get Video</button>
        
        <div id="loading" class="loader">🔍 Analyzing link, please wait...</div>

        <div id="result">
            <p id="videoTitle" style="font-size: 12px; color: #94a3b8;"></p>
            <a href="#" id="finalDownload" class="dl-btn">📥 DOWNLOAD NOW</a>
        </div>

        <div class="footer">POWERED BY EXTREMEWRITES AI</div>
    </div>

    <script>
        async function getDownloadLink() {
            const urlInput = document.getElementById('videoUrl').value;
            const btn = document.getElementById('mainBtn');
            const loader = document.getElementById('loading');
            const resultDiv = document.getElementById('result');

            if(!urlInput) return alert("Please paste a link!");

            btn.disabled = true;
            btn.innerText = "Processing...";
            loader.style.display = "block";
            resultDiv.style.display = "none";

            try {
                const response = await fetch('/api/get_info', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: urlInput})
                });
                const data = await response.json();

                if(data.success) {
                    document.getElementById('videoTitle').innerText = data.title;
                    const dlBtn = document.getElementById('finalDownload');
                    dlBtn.href = data.download_url;
                    
                    // یہ جادو ہے: اس سے کالی اسکرین نہیں کھلے گی
                    dlBtn.setAttribute('download', 'video.mp4');
                    
                    resultDiv.style.display = "block";
                } else {
                    alert("Error: " + data.error);
                }
            } catch (e) {
                alert("Something went wrong!");
            } finally {
                btn.disabled = false;
                btn.innerText = "Get Video";
                loader.style.display = "none";
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/get_info', methods=['POST'])
def get_info():
    data = request.get_json()
    url = data.get('url')
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "success": True,
                "title": info.get('title', 'Video Ready'),
                "download_url": info.get('url')
            })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
