# Fog-project
## Usage :
First install the required libraries :

pip install requirement.txt

Then run the program as follow :

python app.py

To encrypt :
- put the key (password) in the key field
- compress the message in a zip file and put it in the zipfile field
- put the bank of image that you want to hide your message in the input field (ex: bank, bank2)
- put your desired output folder in the output field

Then send the image contained in the output folder and the message length (in terminal) to the receiver 

To decrypt :
- put the key (password) in the key field
- put the message length in the size field
- put the image fold (where the message is encoded) in the input field
- put the desired output folder where your decoded zipfile will be generated

/!\ Warning /!\ 
This program will work only with the same amount of images, if there is others, it will try to decode with others

/!\ Warning /!\ 
This program is very light and may be very slow (like hours if the message is big), small lines are preffered

/!\ Warning /!\ 
You can send all the images through different means of communications they have to stay in png and not compress, you might lose information

## Objectives
The goal of this project is to encrypt/hide a zip file (small) into a bank of images

The program has two main functions :
- fog : hide the message
- wind : uncover the message

## How does it work ?
First it use Chacha20 to create a pseudo-random number generator.

This generator will be use to get the same pseudo-random numbers when the same key is entered

The program need a bank of image to run (png)

Secondly, it convert the zip folder (message you want to hide) in a binary string

Once you have the binary string it iterates through the string, for each bit, it chooses a random image in the bank and then a random pixel to be encoded in. (the R part of RGB)

The meta-data of thye image is then set with a nonce and the image number in order to be able to decode everything

Once the program has terminated, a size will be displayed and the new set of images will be generated with the message included. 

Send the size of the message and the bank of image to the receiver.

With those information you can decode everything

## Why ? 
I think it is an interesting mean of obfuscation, and very hard to decode since the algorithm of pseudo-random number is cryptographically secure.

It is between encryption and obfuscation, the message not encrypted but hidden securely.

If you dont have the key, the information is flooded in the bank of image.

The information you have if you try to decode without the key are :

- "eventually" the size of the message
- "eventually" the order of the images
- the nonce

I think the best way to decrypt the message is to find/guess the key, else it will be impossible. 





