from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from socket import error as SocketError
import threading
from typing import Optional
import json
from queue import Queue, Empty


def show(msg:str) -> None:
    print(f'{threading.get_native_id()}: {msg}')
    return

class BulletinBoard:
    '''
    A place where you can subscribe to listen to published messages.
    '''

    class Subscriber:
        '''
        Just a structure for the BulletinBoard to represent a subscriber.
        '''

        def __init__(self):
            #self.tid = tid
            self.queue = Queue()
            return

        def publish(self, msg: str) -> bool:
            '''
            Pass the message to the listener
            '''
            self.queue.put(msg, block=True, timeout=None)
            return True

        def listen(self) -> str:
            '''
            Returns '' in case of timeout, None in case of failure
            '''
            try:
                msg = self.queue.get(block=True, timeout=1)
            except Empty:
                msg = ''
            return msg

    def __init__(self):
        self.lock = threading.Lock()  # to guard access to self.subscribers
        self.subscribers = {}
        return

    def subscribe(self) -> Subscriber:
        '''
        Caller wants to start listening to the published messages.
        Returned is an opaque subscription handle - pass it to listen
        or unsubscribe
        '''
        tid = threading.get_native_id()
        sub = BulletinBoard.Subscriber()
        with self.lock:
            self.subscribers[tid] = sub
        show(f'subscribe({tid}) now:{len(self.subscribers)}')
        return sub

    def unsubscribe(self, sub: Subscriber) -> bool:
        '''
        Start listening to the published messages.
        Returned is an event which will be signaled when new message is
        available.
        '''
        tid = threading.get_native_id()
        with self.lock:
            subs = self.subscribers.pop(tid, None)
        if subs is None:
            show(f'unsubscribe({tid}) => False, 1')
            return False
        if subs != sub:
            show(f'unsubscribe({tid}) => False, 2')
            return False
        show(f'unsubscribe({tid}) => True, now:{len(self.subscribers)}')
        return True

    def listen(self, sub: Subscriber) -> Optional[str]:
        '''
        Blocks the calling thread until a new message is published.
        Returns the message published or None in case of failure.
        '''
        tid = threading.get_native_id()
        with self.lock:
            res = tid in self.subscribers
        if not res:
            show(f'listen({tid}) => None')
            return None
        res = sub.listen()
        if res:
            show(f'listen({tid}) => {res}')
        return res

    def publish(self, msg: str) -> bool:
        '''
        Spread the word to all the subscribers.
        Returns True if there were any listeners AND there were all notified.
        '''
        if not self.subscribers:
            show('publish() => False')
            return False

        res = True
        with self.lock:
            for sub in self.subscribers.values():
                res = sub.publish(msg) and res
        show(f'publish() => {res}')
        return res


theBulletinBoard = BulletinBoard()

class ChatRequestHandler(BaseHTTPRequestHandler):
    '''
    Accept chat message via HTTP POST
    - When one client sends a message to the server, it should be broadcast to
      all the clients except the sender;
    - Server should handle clients connecting and disconnecting at arbitrary
      times;
    - Server must broadcast messages to clients without client intervention
      (it shouldn’t be necessary for a client to send a message in order to
      receive a message or vice versa)
    '''

    def write(self, msg:str) -> None:
        self.wfile.write(msg.encode(encoding='utf-8'))
        return

    def do_GET(self):
        '''
        Read the messages being broadcasted
        '''
        self.send_response(200)
        self.send_header("Content-type", 'application/json')
        self.end_headers()
        show('do_GET')

        h = theBulletinBoard.subscribe()

        self.write('[\n')
        try:
            while True:
                msg = theBulletinBoard.listen(h)
                if msg is None:
                    break
                if msg:
                    self.write(json.dumps({"message": msg}))
                    self.write('\n')

            self.write(']\n')

        except SocketError as e:
            show(f'SocketError caught in do_GET {e}')
            # typically [Errno 104] Connection reset by peer
            # or [Errno 32] Broken pipe

        theBulletinBoard.unsubscribe(h)
        return

    def do_POST(self):
        '''
        Post a message to all the chat participants - those doing GET now
        '''

        # read the body of the request
        content_length = int(self.headers['Content-Length'])
        reqBody = self.rfile.read(content_length)
        reqBodyStr = reqBody.decode('utf-8')
        reqBodyJson = json.loads(reqBodyStr)

        show(f'do_POST {reqBodyJson}')

        res = theBulletinBoard.publish(reqBodyJson.get('message', ''))

        # send the response
        self.send_response(200)
        self.send_header("Content-type", 'application/json')
        self.end_headers()
        if res:
            json_str = '{"response"="ack"}\n'
        else:
            json_str = '{"response"="nack"}\n'
        self.write(json_str)
        return


def run_chat_server(hostName: str, serverPort: int) -> None:
    chatServer = ThreadingHTTPServer((hostName, serverPort), ChatRequestHandler)
    show(f"Server started http://{hostName}:{serverPort}")

    try:
        chatServer.serve_forever()
    except KeyboardInterrupt:
        pass

    chatServer.server_close()
    show("bye")
    return


if __name__ == "__main__":
    run_chat_server('localhost', 8080)
