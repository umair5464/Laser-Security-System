import firebase_admin
from firebase_admin import credentials, db
import os
from datetime import datetime

class ShieldGuardBackend:
    def __init__(self):
        self.CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
        self.JSON_PATH = os.path.join(self.CURRENT_DIR, "serviceAccountKey.json")
        self.CONFIG_FILE = os.path.join(self.CURRENT_DIR, "laser_guard_config.txt")
        self.LOG_FILE = os.path.join(self.CURRENT_DIR, "security_logs.txt")
        
        self.dev_id = ""
        self.dev_pw = ""
        self._init_firebase()

    def _init_firebase(self):
        # Stop execution and warn user if JSON is missing
        if not os.path.exists(self.JSON_PATH):
            print("\n" + "="*50)
            print("🚨 SETUP REQUIRED: Firebase Key Missing!")
            print("1. Go to Firebase Console (Project Settings -> Service Accounts).")
            print("2. Click on 'Generate new private key'.")
            print("3. Rename the downloaded file to 'serviceAccountKey.json'.")
            print("4. Paste it in the same folder as main.py.")
            print("="*50 + "\n")
            return 

        if not firebase_admin._apps:
            try:
                cred = credentials.Certificate(self.JSON_PATH)
                # USER INSTRUCTION: Update the database URL below
                firebase_admin.initialize_app(cred, {'databaseURL': 'https://YOUR-PROJECT-ID.firebaseio.com/'})
            except Exception as e:
                print("Firebase Connection Error:", e)

    # --- SETUP & LOGIN LOGIC ---
    def is_setup_complete(self):
        return os.path.exists(self.CONFIG_FILE)

    def register_device(self, d_id, d_pw):
        with open(self.CONFIG_FILE, "w") as f: 
            f.write(f"{d_id}:{d_pw}")
        self.log_event("Device Paired and Registered.")

    def verify_login(self, input_pw):
        with open(self.CONFIG_FILE, "r") as f: 
            data = f.read().split(":")
            self.dev_id = data[0]
            self.dev_pw = data[1]
        return input_pw == self.dev_pw

    def remove_account(self):
        if os.path.exists(self.CONFIG_FILE): 
            os.remove(self.CONFIG_FILE)
            self.log_event("Account Data Removed/Factory Reset.")

    # --- LOGS LOGIC ---
    def log_event(self, event_text):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {event_text}\n"
        with open(self.LOG_FILE, "a") as f: 
            f.write(log_entry)
        return log_entry

    def get_all_logs(self):
        if os.path.exists(self.LOG_FILE):
            with open(self.LOG_FILE, "r") as f: 
                return f.read()
        return ""

    # --- HARDWARE COMMANDS ---
    def send_arm_command(self):
        try: db.reference(f'/{self.dev_id}/system/arm_command').set(True)
        except: pass

    def send_reset_command(self):
        try: db.reference(f'/{self.dev_id}/system/reset').set(True)
        except: pass

    def update_manual_threshold(self, value):
        try: db.reference(f'/{self.dev_id}/system/threshold').set(int(value))
        except: pass

    # --- REAL-TIME LISTENERS ---
    def start_listeners(self, status_callback, ldr_callback):
        try:
            db.reference(f'/{self.dev_id}/system/status').listen(status_callback)
            db.reference(f'/{self.dev_id}/system/current_ldr').listen(ldr_callback)
        except Exception as e:
            print("Listener Error:", e)