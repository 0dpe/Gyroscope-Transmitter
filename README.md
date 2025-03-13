# Gyroscope-Transmitter
Send live gyroscope data from an iPhone to a computer on the same WiFi network via a local WebSocket server.

## Setup
On the computer:
1. Install Python and the `websockets` library.
1. Install [mkcert](https://github.com/FiloSottile/mkcert).
1. Run in a terminal `mkcert -install`. In the terminal, change directory to this Gyroscope-Transmitter directory and run `mkcert -key-file key.pem -cert-file cert.pem localhost`.
1. Run in a terminal `mkcert -CAROOT`. Go to the directory and find the file `rootCA.pem`. Send this file to the iPhone.

On the iPhone:
1. Save `rootCA.pem` somewhere on the iPhone and try to open it.
1. Go to the Settings app and go to `Profile Downloaded`. Install the profile.\
   To remove this certificate later if needed, go to `General > VPN & Device Management`.

## Usage
1. On the computer, run in a terminal `python server.py` or `python3 server.py`.
   * Optionally, specify ports with the `--https-port` and `--ws-port` flags. If `--ws-port` is specified, the `websocketPort` constant must be modified in `index.html` accordingly.
1. Follow the instructions in the terminal.

## Development Notes
For the iPhone to send gyroscope data, the webpage must request permission. Permission can only be requested over an `https` connection.

Generating a certificate for all dynamic local IP addresses is [not possible](https://github.com/FiloSottile/mkcert/discussions/434). However, generating a certificate for just `localhost` seems to work.
