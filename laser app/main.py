import customtkinter as ctk
import os
import threading
import time
from win10toast import ToastNotifier
from PIL import Image 
from backend import ShieldGuardBackend 

# --- ULTRA-MODERN BRANDING & COLORS ---
COMPANY_NAME = "ShieldGuard"
THEME_COLOR = "#153A4A"        # Main Background
CARD_COLOR = "#1c4f63"         # Slightly lighter for depth/cards
ACCENT_COLOR = "#1fcf8d"       # Neon Green 
DANGER_COLOR = "#ff4757"       # Soft Red for alerts/resets
APP_VERSION = "v7.0 (Ultra UI)"

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
LOGO_PATH = os.path.join(CURRENT_DIR, "logo.png") 
ICON_PATH = os.path.join(CURRENT_DIR, "icon.ico") 

toaster = ToastNotifier()

class ShieldGuardUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(COMPANY_NAME)
        self.geometry("400x750") 
        self.resizable(False, False) # Fixed size for perfect mobile layout
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=THEME_COLOR)
        
        try: self.iconbitmap(ICON_PATH)
        except: pass

        self.engine = ShieldGuardBackend()
        self.is_breached = False 
        
        # Main Window Container
        self.container = ctk.CTkFrame(self, fg_color=THEME_COLOR, corner_radius=0)
        self.container.pack(fill="both", expand=True)

        self.show_splash_screen()

    # ==========================================
    # 1. PURE IMAGE SPLASH SCREEN (PERFECTLY CENTERED)
    # ==========================================
    def show_splash_screen(self):
        self.splash_frame = ctk.CTkFrame(self.container, fg_color=THEME_COLOR, corner_radius=0)
        self.splash_frame.place(relwidth=1, relheight=1) # Fills entire screen
        
        try:
            my_image = ctk.CTkImage(light_image=Image.open(LOGO_PATH), dark_image=Image.open(LOGO_PATH), size=(180, 180))
            logo_label = ctk.CTkLabel(self.splash_frame, image=my_image, text="")
        except:
            logo_label = ctk.CTkLabel(self.splash_frame, text="🛡️", font=("Arial", 100))
            
        # Absolute Center Alignment
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
        
        self.after(2500, self.route_auth)

    def route_auth(self):
        self.splash_frame.destroy()
        if not self.engine.is_setup_complete(): 
            self.build_setup_ui()
        else: 
            self.build_login_ui()

    # ==========================================
    # 2. SETUP & LOGIN (CARD-BASED CENTERED UI)
    # ==========================================
    def build_setup_ui(self):
        self.setup_frame = ctk.CTkFrame(self.container, fg_color=THEME_COLOR, corner_radius=0)
        self.setup_frame.place(relwidth=1, relheight=1)
        
        # Centered Card
        card = ctk.CTkFrame(self.setup_frame, fg_color=CARD_COLOR, corner_radius=20)
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.5)
        
        ctk.CTkLabel(card, text="Device Setup", font=("Arial", 26, "bold")).pack(pady=(40, 20))
        self.s_id = ctk.CTkEntry(card, placeholder_text="Enter Hardware ID", width=240, height=45, border_width=1)
        self.s_id.pack(pady=10)
        self.s_pw = ctk.CTkEntry(card, placeholder_text="Create Master Password", show="*", width=240, height=45, border_width=1)
        self.s_pw.pack(pady=10)
        
        ctk.CTkButton(card, text="REGISTER", font=("Arial", 14, "bold"), height=45, fg_color=ACCENT_COLOR, text_color="black", command=self.handle_setup).pack(pady=(25, 20))

    def handle_setup(self):
        if self.s_id.get() and self.s_pw.get():
            self.engine.register_device(self.s_id.get(), self.s_pw.get())
            self.setup_frame.destroy()
            self.build_login_ui()

    def build_login_ui(self):
        self.login_frame = ctk.CTkFrame(self.container, fg_color=THEME_COLOR, corner_radius=0)
        self.login_frame.place(relwidth=1, relheight=1)
        
        try:
            img = ctk.CTkImage(Image.open(LOGO_PATH), size=(100, 100))
            logo_lbl = ctk.CTkLabel(self.login_frame, image=img, text="")
        except:
            logo_lbl = ctk.CTkLabel(self.login_frame, text="🔒", font=("Arial", 70))
        logo_lbl.place(relx=0.5, rely=0.25, anchor="center")

        card = ctk.CTkFrame(self.login_frame, fg_color=CARD_COLOR, corner_radius=20)
        card.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.85, relheight=0.4)

        ctk.CTkLabel(card, text="Secure Login", font=("Arial", 24, "bold")).pack(pady=(30, 20))
        self.l_pw = ctk.CTkEntry(card, placeholder_text="Enter Password", show="*", width=240, height=45)
        self.l_pw.pack(pady=10)
        
        self.login_error = ctk.CTkLabel(card, text="", text_color=DANGER_COLOR, font=("Arial", 12))
        self.login_error.pack()
        
        ctk.CTkButton(card, text="UNLOCK APP", font=("Arial", 14, "bold"), height=45, width=240, fg_color=ACCENT_COLOR, text_color="black", command=self.handle_login).pack(pady=(15, 20))

    def handle_login(self):
        if self.engine.verify_login(self.l_pw.get()):
            self.login_frame.destroy()
            self.build_main_ui()
        else:
            self.login_error.configure(text="Incorrect Password. Try again.")

    # ==========================================
    # 3. MAIN APP INTERFACE (MODERN LAYOUT)
    # ==========================================
    def build_main_ui(self):
        # --- Top Header ---
        self.header = ctk.CTkFrame(self.container, fg_color=CARD_COLOR, height=60, corner_radius=0)
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)
        ctk.CTkLabel(self.header, text=COMPANY_NAME, font=("Arial", 20, "bold"), text_color=ACCENT_COLOR).pack(side="left", padx=20, pady=15)

        # --- Dynamic Body ---
        self.body = ctk.CTkFrame(self.container, fg_color=THEME_COLOR, corner_radius=0)
        self.body.pack(fill="both", expand=True)

        # --- Bottom Navigation (Perfectly Aligned Grid) ---
        self.nav_bar = ctk.CTkFrame(self.container, fg_color=CARD_COLOR, height=70, corner_radius=0)
        self.nav_bar.pack(side="bottom", fill="x")
        self.nav_bar.pack_propagate(False)
        
        self.nav_bar.columnconfigure((0, 1, 2), weight=1) # Splits width into 3 equal parts
        
        nav_font = ("Arial", 14, "bold")
        ctk.CTkButton(self.nav_bar, text="🛡️ Home", font=nav_font, fg_color="transparent", hover_color=THEME_COLOR, command=lambda: self.switch_tab("dashboard")).grid(row=0, column=0, sticky="nsew", pady=15)
        ctk.CTkButton(self.nav_bar, text="⚙️ Settings", font=nav_font, fg_color="transparent", hover_color=THEME_COLOR, command=lambda: self.switch_tab("details")).grid(row=0, column=1, sticky="nsew", pady=15)
        ctk.CTkButton(self.nav_bar, text="🏢 Profile", font=nav_font, fg_color="transparent", hover_color=THEME_COLOR, command=lambda: self.switch_tab("info")).grid(row=0, column=2, sticky="nsew", pady=15)

        # --- Initialize Tabs ---
        self.frames = {}
        self.create_dashboard_frame()
        self.create_details_frame()
        self.create_info_frame()

        self.switch_tab("dashboard") 
        self.engine.start_listeners(self.on_firebase_status, self.on_firebase_ldr)

    # ==========================================
    # TAB 1: DASHBOARD
    # ==========================================
    def create_dashboard_frame(self):
        frame = ctk.CTkFrame(self.body, fg_color="transparent")
        self.frames["dashboard"] = frame
        
        # Status Card
        status_card = ctk.CTkFrame(frame, fg_color=CARD_COLOR, corner_radius=20)
        status_card.pack(pady=(40, 20), padx=20, fill="x")
        
        ctk.CTkLabel(status_card, text="CURRENT STATUS", font=("Arial", 12, "bold"), text_color="gray").pack(pady=(20, 0))
        self.status_disp = ctk.CTkLabel(status_card, text="READY", font=("Impact", 50), text_color=ACCENT_COLOR)
        self.status_disp.pack(pady=(0, 30))

        # Action Buttons
        self.arm_btn = ctk.CTkButton(frame, text="ARM SECURITY", font=("Arial", 18, "bold"), height=65, corner_radius=15, fg_color=ACCENT_COLOR, text_color="black", command=self.click_arm)
        self.arm_btn.pack(pady=20, fill="x", padx=30)
        
        ctk.CTkButton(frame, text="DISARM / RESET", font=("Arial", 16, "bold"), height=55, corner_radius=15, fg_color="transparent", border_width=2, border_color=DANGER_COLOR, text_color=DANGER_COLOR, hover_color=DANGER_COLOR, command=self.click_reset).pack(pady=10, fill="x", padx=30)

    # ==========================================
    # TAB 2: ADVANCED DETAILS & SETTINGS
    # ==========================================
    def create_details_frame(self):
        frame = ctk.CTkFrame(self.body, fg_color="transparent")
        self.frames["details"] = frame
        
        ctk.CTkLabel(frame, text="Live Telemetry", font=("Arial", 20, "bold")).pack(pady=(20, 10), anchor="w", padx=25)
        
        # Live Sensor Monitor Card
        monitor_card = ctk.CTkFrame(frame, fg_color=CARD_COLOR, corner_radius=15)
        monitor_card.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(monitor_card, text="Real-Time LDR Intensity", font=("Arial", 12), text_color="gray").pack(pady=(15,0))
        self.ldr_val_lbl = ctk.CTkLabel(monitor_card, text="000", font=("Arial", 45, "bold"), text_color="yellow")
        self.ldr_val_lbl.pack(pady=(0,15))

        # Threshold Control Card
        control_card = ctk.CTkFrame(frame, fg_color=CARD_COLOR, corner_radius=15)
        control_card.pack(pady=10, padx=20, fill="x")
        
        header_frame = ctk.CTkFrame(control_card, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(15, 5))
        ctk.CTkLabel(header_frame, text="Trigger Threshold", font=("Arial", 14, "bold")).pack(side="left")
        self.thresh_lbl = ctk.CTkLabel(header_frame, text="400", font=("Arial", 14, "bold"), text_color=ACCENT_COLOR)
        self.thresh_lbl.pack(side="right")
        
        self.sld = ctk.CTkSlider(control_card, from_=0, to=1023, button_color=ACCENT_COLOR, progress_color=ACCENT_COLOR, command=self.update_threshold_ui)
        self.sld.set(400)
        self.sld.pack(pady=(0, 20), padx=20, fill="x")

        # Logs Section
        ctk.CTkLabel(frame, text="System Logs", font=("Arial", 16, "bold")).pack(pady=(15, 5), anchor="w", padx=25)
        self.log_textbox = ctk.CTkTextbox(frame, fg_color=CARD_COLOR, text_color="lightgray", corner_radius=10)
        self.log_textbox.pack(pady=5, padx=20, fill="both", expand=True)
        self.log_textbox.insert("end", self.engine.get_all_logs())

    # ==========================================
    # TAB 3: PROFILE & INFO
    # ==========================================
    def create_info_frame(self):
        frame = ctk.CTkFrame(self.body, fg_color="transparent")
        self.frames["info"] = frame
        
        ctk.CTkLabel(frame, text="Admin Profile", font=("Arial", 24, "bold")).pack(pady=(30, 20))
        
        # Info Card
        info_card = ctk.CTkFrame(frame, fg_color=CARD_COLOR, corner_radius=15)
        info_card.pack(pady=10, padx=25, fill="x")
        
        try:
            my_img = ctk.CTkImage(light_image=Image.open(LOGO_PATH), dark_image=Image.open(LOGO_PATH), size=(70, 70))
            ctk.CTkLabel(info_card, image=my_img, text="").pack(pady=(20, 5))
        except: ctk.CTkLabel(info_card, text="🛡️", font=("Arial", 50)).pack(pady=(20, 5))
            
        ctk.CTkLabel(info_card, text=COMPANY_NAME, font=("Arial", 20, "bold"), text_color=ACCENT_COLOR).pack()
        ctk.CTkLabel(info_card, text=APP_VERSION, text_color="gray", font=("Arial", 12)).pack(pady=(0, 20))

        # Contact Details Card
        contact_card = ctk.CTkFrame(frame, fg_color=CARD_COLOR, corner_radius=15)
        contact_card.pack(pady=10, padx=25, fill="x")
        
        contact_text = "📍 Headquarters: Multan, Pakistan\n📞 Contact: +92-370-0610358\n✉️ Email: m.umair546.4@gmail.com."
        ctk.CTkLabel(contact_card, text=contact_text, justify="left", font=("Arial", 14), anchor="w").pack(pady=20, padx=20, fill="x")
        
        # Danger Zone
        ctk.CTkLabel(frame, text="Danger Zone", font=("Arial", 12, "bold"), text_color=DANGER_COLOR).pack(pady=(30, 5), anchor="w", padx=30)
        ctk.CTkButton(frame, text="FACTORY RESET DEVICE", font=("Arial", 14, "bold"), height=50, corner_radius=10, fg_color=DANGER_COLOR, hover_color="#cc0000", command=self.click_factory_reset).pack(padx=25, fill="x")

    # ==========================================
    # APP LOGIC & CALLBACKS
    # ==========================================
    def switch_tab(self, name):
        for f in self.frames.values(): f.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    def update_threshold_ui(self, val):
        self.thresh_lbl.configure(text=str(int(val)))
        self.engine.update_manual_threshold(val)

    def click_arm(self):
        self.status_disp.configure(text="CALIBRATING", text_color="yellow")
        self.arm_btn.configure(state="disabled", text="PLEASE WAIT...")
        self.engine.send_arm_command()

    def click_reset(self):
        self.is_breached = False
        self.status_disp.configure(text="READY", text_color=ACCENT_COLOR)
        self.arm_btn.configure(state="normal", text="ARM SECURITY")
        self.engine.send_reset_command()

    def click_factory_reset(self):
        self.engine.remove_account()
        self.destroy()

    def on_firebase_ldr(self, event):
        if event.data is not None: 
            self.after(0, lambda: self.ldr_val_lbl.configure(text=str(event.data)))

    def on_firebase_status(self, event):
        status = str(event.data)
        self.after(0, self.update_status_ui, status)

    def update_status_ui(self, status):
        if "ARMED" in status:
            self.status_disp.configure(text="ARMED", text_color="orange")
            self.arm_btn.configure(text="SECURED")
        elif "BREACH" in status:
            self.status_disp.configure(text="BREACH!", text_color=DANGER_COLOR)
            if not self.is_breached:
                self.is_breached = True
                threading.Thread(target=self.alert_loop, daemon=True).start()

    def alert_loop(self):
        while self.is_breached:
            toaster.show_toast("🚨 ShieldGuard Alert", "Intrusion Detected in Secure Zone!", duration=4, threaded=True)
            time.sleep(5)

if __name__ == "__main__":
    app = ShieldGuardUI()
    app.mainloop()