import threading, socket, json, os
from datetime import datetime
from plyer import notification

CONFIG_FILE = "security_config.json"

class SecuritySystem:
    def __init__(self):
        self.is_breached = False
        self.running = False
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f: return json.load(f)
        return {"nodemcu_ip": "192.168.1.1", "is_first_login": True, "logs": [], "theme": "Dark"}

    def save_config(self):
        with open(CONFIG_FILE, 'w') as f: json.dump(self.config, f)

    def send_wifi_command(self, cmd):
        target = self.config.get("nodemcu_ip")
        def task():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((target, 8081))
                s.sendall(cmd.encode())
                s.close()
                print(f"[SUCCESS] {cmd} command delivered to NodeMCU")
            except Exception as e:
                print(f"[ERROR] Connection failed: {e}")
        threading.Thread(target=task, daemon=True).start()

    def start_monitoring(self, callback):
        self.running = True
        threading.Thread(target=self._listener, args=(callback,), daemon=True).start()

    def _listener(self, callback):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 8080))
        s.listen(1)
        while self.running:
            try:
                s.settimeout(2)
                conn, addr = s.accept()
                if "BREACH" in conn.recv(1024).decode():
                    self.is_breached = True
                    notification.notify(title="🚨 SECURITY ALERT", message="Laser Beam Broken!")
                    callback()
                conn.close()
            except: continue