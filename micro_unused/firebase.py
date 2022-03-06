from usseclient import SSEClient
import urequests as requests

import ujson as json
import usocket as socket
import _thread

def firebaseURL(URL):
    if '.firebaseio.com' not in URL.lower():
        if '.json' == URL[-5:]:
            URL = URL[:-5]
        if '/' in URL:
            if '/' == URL[-1]:
                URL = URL[:-1]
            URL = 'https://' + \
                  URL.split('/')[0] + '.firebaseio.com/' + URL.split('/', 1)[1] + '.json'
        else:
            URL = 'https://' + URL + '.firebaseio.com/.json'
        return URL

    if 'http://' in URL:
        URL = URL.replace('http://', 'https://')
    if 'https://' not in URL:
        URL = 'https://' + URL
    if '.json' not in URL.lower():
        if '/' != URL[-1]:
            URL = URL + '/.json'
        else:
            URL = URL + '.json'
    return URL

class subscriber:
    def __init__(self, url, callback):
        self.url = firebaseURL(url)
        self.callback = callback
    
    def start(self):
        self.thread = _thread.start_new_thread(self.request, ())
        self.is_running = True

    def request(self):
        while self.is_running:
            try:
                headers = {'Accept': 'text/event-stream'}

                self.response = requests.get(self.url, stream=True, headers=headers)

                for chunk in self.response.iter_lines(1, b'\n\n'):
                    if (chunk):
                        """
                        Ex:
                        event: put
                        data: {"path":"/","data":"hello world"}

                        event: keep-alive
                        data: null
                        """
                        message = chunk.decode(self.response.encoding)
                        
                        split = message.split('\n')

                        event = split[0].split(':')[1].strip()
                        data = json.loads(split[1].split(':', 1)[1].strip())

                        if (event == 'put'):
                            path = data.get('path')
                            data = data.get('data')
                            self.callback(path, data)
            
            except Exception as e:
                print(e)
                self.is_running = False
        
    def stop(self):
        self.response.close()
        self.is_running = False


class FirebaseException(Exception):
    pass


def put(URL, msg):
    to_post = json.dumps(msg)
    response = requests.put(firebaseURL(URL), data=to_post)
    response.close()
    if response.status_code != 200:
        raise FirebaseException(response.text)


def patch(URL, msg):
    to_post = json.dumps(msg)
    response = requests.patch(firebaseURL(URL), data=to_post)
    response.close()
    if response.status_code != 200:
        raise FirebaseException(response.text)


def get(URL):
    response = requests.get(firebaseURL(URL))
    response.close()
    if response.status_code != 200:
        raise FirebaseException(response.text)
    return json.loads(response.text)


def push(URL, msg):
    to_post = json.dumps(msg)
    response = requests.post(firebaseURL(URL), data=to_post)
    response.close()
    if response.status_code != 200:
        raise Exception(response.text)
