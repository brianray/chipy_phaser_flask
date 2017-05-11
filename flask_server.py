from flask import (Flask, render_template, request, send_from_directory)
from flask_socketio import SocketIO, emit
import logging as log
import os
from complete_pie import run_belt

DEBUG = True


def get_root_dir():
    root_dir = os.path.dirname(__file__)
    if __name__ == "__main__":
        root_dir = os.getcwd()
    root_dir += "/static/"
    return os.path.abspath(root_dir)

root_dir = get_root_dir()
app = Flask(__name__, template_folder=root_dir)
app.config['SECRET_KEY'] = 'easy_as_pie!'
socketio = SocketIO(app)


def no_msg(app, message):
    app.logger.warn("no method found in callbacks {}".format(app.callbacks))


@socketio.on('callback')
def on_callback(message):
    "Calls the callback(s) for 'action' "
    action = message['action']
    app.logger.info("on-calback: {}".format(action))
    out = {}
    for callback in app.callbacks.get(action, [no_msg]):
        try:
            returns = callback(app, message)
        except Exception as e:
            out['error'] = str(e)
        if returns and type(returns) == dict:
            out.update(returns)
    emit('do_{}'.format(action), out)


@app.route('/')
def index():
    app.logger.info('Index')
    url = request.url
    app.logger.info("url {}".format(url))
    return render_template('index.html', url=url)


@app.route('/static/<path:path>')
def misc_static(path):
    return send_from_directory('static', path)


@socketio.on('connect')
def test_connect():
    app.logger.info("connect")
    emit('on_connect', {'totals': app.belt.get_totals()})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


def set_logging():
    logger = log.getLogger()
    if DEBUG:
        logger.setLevel(log.DEBUG)
    ch = log.StreamHandler()
    app.logger.addHandler(ch)


def run_flask_socket_app(belt=None):
    print("starting app")
    app.logger.info('starting')
    app.callbacks = belt.callbacks
    app.belt = belt
    set_logging()
    app.logger.debug("root dir: {}".format(root_dir))
    return socketio.run(app, debug=DEBUG)


if __name__ == "__main__":
    run_belt(runner=run_flask_socket_app)
