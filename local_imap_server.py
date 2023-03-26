import asyncio
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Sink
from imapclient import IMAPClient

class CustomIMAPHandler(Sink):
    def __init__(self, email_config, proxy_config):
        self.email_config = email_config
        self.proxy_config = proxy_config

    async def handle_fetch(self):
        with CustomIMAPClient(*self.email_config[:2], proxy_config=self.proxy_config) as client:
            client.login(*self.email_config[2:])
            client.select_folder("INBOX")
            messages = client.search()
            print("Fetched messages:", messages)

class CustomIMAPClient(IMAPClient):
    def __init__(self, *args, proxy_config=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxy_config = proxy_config

    def _create_socket(self):
        if self.proxy_config is not None:
            sock = socks.socksocket()
            sock.set_proxy(socks.SOCKS5, *self.proxy_config)
            return sock
        return super()._create_socket()

async def main(args):
    handler = CustomIMAPHandler(
        email_config=(args.email_server, args.email_port, args.email_user, args.email_pass),
        proxy_config=(args.proxy_server, args.proxy_port)
    )
    controller = Controller(handler, hostname="localhost", port=8143)
    controller.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A small CLI version of ProtonBridge with SOCKS5 proxy support.")
    parser.add_argument("--email_server", type=str, required=True, help="Email server address")
    parser.add_argument("--email_port", type=int, required=True, help="Email server port")
    parser.add_argument("--email_user", type=str, required=True, help="Email username")
    parser.add_argument("--email_pass", type=str, required=True, help="Email password")
    parser.add_argument("--proxy_server", type=str, required=True, help="SOCKS5 proxy server address")
    parser.add_argument("--proxy_port", type=int, required=True, help="SOCKS5 proxy server port")

    args = parser.parse_args()

    asyncio.run(main(args))
