import argparse
import asyncio
import os
from dotenv import load_dotenv
import smtplib
import socks
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Sink
import configparser
import socket
import aiodns

def read_env(file_path: str):
    config = configparser.ConfigParser()
    config.read(file_path)

    options = {}

    for section in config.sections():
        for key, value in config.items(section):
            options[key] = value

    return options

async def resolve_ip(host):
    resolver = aiodns.DNSResolver()

    try:
        # Try resolving IPv6 address
        result = await resolver.gethostbyname(host, socket.AF_INET6)
        return result.addresses[0]
    except aiodns.error.DNSError:
        try:
            # Fall back to resolving IPv4 address
            result = await resolver.gethostbyname(host, socket.AF_INET)
            return result.addresses[0]
        except aiodns.error.DNSError:
            print(f"Error resolving {host}: both IPv4 and IPv6 resolution failed")
            return None

async def send_message_async(email_server, email_port, email_user, email_pass):
    recipient = input("Enter the recipient email address: ")
    message = input("Enter the message: ")

    ip_address = await resolve_ip(email_server)

    if ip_address is None:
        return

    socks.set_default_proxy(socks.SOCKS5, args.proxy_server, args.proxy_port)
    socks.wrap_module(smtplib)

    try:
        with smtplib.SMTP_SSL(ip_address, email_port) as smtp:
            smtp.set_debuglevel(1)
            smtp.login(email_user, email_pass)
            smtp.sendmail(email_user, recipient, message)
        print("Email sent successfully!")
    except Exception as e:
        print("Error:", e)

def send_message(email_server, email_port, email_user, email_pass):
    asyncio.run(send_message_async(email_server, email_port, email_user, email_pass))

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
    options = read_env('.env')

    class Args:
        email_server = options['email_server']
        email_port = int(options['email_port'])
        email_user = options['email_user']
        email_pass = options['email_pass']
        proxy_server = options['proxy_server']
        proxy_port = int(options['proxy_port'])

    args = Args()
    asyncio.run(main(args))
    send_message(args.email_server, args.email_port, args.email_user, args.email_pass)
