/* * PROJECT: ShieldGuard Enterprise Security
 * VERSION: 7.0 (Expo Edition)
 * AUTHOR: ShieldGuard Technologies
 * DESCRIPTION: Real-time Cloud-Connected Laser Security System
 */

#include <ESP8266WiFi.h>
#include <FirebaseESP8266.h>

// ==========================================
// 1. NETWORK & CLOUD CONFIGURATION
// ==========================================
// Enter your local WiFi credentials here:
#define WIFI_SSID "YOUR_WIFI_SSID"                
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"        

// WHERE TO FIND FIREBASE_HOST:
// Go to Firebase Console -> Realtime Database. 
// Copy the link (Remove "https://" from the start and "/" from the end)
#define FIREBASE_HOST "your-project-id.firebaseio.com" 

// WHERE TO FIND FIREBASE_AUTH (DATABASE SECRET):
// Go to Firebase Console -> Project Settings (⚙️) -> Service Accounts -> Database Secrets 
// Copy the 'Secret' and paste it here:
#define FIREBASE_AUTH "YOUR_DATABASE_SECRET_HERE"    

// ==========================================
// 2. HARDWARE ARCHITECTURE (PIN MAP)
// ==========================================
#define LDR_PIN A0     // Light Sensor (Input)
#define BUZZER_PIN 5   // Alarm Siren (Output)

// Communication Handlers
FirebaseData firebaseData; 
FirebaseAuth auth;         
FirebaseConfig config;     

// System Global States
bool isArmed = false;      // Security Active Switch
bool alarmActive = false;  // Siren Active Switch
int threshold = 400;       // Light sensitivity trigger point

// Non-blocking Timing Modules (Advanced millis() logic)
unsigned long lastSyncTime = 0;   
const long syncInterval = 2000;   // Data sync with App every 2s
unsigned long lastLdrSync = 0;    // Live monitoring every 400ms
unsigned long breachStartTime = 0; // Breach verification timer

String deviceID;           // Unique Processor ID
String basePath;           // Unique Cloud Path for this device

// ------------------------------------------
// FUNCTION: AUDIO FEEDBACK (BUZZER)
// ------------------------------------------
void playBeep(int duration, int repeats) {
  for(int i = 0; i < repeats; i++) {
    digitalWrite(BUZZER_PIN, HIGH); delay(duration); digitalWrite(BUZZER_PIN, LOW);
    if(repeats > 1) delay(100);     
  }
}

// ==========================================
// 3. SYSTEM INITIALIZATION (SETUP)
// ==========================================
void setup() {
  Serial.begin(115200);            // Start Serial Console
  pinMode(BUZZER_PIN, OUTPUT);     // Configure Siren Pin
  
  // UNIQUE IDENTITY GENERATION
  // Assigns a unique digital fingerprint to the hardware
  deviceID = "8081";
  basePath = "/" + deviceID + "/system"; 

  Serial.println("\n--- ShieldGuard Enterprise Hardware Booting ---");
  Serial.println("UID: " + deviceID);

  // ESTABLISH WIFI CONNECTION
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  // INITIALIZE CLOUD SYNCHRONIZATION
  config.host = FIREBASE_HOST;
  config.signer.tokens.legacy_token = FIREBASE_AUTH;
  Firebase.begin(&config, &auth);
  
  playBeep(100, 2); // Ready Signal
  Serial.println("\nSystem Online.");
}

// ==========================================
// 4. MASTER LOOP (CORE LOGIC)
// ==========================================
void loop() {
  unsigned long currentMillis = millis(); 
  int ldrValue = analogRead(LDR_PIN);     

  // [A] TELEMETRY MODULE: Push live sensor data to App
  if (currentMillis - lastLdrSync >= 400) {
    lastLdrSync = currentMillis;
    Firebase.setInt(firebaseData, basePath + "/current_ldr", ldrValue);
  }

  // [B] COMMAND MODULE: Fetch instructions from Python Dashboard
  if (currentMillis - lastSyncTime >= syncInterval) {
    lastSyncTime = currentMillis; 
    
    // Logic for "Smart Arming" (Auto-Calibration)
    if (Firebase.getBool(firebaseData, basePath + "/arm_command") && firebaseData.boolData() == true) {
        threshold = ldrValue;      // Capture current environment light
        isArmed = true;            // Activate security
        Firebase.setBool(firebaseData, basePath + "/arm_command", false); 
        Firebase.setString(firebaseData, basePath + "/status", "🛡️ ARMED"); 
        playBeep(300, 1); 
    }
    
    // Logic for System Reset
    if (Firebase.getBool(firebaseData, basePath + "/reset") && firebaseData.boolData() == true) {
        alarmActive = false;        
        isArmed = false;            
        breachStartTime = 0;        
        digitalWrite(BUZZER_PIN, LOW); 
        Firebase.setBool(firebaseData, basePath + "/reset", false); 
        Firebase.setString(firebaseData, basePath + "/status", "Ready");
        playBeep(200, 1); 
    }
  }

  // [C] SECURITY MODULE: INTRUSION DETECTION
  if (isArmed && !alarmActive) {
    // If laser path is interrupted
    if (ldrValue > (threshold + 80)) {
      if (breachStartTime == 0) breachStartTime = currentMillis; 
      
      // EXPO SPECIAL: 250ms Response Time (Ultra-Fast Detection)
      if (currentMillis - breachStartTime >= 250) { 
        alarmActive = true; 
        digitalWrite(BUZZER_PIN, HIGH); // Instant Siren Trigger
        Firebase.setString(firebaseData, basePath + "/status", "🚨 BREACH!"); // Cloud Alert
      }
    } else {
      breachStartTime = 0; // Reset timer if interruption was a glitch
    }
  }

  // Lock the Alarm Siren if Breach is confirmed
  if (alarmActive) digitalWrite(BUZZER_PIN, HIGH); 
}