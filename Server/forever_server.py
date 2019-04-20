import logging
import os
import re
import socketserver
from md5checker import get_md5_regex_pattern, get_md5


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        requested_file = '4chanWebScrapper.zip'
        # Echo the back to the client
        request = self.request.recv(1024)
        decoded_request = request.decode()
        logging.info(f"REQUEST RECEIVED: [{decoded_request}]")
        if re.match(get_md5_regex_pattern(), decoded_request):
            logging.info("Client requested check MD5 of server's zip file.")
            md5_of_zip_file = get_md5(requested_file)
            logging.debug(f"DECODED_REQUEST={decoded_request}, MD5_OF_ZIP_FILE={md5_of_zip_file}.")
            if decoded_request == md5_of_zip_file:
                self.request.send(f"ACTUAL {str(os.path.getsize(requested_file))}".encode())
            else:
                self.request.send(f"OBSOLETE {str(os.path.getsize(requested_file))}".encode())
        elif re.match(r'^(.+)\.zip$', decoded_request):
            logging.info(f"Received filename: [{decoded_request}]")
            if os.path.isfile(decoded_request):
                logging.info(f"File exists [{decoded_request}].")
                self.request.send(f"EXISTS {str(os.path.getsize(decoded_request))}".encode())
            else:
                self.request.send(f"ERROR file does not exists".encode())
        elif re.match(r'^OK$', decoded_request):
            logging.info("Client requested download file.")
            with open(requested_file, 'rb') as file_to_send:
                bytes_to_send = file_to_send.read(1024)
                self.request.send(bytes_to_send)
                while bytes_to_send:
                    bytes_to_send = file_to_send.read(1024)
                    self.request.send(bytes_to_send)
                logging.info(f"File sent successfully.")


class MyStreamHandler(socketserver.StreamRequestHandler):

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data.upper())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(name)s: %(message)s',
                        )
    HOST, PORT = '127.0.0.1', 5000

    # Create the server, binding to localhost on port 5000
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you interrupt the program with Ctrl-C
    server.serve_forever()
