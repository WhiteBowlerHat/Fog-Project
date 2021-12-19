import random
import sys
from PIL import Image, ImageFont, ImageDraw
from PIL.PngImagePlugin import PngImageFile, PngInfo
import glob

def vers_8bit(c):
	chaine_binaire = bin(ord(c))[2:]
	return "0"*(8-len(chaine_binaire))+chaine_binaire

def modifier_pixel(pixel, bit):
	# on modifie que la composante rouge
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
   array = the_shuffle(image,key)
   dimX,dimY = image.size
   im = image.load()
   posx_pixel = 0
   posy_pixel = 0
   i=0
   for rang_car in range(0,taille):
      rep_binaire = ""
      for rang_bit in range(0,8):
         posy_pixel, posx_pixel = divmod(array[i], dimX)
         rep_binaire += recuperer_bit_pfaible(im[posx_pixel,posy_pixel])
         i+=1
      message += chr(int(rep_binaire, 2))
   image.close()
   return message

def hide(image_file,message,order,key):
   image = Image.open(image_file)
   dimX,dimY = image.size
   array = the_shuffle(image,key)
   im = image.load()
   message_binaire = ''.join([vers_8bit(c) for c in message])
   metadata = PngInfo()
   metadata.add_text("Order", str(order))
   i=0
   for bit in message_binaire:
      posy_pixel, posx_pixel = divmod(array[i], dimX)
     # print("X: "+str(posx_pixel)+" ; Y: "+str(posy_pixel)+"\n")
      im[posx_pixel,posy_pixel] = modifier_pixel(im[posx_pixel,posy_pixel],bit)
      i += 1
   return metadata,image

def split_msg(msg,key,nb):
   #random.seed(key)
   image_nb = [random.randrange(0,nb) for i in range(len(msg))]
   #order = [i for i in range(len(msg))]
   #random.shuffle(order)
   return image_nb#, order

def split_msg2(taille,key,nb):
   #random.seed(key)
   image_nb = [random.randrange(0,nb) for i in range(taille)]
   #order = [i for i in range(len(msg))]
   #random.shuffle(order)
   return image_nb

def the_shuffle(img,key):
   #random.seed(key)
   dimX,dimY = img.size
   length =  dimX*dimY
   array = []
   for i in range(length):
      array.append(i)
   random.shuffle(array)
   print(array[0])
   #pixel_row, pixel_col = divmod(array[0], dimX)
   return array

def smallf(x,arr,msg):
   string =""
   for i in range(len(arr)):
      if arr[i] == x:
         string+=msg[i]
   return string

def fog(key,message,image_bank):
   random.seed(key)
   img_list=glob.glob(image_bank+'/*.png')
   image_nb = split_msg(message,key,len(img_list))
   splitted_msg =[]
   #print(image_nb)
   for i in range(len(img_list)):
      splitted_msg.append(smallf(i,image_nb,message))
   #print(splitted_msg)
   for idx,i in enumerate(img_list):
      #print(i)
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
   img_nb=split_msg2(size,key,len(img_list))
   #print(img_nb)
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
   #print(arr_size)
   msg_array_unordered=[]
   for idx,i in enumerate(sorted_img_list):
      #print(i)
      if arr_size[idx] != 0:
         msg_array_unordered.append(extract_message(i,arr_size[idx],key))
      else:
         msg_array_unordered.append("")
   content=""
   for i in range(len(img_nb)):
      s = msg_array_unordered[img_nb[i]]
      content+=s[0]
      msg_array_unordered[img_nb[i]]=s[1:]
   print(content)
#img,arr = the_shuffle("suda.png", sys.argv[1])
#hide(img, sys.argv[2], arr)
#img.close()
#img,arr = the_shuffle("modified", sys.argv[1])
#print(extract_message("modified",6,arr))
print("Starting encryption...")
fog("key","maximus premierp","bank")
print("Encryption ended successfully ! Images are stored in the 'fog' directory !")
print("Starting decryption...")
wind("key",16,"fog")
