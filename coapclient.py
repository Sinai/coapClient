#!/usr/bin/env python2

import os
import time
import json
import ipaddress
import sys
import logging
import signal
import getopt
import socket

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri
from settingshelper import SettingsHelper
from os.path import join, isfile, isdir
from os import mkdir, getcwd
from coapthon.layers.messagelayer import MessageLayer


class CoapClient(MessageLayer):
  
   def __init__(self):
      self.completePath = None
      self.payload = None
      self.proxy = None
      self.host = None
      self.port = None
      self.path = None
      self.client = None
      self.logger = None
      self.helper = None
      self.token = None
      self.currentPath=os.getcwd()
   
   def initialize(self):

      self.helper = SettingsHelper(self.currentPath)
      
      if not self.helper.initialize():
         print("Error initialization of the helper\n")
         sys.exit(0)

      self.completePath = self.helper.getSettingValue("KEY_SERVER_PATH")
      self.proxy = self.helper.getSettingValue("KEY_SERVER_PROXY")
      self.host, self.port, self.path = parse_uri(self.completePath)
      #hablde logging
      self.setLogger()
      #get Token
      token = self.helper.getSettingValue("KEY_SECURITY_TOKEN") 
      self.logger.info("I got the following token from settings: %s" % token)
      self.token = str.encode(str(token)) #convert it to bytes
        

   def receive_response(self, response):
       if response!=None and response!="":
          self.logger.info("FROM RECEIVE_RESPONSE Got the following response:")
          self.logger.info(response)


   def starClient(self):
       #path
       try:
           tmp = socket.gethostbyname(self.host)
           self.host=tmp
       except Exception as Argument:
           self.logger.exception(Argument)
           pass
       except socket.gaierror:
           self.logger.error("gaierror while trying to init client")
           pass
       self.client = HelperClient(server=(self.host, self.port))
      

   def setLogger(self):

       formatter = logging.Formatter("%(asctime)s.%(msecs)03d(%(levelname)s)|%(name)s=>%(funcName)s:%(lineno)d: %(message)s","%Y-%m-%d,%H:%M:%S")
       if self.helper!=None:
          loggerPath = self.helper.getSettingValue("KEY_LOG_DIR")
       else:
          loggerPath = "/var/log/easylogicSystem/swapbox/coapServer"
       if not isdir(loggerPath):
          mkdir(loggerPath)
       mainlogFile = join(loggerPath, "main.log")
       errorlogFile = join(loggerPath, "error.log")

       mainlog = logging.handlers.RotatingFileHandler(mainlogFile, maxBytes=2000000, backupCount=3)
       mainlog.setLevel(level=logging.DEBUG)
       mainlog.setFormatter(formatter)

       errorlog = logging.handlers.RotatingFileHandler(errorlogFile, maxBytes=2000000, backupCount=3)
       errorlog.setLevel(level=logging.ERROR)
       errorlog.setFormatter(formatter)

       loggerRoot = logging.getLogger('')
       loggerRoot.setLevel(logging.DEBUG)

       #Console
       ch = logging.StreamHandler()
       ch.setLevel(logging.DEBUG)
       ch.setFormatter(formatter)
       loggerRoot.addHandler(ch)

       loggerRoot.addHandler(mainlog)
       loggerRoot.addHandler(errorlog)

       self.logger = logging.getLogger(__name__)

   def encodePayload(self, payload):
       self.logger.info("Going to encode payload: %s"%payload)
       if payload!=None and payload!="" and self.token!=None:
          payloadBytes = str.encode(str(payload))
          payloadComplete=payloadBytes + self.token
          return payloadComplete
       return None

   def handleGet(self, response):
       if response!=None and response!="":
          payload = response.payload
          code = response.code
          self.logger.info("Received the following GET, payload: %s" % str(payload))
          self.logger.info("Received the following GET, code: %s" % str(code))
       else:
          self.logger.error("Received an empty response")

   def operation(self, operation, payload):
       self.logger.info("CoAP client operation: %s , with payload: %s " % (operation, payload))
       if operation=="PUT":
          if self.path!=None and payload!=None and self.proxy!=None and self.client!=None:
             response = self.client.put(self.path, payload, self.proxy)
             self.logger.info("Response: %s" % response)
             #self.client.stop()
          else:
             self.logger.error("Error while trying to perfrom a PUT, client: %s, path: %s , payload: %s, proxy: %s" % (self.client, self.path, payload, self.proxy))
             
       elif operation=="POST":
          if self.path!=None and payload!=None and self.proxy!=None and self.client!=None:
             response = self.client.post(self.path, payload, self.proxy)
             self.logger.info("Response: %s"% response.pretty_print())
             #self.client.stop()
          else:
             self.logger.error("Error while trying to perfrom a POST, client: %s, path: %s , payload: %s, proxy: %s" % (self.client, self.path, payload, self.proxy))
       elif operation=="DELETE":
          if self.path!=None and self.proxy!=None and self.client!=None:
             response = self.client.delete(self.path , self.proxy) 
             self.logger.info("Response: %s"% response.pretty_print())
             #self.client.stop()
          else:
             self.logger.error("Error while performing a DELETE operation, client: %s,  path: %s , proxy: %s" % (self.client, self.path, self.proxy))  
       elif operation=="GET":
          if self.path!=None and self.proxy!=None and self.client!=None:
             response = self.client.get(self.path, self.proxy)
             time.sleep(10) # wait for response
             self.logger.info("Response: ")
             self.logger.info(response)
             self.handleGet(response)
          else:
             self.logger.error("Error while performing a GET operation, client: %s,  path: %s , proxy: %s" % (self.client, self.path, self.proxy))


   def stop(self):
       if self.client != None:
          self.client.stop()
       sys.exit(0)   
