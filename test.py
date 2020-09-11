"""

Project:    AVLTree
Author:     LanHao
Date:       2020/9/11
Python:     python3.6

"""
import logging

from cores import *

logging.basicConfig(level=logging.INFO)

cache = AVLTree()

for i in range(100):
    cache[i] = i
logging.info(cache)
for i in range(99,-1,-1):
    del cache[i]
logging.info(cache)
for i in range(10):
    cache[i] = i
logging.info(cache)
# logging.info(cache[99])

