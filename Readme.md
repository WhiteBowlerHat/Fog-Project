# Fog-project
## Objectives
The goal of this project is to encrypt/hide a message into a bank of images

For now, you have a bank of 7 images (can change).
The program has two main functions :
-fog : hide the message
-wind : uncover the message

The program needs an symetric key (example: "key")

## How does it work ?

First let *message* be the message we want to hide.
And let *key* be the key to encrypt the message

m  | e  | s  | s  | a  | g  | e 
----|----|----|----|----|----|----

**STEP 1:** Then the program will choose on which image goes which letter (according to the key)

Example (for a bank of 7 images):

 6 | 2 | 0 | 6 | 3 | 5 | 6 
---|---|---|---|---|---|---

Here we can see that *m* will go in the *7th* image, *e* in the *3rd*, etc...

**STEP 2:** The program concats the string that goes on the same image. (Less time consumption, only 1 shuffle per image)
E.g. 
's'|''|'e'|'a'|''|'g'|'mse'
---|---|---|---|---|---|---
im0|im1|im2|im3|im4|im5|im6

**STEP 3:** The program will convert each array element to binary (here's the result for *"mse"*) :

| 01101101 | 01110011 | 01100101 |
|----------|----------|----------|

**STEP 4:** Each bit will go in the shuffled array.

**The shuffle :**

Lets assume the 7th image is 6x6 pixel wide :
| X | A  | B  | C  | D  | E  | F  |
|---|----|----|----|----|----|----|
| 1 | 0  | 1  | 2  | 3  | 4  | 5  |
| 2 | 6  | 7  | 8  | 9  | 10 | 11 |
| 3 | 12 | 13 | 14 | 15 | 16 | 17 |
| 4 | 18 | 19 | 20 | 21 | 22 | 23 |
| 5 | 24 | 25 | 26 | 27 | 28 | 29 |
| 6 | 30 | 31 | 32 | 33 | 34 | 35 |

Becomes (after shuffle) :
| X | A  | B  | C  | D  | E  | F  |
|---|----|----|----|----|----|----|
| 1 | 11 | 33 | 35 | 32 | 3  | 20 |
| 2 | 1  | 27 | 19 | 31 | 10 | 5  |
| 3 | 21 | 17 | 7  | 4  | 23 | 25 |
| 4 | 14 | 0  | 16 | 15 | 6  | 29 |
| 5 | 28 | 9  | 34 | 8  | 12 | 13 |
| 6 | 26 | 22 | 24 | 30 | 18 | 2  |

So the first element to be place will be in *B4* instead of *A1*:

For the 7th image :
- *B4* = 0
- *A2* = 1
- *F6* = 1
- ...

**Step 5 :** Repeat the shuffle for each image and for non-empty string in the *step 2* array


## Decrypt

The decrypting process is quite the same (find the order of images-> get the table form *step 2* -> shuffle each array and find the content)

### Info
- To place one bit in a specific pixel, we only use the *red* property, convert it in binary and replace the last bit.
- The shuffle is currently using the ChaCha20 algorithm with the same nonce
- The step 2 array is generated using *random.randrange(0,number of images)* with *random.seed(key)* 

