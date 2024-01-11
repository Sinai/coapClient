#!/usr/bin/env python2

import os
import sys

from coapthon.utils import parse_uri

CompletePath="coap://172.16.14.202:5683/tags/"
host, port, path = parse_uri(CompletePath)
print("The CompletePath: %s\n"% CompletePath)
print("The host: %s\n" % host)
print("The port: %s\n" % port)
print("The path: %s\n" % path)
print("The End! \n")
