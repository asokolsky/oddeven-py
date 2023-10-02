#
# Test plan
#
# Posting a message
# curl -X POST -H "Content-Type: application/json" -d '{"message":"hi?"}' http://localhost:8080
#
# Chat participants read messages:
# curl http://localhost:8080
#
import json
from multiprocessing import Process, Pool
from requests import Session, Response
import subprocess
#import time
from unittest import TestCase, main

from server import run_chat_server, show

server_host = 'localhost'
server_port = 8080


def client_post_proc(messages) -> None:
    show(f'client_post_proc({server_host}, {server_port}, {messages})')
    url = f'http://{server_host}:{server_port}'
    ses = Session()
    for msg in messages:
        resp = ses.post(url, json={'message': msg})
        assert resp.status_code == 200
        #body = resp.json()
        show(resp)
    return

class TestChatServer(TestCase):
    #
    # these will be sent to the server by various clients
    #
    messages = (
        (('0.1110', '0.1111'),),
        (('1.1110', '1.222'),),
        (('2.1110', '2.1111', '2.1112'),)
    )

    @classmethod
    def setUpClass(cls):
        '''
        automatically called before any test
        '''
        return

    @classmethod
    def tearDownClass(cls):
        '''
        automatically called after all the tests
        '''
        return

    def setUp(self):
        '''
        automatically called before every test
        '''
        #
        # start the server
        #
        show('Starting the chat server')
        self.sever_process = Process(
            target=run_chat_server, args=(server_host, server_port,))
        self.sever_process.start()
        #
        # start the reading client
        #
        self.reader = subprocess.Popen(
            ["curl", "--silent", f"http://{server_host}:{server_port}"],
            shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True)
        show(f'Reader client: {self.reader}')

        return

    def tearDown(self):
        '''
        automatically called after every test
        '''
        #
        # shut the server
        #
        show('Shutting chat server')
        self.sever_process.terminate()
        self.sever_process.join()
        self.sever_process = None
        #
        # shut the reading client
        #
        show('Shutting the reading client')
        try:
            outs, errs = self.reader.communicate(timeout=1)
        except subprocess.TimeoutExpired:
            self.reader.kill()
            outs, errs = self.reader.communicate()

        show(f'reading client stdout: {outs}')
        show(f'reading client stderr: {errs}')
        lines = outs.splitlines()
        line = lines.pop(0)
        show(f'popped line: {line}')
        self.assertEqual(line, '[')

        total_messages = 0
        for args in self.messages:
            msgs = args[0]
            total_messages += len(msgs)
        self.assertEqual(len(lines), total_messages)

        for line in lines:
            show(f'line: {line}')
            msg = json.loads(line)
            self.assertIn('message', msg)

        return

    def test_all(self):
        self.assertTrue(isinstance(self.sever_process, Process))

        show('starting a pool of POSTing clients')
        with Pool(processes=len(self.messages)) as pool:
            pool.starmap(client_post_proc, self.messages)
            pool.close()
            pool.join()
        show('done with the pool of POSTing clients')
        return


if __name__ == '__main__':
    main()
