import sys
import os
import urllib.request
import urllib.parse
import json
import webbrowser
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8080
HOST = "127.0.0.1"

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
        with urllib.request.urlopen(req, timeout=3.5) as response:
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
            
            # Chay song song tat ca cac nam qua ThreadPool de phan hoi trong 0.2s
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
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, AppHandler)
    url = f"http://{HOST}:{PORT}/"
    print("=" * 60)
    print("  MAY CHU TRA CUU DIEM THI & TINH DIEM HOC BA 2026")
    print(f"  Dia chi web: {url}")
    print("  Hoat dong 100% tren may tinh, KHONG BI CHAN CORS!")
    print("  Nhan Ctrl + C de dung server.")
    print("=" * 60)
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nDa dung server.")
        httpd.server_close()

if __name__ == "__main__":
    run()
