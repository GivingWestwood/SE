import hashlib

def compute_sha256(input):
    h = hashlib.new('sha256',b"swufe")
    return h.hexdigest()