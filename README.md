# CAPTCHA-Extractor-and-Solver
![Python](https://img.shields.io/badge/Python-3.13.4-green)
![Status](https://img.shields.io/badge/Status-in%20progress-yellow)
<br/>
A system combining a Chrome extension and a Flask backend, designed to intercept reCAPTCHA v2 challenge iframes, extract their data and (***TBA***) solve the challenges automatically.

## Disclaimer
This project is intended for educational and research purposes only.  
Automating CAPTCHA solving may violate the terms of service of some websites.

## Requirements
- Python 3.13+
- Google Chrome
- mkcert

## Installation instructions
### Install mkcert utility
If you have [Scoop](https://github.com/ScoopInstaller/Scoop) installed:

```
scoop bucket add extras
scoop install mkcert
```

Otherwise, you may download the latest release from the [mkcert releases page](https://github.com/filosottile/mkcert/releases).

### Initialize local HTTPS Certificate Authority and generate your keys

```
mkcert -install
```

When prompted, approve the security warning to trust your local CA.<br/>
Then, generate the certificate and the private key:

```
mkcert localhost 127.0.0.1 ::1
```

Make sure you have the files `localhost+2.pem` and `localhost+2-key.pem` in your current directory.
### Clone the repo

```
git clone https://github.com/SergYof/CAPTCHA-Extractor-and-Solver
cd CAPTCHA-Extractor-and-Solver
```

Move the generated `.pem` files into the `certs/` directory.
### Install dependencies
```
pip install -r requirements.txt
```

### Install the Chrome extension
Open `chrome://extensions` in Google Chrome. Enable **Developer mode**. Click the button "Load unpacked" and select the `extension/` folder. Activate the extension if needed.

## Usage

```
python app.py
```

Open `https://localhost:5000` to verify the server is running.
You can inspect the communication between the extension and the server via the DevTools console (`Ctrl+Shift+I`).

## System Overview
The system consists of two complementary parts:
- A Chrome extension that:
  - Injects content scripts into CAPTCHA iframes
  - Detects CAPTCHA type and grid size
  - Sends challenge data to the backend
  - ***(TBA)*** Receives the response and checks the needed tiles.
- and a Flask server that:
  - Downloads the challenge image
  - ***(TBA)*** Splits the image into tiles
  - ***(TBA)*** Uses an LLM to determine the correct tiles
  - ***(TBA)*** Sends back the solution
