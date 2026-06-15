# ☁️ Firebase Database Setup Guide

Follow these steps to create your own Firebase Realtime Database and connect it to the ShieldGuard Wearable Monitoring System.

## Step 1: Create a Firebase Project
1. Go to the [Firebase Console](https://console.firebase.google.com/).
2. Click on **Add Project** (or Create a Project).
3. Enter a name for your project (e.g., `ShieldGuard-System`) and click **Continue**.
4. You can disable Google Analytics for this project, then click **Create Project**.

---

## Step 2: Set Up the Realtime Database
1. Once your project is ready, look at the left-hand menu and click on **Build** > **Realtime Database**.
2. Click the **Create Database** button.
3. Choose your preferred database location and click **Next**.
4. Select **Start in Test Mode** (this allows your hardware and app to communicate immediately) and click **Enable**.

---

## Step 3: Configure Database Rules
To ensure your hardware and Python app can read and write data without permission errors, you need to configure the rules:
1. Inside the Realtime Database page, click on the **Rules** tab at the top.
2. Replace the existing code with the following:
   ```json
   {
     "rules": {
       ".read": true,
       ".write": true
     }
   }
   ```
3. Click **Publish**. *(Note: This makes your database open for development. For production, you should secure these rules later).*

---

## Step 4: Get Credentials for the Python App
Your Python dashboard needs a secure key to talk to Firebase.

1. Click the **Gear Icon** (⚙️) next to "Project Overview" in the top-left corner and select **Project settings**.
2. Go to the **Service accounts** tab.
3. Scroll down and click the **Generate new private key** button.
4. A `.json` file will download to your computer.

> **CRITICAL:** Rename this downloaded file exactly to `serviceAccountKey.json` and place it in the same folder as your `main.py` file.

---

## Step 5: Get Credentials for the ESP8266 Hardware
Your hardware needs the Database URL and a Secret Key to push live telemetry data.

1. Stay in the **Project settings** > **Service accounts** tab.
2. Click on the **Database secrets** sub-tab.
3. Hover over the hidden secret and click **Show**, then copy this code. This is your `FIREBASE_AUTH`.
4. Next, go back to **Build** > **Realtime Database** from the left menu.
5. Copy the URL displayed at the top (it looks like `https://your-project-id.firebaseio.com/`). Make sure to remove the `https://` and the trailing `/`. This is your `FIREBASE_HOST`.

---

## Step 6: Update Your Code
Now, open your hardware code (`sketch.ino`) in the Arduino IDE and paste the credentials you just gathered:

```cpp
#define FIREBASE_HOST "your-project-id.firebaseio.com" // From Step 5
#define FIREBASE_AUTH "your-database-secret"           // From Step 5
```

Open `backend.py` and ensure the database URL matches yours:

```python
firebase_admin.initialize_app(cred, {'databaseURL': '[https://your-project-id.firebaseio.com/](https://your-project-id.firebaseio.com/)'})
```

🎉 **You are all set!** Upload the code to your ESP8266, run `main.py`, and your system will be fully operational.