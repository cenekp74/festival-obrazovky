import hashlib

def hash_sha256(input_string):
    encoded_string = input_string.encode()
    sha256 = hashlib.sha256()
    sha256.update(encoded_string)
    hash_result = sha256.hexdigest()
    return hash_result