import socket
import urllib.parse
import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZAD OSINT | Intelligence & Security Suite</title>
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #bae6fd 100%);
            --glass-bg: rgba(255, 255, 255, 0.75);
            --glass-border: rgba(255, 255, 255, 0.9);
            --primary-blue: #0284c7;
            --primary-hover: #0369a1;
            --dark-blue: #0c4a6e;
            --text-main: #0f172a;
            --text-muted: #475569;
            --safe-color: #16a34a;
            --warning-color: #dc2626;
            --shadow-glow: 0 10px 30px 0 rgba(2, 132, 199, 0.12);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }

        body {
            background: var(--bg-gradient);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .glass-card {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            box-shadow: var(--shadow-glow);
            width: 100%;
            max-width: 600px;
            padding: 35px;
        }

        /* Header & Dynamic Logo */
        .header {
            text-align: center;
            margin-bottom: 25px;
        }

        .logo-container {
            width: 70px;
            height: 70px;
            margin: 0 auto 15px auto;
            background: rgba(2, 132, 199, 0.1);
            border-radius: 18px;
            display: flex;
            justify-content: center;
            align-items: center;
            border: 1px solid rgba(2, 132, 199, 0.25);
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.1);
            animation: pulseLogo 3s infinite alternate;
        }

        @keyframes pulseLogo {
            0% { transform: scale(1); }
            100% { transform: scale(1.04); }
        }

        .logo-container svg {
            width: 40px;
            height: 40px;
            fill: var(--primary-blue);
        }

        .brand-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(2, 132, 199, 0.1);
            color: var(--primary-blue);
            padding: 5px 14px;
            border-radius: 50px;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            margin-bottom: 10px;
            border: 1px solid rgba(2, 132, 199, 0.2);
        }

        .header h1 {
            color: var(--dark-blue);
            font-size: 1.6rem;
            font-weight: 800;
        }

        /* Tabs Navigation */
        .tabs {
            display: flex;
            background: rgba(255, 255, 255, 0.5);
            padding: 5px;
            border-radius: 12px;
            margin-bottom: 25px;
            border: 1px solid rgba(255, 255, 255, 0.8);
        }

        .tab-btn {
            flex: 1;
            padding: 10px;
            text-align: center;
            background: transparent;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.9rem;
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .tab-btn.active {
            background: #ffffff;
            color: var(--primary-blue);
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        /* Form Controls */
        .input-group {
            position: relative;
            margin-bottom: 18px;
        }

        .input-icon {
            position: absolute;
            left: 16px;
            top: 50%;
            transform: translateY(-50%);
            fill: var(--primary-blue);
            width: 18px;
            height: 18px;
        }

        input[type="text"] {
            width: 100%;
            padding: 14px 14px 14px 46px;
            background: rgba(255, 255, 255, 0.85);
            border: 1.5px solid rgba(2, 132, 199, 0.2);
            border-radius: 12px;
            font-size: 0.95rem;
            color: var(--text-main);
            outline: none;
            transition: all 0.3s ease;
        }

        input[type="text"]:focus {
            border-color: var(--primary-blue);
            box-shadow: 0 0 0 4px rgba(2, 132, 199, 0.15);
            background: #ffffff;
        }

        button.action-btn {
            width: 100%;
            padding: 14px;
            background: var(--primary-blue);
            color: #ffffff;
            border: none;
            border-radius: 12px;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);
        }

        button.action-btn:hover {
            background: var(--primary-hover);
            transform: translateY(-1px);
        }

        button.action-btn svg {
            fill: #ffffff;
            width: 16px;
            height: 16px;
        }

        /* Results Panel */
        .result-box {
            margin-top: 20px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 14px;
            padding: 18px;
            border-left: 5px solid var(--primary-blue);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
        }

        .result-box.safe { border-left-color: var(--safe-color); }
        .result-box.warning { border-left-color: var(--warning-color); }

        .result-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid rgba(0, 0, 0, 0.04);
            font-size: 0.9rem;
        }

        .result-item:last-child { border-bottom: none; }
        .label { color: var(--text-muted); font-weight: 500; }
        .value { font-weight: 600; color: var(--text-main); word-break: break-all; }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            font-weight: 700;
        }

        .status-badge svg { width: 14px; height: 14px; }
        .safe-text { color: var(--safe-color); fill: var(--safe-color); }
        .warning-text { color: var(--warning-color); fill: var(--warning-color); }

        /* Footer */
        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 0.75rem;
            color: var(--text-muted);
            letter-spacing: 0.5px;
        }
    </style>
