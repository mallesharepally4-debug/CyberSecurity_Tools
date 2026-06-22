import socket
import sys
import json
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import threading
from colorama import init, Fore, Style

# Colorama ప్రారంభించడం
init(autoreset=True)

print_lock = threading.Lock()
open_ports_data = {}

# Shodan API Key (మీకు కీ ఉంటే ఇక్కడ పెట్టండి, లేదంటే పబ్లిక్ ఫీచర్స్ రన్ అవుతాయి)
SHODAN_API_KEY = "YOUR_SHODAN_API_KEY_HERE" 

COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 
    445: "SMB", 1433: "MSSQL", 3306: "MySQL", 3389: "RDP", 8080: "HTTP-Proxy"
}

print(Fore.CYAN + "-" * 75)
print(Fore.YELLOW + "   🔥 ULTIMATE LEVEL: MULTI-THREADED OSINT & BANNER SCANNER v5.1 PRO 🔥")
print(Fore.CYAN + "-" * 75)

target = input("Enter Target IP Address or Website: ")

try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print(Fore.RED + "\n[!] Error: Invalid Hostname or IP. Exiting...")
    sys.exit()

try:
    start_port = int(input("Enter Start Port: "))
    end_port = int(input("Enter End Port: "))
except ValueError:
    print(Fore.RED + "[!] Error: Ports must be numbers. Exiting...")
    sys.exit()

if start_port > end_port:
    print(Fore.RED + "[!] Error: Start port cannot be greater than End port.")
    sys.exit()

save_report = input("Do you want to save results to a JSON file? (y/n): ").lower() == 'y'

print(Fore.CYAN + "-" * 75)
print(Fore.GREEN + f"[*] Target Host   : {target}")
print(Fore.GREEN + f"[*] Target IP     : {target_ip}")
print(Fore.GREEN + f"[*] Port Range    : {start_port} to {end_port}")
print(Fore.GREEN + f"[*] Scan Started  : {str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}")
print(Fore.CYAN + "-" * 75)

# 1. ADVANCED: GEO-IP LOOKUP (ఫిక్స్ చేయబడిన పర్ఫెక్ట్ URL)
print(Fore.BLUE + "[*] Fetching Geo-IP Intelligence...")
try:
    geo_resp = requests.get(f"http://ip-api.com/json/{target_ip}", timeout=5).json()
    if geo_resp.get('status') == 'success':
        print(f"    ↳ Country : {geo_resp.get('country', 'Unknown')} ({geo_resp.get('countryCode', '??')})")
        print(f"    ↳ Region  : {geo_resp.get('regionName', 'Unknown')}, {geo_resp.get('city', 'Unknown')}")
        print(f"    ↳ ISP     : {geo_resp.get('isp', 'Unknown')}")
        print(f"    ↳ ASN     : {geo_resp.get('as', 'Unknown')}")
    else:
        print(Fore.YELLOW + f"    [!] Geo-IP info failed: {geo_resp.get('message', 'Unknown error')}")
except Exception:
    print(Fore.RED + "    [!] Could not connect to Geo-IP service.")

# 2. ADVANCED: SHODAN OSINT LOOKUP (API ఎండ్‌పాయింట్ ఫిక్స్ చేయబడింది)
if SHODAN_API_KEY != "YOUR_SHODAN_API_KEY_HERE":
    print(Fore.BLUE + "\n[*] Querying Shodan Intelligence Database...")
    try:
        shodan_url = f"https://api.shodan.io/shodan/host/{target_ip}?key={SHODAN_API_KEY}"
        shodan_resp = requests.get(shodan_url, timeout=5).json()
        if "ports" in shodan_resp:
            print(Fore.MAGENTA + f"    ↳ Shodan Historical Open Ports: {shodan_resp['ports']}")
            if "vulns" in shodan_resp:
                print(Fore.RED + f"    ↳ Potential Vulnerabilities: {shodan_resp['vulns'][:5]}")
        else:
            print("    ↳ No historical records found in Shodan.")
    except Exception:
        print(Fore.RED + "    [!] Shodan lookup failed (Check API Key).")

print(Fore.CYAN + "\n" + "-" * 75)
print(Fore.YELLOW + "[*] Starting Active Multi-Threaded Port Scan...")
print(Fore.CYAN + "-" * 75)

# సింగిల్ పోర్ట్ స్కాన్ ఫంక్షన్
def scan_and_grab(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.5) 
        result = s.connect_ex((target_ip, port))
        
        if result == 0:
            banner = "[No Banner Discovered]"
            guessed_service = COMMON_SERVICES.get(port, "Unknown Service")
            
            try:
                # కండిషన్ ఇక్కడ పక్కాగా ఫిక్స్ చేయబడింది
                if port in [80, 8080, 443]:
                    req = f"HEAD / HTTP/1.1\r\nHost: {target}\r\nConnection: close\r\n\r\n"
                    s.sendall(req.encode())
                
                response = s.recv(1024).decode('utf-8', errors='ignore').strip()
                if response:
                    banner = response.split('\n')[0].strip()
            except:
                pass
                
            with print_lock:
                print(Fore.GREEN + f"[+] Port {port:<5} : OPEN")
                print(Style.DIM + f"    ↳ Service : {guessed_service}")
                print(Style.DIM + f"    ↳ Banner  : {banner}\n")
                
                open_ports_data[port] = {
                    "status": "OPEN",
                    "probable_service": guessed_service,
                    "banner": banner
                }
            
        s.close()
    except Exception:
        pass

# మల్టీ-థ్రెడింగ్ ఇంజిన్
ports_to_scan = range(start_port, end_port + 1)
with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scan_and_grab, ports_to_scan)

print(Fore.CYAN + "-" * 75)
print(Fore.GREEN + f"[*] Scan Completed! Total Open Ports Found: {len(open_ports_data)}")

if save_report and open_ports_data:
    filename = f"advanced_report_{target_ip}.json"
    with open(filename, 'w') as f:
        json.dump(open_ports_data, f, indent=4)
    print(Fore.YELLOW + f"[+] Advanced Report saved to: {filename}")

print(Fore.CYAN + "-" * 75)

