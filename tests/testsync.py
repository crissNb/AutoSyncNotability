import unittest
import socket
import os

class TestSync (unittest.TestCase):
    def setUp(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 8000))

    def test_sync_unchanged(self):
        # get absolute path of LoremIpsum.pdf in data/ directory
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'LoremIpsum1.pdf')

        # format the data:
        encoded_data = file_path + ":::" + str(False) + ";;;" + file_path + ":::" + str(False) +";;;"

        self.client_socket.send(encoded_data.encode('utf-8'))

        # receive the data from the server
        data = self.client_socket.recv(1024).decode('utf-8')

        # check if the data is correct
        self.assertEqual(data, "Received data")

    def test_sync2_unchanged(self):
        # get absolute path of LoremIpsum.pdf in data/ directory
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'LoremIpsum2.pdf')

        # format the data:
        encoded_data = file_path + ":::" + str(False) + ";;;" + file_path + ":::" + str(False) +";;;"

        self.client_socket.send(encoded_data.encode('utf-8'))

        # receive the data from the server
        data = self.client_socket.recv(1024).decode('utf-8')

        # check if the data is correct
        self.assertEqual(data, "Received data")

    def test_sync3_unchanged(self):
        # get absolute path of LoremIpsum.pdf in data/ directory
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'LoremIpsum3.pdf')

        # format the data:
        encoded_data = file_path + ":::" + str(False) + ";;;" + file_path + ":::" + str(False) +";;;"

        self.client_socket.send(encoded_data.encode('utf-8'))

        # receive the data from the server
        data = self.client_socket.recv(1024).decode('utf-8')

        # check if the data is correct
        self.assertEqual(data, "Received data")

    def test_sync_large_unchanged(self):
        # get absolute path of LoremIpsum.pdf in data/ directory
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'LoremIpsum24.pdf')

        # format the data:
        encoded_data = file_path + ":::" + str(False) + ";;;" + file_path + ":::" + str(False) +";;;"

        self.client_socket.send(encoded_data.encode('utf-8'))

        # receive the data from the server
        data = self.client_socket.recv(1024).decode('utf-8')

        # check if the data is correct
        self.assertEqual(data, "Received data")

if __name__ == '__main__':
    unittest.main()
