# AVLTree
 平衡二叉树

希望完成rpc 任务计算结果的回发操作。

此处针对的是python 异步rpc通过另一对接返回结果时,字典数据结构无法很好的降低内存

https://aio-pika.readthedocs.io/en/latest/rabbitmq-tutorial/6-rpc.html



### 对比数据

- 数据量大时插入速度
    
    字典可以很快插入几十万的简单数据，但是平衡二叉树，数据量越大，插入就越来越慢了。在插入效率上，差别很大
    
    同时，同体积下，目前平衡二叉树占用内存原高于字典
 
- 删除是否可以降低内存

    可以。

    字典会在删除数据时，也会降低整个程序的内存占用，大概能降低一半，但是字典那个变量所占用的内存大小是不变化的，所以整个程序的内存下降并不多
    
    平衡二叉树的实现，在删除所有数据后，内存占用能回到初始值。