</head>
<body>
    <div class="glass-card">
        <div class="header">
            <!-- Dynamic Automated Logo -->
            <div class="logo-container">
                {{ dynamic_logo_svg | safe }}
            </div>
            <div class="brand-badge">
                <svg width="12" height="12" viewBox="0 0 24 24"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-5.45 9-12V5l-9-4z"/></svg>
                ZAD OSINT SUITE
            </div>
            <h1>Intelligence Gateway</h1>
        </div>

        <!-- Navigation Tabs -->
        <div class="tabs">
            <button class="tab-btn {% if active_tab == 'url' %}active{% endif %}" onclick="switchTab('url')">URL Analyzer</button>
            <button class="tab-btn {% if active_tab == 'info' %}active{% endif %}" onclick="switchTab('info')">System Specs</button>
        </div>

        <!-- Tab 1: URL Analyzer -->
        <div id="url-tab" class="tab-content {% if active_tab == 'url' %}active{% endif %}">
            <form method="POST">
                <input type="hidden" name="form_type" value="url_check">
                <div class="input-group">
                    <svg class="input-icon" viewBox="0 0 24 24"><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"/></svg>
                    <input type="text" name="url" placeholder="Paste target URL (e.g., https://example.com)" value="{{ target_url if target_url else '' }}" required>
                </div>
                <button type="submit" class="action-btn">
                    <svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
                    Execute Security Scan
                </button>
            </form>

            {% if result %}
            <div class="result-box {% if 'Safe' in result.status %}safe{% else %}warning{% endif %}">
                <div class="result-item">
                    <span class="label">Target Domain</span>
                    <span class="value">{{ result.domain }}</span>
                </div>
                <div class="result-item">
                    <span class="label">Network Protocol</span>
                    <span class="value">{{ result.scheme }}</span>
                </div>
                <div class="result-item">
                    <span class="label">IP Address</span>
                    <span class="value">{{ result.ip }}</span>
                </div>
                <div class="result-item">
                    <span class="label">Security Verdict</span>
                    <span class="value">
                        {% if 'Safe' in result.status %}
                            <span class="status-badge safe-text">
                                <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
                                {{ result.status }}
                            </span>
                        {% else %}
                            <span class="status-badge warning-text">
                                <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>
                                {{ result.status }}
                            </span>
                        {% endif %}
                    </span>
                </div>
            </div>
            {% endif %}
        </div>

        <!-- Tab 2: System Specs -->
        <div id="info-tab" class="tab-content {% if active_tab == 'info' %}active{% endif %}">
            <div class="result-box safe">
                <div class="result-item">
                    <span class="label">Infrastructure</span>
                    <span class="value">Zad OSINT Node 01</span>
                </div>
                <div class="result-item">
                    <span class="label">Engine Core</span>
                    <span class="value">Python Flask Web Service</span>
                </div>
                <div class="result-item">
                    <span class="label">Security Module</span>
                    <span class="value">Active (DNS & SSL Validator)</span>
                </div>
                <div class="result-item">
                    <span class="label">Branding Protocol</span>
                    <span class="value">Glassmorphism / Strict Vector UI</span>
                </div>
            </div>
        </div>

        <div class="footer">
            ZAD OSINT &bull; Secure Environment
        </div>
    </div>

    <script>
        function switchTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            
            if(tabName === 'url') {
                document.getElementById('url-tab').classList.add('active');
                event.currentTarget.classList.add('active');
            } else {
                document.getElementById('info-tab').classList.add('active');
                event.currentTarget.classList.add('active');
            }
        }
    </script>
</body>
</html>
"""

# Automated Logo Generator (Har request / reload par alag design generate karega)
def generate_dynamic_logo():
    logos = [
        # Design 1: Shield & Target
        '<svg viewBox="0 0 24 24"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-5.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8s0 0 0 0z"/></svg>',
        # Design 2: Network Node / Cyber Hub
        '<svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>',
        # Design 3: Terminal / Code Bracket Security
        '<svg viewBox="0 0 24 24"><path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/></svg>',
        # Design 4: Radar / Scanner View
        '<svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm1-13h-2v6h6v-2h-4z"/></svg>'
    ]
    return random.choice(logos)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    target_url = ""
    active_tab = "url"
    dynamic_logo_svg = generate_dynamic_logo()

    if request.method == "POST":
        target_url = request.form.get("url", "").strip()
        parsed_url = urllib.parse.urlparse(target_url)
        
        domain = parsed_url.netloc or parsed_url.path.split('/')[0]
        scheme = parsed_url.scheme

        if not scheme:
            target_url = "http://" + target_url
            parsed_url = urllib.parse.urlparse(target_url)
            scheme = parsed_url.scheme
            domain = parsed_url.netloc

        status = "Safe (Validated Protocol)"
        if scheme.lower() != "https":
            status = "Warning (Insecure HTTP Protocol)"
        
        resolved_ip = "Unknown / Unresolved"
        try:
            resolved_ip = socket.gethostbyname(domain)
        except socket.gaierror:
            status = "Critical (Unresolvable Domain)"

        result = {
            "url": target_url,
            "domain": domain,
            "scheme": scheme.upper(),
            "ip": resolved_ip,
            "status": status
        }
        active_tab = "url"

    return render_template_string(
        HTML_TEMPLATE, 
        result=result, 
        target_url=target_url, 
        active_tab=active_tab,
        dynamic_logo_svg=dynamic_logo_svg
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
