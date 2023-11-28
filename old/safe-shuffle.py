import numpy as np
import hashlib
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes


def vers_8bit(c):
	chaine_binaire = bin(ord(c))[2:]
	return "0"*(8-len(chaine_binaire))+chaine_binaire

array = np.arange(100) # [0 1 2 3 4 5 6 7 8 9]


def sample(max,cipher,zerobuf):
    # rejection sampling using rand(0..n * max) % max
    # the value 2 is in there to make sure the number of bits is at least
    # two higher than max, so that the chance of each candicate succeeding
    # is higher
    stream_size = (max.bit_length() + 2 + 7) // 8
    max_stream_value = 1 << (stream_size * 8)
    max_candidate = max_stream_value - max_stream_value % max
    while True:
        stream = cipher.encrypt(zerobuf[0:stream_size])
        candidate = int.from_bytes(stream, "big")
        if (candidate < max_candidate):
            break
    return candidate % max

def shuffle(key,list):
    m = hashlib.sha512()
    m.update(key.encode('utf-8'))
    seed = m.digest() # use SHA-256 to hash different size seeds
    nonce_rfc7539 = bytes([0x00]) * 12
    cipher = ChaCha20.new(key=seed, nonce=nonce_rfc7539)
    zerobuf = bytes([0x00]) * 5
    # do the Fisher-Yates shuffle
    for i in range(len(list) - 1, 0, -1):
        j = sample(i + 1,cipher,zerobuf)
        list[i],list[j] = list[j],list[i]
    


# test only
print(array)
#for i in range(0, 100):
shuffle("hello2",array)
print(array)
