
---

#  OPUSAUDIT - WhatsApp Audio Analysis Tool

  

**OPUSAUDIT** is a tool developed for **digital forensic analysis** and **cybersecurity awareness**. It can be used by professionals in judicial investigations as well as by cybersecurity teams in awareness campaigns to demonstrate the sensitivity of information transmitted via audio on **Android** devices.

  

##  What is it for?

  

OPUSAUDIT allows you to analyze WhatsApp audios stored on an **Android** device, automatically extracting them via ADB and processing them with artificial intelligence to search for sensitive keywords such as passwords, banking data, usernames, or any personal information that could pose a risk if intercepted by a cybercriminal.

  

##  Use cases

  

- **Digital forensics:** Search for names, passwords, keys, and patterns in audios related to judicial investigations.

-  **Awareness campaigns:** Demonstrate the impact of audio data leaks to companies or users.

- **Privacy audits:** Verification of critical information leaked via voice messages.

  

---

  

## 🛠 How does it work?

  

1. Connect an Android phone with **USB Debugging** enabled.

2. OPUSAUDIT automatically extracts WhatsApp voice messages.

3. Uses **Whisper** (OpenAI's transcription model) to convert audio to text.

4. Analyzes transcriptions for **sensitive keywords**.

5. Displays potential findings on screen and saves them to a file (`secretleak.txt`).

  

---

  

## Prerequisites

  

### Windows

1.  **Download Android Platform Tools:**

- Download from: https://dl.google.com/android/repository/platform-tools-latest-windows.zip

- Extract to `C:\platform-tools\`

- Add `C:\platform-tools\` to your system PATH

  

2.  **Install Python dependencies:**

```bash

pip install PyQt5 openai-whisper

```

  

### Linux (Ubuntu/Debian)

1.  **Install ADB:**

```bash

sudo apt update

sudo apt install android-tools-adb

```

  

2.  **Install Python dependencies:**

```bash

pip install PyQt5 openai-whisper

```

  

### Verify ADB Installation

Check that ADB is properly installed and working:

```bash

adb  version

```

  

---

  

## How to enable USB Debugging?

  

1. Open **Settings** on your Android phone.

2. Go to **About phone**.

3. Tap 7 times on **Build number** to enable developer options.

4. Go back and enter **Developer options**.

5. Enable **USB Debugging**.

  

---

  

##  Usage Guide

  

1. Run `OpusAudit.py`.

2. Connect your Android phone via USB. The tool will show "Waiting for ADB connection..." until detected.

3. Once the device is detected, analysis options will be unlocked:

-  **All audios** (default option), or

- The **last X audios** (configurable).

  

4. You can add **additional keywords** to the default filters:

-  **English default filters:**  `credit card`, `password`, `key`, `user`, `card`, `email`, `access`, `bank`

-  **Spanish default filters:**  `tarjeta de credito`, `contraseña`, `clave`, `usuario`, `tarjeta`, `correo`, `acceso`, `banco`

  

5. Click **"Start analysis"** / **"Iniciar análisis"**.

6. The tool will show step by step:

-  Audio extraction

- Transcription with Whisper

- Keyword search

- Found results

  

7. Upon completion, it will show a summary of detected content and generate a file called `secretleak.txt` with the results and the audios used.

  

---

  

## Language Support

  

OPUSAUDIT supports both **English** and **Spanish** interfaces. Use the language dropdown at the top of the application to switch between languages. The tool will automatically use the appropriate keyword filters based on the selected language.

  

---

  

##  Troubleshooting

  

### ADB Device Not Detected

1. Ensure USB Debugging is enabled on your Android device

2. Check that ADB is in your system PATH:

```bash

adb devices

```

3. Try different USB cables or ports

4. On some devices, you may need to change USB connection mode to "File Transfer" or "MTP"

  

### Missing Dependencies

If you encounter import errors, make sure all dependencies are installed:

```bash

pip  install  PyQt5  openai-whisper

```

  

---

  

##  Screenshots

  

### Main Interface with Language Selection:

The application features a clean interface with ASCII banner and language selection dropdown.

  <img width="701" height="708" alt="OpusAudit02" src="https://github.com/user-attachments/assets/d688ce1c-6af4-4d62-a6a5-d8977e435ce6" />


### Analysis Results:

Results are displayed in real-time showing the step-by-step process and any sensitive information found.


  

<img width="700" height="716" alt="OpusAudit03" src="https://github.com/user-attachments/assets/f353e817-8169-41c7-bd2a-c8d518ed567e" />

---
  

##  Disclaimer

> This tool is provided exclusively for educational and research purposes.

> The author is not responsible for the misuse of this script or its application outside controlled environments.

> Use it responsibly, ethically, and with respect for the law.

---
 
## License

This project is provided as-is for educational purposes. Please use responsibly and in accordance with local laws and regulations.
