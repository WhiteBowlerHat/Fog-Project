# Fog-project
## Usage :
This program needs to be excuted on linux with imported libraries.
The command is : python3 fast-fog.py (fog.py is obsolete but interesting)

## Objectives
The goal of this project is to encrypt/hide a message into a bank of images

The program has two main functions :
- fog : hide the message
- wind : uncover the message

The program needs an symetric key (example: "key")

## How does it work ?

First let *message* be the message we want to hide.
And let *key* be the key to encrypt the message

m  | e  | s  | s  | a  | g  | e 
----|----|----|----|----|----|----

**STEP 1:** Convert message to binary

m        | e        | s        | s        | a        | g        | e 
-------- | -------- | -------- | -------- | -------- | -------- | -------- 
01101101 | 01100101 | 01110011 | 01110011 | 01100001 | 01100111 | 01100101 
 
*NB*: each letter is encoded on 16 bits to be able to handle complex characters (e.g. "비읍시옷")
*8 bits are only displayed here for comprehension purpose*.

**STEP 2** Choose which char goes where

Let s = "01101101011001010111001101110011011000010110011101100101"
be the string we want to hide

For each characters of the string, we attribute a "random" image number.
Example (for a bank of 7 images):
 0 | 1 | 1 | 0 | 1 | 1 | ...
 ---|---|---|---|---|---|---
 6 | 2 | 0 | 6 | 3 | 5 |...

**STEP 3:** 
The program concats each bit that goes on the same image. (Less time consumption)
For each image we now have one binary string.

**STEP 4:** Each bit will go in the image.

**Repartition :**
Lets assume an image is 6x6 pixel wide:
| X | A  | B  | C  | D  | E  | F  |
|---|----|----|----|----|----|----|
| 1 | 0  | 1  | 2  | 3  | 4  | 5  |
| 2 | 6  | 7  | 8  | 9  | 10 | 11 |
| 3 | 12 | 13 | 14 | 15 | 16 | 17 |
| 4 | 18 | 19 | 20 | 21 | 22 | 23 |
| 5 | 24 | 25 | 26 | 27 | 28 | 29 |
| 6 | 30 | 31 | 32 | 33 | 34 | 35 |

For each bits we want to hide in this picture, we choose a random position.

Once we found every position we hide each bits.

The program saves the image in the directory specified by the user and repeat the process for each binary string (*step 3*).


### Info
- To place one bit in a specific pixel, we only use the *red* property, convert it in binary and replace the last bit.
- The Chacha20 algorithm is used for determinist pseudo-random numbers generation.
