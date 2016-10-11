import os
import tornado.ioloop
import tornado.web
from tornado import escape

from tornado.options import define, options, parse_command_line

from ttt import db_connector
from ttt import game
import ttt

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")

ROOT_DIT = os.path.dirname(__file__)

conn = db_connector.DBConnectionSQLAlchemy()
conn.init_db()


class BuildResponse:
    def __init__(self, message, result=True, response_dict=None):
        result_message = "Success" if result else "Failure"
        response_dict.update(
            dict(
                result=result_message,
                message=message,
            )
        )
        self.json_response = response_dict

    def get_response(self):
        return escape.json_encode(self.json_response)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        html_to_send_path = os.path.join(ROOT_DIT, 'static', 'tik-tak-toe.html')
        with open(html_to_send_path) as f:
            str_to_send = f.read()
        self.write(str_to_send)


class PlayerHandler(tornado.web.RequestHandler):
    def get(self):
        # listplayers
        # GET tik-tak-toe/api/v1/players
        player_list = conn.get_player_list()
        json_response = dict(
            players=[player.to_json() for player in player_list]
        )
        self.write(escape.json_encode(json_response))

    def post(self, *args, **kwargs):
        # create new player
        # POST tik-tak-toe/api/v1/players
        request_json = escape.json_decode(self.request.body)
        player_name = request_json["player"][0]["player_name"]
        player = conn.create_new_player(player_name)
        response_dict = dict(
            players=[player.to_json()]
        )
        result = True
        message = "User {player_name} was added ({player_id_expected})".format(
            player_name=player.name,
            player_id_expected=player.id,
        )
        response_instance = BuildResponse(message, result, response_dict)
        self.write(response_instance.get_response())


class GameListHandler(tornado.web.RequestHandler):
    def get(self):
        # listplayers
        # GET tik-tak-toe/api/v1/players
        game_list = conn.get_game_list()
        json_response = dict(
            games=[game.to_json() for game in game_list]
        )
        self.write(escape.json_encode(json_response))

    def post(self, *args, **kwargs):
        # listplayers
        # GET tik-tak-toe/api/v1/players
        game_state = conn.create_new_game()
        json_response = dict(
            games=[game_state.to_json()]
        )
        message = "Game created"
        result=True
        response_instance = BuildResponse(message, result, json_response)
        self.write(response_instance.get_response())


class GameHandler(tornado.web.RequestHandler):
    def get(self, game_id):
        # listplayers
        # GET tik-tak-toe/api/v1/players
        game = conn.get_game_state(game_id)
        json_response = dict(
            games=[game.to_json()]
        )
        message = "Game state"
        result = True
        response_instance = BuildResponse(message, result, json_response)
        self.write(response_instance.get_response())

    def post(self, game_id):
        game_state = conn.get_game_state(game_id)
        game_status = game_state.get_game_status()
        if game_status == game.GameStatusOptions.started:
            message = "Game has started"
            result = False
            json_response = {}
            response_instance = BuildResponse(message, result, json_response)
        elif game_status == game.GameStatusOptions.ended:
            message = "Game has ended"
            result = False
            json_response = {}
            response_instance = BuildResponse(message, result, json_response)
        else:
            request_json = escape.json_decode(self.request.body)
            player_type = request_json["player_type"]
            player_id = request_json["player_id"]
            try:
                player = conn.get_player(player_id)
            except:
                player = None
            if player_type in ['x', 'o', 'player_turn'] and (player is not None):
                player = conn.get_player(player_id)
                if player_type == 'x':
                    game_state.player_x = player
                elif player_type == 'o':
                    game_state.player_y = player
                else:
                    game_state.player_turn = player
                conn.set_game_state(game_id, game_state)
                json_response = dict(
                    games=[game_state.to_json()]
                )
                message = "Game created"
                result=True
                response_instance = BuildResponse(message, result, json_response)
            else:
                message = "Invalid request."
                if player is None:
                    message += " player is none"
                else:
                    message += " player type illegal"
                result = False
                json_response = {}
                response_instance = BuildResponse(message, result, json_response)
        self.write(response_instance.get_response())


def make_app():
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/api/v1/players", PlayerHandler),
            (r"/api/v1/games", GameListHandler),
            (r"/api/v1/games/([0-9]+)", GameHandler),
        ],
        # cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=False,
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
