import sys
import os
import io
import urllib.request
import urllib.parse
import json
import webbrowser
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.server import HTTPServer, SimpleHTTPRequestHandler, ThreadingHTTPServer

# Safe stdout/stderr fallbacks when running silently in background (e.g. via pythonw)
class SafeWriter:
    def write(self, s):
        pass
    def flush(self):
        pass
    def isatty(self):
        return False

if sys.stdout is None:
    sys.stdout = SafeWriter()
if sys.stderr is None:
    sys.stderr = SafeWriter()



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
        pass
    
    try:
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if not ip.startswith("127.") and not ip.startswith("169.254."):
                return ip
    except Exception:
        pass
        
    return "127.0.0.1"

def update_client_launchers(local_ip, hostname):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Generate resilient client launcher file for LAN access
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mở Trang Tra Cứu Tuyển Sinh 2026 - Mạng LAN</title>
    <style>
        * {{
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            padding: 16px;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #f8fafc;
            text-align: center;
        }}
        .card {{
            background: rgba(30, 41, 59, 0.95);
            backdrop-filter: blur(12px);
            padding: 32px 24px;
            border-radius: 20px;
            box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.1);
            max-width: 480px;
            width: 100%;
        }}
        .spinner {{
            width: 44px;
            height: 44px;
            border: 4px solid rgba(59, 130, 246, 0.2);
            border-top-color: #3b82f6;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin: 0 auto 18px;
        }}
        @keyframes spin {{
            to {{
                transform: rotate(360deg);
            }}
        }}
        .title {{
            margin: 0 0 8px;
            font-size: 19px;
            font-weight: 700;
            color: #60a5fa;
            letter-spacing: -0.02em;
        }}
        .status {{
            font-size: 14px;
            color: #94a3b8;
            margin: 0 0 20px;
            line-height: 1.5;
        }}
        .server-badge {{
            display: inline-block;
            background: rgba(59, 130, 246, 0.15);
            border: 1px solid rgba(59, 130, 246, 0.3);
            color: #93c5fd;
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 13px;
            font-family: monospace;
            font-weight: 600;
            margin-bottom: 20px;
        }}
        .btn {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            width: 100%;
            padding: 13px 20px;
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: white;
            border-radius: 12px;
            text-decoration: none;
            font-weight: 700;
            font-size: 15px;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);
            transition: all 0.2s ease;
            border: none;
            cursor: pointer;
        }}
        .btn:hover {{
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);
        }}
        .guide-box {{
            margin-top: 24px;
            padding: 16px;
            background: rgba(15, 23, 42, 0.6);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.06);
            text-align: left;
            font-size: 13px;
            color: #cbd5e1;
        }}
        .guide-box h4 {{
            margin: 0 0 8px;
            color: #f59e0b;
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .guide-box ul {{
            margin: 0;
            padding-left: 18px;
        }}
        .guide-box li {{
            margin-bottom: 6px;
            line-height: 1.4;
        }}
        .guide-box li:last-child {{
            margin-bottom: 0;
        }}
        .code {{
            background: rgba(0, 0, 0, 0.3);
            padding: 2px 6px;
            border-radius: 4px;
            color: #38bdf8;
            font-family: monospace;
        }}
    </style>
</head>
<body>
    <div class="card">
        <div id="loading-spinner" class="spinner"></div>
        <h2 class="title">Đang Kết Nối Máy Chủ Tuyển Sinh 2026</h2>
        <div class="server-badge">IP Máy Chủ: {local_ip}:{PORT}</div>
        <p id="status" class="status">Đang tự động nhận diện và kết nối máy chủ qua mạng LAN...</p>
        
        <div style="margin-top: 10px;">
            <a id="direct-btn" href="http://{local_ip}:{PORT}/" class="btn">
                🚀 Mở Trực Tiếp: http://{local_ip}:{PORT}/
            </a>
        </div>

        <div id="guide" class="guide-box" style="display: none;">
            <h4>⚠️ Chưa kết nối được? Hãy kiểm tra:</h4>
            <ul>
                <li>1. <b>Chung mạng LAN/Wi-Fi</b>: Đảm bảo máy này và máy chủ đang kết nối cùng 1 modem Wi-Fi hoặc mạng dây.</li>
                <li>2. <b>Máy chủ đang bật</b>: Đảm bảo máy tính chứa server (<span class="code">{local_ip}</span>) đang chạy file server.</li>
                <li>3. <b>Tường lửa (Firewall)</b>: Trên máy chủ, chạy file <span class="code">open_firewall_lan.bat</span> (bấm chuột phải chọn <i>Run as administrator</i>).</li>
            </ul>
        </div>
    </div>

    <script>
        const KNOWN_IP = "{local_ip}";
        const KNOWN_HOSTNAME = "{hostname}";
        const PORT = {PORT};

        let redirected = false;

        function redirectTo(url) {{
            if (redirected) return;
            redirected = true;
            const statusEl = document.getElementById('status');
            if (statusEl) statusEl.innerHTML = '<span style="color:#4ade80;font-weight:600;">✓ Kết nối thành công! Đang chuyển hướng...</span>';
            const spinner = document.getElementById('loading-spinner');
            if (spinner) spinner.style.borderTopColor = '#4ade80';
            
            setTimeout(() => {{
                window.location.href = url;
            }}, 300);
        }}

        // Probe endpoint using fetch and Image as fallback (bypasses CORS restrictions)
        function probe(ipOrHost, timeoutMs = 1200) {{
            return new Promise((resolve) => {{
                if (redirected) return resolve(true);
                const baseUrl = `http://${{ipOrHost}}:${{PORT}}`;
                let done = false;

                const finish = (success) => {{
                    if (done) return;
                    done = true;
                    if (success) {{
                        redirectTo(baseUrl + '/');
                        resolve(true);
                    }} else {{
                        resolve(false);
                    }}
                }};

                // 1. Fetch probe
                try {{
                    const controller = new AbortController();
                    const timer = setTimeout(() => controller.abort(), timeoutMs);
                    fetch(`${{baseUrl}}/api/ping`, {{ 
                        mode: 'cors',
                        cache: 'no-store',
                        signal: controller.signal 
                    }})
                    .then(res => {{
                        clearTimeout(timer);
                        if (res.ok) finish(true);
                        else finish(false);
                    }})
                    .catch(() => finish(false));
                }} catch (e) {{
                    finish(false);
                }}

                // 2. Image probe backup
                const img = new Image();
                img.onload = () => finish(true);
                img.onerror = () => {{}}; // Ignore image 404/error, fetch handles
                img.src = `${{baseUrl}}/favicon.ico?_t=${{Date.now()}}`;

                setTimeout(() => finish(false), timeoutMs + 100);
            }});
        }}

        async function autoDiscover() {{
            // 1. Try known server IP directly
            if (await probe(KNOWN_IP, 1000)) return;
            
            // 2. Try known Hostname
            if (KNOWN_HOSTNAME && await probe(KNOWN_HOSTNAME, 1000)) return;

            // 3. Try Localhost
            if (await probe('127.0.0.1', 600)) return;
            if (await probe('localhost', 600)) return;

            // 4. Fast scan local subnet if IP shifted
            if (KNOWN_IP && KNOWN_IP.includes('.')) {{
                const prefix = KNOWN_IP.substring(0, KNOWN_IP.lastIndexOf('.') + 1);
                const scanPromises = [];
                for (let i = 1; i <= 254; i++) {{
                    scanPromises.push(probe(prefix + i, 800));
                }}
                await Promise.all(scanPromises);
            }}

            if (!redirected) {{
                const statusEl = document.getElementById('status');
                if (statusEl) {{
                    statusEl.innerHTML = '<span style="color:#f87171;">Không tự động nhận diện được máy chủ.</span><br>Vui lòng bấm nút mở trực tiếp bên dưới:';
                }}
                const guideEl = document.getElementById('guide');
                if (guideEl) guideEl.style.display = 'block';
                const spinner = document.getElementById('loading-spinner');
                if (spinner) spinner.style.display = 'none';
            }}
        }}

        autoDiscover();
    </script>
</body>
</html>
"""
    with open(os.path.join(base_dir, "ToolTS2026.html"), "w", encoding="utf-8") as f:
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
    def log_message(self, format, *args):
        # Prevent crash when stderr is None or during background headless execution
        try:
            if sys.stderr is not None:
                sys.stderr.write("%s - - [%s] %s\n" %
                                 (self.address_string(),
                                  self.log_date_time_string(),
                                  format % args))
        except Exception:
            pass
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, HEAD")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Access-Control-Request-Private-Network, X-Requested-With")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Access-Control-Max-Age", "86400")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_HEAD(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ["/api/ping", "/ping", "/favicon.ico"]:
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            return
        return super().do_HEAD()

    def do_GET(self):
        try:
            parsed = urllib.parse.urlparse(self.path)

            # Healthcheck endpoint for instant LAN discovery
            if parsed.path in ["/api/ping", "/ping"]:
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                resp = {
                    "status": True,
                    "service": "TS2026 Server",
                    "version": "2026.1",
                    "ip": get_local_ip(),
                    "port": PORT
                }
                self.wfile.write(json.dumps(resp).encode("utf-8"))
                return

            if parsed.path == "/api/score":
                query = urllib.parse.parse_qs(parsed.query)
                sbd = query.get("sbd", [""])[0].strip()
                year = query.get("year", ["2026"])[0].strip() or "2026"
                
                if not sbd:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": False, "message": "Missing SBD parameter"}).encode("utf-8"))
                    return

                result_data = fetch_year(sbd, year)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                
                if result_data:
                    self.wfile.write(json.dumps(result_data).encode("utf-8"))
                else:
                    self.wfile.write(json.dumps({
                        "status": False,
                        "errorCode": 404,
                        "messages": [f"Không tìm thấy dữ liệu điểm thi năm {year}"],
                        "data": {"model": False}
                    }).encode("utf-8"))
                return

            if parsed.path == "/" or parsed.path == "":
                self.path = "/index.html"
            return super().do_GET()
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass

    def copyfile(self, source, outputfile):
        try:
            super().copyfile(source, outputfile)
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass

def run():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    local_ip = get_local_ip()
    hostname = socket.gethostname()
    
    # Automatically generate launcher.html
    update_client_launchers(local_ip, hostname)

    server_address = (HOST, PORT)
    ThreadingHTTPServer.allow_reuse_address = True
    httpd = ThreadingHTTPServer(server_address, AppHandler)
    httpd.daemon_threads = True
    local_url = f"http://127.0.0.1:{PORT}/"
    lan_url = f"http://{local_ip}:{PORT}/"
    host_url = f"http://{hostname}:{PORT}/"

    print("=" * 68)
    print("      TS2026 SERVER - LOCAL EXAM LOOKUP & HIGH SCHOOL TRANSCRIPT")
    print("=" * 68)
    print(f"  * Local Host Access   : {local_url}")
    print(f"  * LAN Network Access  : {lan_url}  or  {host_url}")
    print("=" * 68)
    print(f"  [>] SHARE THIS FILE WITH OTHER CLIENTS: ToolTS2026.html")
    print(f"  [>] DIRECT ACCESS LINK FOR BROWSER/PHONES: {lan_url}")
    print("=" * 68)
    print("  Press Ctrl + C to stop the server.")
    print("=" * 68)

    # Only open browser if run directly with interactive console
    try:
        if hasattr(sys.stdout, "isatty") and sys.stdout.isatty():
            webbrowser.open(local_url)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        import traceback
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "server_error.log"), "w", encoding="utf-8") as f:
                traceback.print_exc(file=f)
        except Exception:
            pass



