#!/usr/bin/env python2


import binascii
import os
import sys
import uuid

print("Start point of the application ....\n")

tagOne="4541535930898910023"


token = uuid.uuid1()

print("The token: %s\n"%token)

#tagBytes = bytes(tagOne, 'utf-8')
tagBytes = str.encode(tagOne)

#tagOneByte = bytearray(bytes(tagOne, 'utf-8'))
#tokenByte = bytes(token, 'utf-8')
#tokenByte = str.encode(token)
tokenBytes = token.bytes
print("Encoded token: %s and tag: %s\n" % (list(tokenBytes), list(tagBytes)))



tagBytesArray = bytearray(tagBytes)
payload=tagBytes + tokenBytes
#payload = tokenByte + tagOneByte 



print("The payload : %s\n" % list(payload))
payloadList = list(payload)
tokenBytesList = list(tokenBytes)
for byte in tokenBytesList:
  print("The byte: %s\n"%byte)
  payloadList.remove(byte)

payloadBytes = b''.join(payloadList)
print("Payload in bytes : %s\n" % payloadBytes)
print("The payload list after removal of token: %s" % payloadList)

returnedTag = payloadBytes.decode("utf-8")

print("The recoverd tag: %s\n" % returnedTag) 

'''   
print("The token: \n")
print(token)
print("\n")
stringValue=str(token)
print("The string version of the token: %s\n" % stringValue)
length=len(stringValue)
print("The string token is : %d long\n" % length)
bytesVersion = bytes(token)
print("The byte version of the token: %s\n" % bytesVersion)
length=len(bytesVersion)
print("The length of bytes is equal to: %d\n" % length)
'''

print("All done\n")
sys.exit(0)

