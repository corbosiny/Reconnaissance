import random
from PIL import Image

def intToByte(num):
    bits = ''
    intValue = num
    while intValue > 0:
        if intValue % 2 == 0:
            bits = '0' + bits
        else:
            bits = '1' + bits
        intValue = int(intValue / 2)
    if len(bits) < 8:
        bits = '0' * (8 - len(bits)) + bits
    return bits

def letterToByte(letter):
    return intToByte(ord(letter))

def stringToByteArray(string):
    byteArray = []
    for letter in string:
        bits = letterToByte(letter)
        byteArray.append(bits)
        
    return byteArray

def byteToInt(byte):
    if len(byte) < 8:
        if byte[0] == 1:                                    #sign extending
            byte = '0' * (8 - len(byte)) + byte
        else:
            byte = '0' * (8 - len(byte)) + byte
    
    total = 0
    for index, bit in enumerate(byte):
        total += (ord(bit) - 48) * (2 ** (len(byte) - index - 1))
    return total
    

def byteToLetter(byte):
    return chr(byteToInt(byte))

def byteStringToMessage(byteString):
    x = 0
    byteArray = []
    while x < len(byteString):
        byte = byteString[x:x+8]
        byteArray.append(byte)
        x += 8
    return byteArrayToString(byteArray)
        
def byteArrayToString(byteArray):
    message = ""
    for byte in byteArray:
        message += byteToLetter(byte)

    return message

def xor(byte1, byte2):
    return((byte1 or byte2) and not(byte1 and byte2))

def xorByteArray(byteArray, key):
    message = ''
    byteArray = ''.join(byteArray)
    if len(byteArray) > len(key):
        key += [0] * (len(byteArray) - len(key))
    for x in range(len(byteArray)):
        message += str(round(xor(int(byteArray[x]), int(key[x]))))
    return message
    
def generateKey(length):
    key = ''
    for x in range(length):
        key += str(round(random.random()))
    return key

if __name__ == "__main__":
    with open("img.png", "rb") as imageFile:
      f = imageFile.read()
      b = bytearray(f)

    checkpoint = 0
    for x in range(8):
        print(b[x], end= " ")
    print()
    checkpoint += 8
    
    bits = ''
    for x in range(checkpoint, checkpoint + 4):
        bits += intToByte(b[x])
    
    print(bits)
    number = byteToInt(bits)
    print(number)
    checkpoint += 4

    for x in range(checkpoint, checkpoint + 4):
        print(b[x], end= " ")
    print()
    checkpoint += 4

    for x in range(checkpoint, checkpoint + number):
        print(b[x], end= " ")
    print()
    checkpoint += number

    for x in range(checkpoint, checkpoint + 4):
        print(b[x], end= " ")
    print()
    checkpoint += 4

    bits = ''
    for x in range(checkpoint, checkpoint + 4):
        bits += intToByte(b[x])
    print(bits)
    number = byteToInt(bits)
    print(number)
    checkpoint += 4

    if number % 2  == 0:
        number += 1
    for x in range(checkpoint, checkpoint + 1):
        try:
            b[x] += 1
        except:
            b[x] = 0
            
    with open("img2.png", "wb") as imageFile:
        imageFile.write(bytes(b))


    
##    message = 'Hi Corey!'
##    byteArray = stringToByteArray(message)
##    bits = ''.join(byteArray)
##    
##    for index, bit in enumerate(bits):
##        b[index] += int(bit)
##
##    with open("img2.png", "wb") as imageFile:
##        imageFile.write(b)

