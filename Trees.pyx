# cython: language_level=3

import logging

cdef class KeyValue:
    """
    key value 存放，用于节点中间存放
    """
    cdef public Key
    cdef public Value

    def __init__(self, key, value):
        self.Key = key
        self.Value = value

    def __str__(self):
        return f"{self.Key}:{self.Value}"

    # 比较相关
    def __eq__(self, other):
        """
        ==
        :param other:
        :return:
        """
        if isinstance(other, KeyValue):
            return self.Key == other.Key
        else:
            return self.Key == other

    def __ne__(self, other):
        """
        !=
        :param other:
        :return:
        """

        if isinstance(other, KeyValue):
            return self.Key != other.Key
        else:
            return self.Key != other

    def __lt__(self, other):
        """
        <
        :param other:
        :return:
        """

        if isinstance(other, KeyValue):
            return self.Key < other.Key
        else:
            return self.Key < other

    def __gt__(self, other):

        if isinstance(other, KeyValue):
            return self.Key > other.Key
        else:
            return self.Key > other

    def __le__(self, other):
        if isinstance(other, KeyValue):
            return self.Key <= other.Key
        else:
            return self.Key <= other

    def __ge__(self, other):

        if isinstance(other, KeyValue):
            return self.Key >= other.Key
        else:
            return self.Key >= other

cdef class BaseNode:
    """
    基础的节点信息
    """
    cdef public KeyValue Data
    cdef public BaseNode Left
    cdef public BaseNode Right

    def __init__(self, KeyValue data):
        self.Data = data
        self.Left = None
        self.Right = None

    # 比较相关
    def __eq__(self, other):
        """
        ==
        :param other:
        :return:
        """
        if isinstance(other, BaseNode):
            return self.Data == other.Data
        else:
            return self.Data == other

    def __ne__(self, other):
        """
        !=
        :param other:
        :return:
        """

        if isinstance(other, BaseNode):
            return self.Data != other.Data
        else:
            return self.Data != other

    def __lt__(self, other):
        """
        <
        :param other:
        :return:
        """
        if isinstance(other, BaseNode):
            return self.Data < other.Data
        else:
            return self.Data < other

    def __gt__(self, other):
        if isinstance(other, BaseNode):
            return self.Data > other.Data
        else:
            return self.Data > other

    def __le__(self, other):
        if isinstance(other, BaseNode):
            return self.Data <= other.Data
        else:
            return self.Data <= other

    def __ge__(self, other):
        if isinstance(other, BaseNode):
            return self.Data >= other.Data
        else:
            return self.Data >= other

    def __str__(self):
        return f"key:{self.Data.key},value:{self.Data.value}"

cdef class AVLNode(BaseNode):
    """
    自平衡二叉树的节点
    """
    cdef public int Depth
    cdef public int Balance
    cdef public AVLNode Parent

    def __init__(self, KeyValue data):
        self.Depth = 1
        self.Balance = 0
        self.Parent = None
        super(AVLNode, self).__init__(data)

    def __str__(self):
        return f"AVLNode: [data:{self.Data},depth:{self.Depth},balance:{self.Balance}]"

