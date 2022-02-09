# from django.test import TestCase
import hashlib


def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


hash_string = 'data1234'
sha_signature = encrypt_string(hash_string)

print(sha_signature)
# Create your tests here.
