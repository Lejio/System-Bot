#!/usr/bin/env python

'''
    main.py: Main file that runs the discord bot and supplies secret api keys.
'''

import os
from dotenv import load_dotenv

if __name__ == "__main__":
    
    # Loading environmental variables
    load_dotenv()
    
    # Testing environmental variables
    print(os.getenv('OPENAI_KEY'))
    
    print('hello')
    
    
    

__author__ = "Gene Ni"
__date__ = "June 1 2023"
__version__ = "0.0.1"
__contact__ = "geneisjuan@gmail.com"

