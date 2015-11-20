import urllib.parse
import urllib.request
import json
import websocket
import _thread
import time
import configparser

import weather
import quote


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    url = "https://slack.com/api/rtm.start"
    token = config['slack']['token']

    parameters = {
        "token": token
    }

    data = urllib.parse.urlencode(parameters)
    data = data.encode('utf-8')

    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as response:
        downloadedPage = response.read()

    pageJson = json.loads(downloadedPage.decode('utf-8'))

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(pageJson.get('url'),
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()


def on_message(ws, message):
    '''
    Called whenever a message is received from the server
    '''
    print(message)
    json_message = json.loads(message)

    if (json_message.get('type') == 'message') and json_message.get('text'):
        target = json_message.get('text').split(' ')[0]
        if (target.lower() in '<@u0eldpzrr>:') or (target.lower() in 'hal:'):
            response = get_response(json_message.get('text').split()[1:], json_message.get('user'))
            send_message_to_channel(ws, 0, response, json_message.get('channel'))


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            time.sleep(1)
            ws.close()
            print("thread terminating...")
    _thread.start_new_thread(run, ())


def send_message_to_channel(ws, messageId, message, channel):
    ws.send(json.dumps({"id": messageId,
                        "type": "message",
                        "channel": channel,
                        "text": message}))


# TODO: more responses
def get_response(message, sender):
    if message[0].lower() in ['hi', 'hey', 'hello']:
        return ("Hello %s" % get_user_name(sender))
    elif message[0].lower() in ['shutdown']:
        return ("Just what do you think you're doing, %s?" % get_user_name(sender))
    elif message[0].lower() in ['weather']:
        if message[1].lower() == 'in':
            return weather.get_weather(' '.join(message[2:]))
        else:
            return weather.get_weather(' '.join(message[1:]))
    elif message[0].lower() in ['quote']:
        return (quote.get_quote_of_the_day())
    else:
        return ("I'm sorry %s, I'm afraid I can't do that." % get_user_name(sender))


def get_user_name(userId):
    config = configparser.ConfigParser()
    config.read('config.ini')

    url = "https://slack.com/api/users.info"
    token = config['slack']['token']

    parameters = {
        "token": token,
        "user": userId
    }

    data = urllib.parse.urlencode(parameters)
    data = data.encode('utf-8')

    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as response:
        downloadedPage = response.read()

    pageJson = json.loads(downloadedPage.decode('utf-8'))

    user = pageJson.get('user')
    username = user.get('name')

    return username


if __name__ == '__main__':
    main()
