#
# Test plan
#
# Posting a message
# curl -X POST -H "Content-Type: application/json" -d '{"message":"hi?"}' http://localhost:8080
#
# Chat participants read messages:
# curl http://localhost:8080
#
from multiprocessing import Process, Pool
from unittest import TestCase, main

from server import run_chat_server, show

class TestChatServer(TestCase):

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
        show('Starting chat server')
        self.sever_process = Process(
            target=run_chat_server, args=('localhost', 8080,))
        self.sever_process.start()
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
        return

    def test_all(self):
        #self.assertEqual('foo'.upper(), 'FOO')
        show('test_all')
        self.assertTrue(isinstance(self.sever_process, Process))

        messages = (
            ('0.1110', '0.1111', ),
            ('1.1110'),
            ('2.1110', '2.1111', '2.1112'),
        )
        with Pool(processes=len(messages)) as pool:
            pool.starmap()
            pass

        return


if __name__ == '__main__':
    main()
