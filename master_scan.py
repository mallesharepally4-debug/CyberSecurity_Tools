import socket
import sys
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# 1. కమాండ్ లైన్ ఆర్గ్యుమెంట్స్ సెటప్ (Nmap లుక్ కోసం)
parser = argparse.ArgumentParser(description="Android Professional Master Scanner")
parser.add_argument("-t", "--target", required=True, help="Target IP or Domain Name")
args = parser.parse_args()

try:
    target_ip = socket.gethostbyname(args.target)
except socket.gaierror:
    print("[!] లోపం: డొమైన్ లేదా ఐపీ అడ్రస్ తప్పుగా ఉంది.")
    sys.exit()

print("-" * 60)
print(f"[*] TARGET: {args.target} ({target_ip})")
print(f"[*] SCAN STARTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("-" * 60)

# రిపోర్ట్ ఫైల్ ఓపెన్ చేయడం
report_file = open("scan_report.txt", "w", encoding="utf-8")
report_file.write(f"Scan Report for {args.target} ({target_ip})\n")
report_file.write("-" * 50 + "\n")

def master_scan(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        result = s.connect_ex((target_ip, port))
        
        if result == 0:
            output = ""
            try:
                banner = s.recv(1024).decode().strip()
                if banner:
                    output = f" [+] పోర్ట్ {port}: ఓపెన్ ➔ [వెర్షన్: {banner}]"
                else:
                    s.send(b"HEAD / HTTP/1.1\r\nHost: " + args.target.encode() + b"\r\n\r\n")
                    banner = s.recv(1024).decode().strip().split('\n')[0]
                    output = f" [+] పోర్ట్ {port}: ఓపెన్ ➔ [సర్వర్: {banner}]"
            except:
                output = f" [+] పోర్ట్ {port}: ఓపెన్ (సాఫ్ట్‌వేర్ వివరాలు దాచబడ్డాయి)"
            
            print(output)
            report_file.write(output + "\n") # ఫైల్‌లోకి ఆటోమేటిక్‌గా సేవ్ చేయడం
            
        s.close()
    except Exception:
        pass

try:
    # 2. మల్టీ-థ్రెడింగ్ రన్ చేయడం
    with ThreadPoolExecutor(max_workers=100) as executor:
        ports = [21, 22, 25, 53, 80, 110, 443, 8080]
        executor.map(master_scan, ports)
        
except KeyboardInterrupt:
    # 3. యూజర్ మధ్యలో ఆపేస్తే వచ్చే ఎర్రర్ కంట్రోల్
    print("\n[!] స్కాన్ యూజర్ ద్వారా మధ్యలో ఆపివేయబడింది.")
    report_file.write("\n[!] Scan interrupted by user.")
    sys.exit()

finally:
    print("-" * 60)
    print("[*] స్కాన్ పూర్తయింది. రిపోర్ట్ 'scan_report.txt' లో సేవ్ చేయబడింది.")
    print("-" * 60)
    report_file.close()

