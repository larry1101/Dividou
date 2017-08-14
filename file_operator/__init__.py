import hashlib

from file_operator.dir_reader import Direader


def get_file_sha512(file_path):
    __hash = None
    with open(file_path, 'rb') as f:
        sha512obj = hashlib.sha512()
        sha512obj.update(f.read())
        __hash = sha512obj.hexdigest()
    return __hash
