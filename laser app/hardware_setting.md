# 🛡️ SHIELDGUARD Live App MONITORING SYSTEM - HARDWARE SETTINGS

Document Version : v1.0
Target Platform  : ESP8266 Architecture (NodeMCU v1.0 / ESP-01 Modules)
Primary Objective: Real-time sensor telemetry and cloud-linked physical alarming

----------------------------------------------------------------------
1. COMPONENT SPECIFICATIONS & PIN MAP
----------------------------------------------------------------------
A. Light Dependent Resistor (LDR) Sensor Module
   - Purpose       : Monitors ambient environmental light levels.
   - Signal Type   : Analog Input (Continuous range tracking from 0 to 1023)
   - Microchip Pin : Pin A0 (Dedicated Analog-to-Digital Converter [ADC] Pin)

B. Active Electronic Buzzer Module
   - Purpose       : Emits high-frequency acoustic warning chirps and continuous sirens.
   - Signal Type   : Digital Output (HIGH / LOW state switching control)
   - Microchip Pin : GPIO Pin 5 (Pin D1 on standard NodeMCU ESP-12E boards)

----------------------------------------------------------------------
2. SCHEMATIC WIRING DIRECTORY
----------------------------------------------------------------------
[LDR Module Wiring Layout]
* VCC Pin (Power)   --->  Connect to ESP8266 [3V3] Pin
* GND Pin (Ground)  --->  Connect to ESP8266 [GND] Pin
* OUT / AO (Signal) --->  Connect to ESP8266 [A0] Pin

[Buzzer Module Wiring Layout]
* VCC Pin / Red Wire --->  Connect to ESP8266 [D1] Pin (GPIO 5)
* GND / Black Wire   --->  Connect to ESP8266 [GND] Pin

----------------------------------------------------------------------
3. CORE ELECTRICAL & ARCHITECTURAL CONSTRAINTS
----------------------------------------------------------------------
- Power Source Limitation: The ESP8266 chip functions strictly on a 3.3V logic threshold level.
- Device Identity Matrix: The microcontroller automatically reads its factory ID using `ESP.getChipId()`.
- Signal Calibration: The software samples the A0 analog port every 400 milliseconds.
"""
