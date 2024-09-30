from unicodedata import name
from PIL import Image
from PIL.PngImagePlugin import PngImageFile, PngInfo
import glob
import hashlib
from Crypto.Cipher import ChaCha20
from base64 import b64encode, b64decode
import base64
import zipfile
import io

# Function used for safe randomization
# Taken here -> https://stackoverflow.com/questions/66528995/cryptographically-secure-pseudo-random-shuffle-a-list-or-array-in-python
def sample(max,cipher,zerobuf):
    stream_size = (max.bit_length() + 2 + 7) // 8
    max_stream_value = 1 << (stream_size * 8)
    max_candidate = max_stream_value - max_stream_value % max
    while True:
        stream = cipher.encrypt(zerobuf[0:stream_size])
        candidate = int.from_bytes(stream, "big")
        if (candidate < max_candidate):
            break
    return candidate % max

# Function that return an array (size "size") of "random" number between 0 - nb
def safe_randrange(nb,size,cipher):
    zerobuf = bytes([0x00]) * 5
    array = []
    for i in range(size):
        print("Number "+str(i)+"/"+str(size))
        elem = sample(nb,cipher,zerobuf)
        array.append(elem)
    return array

def retrieve_last_bit(pixel):
	r_val = pixel[0]
	return bin(r_val)[-1]

def pos_arr_builder(img,lenmsg,cipher):
   length = img.size[0]*img.size[1]
   array = []
   zerobuf = bytes([0x00]) * 5
   for i in range(lenmsg):
      if len(array)== 0:
         array.append(sample(length,cipher,zerobuf))
         length-=1
      else:
         e=sample(length,cipher,zerobuf)
         for j in array:
            if e >= j:
               e+=1
         length-=1
         array.append(e)
   return array


def extract_message(image_file,size,cipher):
   message = ""
   image =Image.open(image_file)
   array = pos_arr_builder(image,size,cipher)
   dimX,dimY = image.size
   im = image.load()
   posx_pixel = 0
   posy_pixel = 0
   i=0
   for rang_car in range(0,size):
      rep_binaire = ""
      posy_pixel, posx_pixel = divmod(array[i], dimX)
      rep_binaire += retrieve_last_bit(im[posx_pixel,posy_pixel])
      i+=1
      message += rep_binaire
   image.close()
   return message

# -- Function that convert a bytestring to zip --
def bytestring_to_zip(s,path):
   z=int(s,2).to_bytes(int(len(s)/8),byteorder="big")
   in_memory = io.BytesIO(z)
   data = in_memory.read()
   with open(path+'.zip','wb') as out:
      out.write(data)

# -- Decrypting function -- 
def wind(key,size,directory):
   print("Starting decryption...")
   # Retrieve all images
   img_list=glob.glob(directory+'/*.png')
   print("Image list : ")
   print(img_list)
   print()
   print(size)
    
   # Encode key with SHA-256
   m = hashlib.sha256()
   m.update(key.encode('utf-8'))
   seed = m.digest()
   print("Seed : "+ str(seed) +"\n")
   
   # Retrieve nonce from image metadata
   targetImage = PngImageFile(img_list[0])
   nonce_rfc7539 = b64decode(targetImage.text["Nonce"])
   print("Nonce : "+ targetImage.text["Nonce"] +"\n")

   # Generate XChacha20 python object from nonce and key
   cipher = ChaCha20.new(key=seed, nonce=nonce_rfc7539)

   print("Length image list : "+ str(len(img_list)))
   # Get array of picture number 
   img_nb=safe_randrange(len(img_list),size,cipher)

   # Split list according to images number
   arr_size = []
   sorted_img_list = [0]*len(img_list)
   for i in range(len(img_list)):
      j=0
      targetImage = PngImageFile(img_list[i])
      sorted_img_list[int(targetImage.text["Order"])]=img_list[i]
      for k in img_nb:
         if k==i:
            j+=1
      arr_size.append(j)

   #Retrieve content in each images
   msg_array_unordered=[]
   for idx,i in enumerate(sorted_img_list):
      if arr_size[idx] != 0:
         msg_array_unordered.append(extract_message(i,arr_size[idx],cipher))
      else:
         msg_array_unordered.append("")
   bcontent=""

   # Append content of each images
   for i in range(len(img_nb)):
      s = msg_array_unordered[img_nb[i]]
      bcontent+=s[0]
      msg_array_unordered[img_nb[i]]=s[1:]

   #Convert byte content to zip
   bytestring_to_zip(bcontent,"out")

# -- Main script to assess time consumption of each function --
import time
inp = input("Size ? : ")
start_time = time.time()
wind("key2",int(inp),"fog")
print("--- %s seconds ---" % (time.time() - start_time))
