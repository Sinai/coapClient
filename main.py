#!/usr/bin/env python2

import time
from coapclient import CoapClient
from settingshelper import SettingsHelper
import logging
import signal 
import sys
from Security.tokenHandler import TokenHandler 

tagOne="45415359308989100027"
tagTwo="45415359308989100028"
tagThree="45415359308989100029"
tagFour="45415359308989100030"
client = None
logger = None
token = None




def addTokenPayload(self, payload, token):
    if token!=None and payload!=None:
       valueToken=None
       valuePayload=None
       valueReturn=None
       if not isinstance(token, bytes):
          valueToken=bytes(token, 'utf-8')
       else:
          valueToken=token
       if not isinstance(payload, bytes):
          valuePayload=bytes(payload, bytes)
       else:
          valuePayload=payload
       valueReturn=valueToken+valuePayload
       return valueReturn  
    return None

def putTester():
    global client, logger 
  
    logger.info("Client started, going encode tagOne")

    #value = addTokenPayload(tagOne, token)
    
    if client!=None:
       #value = client.encodePayload(tagOne)
       value = client.completePayload(tagOne)
       logger.info("Going to sent tagOne - encoded: %s" % value)
       client.operation("PUT", value)

       #print("Just performed a put and going to stop\n")
       logger.info("Just did a PUT for tagOne")

       time.sleep(30)

       #value = addTokenPayload(tagTwo, token)
       #value = client.encodePayload(tagTwo)
       value = client.completePayload(tagTwo)
       client.operation("PUT", value)
       logger.info("Just did a PUT for tagTwo")

       time.sleep(30)
    
       #value = addTokenPayload(tagThree, token)
       #value = client.encodePayload(tagThree)
       value = client.completePayload(tagThree)
       client.operation("PUT", value)
       logger.info("Just did a PUT for tagThree")

       time.sleep(30)

       #value = addTokenPayload(tagFour, token)
       #value = client.encodePayload(tagFour)
       value = client.completePayload(tagFour)
       client.operation("PUT", value)
       logger.info("Just did a PUT for tagFour")

       time.sleep(30)


def getTester():
    global client, logger
    if logger!=None:
       logger.info("GET client started!")
    if client!=None:
       logger.info("Going to do the First GET")
       client.operation("GET", None) 
       logger.info("Just did the first GET")
       time.sleep(30)
       
       client.operation("GET", None)
       logger.info("Just did the second GET")
       time.sleep(30)

       client.operation("GET", None)
       logger.info("Just did the third GET")
       time.sleep(30)
    
  
    

def main():
    global logger, client

    print("Main:  Going to start\n")
    client = CoapClient()
    client.initialize()
   

   # print("Going to create token\n")
    #tokenClient = TokenHandler()
    #token=tokenClient.createToken(None, None)

    logger = logging.getLogger(__name__)
    #logger.info("The token : %s"%token)


    #print("After the initialization\n")
    logger.info("After the initialization\n")

    client.starClient()
    #print("Client started , going to do a PUT\n")
    
    putTester()
    #getTester()
    
    logger.info("Before client stop!")

    client.stop()

    logger.info("After client stop!")

    logger.info("Going to stop")
    stop()


def stop():
    global logger, client
    if logger!=None:
       logger.info("Going to shutdown")
    if client!=None:
       client.stop()
    sys.exit(0)

def handler(signum, frame):
    global logger
    print("Received an sig term!!!!!!\n")
    if logger!=None:
       logger.info("Received a sigterm\n")
    stop()

if __name__ == "__main__":

   signal.signal(signal.SIGINT, handler)
   signal.signal(signal.SIGTERM, handler)
   signal.signal(signal.SIGHUP, handler)
   try:
       result = main()
   except SystemError as Argument:
       print("System Error: %s\n"% Argument)
       stop()
   except Exception as Argument:
       print("System Exception: %s\n"% Argument)
       print(Argument)
       stop()



