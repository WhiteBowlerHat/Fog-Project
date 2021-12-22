#Fog-project
The goal of this project is to encrypt/hide a message into a bank of images

For now, you have a bank of 7 images (can change).
The program has two main functions :
-fog : hide the message
-wind : uncover the message

The program needs an assymetric key (example: "key")

How does it work ?

Encryption (fog):

Let n be the length of the message you want to hide.
The program will firstly set the random.seed to the key value.

Then the function create an array with n elements.
Each element is a random value from 0 to the number of images

This array will determine which letter goes in which image.

Then the function goes through each image shuffle the order of the indexes
E.g. 
If an image has 4 pixels then [0,1,2,3] (the initial order) -> [3,0,2,1] 

Then the function places the message (converted in binary) according to the pixel order in each images.

