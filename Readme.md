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
## Objectives
The goal of this project is to encrypt/hide a zip file (small) into a bank of images

The program has two main functions :
- fog : hide the message
- wind : uncover the message
