#! /usr/bin/python
# 
#  test.py
#  puff
#  
#  Created by Jay Roberts on 2011-04-25.
# 

import puff

print('Starting')


puffer = puff.Puffer()

succeeded = puffer.post('http://www.largesound.com/ashborytour/sound/brobob.mp3')
