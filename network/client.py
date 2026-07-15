from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import threading
import urllib.request


class ServerClient:

    def __init__(
        self,
        server_host="192.168.31.241",
        listen_host="0.0.0.0",
        port=80
    ):

        # Куда Raspberry отправляет события
        self.server_host = server_host

        # Где Raspberry принимает команды
        self.listen_host = listen_host

        self.port = port

        self.on_command = None

        self.server = None
        self.thread = None



    # ==================================================
    # Запуск HTTP сервера Raspberry
    # ==================================================

    def start(self):

        handler = self._create_handler()

        self.server = HTTPServer(
            (
                self.listen_host,
                self.port
            ),
            handler
        )

        print(
            f"[HTTP] Raspberry server started "
            f"{self.listen_host}:{self.port}"
        )


        self.thread = threading.Thread(
            target=self.server.serve_forever,
            daemon=True
        )

        self.thread.start()



    # ==================================================
    # HTTP обработчик входящих команд
    # ==================================================

    def _create_handler(self):

        parent = self


        class Handler(BaseHTTPRequestHandler):


            def do_GET(self):

                url = urlparse(self.path)


                # ------------------------------
                # Команды от Server
                # ------------------------------

                if url.path == "/cmd":

                    params = parse_qs(
                        url.query
                    )

                    cmd = params.get(
                        "c",
                        [""]
                    )[0]


                    if cmd:

                        print(
                            "RECV CMD:",
                            cmd
                        )


                        if parent.on_command:

                            parent.on_command(
                                cmd
                            )


                    self.send_response(200)

                    self.send_header(
                        "Content-type",
                        "text/plain"
                    )

                    self.end_headers()


                    self.wfile.write(
                        b"OK"
                    )


                else:

                    self.send_response(
                        404
                    )

                    self.end_headers()



            # отключаем стандартный лог HTTP
            def log_message(
                self,
                format,
                *args
            ):
                return



        return Handler



    # ==================================================
    # Отправка состояния на Server
    # ==================================================

    def send(
        self,
        cmd: str
    ):

        url = (
            f"http://{self.server_host}"
            f"/cmd?c={cmd}"
        )


        print(
            "SEND:",
            cmd
        )


        try:

            response = urllib.request.urlopen(
                url,
                timeout=1
            )


            response.close()


        except Exception as e:

            print(
                "SEND ERROR:",
                e
            )



    # ==================================================
    # Остановка
    # ==================================================

    def close(self):

        if self.server:

            self.server.shutdown()


        print(
            "[HTTP] Server stopped"
        )