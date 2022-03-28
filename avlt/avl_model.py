import mvc_base.model_double_child as mdc
from core.constants import green
from core.constants import left, right


class AVLTNode(mdc.DCNode):
    color = green

    def __init__(self, value, x, y, tree, l_edge=None, r_edge=None, parent=None):
        super().__init__(value, x, y, tree, l_edge, r_edge, parent)
        self.height = 1

    # Node derived methods override

    def insert_value(self, value):
        """Additionally updates height of self node"""
        newNode = super().insert_value(value)
        self.tree.view.draw_exp_text(newNode, f'Insert node ({newNode.value})', False)
        self.height = 1 + max(self.left.height, self.right.height)
        return newNode

    def delete_value(self, value):
        super().delete_value(value)
        self.fix_delete()
        self.tree.view.animate(self.tree.root)
        self.tree.view.explanation.append(f'Deletion finished')
        if type(self.tree.root) is mdc.DCLeaf:
            self.tree.clear()

    # DCNode derived methods override

    def fix_insert(self, value=None):
        """
        Fixes the AVL subtree after the insertion process. Starts in self
        :param value: value that was inserted
        :return: returns nothing
        """
        self.height = 1 + max(self.left.height, self.right.height)
        balance = self.get_balance()
        if balance > 1 and type(self.left) is AVLTNode and value < self.left.value:
            self.tree.view.draw_exp_text(self, f'Balance of ({self.value}) = {balance}')
            self.rotate(right)
        if balance < -1 and type(self.right) is AVLTNode and value > self.right.value:
            self.tree.view.draw_exp_text(self, f'Balance of ({self.value}) = {balance}')
            self.rotate(left)
        if balance > 1 and type(self.left) is AVLTNode and value > self.left.value:
            self.tree.view.draw_exp_text(self, f'Balance of ({self.value}) = {balance}')
            self.left.rotate(left)
            self.rotate(right)
        if balance < -1 and type(self.right) is AVLTNode and value < self.right.value:
            self.tree.view.draw_exp_text(self, f'Balance of ({self.value}) = {balance}')
            self.right.rotate(right)
            self.rotate(left)
        if self.parent is not None:
            self.parent.fix_insert(value)

    def fix_delete(self):
        """
        Fixes the AVL tree constraints in node subtree after the deletion process
        :node: node to start fixing process
        :return: returns nothing
        """
        self.height = 1 + max(self.left.height, self.right.height)
        balance = self.get_balance()
        if balance > 1 and type(self.left) is AVLTNode and self.left.get_balance() >= 0:
            self.rotate(right)
        if balance < -1 and type(self.right) is AVLTNode and self.right.get_balance() <= 0:
            self.rotate(left)
        if balance > 1 and type(self.left) is AVLTNode and self.left.get_balance() < 0:
            self.left.rotate(left)
            self.rotate(right)
        if balance < -1 and type(self.right) is AVLTNode and self.right.get_balance() > 0:
            self.right.rotate(right)
            self.rotate(left)
        if self.parent is not None:
            self.parent.fix_delete()

    def rotate(self, side):
        """Additionally updates height, performs rotations in GUI and returns node which is now the root of subtree"""
        y = super().rotate(side)
        self.height = 1 + max(self.left.height, self.right.height)
        y.height = 1 + max(y.left.height, y.right.height)
        self.tree.root.update_positions()
        self.tree.view.animate(y)
        return y

    # AVLTNode specific methods

    def get_balance(self):
        return self.left.height - self.right.height


class AVLTree(mdc.DCTree):
    node_class = AVLTNode

    # DCTree derived methods override

    def insert_value(self, value):
        if self.root is None:
            self.root = AVLTNode(value, self.view.width // 2, self.view.y_space, self, 0, self.view.width)
            self.view.explanation.append(f'Tree is empty. Insert node ({value})')
        else:
            self.insert_value_helper(value)
            self.view.draw_exp_text(self.root, f'Recalculate height for all nodes')

    def delete_value(self, value):
        """ Additionally draws explanation text for recalculation"""
        if self.root is None:
            self.view.explanation.append(f'Tree is empty. Impossible to delete from an empty tree')
        else:
            self.root.delete_value(value)
            self.view.draw_exp_text(self.root, f'Recalculate height for all nodes')
