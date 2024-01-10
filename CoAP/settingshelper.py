#!/usr/bin/env python2
## Copyright (c) 2012-2024 Easylogic B.V. All rights reserved
## settingshelper.py
## version 1.0
## Date 03-01-2024
## This is settings helper class
import time
import json
import os
from os.path import join, isfile, isdir
from os import mkdir, getcwd
import logging
import shutil


class SettingsHelper:

    def __init__(self, currentpath=os.getcwd()):
        self.name = "settings.json"
        self.currentpath = currentpath
        self.settingspath = join(self.currentpath, "data/")
        self.settingsfile = join(self.settingspath, self.name)
        self.settings = None
        self.version = ""
        self.isDirty = False

    def initialize(self):
        print("In the begining of initialization\n")
        if isfile(self.settingsfile):
           with open(self.settingsfile) as reader:
                          self.settings = json.load(reader)
                          with open(self.settingsfile, "w") as writer:
                              json.dump(self.settings, writer, sort_keys = True, indent = 4)
           reader.close()
           return True
        else:
           print("Going to create the settings file and dir\n")
           if self.createSettingsFile():
              print("Create settings file was succesed!\n")
              return self.loadSettings()

    def createSettingsFile(self):
        print("In the create settings dir\n")
        try:
            if not isdir(self.settingspath):
                mkdir(self.settingspath)
            if isdir(self.settingspath):
               try:
                   settingsFileReserve = join(getcwd(), self.name)
                   if isfile(settingsFileReserve):
                      shutil.copy(settingsFileReserve, self.settingspath)
                      return True
               except Exception as Argument:
                   print("Error Exception: %s" % str(Argument))
                   self.logger.exception(Argument)
        except Exception as Argument:
            print("Error exception: %s" % str(Argument))
            return False

    def loadSettings(self):
        try:
            with open(self.settingsfile) as reader:
                self.settings = json.load(reader)
            self.version = self.settings["version"]
            self.date = self.settings["date"]
            return True
        except Exception as Argument:
            print("Error %s\n" % str(Argument))
            return False

    def saveSettings(self):
        try:
            if self.isDirty:
               with open(self.settingsfile, "w") as writer:
                    json.dump(self.settings, writer, sort_keys=True, indent=4)
               self.isDirty = False
        except Exception as Argument:
            print("Exception occurred: %s" % str(Argument))

    def getSettingValue(self, key):
        for setting in self.settings["items"]:
            if setting["key"] == key:
                return setting["value"]
        return ""

    def setSettingValue(self, key, value):
        for setting in self.settings["items"]:
            if setting["key"] == key:
               if setting["value"] != value:
                  setting["value"] = value
                  self.isDirty = True
