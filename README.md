# nymstr-bridge
PoC based on Proton-bridge in Python to act as SMTP/IMAP server on the client side to route all traffic through NYM mixnet over SOCKS5 proxy

## Structure

```
├── .env
├── .gitignore
├── README.md
├── launcher.py
├── local_imap_server.py
└── local_smtp_server.py
```


## Requirements

- Python 3.7+
- python-dotenv
- aiosmtpd
- PySocks
- IMAPClient

## Installation

1. Clone the repository: 

```
git clone https://github.com/gyrusdentatus/nymstr-bridge
```


2. Create a virtual environment and activate it:

```
python -m venv venv
source venv/bin/activate
```

3. Install the required packages:

```
pip install -r requirements.txt

```


4. Create an `.env` file with your email server, proxy, and user credentials (see the sample provided in the project).


## Usage

1. Run the `launcher.py` script to start both the local SMTP and IMAP servers:

2. Configure your email client to use the local SMTP server at `localhost:8025` for outgoing email and the local IMAP server at `localhost:8143` for incoming email.

3. Send and receive emails using your email client. The traffic will be routed through the SOCKS5 proxy specified in your `.env` file.

## Note

This project is a very simplified and hacky version of the ProtonBridge functionality and is not suitable for production use. Additional error handling, logging, and features may be required to make it more robust and production-ready.


