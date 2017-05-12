from flask import (Flask, render_template, request, send_from_directory)
from flask_socketio import SocketIO, emit
import logging as log
import os
import time

DEBUG = True


def get_root_dir():
    root_dir = os.path.dirname(__file__)
    if __name__ == "__main__":
        root_dir = os.getcwd()
    root_dir += "/static/"
    return os.path.abspath(root_dir)

root_dir = get_root_dir()
app = Flask(__name__, template_folder=root_dir)
app.config['SECRET_KEY'] = 'easy_as_pie!2'
socketio = SocketIO(app)


@app.route('/')
def index():
    app.logger.info('Index')
    url = request.url
    app.logger.info("url {}".format(url))
    return render_template('index2.html', url=url)


@app.route('/static/<path:path>')
def misc_static(path):
    return send_from_directory('static', path)


@socketio.on('connect')
def test_connect():
    app.logger.info("connect")
    

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('handle_hello')
def do_handle_hello(message):
    app.logger.info("got hello")
    # 3 -----
    emit('do_time', time.strftime("%d/%m/%Y %H:%M:%S"))


def set_logging():
    logger = log.getLogger()
    if DEBUG:
        logger.setLevel(log.DEBUG)
    ch = log.StreamHandler()
    app.logger.addHandler(ch)


def run_flask_socket_app():
    print("starting app")
    app.logger.info('starting')
    set_logging()
    app.logger.debug("root dir: {}".format(root_dir))
    return socketio.run(app, debug=DEBUG)


if __name__ == "__main__":
    run_flask_socket_app()
