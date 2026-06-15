# 🛡️ ShieldGuard Live App Monitoring System v7.0 (Ultra UI)

Welcome to the official repository for the ShieldGuard Wearable Monitoring System. This project seamlessly integrates an IoT hardware layer (ESP8266) with a modern, feature-rich desktop dashboard application (Python/CustomTkinter) via Google Firebase Realtime Database.

---

## 📂 Repository Navigation: What to Read First?

To understand the project layout and deploy it successfully, explore the files in this specific sequence:

1. **`README.md` (This File):** Read this first for a high-level conceptual overview, feature breakdown, and complete database/software deployment instructions.
2. **`hardware_settings.txt`:** Review this file next to understand the physical components, complete wiring schematics, pin maps, and power distributions.
3. **`sketch_apr29a.ino`:** Inspect the hardware source code to see how the microcontroller initializes Wi-Fi, handles live calibration, reads raw telemetry, and synchronizes state with the cloud.
4. **`backend.py`:** Examine this background controller layer that manages administrative file tasks, system log writing, and live data streaming hooks via the Firebase Admin SDK.
5. **`main.py`:** Finally, launch or read the frontend code to see the modern user interface, view routing, real-time threshold slider controls, and asynchronous warning loops.

---

## ✨ System Features (Ultra UI Edition)

* **🎛️ Interactive Smart Calibration:** Set a customized light triggering threshold dynamically directly from the desktop dashboard (0-1023 slider range).
* **📊 Live Telemetry Streaming:** Streams raw light value metrics from the wearable module straight to your dashboard UI with low-latency monitoring (< 400ms interval updates).
* **🚨 Desktop Intrusion Alerts:** Uses an asynchronous, multi-threaded worker loop to push persistent Windows desktop banner alerts (`win10toast`) the split-second a beam disruption occurs.
* **🔒 Secure Local Authentication:** Features a dual-screen initialization layout. First-time users are forced to link their device ID and create a unique master password.
* **🔄 State Synchronization:** Dedicated interactive dashboard commands to ARM the system or issue a complete remote DISARM / ALARM RESET sequence.
* **📜 Integrated Activity Logs:** A built-in terminal text view that actively aggregates all administrative and cloud events.
* **🗑️ Factory Reset Sandbox:** A secure "Danger Zone" button that unlinks paired configuration files, flushes active credentials, and performs a complete system factory reset.

---

## 🚀 Deployment and Setup Guide

### Phase 1: ☁️ Firebase Cloud Configuration
1. Navigate to the [Firebase Console](https://console.firebase.google.com/) and spin up a new project.
2. Under **Build** > **Realtime Database**, click **Create Database** (Start in Test Mode).
3. Under the **Rules** tab, ensure `.read` and `.write` are set to `true`.
4. Go to **Project settings** (⚙️) > **Service accounts** and click **Generate new private key**.
5. Rename the downloaded file to `serviceAccountKey.json` and place it in the root folder of your Python app.
6. Under **Database secrets**, copy your token (`FIREBASE_AUTH`).
7. Copy your Realtime Database URL, removing `https://` and the trailing `/` (`FIREBASE_HOST`).

### Phase 2: 💻 Microcontroller Upload
1. Open `sketch_apr29a.ino` in the Arduino IDE.
2. Replace the placeholder fields with your local configuration (WIFI_SSID, WIFI_PASSWORD, FIREBASE_HOST, FIREBASE_AUTH).
3. Connect your ESP8266 and upload the sketch.

### Phase 3: 🖥️ Desktop Dashboard Activation
1. Verify Python 3.x is installed.
2. Open your terminal in the workspace and run: `pip install customtkinter firebase-admin win10toast plyer pillow`
3. Boot the dashboard: `python main.py`
"""