cdef class AVLTree:
    """
    自平衡二叉树具体实现
    """
    cdef public AVLNode Head

    def __init__(self):
        self.Head = None
        super(AVLTree, self).__init__()

    cdef AVLNode  _get_node(self, key):
        """
        通过key 检索节点
        :param key: 
        :return: 
        """

        cpdef AVLNode node_back, node_now

        node_back = None  # 赋予默认值
        node_now = self.Head

        while node_now:
            if key == node_now:
                node_back = node_now
                break
            else:
                if key < node_now:
                    node_now = node_now.Left
                else:
                    node_now = node_now.Right

        return node_back

    def __getitem__(self, item):
        """
        提供类字典的访问方法
        :param item:
        :return:
        """
        cdef KeyValue data = None

        value = None
        cdef AVLNode node = self._get_node(item)
        if node:
            data = node.Data
        if data:
            value = data.Value

        return value

    cpdef pop(self, key):
        """
        从整颗树中提取pop 出指定key 的节点
        :param key: 
        :return: 
        """
        cdef AVLNode node = self._get_node(key)
        cdef KeyValue  data = node.Data

        if node:
            self._delete_itemm(node)  # 从树中删除操作
            return data.Value
        return None

    def __setitem__(self, key, value):
        cdef KeyValue key_value = KeyValue(key, value)
        self._insert(key_value)
        # 以上仅实现了添加,但是没有平衡判断旋转判断

    cdef void _insert(self, KeyValue key_value):

        cpdef AVLNode node_insert = AVLNode(key_value)

        if self.Head is None:
            self.Head = node_insert
        else:
            node_now = self.Head  # 尽量不用递归来判断
            while node_now:
                if key_value < node_now.Data:
                    if node_now.Left is None:
                        node_now.Left = node_insert
                        node_insert.Parent = node_now
                        break
                    else:
                        node_now = node_now.Left  # 递归去寻找
                elif key_value > node_now.Data:
                    if node_now.Right is None:
                        node_now.Right = node_insert
                        node_insert.Parent = node_now
                        break
                    else:
                        node_now = node_now.Right
                else:
                    node_now.Data = key_value  # 覆盖值但是不覆盖这个节点对象
                    break

        self._update_after_insert(node_insert)  # 只需要更新这条记录对应的数据父节点以及父父节点等
        logging.debug(f"insert result :{node_insert}")
        node_tmp = node_insert
        while node_tmp:
            logging.debug(
                f"更新前node: {node_tmp},depth:{node_tmp.Depth},balance:{node_tmp.Balance},left:{node_tmp.Left},right:{node_tmp.Right},parent:{node_tmp.Parent}")
            self._rotate(node_tmp)
            logging.debug(
                f"更新后node: {node_tmp},depth:{node_tmp.Depth},balance:{node_tmp.Balance},left:{node_tmp.Left},right:{node_tmp.Right},parent:{node_tmp.Parent}")
            node_tmp = node_tmp.Parent  # 依次往上类推,找到我们需要的旋转的节点,未被改动的部分,逻辑上是不需要旋转变化的

    cdef void _update_after_insert(self, AVLNode nodein):
        """
        追着此节点node 往上一直更新到根节点
        :param node:
        :return:
        """

        cpdef AVLNode node = nodein

        while node:
            self._update_single_node(node)
            node = node.Parent

    cdef void _update_single_node(self, AVLNode node):
        cdef int left_depth,right_depth
        left_depth = 0
        right_depth = 0
        cdef AVLNode left_node,right_node

        if node:
            left_node = node.Left
            right_node = node.Right

            if left_node:
                left_depth = left_node.Depth
            if right_node:
                right_depth = right_node.Depth

            node.Depth = max(left_depth, right_depth) + 1
            node.Balance = left_depth - right_depth
        else:
            logging.warning(f"尝试更新一个NoneType 类型作为Node")

    cdef void _rotate(self, AVLNode node):
        """
        主动控制旋转 
        :param node:
        :return:
        """

        logging.debug(f"检查平衡状态:{node}")
        if node.Balance >= 2:
            if node.Left.Balance == -1:
                logging.debug("但是需要先左旋")
                self._left_rotate(node.Left)
            self._right_rotate(node)
        if node.Balance <= -2:
            logging.debug(f"需要左旋：{node}")
            if node.Right and node.Right.Balance == 1:
                logging.debug("但是需要先右旋")
                self._right_rotate(node.Right)
            self._left_rotate(node)

    cdef void _left_rotate(self, AVLNode node):
        """
        左旋,right 不可为空
        :param node:
        :return:
        """
        cdef AVLNode left,right,parent

        logging.debug(f"即将发生左旋节点：{node}")
        left = node.Left
        right = node.Right
        parent = node.Parent

        assert right is not None, Exception("左旋 right 不可为空")

        # 改变三组位置关系
        if parent:  # 建立父节点到上位节点的单向位置关系
            if parent.Left is node:
                parent.Left = right
            else:
                parent.Right = right
        else:
            self.Head = right
        right.Parent = parent  # 建立上位节点到父节点的单向关系

        node.Right = right.Left  # 建立被替代节点到上位节点left 之间的单向关系
        if right.Left:
            right.Left.Parent = node  # 建立上位节点left 到被替代节点之间的单向关系

        node.Parent = right  # 建立被替换节点到上位节点之间的单向关系
        right.Left = node  # 建立上位节点到被替代节点之间的单向关系

        self._update_single_node(node)
        if node.Parent:
            self._update_single_node(node.Parent)

    def __str__(self):
        """
        尝试以中序遍历,输出所有的数据
        :return:
        """
        str_list_back = [f"AVLDict id {id(self)}:"]
        if self.Head:
            stack_cache = [self.Head]
            while stack_cache:
                while stack_cache[-1].Left is not None:
                    stack_cache.append(stack_cache[-1].Left)
                while stack_cache:
                    node = stack_cache.pop()
                    str_list_back.append(str(node))
                    if node.Right is not None:
                        stack_cache.append(node.Right)
                        break

        str_list_back.append("End")

        return "\r\n".join(str_list_back)

    cpdef void _delete_itemm(self, AVLNode node):
        cdef AVLNode left_node, right_node, parent, stack_left_min

        if node:
            left_node = node.Left
            right_node = node.Right
            parent = node.Parent
            node.Left = None
            node.Right = None
            node.Parent = None
            if left_node:
                stack_left_min = left_node
                while stack_left_min.Left:
                    stack_left_min = stack_left_min.Left
                stack_left_min.Left = right_node
                if right_node:
                    right_node.Parent = stack_left_min  # 建立两者之间关系
            else:
                left_node = right_node

            if parent:
                if parent.Right == node:
                    parent.Right = left_node
                else:
                    parent.Left = left_node
                if left_node:
                    left_node.Parent = parent
            else:
                logging.debug(f"删除:{node}")
                self.Head = left_node
                if self.Head:
                    self.Head.Parent = None

            # 以上仅能满足按序排列的二叉树
            del node
            if right_node:
                self._update_after_insert(right_node)
            else:
                if left_node:
                    self._update_after_insert(left_node.Parent)

    def __delitem__(self, key):
        # 如何移除这个元素呢？
        cdef AVLNode node = self._get_node(key)
        if node:
            self._delete_itemm(node)

    cdef void _right_rotate(self, AVLNode node):
        """
        右旋,left不可能为空
        :param node:
        :return:
        """

        logging.debug(
            f"右旋前: {node},depth:{node.Depth},balance:{node.Balance},left:{node.Left},right:{node.Right},parent:{node.Parent}")
        cdef AVLNode left, right, parent

        left = node.Left  # 将顶替node 位置的存在
        right = node.Right  # 一直保持在node 的right 分支，
        parent = node.Parent  # 如果为空,将需要额外的处理
        assert left is not None, Exception(
            f"右旋时，节点左侧需要存在值,node:{node},data:{node.Data},left:{node.Left},right:{node.Right},Parent:{node.Parent}")

        # 需要改变三组关系
        if parent:  # 建立父节点到上位节点的单向关系
            if parent.Left is node:
                parent.Left = left
            else:
                parent.Right = left
        else:
            self.Head = left
        left.Parent = parent  # 建立上位节点到父节点的单向关系

        node.Left = left.Right  # 建立被替代节点到上位节点right 的单向关系
        if left.Right:
            left.Right.Parent = node  # 建立上位节点right 到被替代节点的单向单向关系

        node.Parent = left  # 建立 被替代节点到上位节点的单向关系
        left.Right = node  # 建立上位节点到被替代节点的单向关系

        self._update_single_node(node)  # 更新单个node 的值

        if node.Parent:
            self._update_single_node(node.Parent)

        logging.debug(
            f"右旋后: {node},depth:{node.Depth},balance:{node.Balance},left:{node.Left},right:{node.Right},parent:{node.Parent}")
