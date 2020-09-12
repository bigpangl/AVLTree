"""
Author: LanHao
Date:2020/9/12
Python: python 3.6
"""
import time
import datetime
import logging

from Trees import AVLTree

logging.basicConfig(level=logging.INFO)

avl = AVLTree()
max_value = 100
# _ = input("123")
logging.info(f"start:{datetime.datetime.now()}")
for i in range(max_value):
    avl[i] = i

logging.info(f"end:{datetime.datetime.now()}")
# _ = input("123")
logging.info(avl.pop(50))
logging.info(f"end:{datetime.datetime.now()}")
logging.info(avl)
# print(avl)

for i in range(max_value):
    del avl[i]
logging.info(avl)
# _ = input("23423")
# print(avl)