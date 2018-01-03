import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine


API_TOKEN = '521030858:AAEJsZO_YYPldQoMcQr-u2LE4AzyubTQEs0'
WEBHOOK_URL = 'https://12895470.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'user',
        'time',
        'count',
        'start_count',
        'echo',
        'repeat',
        'notice'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'time',
            'conditions': 'is_going_to_time'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'count',
            'conditions': 'is_going_to_count'
        },
        {
            'trigger': 'go_back',
            'source': [
                'time',
                'start_count'
            ],
            'dest': 'user'
        },
        {
            'trigger': 'advance',
            'source': 'count',
            'dest': 'start_count',
            'conditions': 'is_going_to_start_count'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'notice',
            'conditions': 'is_going_to_notice'
        },
        {
            'trigger': 'going_to_echo',
            'source': 'notice',
            'dest': 'echo',
        },
        {
            'trigger': 'advance',
            'source': 'echo',
            'dest': 'repeat',
            'conditions': 'is_going_to_repeat'
        },
        {
            'trigger': 'repeat_back',
            'source': 'repeat',
            'dest': 'echo',
        },
        {
            'trigger': 'advance',
            'source': 'echo',
            'dest': 'user',
            'conditions': 'is_going_to_user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run(port=5000)
