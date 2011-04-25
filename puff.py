#! /usr/local/bin/python3

# 
#  puff.py
#  puff
#  
#  Post to Huffduffer from python.
#
#  Created by Jay Roberts on 2011-04-25.
# 

import os
import sys
import configparser
from io import StringIO

default_config = """
[huffduffer]
username = yourusername
password = yourpassword
"""

class Puffer(object):
    """Huffduffer API wrapper."""
    
    def __init__(self, username = None, password = None):
        if username == None or password == None:
            self.load_config()
        else:
            self.username = username
            self.password = password

    def load_config(self):
        
        # Load configuration
        try:
            config = configparser.ConfigParser()
            config.readfp(StringIO(default_config))
        except configparser.Error as cpe:
            self.log('load_config(): %s' % cpe)
        
        
        if os.path.isfile('puff.ini'):
            self.log('Found configuration, loading...')

            try:
                config.read('puff.ini')
            except configparser.Error as cpe:
                self.log('load_config(): %s' % cpe)
        else:
            try:
                config_file = open('puff.ini', 'w')
                config.write(config_file)
                self.log('Default puff.ini created. Please edit and retry.')
                exit()
            except Exception as e:
                self.log('load_config(): %s' % e)
            finally:
                config_file.close()
        
        self.username = config.get('huffduffer', 'username')
        self.password = config.get('huffduffer', 'password')
        self.log('Loaded configuration')
    
    def post(self, url):
        self.log('Posting: %s'% url)
        return
        
        
    def log(self, message):
        sys.stdout.write('%s\n' % message )
        sys.stdout.flush()