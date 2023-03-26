import argparse
import asyncio
import os
from dotenv import load_dotenv
import smtplib
import socks
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Sink

load_dotenv()

class CustomSMTPHandler(Sink):
    def __init__(self, email_server, email_port, email_user, email_pass, proxy_server, proxy_port):
        self.email_server = email_server
        self.email_port = email_port
        self.email_user = email_user
        self.email_pass = email_pass
        self.proxy_server = proxy_server
        self.proxy_port = proxy_port

    async def handle_DATA(self, server, session, envelope):
        socks.set_default_proxy(socks.SOCKS5, self.proxy_server, self.proxy_port)
        socks.wrap_module(smtplib)

        try:
            with smtplib.SMTP(self.email_server, self.email_port) as smtp:
                smtp.starttls()
                smtp.login(self.email_user, self.email_pass)
                smtp.sendmail(envelope.mail_from, envelope.rcpt_tos, envelope.content)

            print("Email sent successfully!")
        except Exception as e:
            print("Error:", e)
            return "554 Error: " + str(e)

        return "250 OK"

async def main(args):
    handler = CustomSMTPHandler(args.email_server, args.email_port, args.email_user, args.email_pass, args.proxy_server, args.proxy_port)
    controller = Controller(handler, hostname="localhost", port=8025)
    controller.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A small CLI version of ProtonBridge with SOCKS5 proxy support.")
    parser.add_argument("--email_server", type=str, default=os.environ.get("EMAIL_SERVER"), required=True, help="Email server address")
    parser.add_argument("--email_port", type=int, default=int(os.environ.get("EMAIL_PORT", 0)), required=True, help="Email server port")
    parser.add_argument("--email_user", type=str, default=os.environ.get("EMAIL_USER"), required=True, help="Email username")
    parser.add_argument("--email_pass", type=str, default=os.environ.get("EMAIL_PASS"), required=True, help="Email password")
    parser.add_argument("--proxy_server", type=str, default=os.environ.get("PROXY_SERVER"), required=True, help="SOCKS5 proxy server address")
    parser.add_argument("--proxy_port", type=int, default=int(os.environ.get("PROXY_PORT", 0)), required=True, help="SOCKS5 proxy server port")

    args = parser.parse_args()

    asyncio.run(main(args))
