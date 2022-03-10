
#!/usr/bin/env python
import logging
import os
import sys

from aiohttp import web
from tartiflette_aiohttp import register_graphql_handlers

from interfaces.iserver import IServer


class Server(IServer):

    def __init__(self, to_serve: str, port: int, graphiql_debug: bool = False):
        self.to_serve = to_serve
        self.graphiql_debug = graphiql_debug
        self.port = port

    def start(self) -> None:
         """@inheritdoc IServer"""

         web.run_app(
            register_graphql_handlers(
                app=web.Application(),
                engine_sdl=os.path.dirname(os.path.abspath(__file__)) + "/" + self.to_serve + "/sdl",
                engine_modules=[
                    f"{self.to_serve}.query_resolvers",
                ],
                executor_http_endpoint="/graphql",
                executor_http_methods=["POST"],
                graphiql_enabled=self.graphiql_debug,
            )
        )
        

def main():
    logging.basicConfig(
        filename="example_rumble_kong_league.log",
        level=logging.DEBUG,
        format="%(relativeCreated)6d %(process)d %(message)s",
    )

    server = Server("example_rumble_kong_league", 8080, True)
    server()

    logging.debug("server started")

if __name__ == "__main__":
    sys.exit(main())
