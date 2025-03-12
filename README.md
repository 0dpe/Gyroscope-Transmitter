# Gyroscope-Transmitter
Send live gyroscope data from an iPhone to a computer on the same WiFi network via a local WebSocket server.

## Setup
On the computer:
1. Install Python and the `websockets` library.
1. Find your local IP address, which probably starts with `192.168.`.
   * Run `ipconfig` in Windows PowerShell.
   * Run `ipconfig getifaddr en0` in MacOS terminal.
1. Make sure the port `8765` is open in the firewall.
1. Install [mkcert](https://github.com/FiloSottile/mkcert).
1. Run in a terminal `mkcert -install`. In the terminal, change directory to this Gyroscope-Transmitter directory and run `mkcert -key-file key.pem -cert-file cert.pem 192.168.X.X`.
1. Run in a terminal `mkcert -CAROOT`. Go to the directory and find the file `rootCA.pem`. Send this file to your iPhone.

On the iPhone:
1. Save `rootCA.pem` somewhere on the iPhone and open it. In the Settings app, got to `Profile Downloaded` and install. Go to `General > About > Certificate Trust Settings` and enable the certificate. 
If you want to remove this certificate later, go to `General > VPN & Device Management`.

## Usage
On the computer, run `https_server.py` and `server.py`.

On the iPhone, open a browser and go to `https://192.168.X.X:8000/index.html` and accept the gyroscope permission request. If no permission request pops up, open Settings app and go to `Apps > Safari > Clear History and Website Data`.

## Development Notes
For the iPhone to send gyroscope data, the webpage must request permission. Permission can only be requested over an `https` connection.

Generating a certificate for all dynamic local IP addresses is [not possible](https://github.com/FiloSottile/mkcert/discussions/434).
