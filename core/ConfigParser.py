
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 23:41:31 2018
@author: Hualin Xiao, dr.hualin.xiao@gmail.com
"""

import configparser
import os

config = configparser.ConfigParser()
config.read('core/config.cfg')
def project_directory():
    try:
        directory=config['DEFAULT']['ProjectDirectory']
        try:
            os.makedirs(directory)
        except:
            pass
        return directory
    except:
        print('Project directory is not set.')
        return '/tmp/'



def max_content_length():
    try:
        size=config['DEFAULT']['MaxContentLength']
    except:
        return 16*1024*1024
    

