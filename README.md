# Gyroscope-Transmitter
Send live gyroscope data from an iPhone to a Windows device on the same WiFi network via a local WebSocket server.

## Setup
For the iPhone to send gyroscope data, the webpage must request permission. Permission can only be requested over an `https` connection.

On Windows:
1. Install Python and the `websockets` library.
1. Find your local IP address by running in a terminal `ipconfig`. Your local IP address should start with `192.168.`.
1. Make sure the port `8765` is open in the firewall.
1. Install [mkcert](https://github.com/FiloSottile/mkcert).
1. Run in a terminal `mkcert -install`. In the terminal, change directory to this Gyroscope-Transmitter directory and run `mkcert -key-file key.pem -cert-file cert.pem 192.168.X.X`.
1. Run in a terminal `mkcert -CAROOT`. Go to the directory and find the file `rootCA.pem`. Send this file to your iPhone.

On iPhone:
1. Save `rootCA.pem` somewhere on the iPhone and open it. In the Settings app, got to `Profile Downloaded` and install. Go to `General > About > Certificate Trust Settings` and enable the certificate. 
If you want to remove this certificate later, go to `General > VPN & Device Management`.

## Usage
On Windows:
1. Run in a terminal in the webpage directory `python https_server.py 8000`
1. Run in another terminal in the webpage directory `python server.py`

On iPhone:
1. Use a browser, preferably Safari, and go to `https://192.168.X.X:8000/index.html` and accept the gyroscope permission request. If no permission request pops up, go to Settings > Apps > Safari > Clear History and Website Data. 

## Development Notes
Generating a certificate for all dynamic local IP addresses is [not possible](https://github.com/FiloSottile/mkcert/discussions/434).
