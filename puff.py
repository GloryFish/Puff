#! /usr/bin/python

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
import ConfigParser
from StringIO import StringIO

import mechanize

default_config = """
[huffduffer]
username = yourusername
password = yourpassword
"""

class Puffer(object):
    """Huffduffer API wrapper."""
    
    def __init__(self, username = None, password = None):
        self.username = ''
        self.password = ''
        self.logged_in = False
        
        if username == None or password == None:
            self.load_config()
        else:
            self.username = username
            self.password = password
        
        self.br = mechanize.Browser()
        self.login()
        
    def load_config(self):
        # Load configuration
        try:
            config = ConfigParser.ConfigParser()
            config.readfp(StringIO(default_config))
        except ConfigParser.Error as cpe:
            self.log('load_config(): %s' % cpe)
        
        
        if os.path.isfile('puff.ini'):
            self.log('Found configuration, loading...')

            try:
                config.read('puff.ini')
            except ConfigParser.Error as cpe:
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
    
    def login(self):
        if self.logged_in:
            return
        
        self.log('Logging in %s' % self.username)

        self.br.open('http://huffduffer.com/login') 
        self.br.select_form(nr=1)

        self.br['login[username]'] = self.username
        self.br['login[password]'] = self.password
        self.br.submit()
        
        if (self.br.title() != 'Sign in on Huffduffer'): 
            self.log('Login succeeded for %s' % self.username)
            self.logged_in = True
        else:
            self.log('Login failed for %s' % self.username)
            
    def post(self, url):
        if self.logged_in != True:
            self.log('Must be logged in')
            return

        self.log('Puffing %s' % url)
        
        self.br.open('http://huffduffer.com/add')
        self.br.select_form(nr=1)
        self.br['bookmark[url]'] = url
        self.br['bookmark[title]'] = 'Puffed Audio'
        
        self.br.submit()

        self.log('Puffed %s' % url)
        return True
        
        
    def log(self, message):
        if __name__ == '__main__':
            sys.stdout.write('%s\n' % message )
            sys.stdout.flush()
        
    def encoded_credentials(self):
        return urllib.urlencode({'login[username]': self.username, 'login[password]': self.password})
        
if __name__ == '__main__':
    try:
        url = sys.argv[1]
    except:
        print 'Please specify a url to Puff'
        exit()

    puffer = Puffer()
    puffer.post(url)