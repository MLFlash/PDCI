'''
Created on 08-Oct-2019

@author: akash
'''
from classes.Node import Node


class AVLTree():
    def __init__(self):
        self.root = None

    def insert(self, proj, point, currentNode=None):
        '''
        Inserts a node into the subtree rooted at this node.

        Args:
            currentNode: The node to be inserted.
            proj: Projection of a point onto unit vector
            point: Query Point
        Time Complexity: O(log(n))
        '''
        if self.root == None:
            self.root = Node(proj, point)
            return

        if proj < currentNode.proj:
            if currentNode.left is None:
                currentNode.left = Node(proj, point, parent=currentNode)
                self.update_balance(currentNode.left)
            else:
                self.insert(proj, point, currentNode.left)

        elif proj > currentNode.proj:
            if currentNode.right is None:
                currentNode.right = Node(proj, point, parent=currentNode)
                self.update_balance(currentNode.right)

            else:
                self.insert(proj, point, currentNode.right)

        else:
            currentNode.points.append(point)

    def update_balance(self, node):
        '''
        Time Complexity: O(log(n))
        '''
        if node.height < -1 or node.height > 1:
            self.rebalance(node)
            return
        if node.parent != None:
            if node.is_left():
                node.parent.height += 1
            elif node.is_right():
                node.parent.height -= 1
            if node.parent.height != 0:
                self.update_balance(node.parent)

    def rebalance(self, node):
        '''
        Time Complexity: O(C)
        If tree is out of balance (it's left and right subtrees height differ by more than abs(1)), than we need to rebalance it.
        Balancing is done by single left or right rotations or with double left or right rotations of the tree.
        '''
        if node.height < 0:
            if node.right.height > 0:
                self.right_rotate(node.right)
                self.left_rotate(node)
            else:
                self.left_rotate(node)
        elif node.height > 0:
            if node.left.height < 0:
                self.left_rotate(node.left)
                self.right_rotate(node)
            else:
                self.right_rotate(node)
    '''
    Rotation
    Tree can be rotated left or right.
    With left rotation, right subtree root replaces current root. With right rotation, left subtree replaces current root.
    '''

    def left_rotate(self, old_root):
        '''
        Time Complexity: O(C)
        '''
        new_root = old_root.right

        old_root.right = new_root.left
        if new_root.left != None:
            new_root.left.parent = old_root

        new_root.parent = old_root.parent

        if old_root.is_root():
            self.root = new_root
        else:
            if old_root.is_left():
                old_root.parent.left = new_root
            else:
                old_root.parent.right = new_root

        new_root.left = old_root
        old_root.parent = new_root

        old_root.height = old_root.height + 1 - min(new_root.height, 0)
        new_root.height = new_root.height + 1 + max(old_root.height, 0)

    def right_rotate(self, old_root):
        '''
        Time Complexity: O(C)
        '''
        new_root = old_root.left

        old_root.left = new_root.right
        if new_root.right != None:
            new_root.right.parent = old_root

        new_root.parent = old_root.parent

        if old_root.is_root():
            self.root = new_root
        else:
            if old_root.is_left():
                old_root.parent.left = new_root
            else:
                old_root.parent.right = new_root

        new_root.right = old_root
        old_root.parent = new_root

        old_root.height = old_root.height - 1 - max(new_root.height, 0)
        new_root.height = new_root.height - 1 - min(old_root.height, 0)

    def predecessor(self, root, pred, proj):
        '''
        Time Complexity: O(log(n))
        '''
        if root is None:
            return None
        if proj < root.proj:
            if root.has_left():
                return self.predecessor(root.left, pred, proj)
            else:
                return pred
        elif proj == root.proj:
            if root.has_left():
                pred = self.maximum(root.left)
            return pred
        else:
            if root.has_right():
                pred = root
                return self.predecessor(root.right, pred, proj)
            else:
                return root

    def maximum(self, root):
        '''
        Time Complexity: O(log(n))
        '''
        while root.has_right():
            root = root.right
        return root

    def successor(self, root, succ, proj):
        '''
        Returns the node that contains the successor proj 

        Args:
            proj: Projection onto the unit vector

        Returns:
            The successor node.

        Time Complexity: O(log(n))
        '''
        if root is None:
            return None
        if proj < root.proj:
            if root.has_left():
                succ = root
                return self.successor(root.left, succ, proj)
            else:
                return root
        elif proj == root.proj:
            if root.has_right():
                succ = self.minimum(root.right)
            return succ
        else:
            if root.has_right():
                return self.successor(root.right, succ, proj)
            else:
                return succ

    def minimum(self, root):
        '''
        Time Complexity: O(log(n))
        '''
        while root.has_left():
            root = root.left
        return root

    def closer(self, pred, succ, proj):
        '''
        Time Complexity: O(C)
        '''
        if abs(pred.proj - proj) < abs(succ.proj - proj):
            return [pred, succ]
        elif abs(pred.proj - proj) > abs(succ.proj - proj):
            return [succ, pred]
        else:
            return [pred, succ]

    def search(self, current_node, proj):
        '''
        Time Complexity: O(log(n))
        '''
        if self.root is None:
            return None
        if proj < current_node.proj:
            if current_node.has_left():
                return self.search(current_node.left, proj)
            else:
                return None
        elif proj > current_node.proj:
            if current_node.has_right():
                return self.search(current_node.right, proj)
            else:
                return None
        else:
            return current_node

    def sort_tree(self, proj, n):
        '''
        Given a projection of a point, sort avl tree, return a list of nodes.
        closest = [node1, node2, ..., node3]
        '''
        if self.root is None:
            return None
        closest = []
        node = self.search(self.root, proj)
        pred = self.predecessor(self.root, None, proj)
        succ = self.successor(self.root, None, proj)
        if node is not None:
            closest += [node]
        while len(closest) < n:
            if pred is not None and succ is not None:
                closest += self.closer(pred, succ, proj)
            elif pred is not None and succ is None:
                closest += [pred]
            elif pred is None and succ is not None:
                closest += [succ]
            else:
                pass
            if pred is not None:
                pred = self.predecessor(self.root, None, pred.proj)
            if succ is not None:
                succ = self.successor(self.root, None, succ.proj)
        return closest
