"""

Project:    AVLTree
Author:     LanHao
Date:       2020/9/11
Python:     python3.6

"""

import abc
import logging
from typing import List


class NotSameInstanceException(Exception):
    def __init__(self, *args):
        self.args = args


class CustomDict(abc.ABC):
    """

    """

    @abc.abstractmethod
    def __getitem__(self, item):
        pass

    @abc.abstractmethod
    def __delitem__(self, key):
        pass

    @abc.abstractmethod
    def keys(self):
        pass

    @abc.abstractmethod
    def __setitem__(self, key, value):
        pass


class Data(object):
    """
    打包键值对,允许根据key 做比较判断
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return f"{self.key}"

    # 比较相关
    def __eq__(self, other):
        """
        ==
        :param other:
        :return:
        """
        if isinstance(other, Data):
            return self.key == other.key
        else:
            return self.key == other

    def __ne__(self, other):
        """
        !=
        :param other:
        :return:
        """

        if isinstance(other, Data):
            return self.key != other.key
        else:
            return self.key != other

    def __lt__(self, other):
        """
        <
        :param other:
        :return:
        """

        if isinstance(other, Data):
            return self.key < other.key
        else:
            return self.key < other

    def __gt__(self, other):

        if isinstance(other, Data):
            return self.key > other.key
        else:
            return self.key > other

    def __le__(self, other):
        if isinstance(other, Data):
            return self.key <= other.key
        else:
            return self.key <= other

    def __ge__(self, other):

        if isinstance(other, Data):
            return self.key >= other.key
        else:
            return self.key >= other


class BaseNode(object):
    """

    定义树的节点,简要使用

    """

    def __init__(self, data):
        self.data = data
        self.left: BaseNode = None
        self.right: BaseNode = None

    @property
    def Data(self):
        return self.data

    @Data.setter
    def Data(self, value):
        self.data = value

    @property
    def Left(self) -> "BaseNode":
        return self.left

    @Left.setter
    def Left(self, value):
        self.left = value

    @property
    def Right(self):
        return self.right

    @Right.setter
    def Right(self, value):
        self.right = value

    # 比较相关
    def __eq__(self, other):
        """
        ==
        :param other:
        :return:
        """
        if isinstance(other, BaseNode):
            return self.data == other.data
        else:
            return self.data == other

    def __ne__(self, other):
        """
        !=
        :param other:
        :return:
        """

        if isinstance(other, BaseNode):
            return self.data != other.data
        else:
            return self.data != other

    def __lt__(self, other):
        """
        <
        :param other:
        :return:
        """
        if isinstance(other, BaseNode):
            return self.data < other.data
        else:
            return self.data < other

    def __gt__(self, other):
        if isinstance(other, BaseNode):
            return self.data > other.data
        else:
            return self.data > other

    def __le__(self, other):
        if isinstance(other, BaseNode):
            return self.data <= other.data
        else:
            return self.data <= other

    def __ge__(self, other):
        if isinstance(other, BaseNode):
            return self.data >= other.data
        else:
            return self.data >= other

    def __str__(self):
        return f"key:{self.Data.key},value:{self.Data.value}"


class AVLNode(BaseNode):
    """
    平衡二叉树中使用的节点性质
    """

    def __init__(self, data):
        self.depth = 1  # 缓存使用,不能真实表示此树的实际高度
        self.balance = 0
        self.parent = None

        super(AVLNode, self).__init__(data)

    @property
    def Depth(self):
        return self.depth

    @Depth.setter
    def Depth(self, value):
        self.depth = value

    @property
    def Balance(self):
        return self.balance

    @Balance.setter
    def Balance(self, value):
        self.balance = value

    @property
    def Parent(self):
        return self.parent

    @Parent.setter
    def Parent(self, value):
        self.parent = value

    def __str__(self):
        return f"Node: [data:{self.Data},depth:{self.Depth},balance:{self.Balance}]"


class AVLTree(CustomDict):
    def __init__(self):
        self.head: AVLNode = None
        super(AVLTree, self).__init__()

    def _get_node(self, key) -> AVLNode:
        node_back = None
        node_now = self.head
        while node_now:
            if key == node_now:
                node_back = node_now
                break
            else:
                if key < node_now:
                    node_now = node_now.left
                else:
                    node_now = node_now.right

        return node_back

    def __getitem__(self, item):

        value = None
        node: AVLNode = self._get_node(item)
        if node:
            data: Data = node.Data
            value = data.value
        return value

    def __setitem__(self, key, value):
        key_value = Data(key, value)
        self._insert(key_value)
        # 以上仅实现了添加,但是没有平衡判断旋转判断

    def __delitem__(self, key):
        # 如何移除这个元素呢？
        node: AVLNode = self._get_node(key)
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
                    right_node.Parent = stack_left_min # 建立两者之间关系
            else:
                left_node = right_node

            if parent:
                if parent.Right==node:
                    parent.Right = left_node
                else:
                    parent.Left = left_node
                if left_node:
                    left_node.Parent = parent
            else:
                logging.warning(f"删除:{node}")
                self.head = left_node
                if self.head:
                    self.head.Parent = None

            # 以上仅能满足按序排列的二叉树
            del node
            if right_node:
                self._update_after_insert(right_node)
            else:
                if left_node:
                    self._update_after_insert(left_node.Parent)
        else:
            logging.warning(f"删除空node：{key}")

    def mid_sort(self):
        """
        中旬遍历
        :return:
        """
        if self.head is not None:  # 中序遍历输出数据
            stack_cache = [self.head]
            while stack_cache:
                while stack_cache[-1].Left is not None:
                    stack_cache.append(stack_cache[-1].Left)

                while stack_cache:
                    node = stack_cache.pop()
                    logging.debug(f"value:{node.Data},left:{node.Left},right:{node.Right}")
                    yield node
                    if node.right is not None:
                        stack_cache.append(node.Right)
                        break

    def keys(self):
        """
        中序遍历
        :return:
        """
        for node in self.mid_sort():
            node: AVLNode
            data: Data = node.Data
            yield data.key

    def __str__(self):
        """
        尝试以中序遍历,输出所有的数据
        :return:
        """
        str_list_back = [f"AVLDict id {id(self)}:"]

        for node in self.mid_sort():
            str_list_back.append(str(node))

        str_list_back.append("End")

        return "\r\n".join(str_list_back)

    # 关于旋转和更新的

    def _insert(self, key_value):

        node_insert = AVLNode(key_value)

        if self.head is None:
            self.head = node_insert
        else:
            node_now = self.head  # 尽量不用递归来判断
            while node_now:
                if key_value < node_now.Data:
                    if node_now.left is None:
                        node_now.left = node_insert
                        node_insert.Parent = node_now
                        break
                    else:
                        node_now = node_now.left  # 递归去寻找
                elif key_value > node_now.Data:
                    if node_now.right is None:
                        node_now.right = node_insert
                        node_insert.Parent = node_now
                        break
                    else:
                        node_now = node_now.right
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

    def _rotate(self, node: AVLNode):
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

    def _right_rotate(self, node: AVLNode):
        """
        右旋,left不可能为空
        :param node:
        :return:
        """

        logging.debug(
            f"右旋前: {node},depth:{node.Depth},balance:{node.Balance},left:{node.Left},right:{node.Right},parent:{node.Parent}")

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
            self.head = left
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

    def _left_rotate(self, node: AVLNode):
        """
        左旋,right 不可为空
        :param node:
        :return:
        """
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
            self.head = right
        right.Parent = parent  # 建立上位节点到父节点的单向关系

        node.Right = right.Left  # 建立被替代节点到上位节点left 之间的单向关系
        if right.Left:
            right.Left.Parent = node  # 建立上位节点left 到被替代节点之间的单向关系

        node.Parent = right  # 建立被替换节点到上位节点之间的单向关系
        right.Left = node  # 建立上位节点到被替代节点之间的单向关系

        self._update_single_node(node)
        if node.Parent:
            self._update_single_node(node.Parent)

    def _update_single_node(self, node: AVLNode):

        if node:
            left_depth = 0
            right_depth = 0
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

    def _update_after_insert(self, nodein: AVLNode):
        """
        追着此节点node 往上一直更新到根节点
        :param node:
        :return:
        """

        node = nodein
        while node:
            self._update_single_node(node)
            node = node.Parent
