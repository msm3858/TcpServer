import logging
import socket
import sys
import zipfile

from md5checker import get_md5


class Client:
    def __init__(self, ip='127.0.0.1', port=5000):
        self.ip = ip
        self.port = port
        self.server = None

    def _start_request(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            logging.info("Trying to connect to TCP server...")
            self.server.connect((self.ip, self.port))
            logging.info(f"Connected to TCP server [IP={self.ip}, PORT={self.port}].")
        except Exception as exception:
            error_message = repr(exception)
            logging.error(f"Could not connect to server...[ERROR={error_message}].")

    def _end_request(self):
        try:
            self.server.close()
        except Exception as exception:
            error_message = repr(exception)
            logging.error(f"Could not end connection to server [ERROR={error_message}].")

    def send_file_name(self, file_name='4chanWebScrapper.zip'):
        self._start_request()
        file_name_encoded = file_name.encode()
        length_to_send = self.server.send(file_name_encoded)
        response = self.server.recv(length_to_send)
        response_decoded = response.decode()
        self._end_request()
        if (response_decoded[:6] == 'EXISTS'):
            logging.info(f"Requested file exists on TCP server[file_name={file_name}].")
            try:
                logging.info(f"Bytes of requested file={response_decoded[7:]}")
                return int(response_decoded[7:])
            except Exception as exception:
                error_message = repr(exception)
                logging.error("Could not resolve number of bytes to receive")
                return 0
        else:
            logging.warning("Requested file does not exists on TCP server.")
            return 0

    def update_client_zip_file(self, file_name='zipped_file.zip'):
        is_downloaded = False
        try:
            my_zip_md5 = get_md5(file_name)
        except FileNotFoundError as exception:
            logging.warning(f"File does not exists: [{file_name}].")
            my_zip_md5 = '1'*32

        logging.info(f"MD5 of local file: [MD5={my_zip_md5}].")
        self._start_request()
        my_zip_md5_encoded = my_zip_md5.encode()
        length_to_send = self.server.send(my_zip_md5_encoded)
        response = self.server.recv(length_to_send)
        response_decoded = response.decode()
        logging.info(f"Response from the server: [Respone={response_decoded}].")
        self._end_request()
        if (response_decoded[:6] == 'ACTUAL'):
            logging.info(f"[{file_name}] is actual does not need update.")
        elif (response_decoded[:8] == 'OBSOLETE'):
            logging.info(f'UPDATING {file_name}...')
            try:
                bytes_to_receive = int(response_decoded[9:])
                logging.info(f"Bytes to receive = {bytes_to_receive}.")
                is_downloaded = self.receive_zip_file(bytes_to_receive)
            except Exception as exception:
                error_message = repr(exception)
                logging.error(f"Unhandled error occured. [ERROR={error_message}].")
                logging.error(f"Exiting...")
                sys.exit(1)
        else:
            logging.warning(f"Could not handle response: [Response={response_decoded}].")
        if is_downloaded:
            self.unzip_zipped_file()

    def unzip_zipped_file(self, file_name='zipped_file.zip'):
        try:
            logging.info(f"Extracting archive: [{file_name}]...")
            zip_ref = zipfile.ZipFile(file_name, 'r')
            zip_ref.extractall('4ChanWebScrapper')
            zip_ref.close()
            logging.info(f"File extracted.")
        except Exception as exception:
            error_message = repr(exception)
            logging.error(f"Unhandled error occured during extracting archive.[ERROR={error_message}].")




    def receive_zip_file(self, bytes_to_receive):
        try:
            if bytes_to_receive > 0:
                self._start_request()
                encoded_message_to_send = 'OK'.encode()
                logging.debug("Sending data %r", encoded_message_to_send)
                length_of_data_to_send = self.server.send(encoded_message_to_send)
                logging.info("Starting receiving data from TCP server...")
                with open('zipped_file.zip', 'wb') as received_file:
                    received_data = self.server.recv(1024)
                    # file_size = received_data[6:].decode()
                    # logging.debug(f"??file_size={file_size}??")
                    totalRecv = len(received_data)
                    logging.debug(f"??totalRecv={totalRecv}??")
                    received_file.write(received_data)
                    while totalRecv < bytes_to_receive:
                        received_data = self.server.recv(1024)
                        totalRecv += len(received_data)
                        received_file.write(received_data)

                        logging.info("{0:.2f}".format((totalRecv / float(bytes_to_receive)) * 100) + "% Done")
                    logging.info("Download Complete!")
                    return True
            else:
                logging.info("Nothing to receive.")
        except Exception as exception:
            error_message = repr(exception)
            logging.error(f"Unexpected error during receiving file[ERROR={error_message}].")
        return False

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, )
    logging.info("Creating client to connect TCP server...")
    client = Client()
    logging.info("Client connected.")
    # bytes_to_receive = client.send_file_name()
    client.update_client_zip_file()
    # client.receive_zip_file(bytes_to_receive)

