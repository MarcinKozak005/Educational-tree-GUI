import copy

import core.root as r
import mvc_base.model_double_child as mdc
from core.constants import left, right, red, black, recolor_txt


class RBTNode(mdc.DCNode):
    def __init__(self, value, x, y, tree, l_edge=None, r_edge=None, parent=None):
        super().__init__(value, x, y, tree, l_edge, r_edge, parent)
        self.color = red

    # Node derived methods override

    def delete_value(self, value):
        view = self.tree.view
        x, y = super().delete_value(value)
        if y is not None and x is not None and y.color == black:
            self.fix_delete(x)
            view.animate(self.tree.root)
            view.draw_recolor_text(x, black)
            r.wait(view.long_animation_time)
            view.erase(recolor_txt)
        view.explanation.append(f'Deletion finished')
        if type(self.tree.root) is mdc.DCLeaf:
            self.tree.clear()

    # DCNode derived methods override

    def fix_insert(self, value=None):
        """
        Fixes the red-black subtree after the insertion process. Starts in self
        :param value: unused in this implementation
        :return: returns nothing
        """
        node = self
        view = self.tree.view

        def fix_insert_subpart(n, side):
            """
            fix_insert(self) subpart which is dependent on the side
            :param n: node to start the fixing subprocess
            :param side: string: 'left' or 'right'
            :return: node to continue fixing process
            """
            uncle = n.parent.parent[right if side == left else left]
            if uncle.color == red:
                n.parent.color = black
                uncle.color = black
                n.parent.parent.color = red
                view.draw_recolor_text(n.parent, black)
                view.draw_recolor_text(uncle, black)
                view.draw_recolor_text(n.parent.parent, red)
                r.wait(view.long_animation_time)
                view.draw_object(n.parent)
                view.draw_object(uncle)
                view.draw_object(n.parent.parent)
                view.erase(recolor_txt)
                return n.parent.parent
            elif n == n.parent[right if side == left else left]:
                n = n.parent
                n.rotate(side)
            elif n is not self.tree.root and n.parent is not self.tree.root:
                n.parent.color = black
                n.parent.parent.color = red
                tmp_node1, tmp_node2 = n.parent, n.parent.parent
                n.parent.parent.rotate(right if side == left else left)
                view.draw_recolor_text(tmp_node1, black)
                view.draw_recolor_text(tmp_node2, red)
                r.wait(view.long_animation_time)
                view.draw_object(tmp_node1)
                view.draw_object(tmp_node2)
                view.erase(recolor_txt)
            return n

        # fix_insert
        while node is not self.tree.root and node.parent.color == red:
            if node.parent == node.parent.parent.left:
                node = fix_insert_subpart(node, left)
            else:
                node = fix_insert_subpart(node, right)
        if self.tree.root.color != black:
            view.draw_recolor_text(self.tree.root, black)
            r.wait(view.long_animation_time)
        self.tree.root.color = black

    def fix_delete(self, node=None):  # node=None to suppress warning
        """
        Fixes the red-black tree constraints in node subtree after the deletion process
        :node: node to start fixing process
        :return: returns nothing
        """

        def fix_delete_subpart(n, side):
            """
            fix_delete(self) subpart which is dependent on the side
            :param n: node to start the fixing subprocess
            :param side: string: 'left' or 'right'
            :return: node to continue fixing process
            """
            snd_side = left if side == right else right
            sibling = n.parent[side]
            non_exception_case1 = True  # Turned out to be needed. I haven't tested all cases
            non_exception_case2 = False  # Consequence of the above
            if type(sibling) is not mdc.DCLeaf and sibling.color == red:
                sibling.color = black
                n.parent.color = red
                tmp_node1, tmp_node2 = sibling, n.parent
                n.parent.rotate(snd_side)
                view.draw_recolor_text(tmp_node1, black)
                view.draw_recolor_text(tmp_node2, red)
                r.wait(view.long_animation_time)
                view.draw_object(tmp_node1)
                view.draw_object(tmp_node2)
                view.erase(recolor_txt)
                sibling = n.parent[side]
            if type(sibling) is not mdc.DCLeaf and sibling[snd_side].color == black and sibling[side].color == black:
                sibling.color = red
                view.draw_recolor_text(sibling, red)
                r.wait(view.long_animation_time)
                view.draw_object(sibling)
                view.erase(recolor_txt)
                n = n.parent
                non_exception_case1 = False
            elif type(sibling) is not mdc.DCLeaf and sibling[side].color == black:
                sibling[snd_side].color = black
                sibling.color = red
                tmp_node1, tmp_node2 = sibling[snd_side], sibling
                sibling.rotate(side)
                view.draw_recolor_text(tmp_node1, black)
                view.draw_recolor_text(tmp_node2, red)
                r.wait(view.long_animation_time)
                view.draw_object(tmp_node1)
                view.draw_object(tmp_node2)
                view.erase(recolor_txt)
                sibling = n.parent[side]
                non_exception_case2 = True
            if n is not self.tree.root and non_exception_case1:
                sibling.color = n.parent.color
                n.parent.color = black
                sibling[side].color = black
                tmp_node1, tmp_node2, tmp_node3 = sibling, n.parent, sibling[side]
                if n.parent is not self.tree.root or (n.parent is self.tree.root and type(n) is mdc.DCLeaf) \
                        or non_exception_case2:
                    n.parent.rotate(snd_side)
                view.draw_recolor_text(tmp_node1, n.parent.color)
                view.draw_recolor_text(tmp_node2, black)
                view.draw_recolor_text(tmp_node3, black)
                r.wait(view.long_animation_time)
                view.draw_object(tmp_node1)
                view.draw_object(tmp_node2)
                view.draw_object(tmp_node3)
                view.erase(recolor_txt)
                n = self.tree.root
            return n

        # fix_delete
        view = self.tree.view
        while node is not self.tree.root and node.color == black:
            if node == node.parent.left:
                node = fix_delete_subpart(node, right)
            else:
                node = fix_delete_subpart(node, left)
        view.draw_recolor_text(node, black)
        node.color = black

    def rotate(self, side):
        """Additionally performs rotations in GUI"""
        y = super().rotate(side)
        self.tree.root.update_positions()
        self.tree.view.animate(y)


class RBTree(mdc.DCTree):
    node_class = RBTNode

    def __deepcopy__(self, memo):
        cp = RBTree(self.view)
        cp.root = copy.deepcopy(self.root, memo)
        return cp

    # DCTree derived methods override

    def insert_value(self, value):
        if self.root is None:
            self.root = RBTNode(value, self.view.width // 2, self.view.y_space, self, 0, self.view.width)
            self.root.color = black
            self.view.explanation.append(f'Tree is empty. Insert black node ({value})')
        else:
            self.insert_value_helper(value)
