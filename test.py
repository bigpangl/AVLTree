"""

Project:    AVLTree
Author:     LanHao
Date:       2020/9/11
Python:     python3.6

"""
import logging
import sys
import os

import psutil


from cores import *

logging.basicConfig(level=logging.INFO)

cache = AVLTree()
_ = input("00")
max_value = 100000 # 当这个值很大时，确实能够减少内存
for i in range(max_value):
    cache[i] = i
logging.info(f"当前程序占用内存:{psutil.Process(os.getpid()).memory_full_info().rss/1024/1024/1024} GB")
logging.info(sys.getsizeof(cache))
_ = input("one")
for i in range(max_value-1,-1,-1):
    del cache[i]
logging.info(f"当前程序占用内存:{psutil.Process(os.getpid()).memory_full_info().rss/1024/1024/1024} GB")
logging.info(sys.getsizeof(cache))
_ = input("two")
for i in range(10):
    cache[i] = i
logging.info(sys.getsizeof(cache))
logging.info(f"当前程序占用内存:{psutil.Process(os.getpid()).memory_full_info().rss/1024/1024/1024} GB")
_ = input("three")
# logging.info(cache[99])

