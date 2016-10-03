import os

import tornado.ioloop
import tornado.web

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        html_to_send_path = os.path.join('static', 'tik-tak-toe.html')
        with open(html_to_send_path) as f:
            str_to_send = f.read()
        self.write(str_to_send)


def make_app():
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
        ],
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        debug=options.debug,
    )
    return app


def main():
    parse_command_line()
    app = make_app()
    app.listen(options.port)
    print("server listen on port: {options.port}".format(options=options))
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
