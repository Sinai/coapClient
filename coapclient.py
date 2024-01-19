#!/usr/bin/env python2

import os
import time
from datetime import datetime
import json
import ipaddress
import sys
import logging
import logging.handlers
import signal
import getopt
import socket
#import bcrypt

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri
from settingshelper import SettingsHelper
from os.path import join, isfile, isdir
from os import mkdir, getcwd
from coapthon.layers.messagelayer import MessageLayer



class CoapClient():
  
   def __init__(self):
      self.completePath = None
      self.payload = None
      self.proxy = None
      self.host = None
      self.port = None
      self.path = None
      self.client = None
      self.logger = None
      self.error = False
      self.helper = None
      self.token = None
      self.userName = None
      self.passW = None
      self.date = None
      self.dateFormat = None
      self.data = {}
      self.currentPath=os.getcwd()
      self.clientId = None
      self.connected = False
   
   def initialize(self):

      self.helper = SettingsHelper(self.currentPath)
      
      if not self.helper.initialize():
         print("Error initialization of the helper\n")
         sys.exit(0)


      #get variable
      self.dateFormat = self.helper.getSettingValue("KEY_DATETIME_FORMAT")
      self.clientId = self.helper.getSettingValue("KEY_SYSTEM_ID")
      self.userName = self.clientId
      self.passW = self.helper.getSettingValue("KEY_SERVER_PASSWORD") #Hashed password!
      #logging
      self.setLogger()
      self.logger.info("the date formatter After the settings value: %s"% self.dateFormat)
   
   def setServerPath(self, type):

       if type!=None and type=="tags/":
          self.completePath = self.helper.getSettingValue("KEY_SERVER_PATH_TAGS")
          self.proxy = self.helper.getSettingValue("KEY_SERVER_PROXY")
          self.host, self.port, self.path = parse_uri(self.completePath)
       elif type!=None and type=="auth/":
          self.completePath = self.helper.getSettingValue("KEY_SERVER_PATH_AUTH")
          self.proxy = self.helper.getSettingValue("KEY_SERVER_PROXY")
          self.host, self.port, self.path = parse_uri(self.completePath)
          self.logger.info("host: %s , port: %s , path: %s"%(self.host, self.port, self.path))
       else:
          self.logger.error("Could not get the correct server path for type: %s"%type)     
          self.error = True       


   def receive_response_get(self, response):
       self.logger.info("call to receive_response_get")
       if response!=None and response!="":
          self.logger.info("FROM RECEIVE_RESPONSE Got the following response:") 
          self.logger.info(response)


   def receive_response_put(self, response):
       self.logger.info("call to receive response put")
       if response!=None and response!="":
          self.logger.info("We got the following response: %s"% response)
          self.logger.info("We got the following response payload: %s"% response.payload)
          data =  json.loads(response.payload)

          if "token" in  data:
             self.logger.info("Detected that token was in the data")
             self.logger.info("token: %s" % data["token"])
             self.logger.info("Signed %d" % data["signedOK"])
             if data["signedOK"]==1:
                self.logger.info("Token: %s" % data["token"])
                self.connected = True
                self.token = data["token"]

          else:
             self.logger.info("Detected different response than AUTH from server")

          #self.token = data["token"]

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


   def clientIsConnected(self):
       return self.connected
      

   def setLogger(self):
       print("Starting point of setting loggers\n")
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
       print("End point of setting loggers\n")


   def getAuthenticationPayload(self):
       if self.userName!=None and self.passW!=None:
          self.data = {}
          self.data["Id"] = self.userName
          passwordBytes = self.passW.encode('utf-8')
          #saltBytes = bcrypt.gensalt(12)
          #hashedPassword=bcrypt.hashpw(passwordBytes, saltBytes)
          #hashedPasswordDecoded = hashedPassword.decode('utf-8')
        
          self.data["Passw"] = passwordBytes
          json_data = json.dumps(self.data)
          return json_data
       else:
          self.logger.error("Error creating auth payload, usr: %s and passw: %s" % (self.userName, self.passW))
          return None

   def encodePayload(self, tag):
       self.logger.info("Going to encode payload: %s"%payload)
       if self.token!=None and tag!=None:
          valueReturn=str(self.token)+str(tag)
          return valueReturn
    return None


   def completePayload(self, tag):
       if self.clientId != None and self.token != None and :
          #self.logger.info("the date formatter: %s"% self.dateFormat)
          #self.data["DeviceId"] = self.clientId
          #self.data["tag"]  = payload
          #passWBytes = self.passW.encode('utf-8')  it is haseh dureing json creation
          data = self.encodePayload(tag)
          if data!=None:
             payload = {}
             payload["data"] = data
             payload["Id"] = self.clientId
          json_data = json.dumps(payload)
          return json_data
       return None   


   def handleGet(self, response):
       if response!=None and response!="":
          payload = response.payload
          code = response.code
          self.logger.info("Received the following GET, payload: %s" % str(payload))
          self.logger.info("Received the following GET, code: %s" % str(code))
       else:
          self.logger.error("Received an empty response")

   def operation(self, operation, payload, path):
       self.logger.info("CoAP client operation: %s , with payload: %s and path: %s " % (operation, payload, path))
       #set the correct path
       if path!=None and  path!=self.path:
          self.logger.info("The path: %s" % path)
          self.setServerPath(path)

       #perform operation
       if operation=="PUT":
          if self.path!=None and payload!=None and self.proxy!=None and self.client!=None:
             response = self.client.put(self.path, payload, self.proxy, self.receive_response_put)
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
             recieved = self.client.get(self.path, self.proxy, self.receive_response_get)
             time.sleep(10) # wait for response
             self.logger.info("Response: ")
             self.logger.info(recieved)
             self.handleGet(recieved)
          else:
             self.logger.error("Error while performing a GET operation, client: %s,  path: %s , proxy: %s" % (self.client, self.path, self.proxy))


   def stop(self):
       if self.client != None:
          self.client.stop()
       
