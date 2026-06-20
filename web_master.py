import requests
import sys
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import random

parser = argparse.ArgumentParser(description="Future Cybersecurity Web Scanner")
parser.add_argument("-t", "--target", required=True, help="Target URL (e.g., http://example.com)")
args = parser.parse_args()
target_url = args.target.rstrip('/')

print("-" * 60)
print(f"[*] ULTIMATE FUTURE WEB AUDITOR ACTIVE")
print(f"[*] TARGET: {target_url}")
print("-" * 60)

# ఫైర్‌వాల్‌ని మోసం చేయడానికి రకరకాల యూజర్ ఏజెంట్లు (WAF Bypass)
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
    'Mozilla/5.0 (Android Master Future Web Scanner v3.0)'
]

try:
    with open("words.txt", "r") as f:
        directories = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print("[!] 'words.txt' ఫైల్ దొరకలేదు.")
    sys.exit()

# రిపోర్ట్ ఫైల్ సెటప్
report = open("live_vulnerability_report.txt", "a", encoding="utf-8")
report.write(f"\n\n--- Scan on {target_url} ({datetime.now()}) ---\n")

def advanced_crawl(path):
    if not path.startswith('/'): path = '/' + path
    full_url = target_url + path
    
    try:
        # ప్రతీ రిక్వెస్ట్‌కి రాండమ్‌గా ఒక బ్రౌజర్ పేరును మార్చడం (Stealth)
        headers = {'User-Agent': random.choice(user_agents)}
        
        # ఇక్కడ allow_redirects=True గా మార్చబడింది (ఇంటర్వ్యూ స్టాండర్డ్)
        response = requests.get(full_url, headers=headers, timeout=4.0, allow_redirects=True)
        
        content_len = len(response.content)
        
        if response.status_code == 200:
            msg = f" [🔥 ALERT] దొрикиంది! ➔ {full_url} [Size: {content_len} bytes]"
            print(msg)
            report.write(msg + "\n")
            
            if "admin" in path or "api" in path:
                print(f"   └── [💡 Hint] ఈ డైరెక్టరీ లోపల సబ్-స్కాన్ రన్ చేయడం బెస్ట్!")
                
        elif response.status_code == 403:
            msg = f" [⚠️ WARNING] లాక్ చేయబడిన రహస్య ఫోల్డర్ ➔ {full_url}"
            print(msg)
            report.write(msg + "\n")
            
    except requests.exceptions.RequestException:
        pass

print(f"[*] {len(directories)} పాత్‌లను అడ్వాన్స్‌డ్ స్టెల్త్ మోడ్‌లో స్కాన్ చేస్తున్నాము...\n")

with ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(advanced_crawl, directories)

report.close()
print("-" * 60)
print("[*] స్కాన్ పూర్తయింది. రిపోర్ట్ 'live_vulnerability_report.txt' లో అప్‌డేట్ అయింది.")
print("-" * 60)

