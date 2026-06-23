# ⚡ ULTIMATE LEVEL: MULTI-THREADED OSINT & BANNER SCANNER v5.1 PRO ⚡

An advanced, high-speed network reconnaissance and intelligence gathering tool built in Python. This tool combines **Multi-Threaded Port Scanning**, **Banner Grabbing (Service Info Detection)**, and **OSINT (Geo-IP & ASN Lookup)** into a single, cohesive cybersecurity suite.

---

## 🔥 Key Features

* 🚀 **Ultra-Fast Performance:** Utilizing Python's `ThreadPoolExecutor` with up to 100 concurrent threads.
* 🛡️ **OSINT Intelligence:** Real-time Geo-IP lookup providing Country, Region, City, ISP, and ASN tracking via `ip-api.com`.
* 📡 **Banner Grabbing:** Extracts service headers and application version info directly from open ports.
* 🧠 **Intelligent Service Detection:** Built-in dictionary to guess probable services even when banners are suppressed.
* 🔒 **Race Condition Prevention:** Implements `threading.Lock()` to ensure clean, uncorrupted terminal outputs.
* 📊 **Structured Reports:** Option to automatically export clean, human-readable scan reports in `.json` format.
* 🎨 **Beautiful UI:** Fully color-coded terminal interface using `Colorama` for a professional CLI experience.

---

## 🛠️ Installation & Dependencies

To run this tool in Termux or any Linux environment, you need to install the required Python libraries first:

```bash
pip install colorama requests

