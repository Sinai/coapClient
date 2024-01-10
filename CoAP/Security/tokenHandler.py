#!/usr/bin/env python2

import logging
import os
import sys
import uuid
import time
import signal
from os import mkdir, getcwd
from os.path import join, isfile, isdir


class TokenHandler():

    def __init__(self):
       self.currentPath = os.getcwd()
       self.token = None
       self.logger = logging.getLogger(__name__)


    def createToken(self, message, bytes):
       self.logger.info("call to generate token with text: %s and bytes: %s" % (message, bytes))
       if message!=None:
          self.token=uuid.UUID(str(message))
       if bytes!=None:
          if not isinstance(bytes, bytes):
             value=bytes(bytes, 'utf-8')
          else:
             value=bytes
          self.token=uuid.UUID(bytes=value) 
       if bytes==None and message==None:
          # make UUID based on host ID and current time 
          self.token=uuid.uuid1() 
       return self.token
     
