import hashlib
import logging


def get_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def save_md5_to_txt(md5, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(md5)

def get_md5_regex_pattern():
    return r"([a-fA-F\d]{32})"

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(name)s: %(message)s',
                        )
    logging.info("Starting...")
    file_path = '/data/4chanWebScrapper.zip'
    output_path = '/data/md5_of_zip.txt'
    md5 = get_md5(file_path)
    logging.info(f"MD5 of file: [MD5={md5}]")
    save_md5_to_txt(md5, output_path)
    logging.info("Finished")
