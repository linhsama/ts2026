import sys
import os
import urllib.request
import urllib.parse
import json
import webbrowser
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8080
HOST = "0.0.0.0"

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def update_client_launchers(local_ip, hostname):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Tạo file duy nhất gửi cho các máy khác trong mạng LAN
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Đang mở Tra Cứu Điểm 2026...</title>
    <style>
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            background: #f8fafc;
            color: #0f172a;
            text-align: center;
        }}
        .card {{
            background: white;
            padding: 32px 24px;
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);
            max-width: 440px;
            border: 1px solid #e2e8f0;
        }}
        .spinner {{
            width: 36px;
            height: 36px;
            border: 3px solid #e2e8f0;
            border-top-color: #1e40af;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin: 0 auto 16px;
        }}
        @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
        .btn {{
            display: inline-block;
            margin-top: 16px;
            padding: 10px 20px;
            background: #1e40af;
            color: white;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="spinner"></div>
        <h2 style="margin: 0 0 8px; font-size: 17px; color: #1e3a8a;">Đang kết nối Máy Chủ Tra Cứu Điểm 2026...</h2>
        <p id="status" style="font-size: 13px; color: #64748b; margin: 0;">Đang tự động nhận diện máy chủ mạng LAN...</p>
        <div id="manual" style="display: none; margin-top: 16px;">
            <a id="link" href="#" class="btn">Mở thủ công</a>
        </div>
    </div>

    <script>
        const KNOWN_IP = "{local_ip}";
        const KNOWN_HOSTNAME = "{hostname}";
        const PORT = {PORT};

        let found = false;

        function redirectTo(url) {{
            if (found) return;
            found = true;
            document.getElementById('status').textContent = "Đã kết nối thành công! Đang chuyển hướng...";
            window.location.replace(url);
        }}

        async function ping(ipOrHost) {{
            const url = `http://${{ipOrHost}}:${{PORT}}/`;
            try {{
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 700);
                await fetch(url + "api/score?sbd=00000000", {{ mode: 'no-cors', signal: controller.signal }});
                clearTimeout(timeoutId);
                redirectTo(url);
                return true;
            }} catch (e) {{
                return false;
            }}
        }}

        async function autoDiscover() {{
            // 1. Thử ngay IP và Tên máy chủ đã biết
            if (await ping(KNOWN_IP)) return;
            if (await ping(KNOWN_HOSTNAME)) return;
            if (await ping("localhost")) return;

            // 2. Quét nhanh dải IP nội bộ nếu máy chủ bị đổi IP
            const prefix = KNOWN_IP.substring(0, KNOWN_IP.lastIndexOf('.') + 1);
            const promises = [];
            for (let i = 1; i <= 254; i++) {{
                promises.push(ping(prefix + i));
            }}
            await Promise.all(promises);

            if (!found) {{
                document.getElementById('status').innerHTML = "Chưa kết nối được máy chủ.<br>Vui lòng đảm bảo máy chủ đã chạy <b>run.bat</b> và 2 máy cùng chung Wi-Fi.";
                document.getElementById('manual').style.display = "block";
                document.getElementById('link').href = `http://${{KNOWN_IP}}:${{PORT}}/`;
                document.getElementById('link').textContent = `Bấm thử vào http://${{KNOWN_IP}}:${{PORT}}/`;
            }}
        }}

        autoDiscover();
    </script>
</body>
</html>
"""
    with open(os.path.join(base_dir, "MoWebTraCuu.html"), "w", encoding="utf-8") as f:
        f.write(html_content)

def fetch_year(sbd, yr):
    target_url = (
        f"https://vietnamnet.vn/newsapi-edu/EducationStudentScore/CheckCandidateNumber?"
        f"ComponentId=COMPONENT002298&PageId=fa4119c27edb45558886cde08459bb1b&"
        f"sbd={sbd}&type=2&year={yr}"
    )
    try:
        req = urllib.request.Request(target_url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*"
        })
        with urllib.request.urlopen(req, timeout=3.0) as response:
            if response.status == 200:
                body = response.read().decode("utf-8")
                res_json = json.loads(body)
                if (
                    res_json.get("status") is True
                    and res_json.get("data", {}).get("model") is True
                    and res_json.get("data", {}).get("data")
                ):
                    return res_json
    except Exception:
        pass
    return None

class AppHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/score":
            query = urllib.parse.parse_qs(parsed.query)
            sbd = query.get("sbd", [""])[0]
            
            if not sbd:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": False, "message": "Thieu SBD"}).encode("utf-8"))
                return

            years_to_try = ["2026", "2025", "2024"]
            result_data = None
            
            with ThreadPoolExecutor(max_workers=3) as executor:
                future_to_yr = {executor.submit(fetch_year, sbd, yr): yr for yr in years_to_try}
                for future in as_completed(future_to_yr):
                    res = future.result()
                    if res:
                        result_data = res
                        break

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            
            if result_data:
                self.wfile.write(json.dumps(result_data).encode("utf-8"))
            else:
                self.wfile.write(json.dumps({
                    "status": False,
                    "errorCode": 404,
                    "messages": ["Không tìm thấy dữ liệu điểm thi"],
                    "data": {"model": False}
                }).encode("utf-8"))
            return

        if parsed.path == "/" or parsed.path == "":
            self.path = "/index.html"
        return super().do_GET()

def run():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    local_ip = get_local_ip()
    hostname = socket.gethostname()
    
    # Tự động cập nhật file MoWebTraCuu.html
    update_client_launchers(local_ip, hostname)

    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, AppHandler)
    local_url = f"http://127.0.0.1:{PORT}/"
    lan_url = f"http://{local_ip}:{PORT}/"
    host_url = f"http://{hostname}:{PORT}/"

    print("=" * 68)
    print("      MAY CHU TRA CUU DIEM THI & TINH DIEM HOC BA 2026")
    print("=" * 68)
    print(f"  * Tren may chu nay     : {local_url}")
    print(f"  * Cac may khac cung LAN: {lan_url}  hoac  {host_url}")
    print("=" * 68)
    print(f"  [>] GUI 1 FILE DUY NHAT CHO MAY KHAC: MoWebTraCuu.html")
    print("=" * 68)
    print("  Nhan Ctrl + C de dung server.")
    print("=" * 68)

    webbrowser.open(local_url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nDa dung server.")
        httpd.server_close()

if __name__ == "__main__":
    run()
