import asyncio
import tornado.escape
import tornado.ioloop
import tornado.locks
import tornado.web
import os.path
import tornado.httpclient
from handlers import MainHandler, PricePredictor

from tornado.options import define, options, parse_command_line

define("port", default=8000, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            ("/get_price", PricePredictor),
            (r"/", MainHandler),
        ],
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        debug=options.debug,
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
    print("Server was started on port ", 8000)


if __name__ == "__main__":
    main()

