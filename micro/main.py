from time import sleep
from wifi import prompt_wifi, disconnect_wifi, connect_wifi
from bluetooth import run_ble
import json
# import firebase


def main():
    connect_wifi('Night Owl - Guest', 'brassbristlebrush')

    import urequests as requests

    url = 'https://project-friendship-lamp-default-rtdb.firebaseio.com/test.json'
    headers = {'Accept': 'text/event-stream'}
        

    with requests.get(url, stream=True, headers=headers) as response:
        for chunk in response.iter_lines(1, b'\n\n'):
            if (chunk):
                """
                Example stream:

                event: put
                data: {"path":"/","data":"hello world"}

                event: keep-alive
                data: null
                """
                message = chunk.decode(response.encoding)
                
                split = message.split('\n')

                event = split[0].split(':')[1].strip()
                data = json.loads(split[1].split(':', 1)[1].strip())

                if (event == 'put'):
                    print(data.get('data'))
                
                



    # for line in response.iter_lines():
    #     if line:
    #         decoded_line = line.decode('utf-8')
    #         print(json.loads(decoded_line))
    # client = SSEClient(response)
    # for event in client.events():
    #     print(json.loads(event.data))

    
    # run_ble()
    # URL = 'project-friendship-lamp-default-rtdb/test'
    # S = firebase.subscriber(URL, pprint)
    # S.start()

    # prompt_wifi()
    # sleep(1000)
    # disconnect_wifi()

main()
