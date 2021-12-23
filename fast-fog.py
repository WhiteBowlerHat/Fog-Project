import random
import sys
from PIL import Image, ImageFont, ImageDraw
from PIL.PngImagePlugin import PngImageFile, PngInfo
import glob
import numpy as np
import hashlib
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes



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

def safe_shuffle(key,list):
    m = hashlib.sha256()
    m.update(key.encode('utf-8'))
    seed = m.digest() # use SHA-256 to hash different size seeds
    nonce_rfc7539 = bytes([0x00]) * 12
    cipher = ChaCha20.new(key=seed, nonce=nonce_rfc7539)
    zerobuf = bytes([0x00]) * 5
    # do the Fisher-Yates shuffle
    for i in range(len(list) - 1, 0, -1):
        j = sample(i + 1,cipher,zerobuf)
        list[i],list[j] = list[j],list[i]


def choose_pixels(key,list,nb):
    m = hashlib.sha256()
    m.update(key.encode('utf-8'))
    seed = m.digest() # use SHA-256 to hash different size seeds
    nonce_rfc7539 = bytes([0x00]) * 12
    cipher = ChaCha20.new(key=seed, nonce=nonce_rfc7539)
    zerobuf = bytes([0x00]) * 5
    j = len(list)-1
    array = []
    for i in range(nb):
        elem = sample(j,cipher,zerobuf)
        array.append(list[elem])
        list.remove(list[elem])
        j=j-1
    return array

def safe_randrange(key, bank_size,nb):
    m = hashlib.sha256()
    m.update(key.encode('utf-8'))
    seed = m.digest() # use SHA-256 to hash different size seeds
    nonce_rfc7539 = bytes([0x00]) * 12
    cipher = ChaCha20.new(key=seed, nonce=nonce_rfc7539)
    zerobuf = bytes([0x00]) * 5
    array = []
    for i in range(nb):
        elem = sample(bank_size,cipher,zerobuf)
        array.append(elem)
    return array

def decode_binary_string(s):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

def vers_8bit(c):
	chaine_binaire = bin(ord(c))[2:]
	return "0"*(8-len(chaine_binaire))+chaine_binaire

def modifier_pixel(pixel, bit):
	r_val = pixel[0]
	rep_binaire = bin(r_val)[2:]
	rep_bin_mod = rep_binaire[:-1] + bit
	r_val = int(rep_bin_mod, 2)
	return tuple([r_val] + list(pixel[1:]))


def recuperer_bit_pfaible(pixel):
	r_val = pixel[0]
	return bin(r_val)[-1]

def extract_message(image_file,taille,key):
   message = ""
   image =Image.open(image_file)
   array = the_shuffle(image,key,taille)
   dimX,dimY = image.size
   im = image.load()
   posx_pixel = 0
   posy_pixel = 0
   i=0
   for rang_car in range(0,taille):
      rep_binaire = ""
      posy_pixel, posx_pixel = divmod(array[i], dimX)
      rep_binaire += recuperer_bit_pfaible(im[posx_pixel,posy_pixel])
      i+=1
      message += rep_binaire#chr(int(rep_binaire, 2))
   image.close()
   return message

def hide(image_file,message_binaire,order,key):
   image = Image.open(image_file)
   array = the_shuffle(image,key,len(message_binaire))
   dimX,dimY = image.size
   im = image.load()
   metadata = PngInfo()
   metadata.add_text("Order", str(order))
   i=0
   for bit in message_binaire:
      posy_pixel, posx_pixel = divmod(array[i], dimX)
      im[posx_pixel,posy_pixel] = modifier_pixel(im[posx_pixel,posy_pixel],bit)
      i += 1
   return metadata,image

def split_msg(msg,key,nb):
   image_nb =  safe_randrange(key, nb, len(msg))
   return image_nb

def split_msg2(taille,key,nb):
   image_nb = safe_randrange(key, nb, taille)
   return image_nb

def the_shuffle(img,key,lenmsg):
   dimX,dimY = img.size
   length =  dimX*dimY
   array = []
   for i in range(length):
      array.append(i)
   arr = choose_pixels(key,array,lenmsg)
   return arr

def smallf(x,arr,msg):
   string =""
   for i in range(len(arr)):
      if arr[i] == x:
         string+=msg[i]
   return string

def fog(key,message,image_bank):
   random.seed(key)
   img_list=glob.glob(image_bank+'/*.png')
   message_binaire = ''.join([vers_8bit(c) for c in message])
   print(len(message_binaire))
   image_nb = split_msg(message_binaire,key,len(img_list))
   splitted_msg =[]
   for i in range(len(img_list)):
      splitted_msg.append(smallf(i,image_nb,message_binaire))
   for idx,i in enumerate(img_list):
      if splitted_msg[idx] != '':
         metadata,image = hide(i,splitted_msg[idx],idx,key)
         savepath = image.filename+"-fog"
         savepath = "fog"+savepath[4:]
         image.save(savepath, "png", pnginfo=metadata)
         image.close()
      else:
         image=Image.open(i)
         metadata = PngInfo()
         metadata.add_text("Order", str(idx))
         savepath=image.filename+"-fog"
         savepath.replace('bank', 'fog')
         savepath = "fog"+savepath[4:]
         image.save(savepath, "png", pnginfo=metadata)
         image.close()

def wind(key,size,directory):
   random.seed(key)
   img_list=glob.glob(directory+'/*.png-fog')
   print(size)
   img_nb=split_msg2(size,key,7)
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
         msg_array_unordered.append(extract_message(i,arr_size[idx],key))
      else:
         msg_array_unordered.append("")
   bcontent=""
   for i in range(len(img_nb)):
      s = msg_array_unordered[img_nb[i]]
      bcontent+=s[0]
      msg_array_unordered[img_nb[i]]=s[1:]
   content = decode_binary_string(bcontent)
   print("Hidden msg : "+content+"\n")


#print("Starting encryption...")
#fog("key2","maximus premierp","bank")
#print("Encryption ended successfully ! Images are stored in the 'fog' directory !")
print("Starting decryption...")
wind("key2",128,"fog")
# img = Image.open('bank/suda.png')
# dimX,dimY = img.size
# length =  dimX*dimY
# array = []
# for i in range(length):
#     array.append(i)
# pixel_array = choose_pixels("lmfaoooooo",array,6)
# for i in pixel_array:
#    posy_pixel, posx_pixel = divmod(i, dimX)
#    print("X :"+str(posy_pixel)+"; Y:"+str(posx_pixel))
# print(safe_randrange("lmfaooooo",7,6))