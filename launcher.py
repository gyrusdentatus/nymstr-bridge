import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

def main():
    smtp_server = subprocess.Popen(["python", "local_smtp_server.py",
                                    "--email_server", os.environ.get("EMAIL_SERVER"),
                                    "--email_port", os.environ.get("EMAIL_PORT"),
                                    "--email_user", os.environ.get("EMAIL_USER"),
                                    "--email_pass", os.environ.get("EMAIL_PASS"),
                                    "--proxy_server", os.environ.get("PROXY_SERVER"),
                                    "--proxy_port", os.environ.get("PROXY_PORT")])

    imap_server = subprocess.Popen(["python", "local_imap_server.py",
                                    "--imap_server", os.environ.get("IMAP_SERVER"),
                                    "--imap_port", os.environ.get("IMAP_PORT"),
                                    "--email_user", os.environ.get("EMAIL_USER"),
                                    "--email_pass", os.environ.get("EMAIL_PASS"),
                                    "--proxy_server", os.environ.get("PROXY_SERVER"),
                                    "--proxy_port", os.environ.get("PROXY_PORT")])

    print("SMTP and IMAP servers are running...")

    try:
        smtp_server.wait()
        imap_server.wait()
    except KeyboardInterrupt:
        print("Terminating SMTP and IMAP servers...")
        smtp_server.terminate()
        imap_server.terminate()

if __name__ == "__main__":
    main()
