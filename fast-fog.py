from unicodedata import name
from PIL import Image
from PIL.PngImagePlugin import PngImageFile, PngInfo
import glob
import hashlib
from Crypto.Cipher import ChaCha20
from base64 import b64encode, b64decode
from Crypto.Random import get_random_bytes
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
        elem = sample(nb,cipher,zerobuf)
        array.append(elem)
    return array



# --- Function only useful for string encryption, not zip files
# def decode_binary_string(s):
#     return ''.join(chr(int(s[i*16:i*16+16],2)) for i in range(len(s)//16))

# def vers_8bit(c):
# 	chaine_binaire = bin(ord(c))[2:]
# 	return "0"*(16-len(chaine_binaire))+chaine_binaire
def retrieve_last_bit(pixel):
	r_val = pixel[0]
	return bin(r_val)[-1]

def split_msg(size,nb,cipher):
   image_nb = safe_randrange(nb, size, cipher)
   return image_nb

def pos_arr_builder(img,image_name,lenmsg,cipher):
   length = img.size[0]*img.size[1]
   array = []
   zerobuf = bytes([0x00]) * 5
   for i in range(lenmsg):
      #print("Image : "+str(image_name)+" - "+str(i)+" : Maxime est un gros bg !\n")
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

# Function that modify the last bit of the red pixel value according
def modify_pixel(pixel, bit):
	r_val = pixel[0]
	rep_binaire = bin(r_val)[2:]
	rep_bin_mod = rep_binaire[:-1] + bit
	r_val = int(rep_bin_mod, 2)
	return tuple([r_val] + list(pixel[1:]))

def hide(image_file,binary_message,cipher):
   image = Image.open(image_file)
   array = pos_arr_builder(image,image_file,len(binary_message),cipher)
   dimX,dimY = image.size
   im = image.load()
   i=0
   for bit in binary_message:
      posy_pixel, posx_pixel = divmod(array[i], dimX)
      im[posx_pixel,posy_pixel] = modify_pixel(im[posx_pixel,posy_pixel],bit)
      i += 1
   return image

def extract_message(image_file,size,cipher):
   message = ""
   image =Image.open(image_file)
   array = pos_arr_builder(image,image_file,size,cipher)
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

def max_size(list):
   size=0
   for i in list:
      image =Image.open(i)
      size+=image.size[0]*image.size[1]
      image.close()
   return size



def smallf(x,arr,msg):
   string =""
   for i in range(len(arr)):
      if arr[i] == x:
         string+=msg[i]
   return string

def zip_to_bytestring(path):
   tst=""
   with open(path, "rb") as f:
      bytes = f.read()
      tst="".join(["{:08b}".format(x) for x in bytes])
   return tst

def bytestring_to_zip(s,path):
   z=int(s,2).to_bytes(int(len(s)/8),byteorder="big")
   in_memory = io.BytesIO(z)
   data = in_memory.read()
   with open(path+'.zip','wb') as out:
      out.write(data)

def fog(key,message,image_bank,destination_folder):
   img_list=glob.glob(image_bank+'/*.png')
   m = hashlib.sha256()
   m.update(key.encode('utf-8'))
   seed = m.digest() # use SHA-256 to hash different size seeds
   nonce_rfc7539 = get_random_bytes(24)
   snonce = b64encode(nonce_rfc7539).decode('utf-8')
   print(snonce)
   print(max_size(img_list))
   cipher = ChaCha20.new(key=seed, nonce=nonce_rfc7539)
   binary_message = zip_to_bytestring(message)#''.join([vers_8bit(c) for c in message])
   print(len(binary_message))
   image_nb = split_msg(len(binary_message),len(img_list),cipher)
   splitted_msg =[]
   for i in range(len(img_list)):
      splitted_msg.append(smallf(i,image_nb,binary_message))
   for idx,i in enumerate(img_list):
      if splitted_msg[idx] != '':
         image = hide(i,splitted_msg[idx],cipher)
         savepath = image.filename+"-fog"
         savepath = destination_folder+savepath[len(image_bank):]
         metadata = PngInfo()
         metadata.add_text("Order", str(idx))
         metadata.add_text("Nonce", snonce)
         image.save(savepath, "png", pnginfo=metadata)
         image.close()
      else:
         image=Image.open(i)
         metadata = PngInfo()
         metadata.add_text("Order", str(idx))
         metadata.add_text("Nonce", snonce)
         savepath=image.filename+"-fog"
         savepath.replace(image_bank, destination_folder)
         savepath = destination_folder+savepath[len(image_bank):]
         image.save(savepath, "png", pnginfo=metadata)
         image.close()
   print(len(binary_message))

def wind(key,size,directory):
   img_list=glob.glob(directory+'/*.png-fog')
   print(size)
   m = hashlib.sha256()
   m.update(key.encode('utf-8'))
   seed = m.digest() # use SHA-256 to hash different size seeds
   # --TO VERIFY-- 
   # nonce_rfc7539 = seed & 0xffffffffffff
   targetImage = PngImageFile(img_list[0])
   nonce_rfc7539 = b64decode(targetImage.text["Nonce"])
   cipher = ChaCha20.new(key=seed, nonce=nonce_rfc7539)
   img_nb=split_msg(size,len(img_list),cipher)
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
   msg_array_unordered=[]
   for idx,i in enumerate(sorted_img_list):
      if arr_size[idx] != 0:
         msg_array_unordered.append(extract_message(i,arr_size[idx],cipher))
      else:
         msg_array_unordered.append("")
   bcontent=""
   for i in range(len(img_nb)):
      s = msg_array_unordered[img_nb[i]]
      bcontent+=s[0]
      msg_array_unordered[img_nb[i]]=s[1:]
   # content = decode_binary_string(bcontent)
   # print("Hidden msg : "+content+"\n")
   bytestring_to_zip(bcontent,"out")


import time
start_time = time.time()
print("Starting encryption...")
fog("key2","hello.zip","bank","fog")
print("--- %s seconds ---" % (time.time() - start_time))
print("Encryption ended successfully ! Images are stored in the 'fog' directory !")
binary_message = zip_to_bytestring('capt.zip')#''.join([vers_8bit(c) for c in message])
print(len(binary_message))
inp = input("Size ? : ")
start_time = time.time()
print("Starting decryption...")
wind("key2",int(inp),"fog")
print("--- %s seconds ---" % (time.time() - start_time))
