import math
import statistics

import mvc_base.model_balanced as mb
from core.constants import hint_frame


class BPTNode(mb.BalNode):
    class_node_id = ord('@')  # distinguishes nodes by using letters

    def delete_value(self, value):
        values = [self.values[i].value for i in range(len(self.values))]
        view = self.tree.view
        # Search for a value to delete
        if not self.is_leaf:
            i = 0
            while i < len(self.values) and value >= self.values[i].value:
                i += 1
            self.children[i].delete_value(value)
        # Value found (in leaf node)
        elif self.is_leaf and value in values:
            i = values.index(value)
            removed_node = self.values.pop(i)
            view.draw_exp_text(removed_node, f'Remove value {removed_node.value}')
            view.move_object(removed_node.tag(), removed_node.x, removed_node.y, removed_node.x, -view.node_height)
            self.fix_delete(value)
        # Fixing indexes' (inner nodes) values
        parent = self.parent
        if parent is not None:
            values = [parent.values[i].value for i in range(len(parent.values))]
            if value in values:
                i = values.index(value)
                view.draw_exp_text(parent.values[i], f'Change value ({parent.values[i].value}) '
                                                     f'in node [{parent.id}] to successor of it\'s right child')
                parent.values[i].value = self.successor(False)

    def search_value(self, value):
        """
        Searches for value in the node
        :param value: searched value
        :return: if found: tuple (node_with_value, position_of_value_in_node), else: None
        """
        i = 0
        view = self.tree.view
        view.hint_frame.draw(self.values[0].x, self.values[0].y)
        # Find first not smaller value in node
        while i < len(self.values) and value > self.values[i].value:
            view.draw_exp_text(self.values[i], f'[{self.id}]: {value} > {self.values[i].value}, check next value',
                               False)
            view.hint_frame.move(self.values[i].x + view.node_width, self.values[i].y, True)
            i += 1
        # The value is found
        if i < len(self.values) and self.is_leaf and value == self.values[i].value:
            view.draw_exp_text(self, f'Value {value} found in node [{self.id}] in place {i}')
            view.erase(hint_frame)
            return self, i
        # Not found strings
        if self.is_leaf:
            exp_string = f'No more values.' if i >= len(self.values) else f'{value} < {self.values[i].value}.'
            view.draw_exp_text(self, f'[{self.id}]: {exp_string}  [{self.id}] is a leaf. Value {value} not found')
            view.erase(hint_frame)
            return None
        # Search in child
        else:
            # Show appropriate explanation string
            if i < len(self.values):
                condition = value < self.values[i].value
                sign = '<' if condition else '=='
                equal_case = '' if condition else '. But it\'s index not value'
                view.draw_exp_text(self.values[i], f'[{self.id}]: {value} {sign} {self.values[i].value}{equal_case}',
                                   False)
                i = i if condition else i + 1
            else:
                view.draw_exp_text(self, f'[{self.id}] No next value.', False)
            if i != 0:
                view.hint_frame.move(self.values[i - 1].x + view.node_width // 2, self.values[i - 1].y, True)
                view.draw_exp_text(self, f'Search in [{self.children[i].id}]', False)
            else:
                view.hint_frame.move(self.values[0].x - view.node_width // 2, self.values[0].y, True)
                view.draw_exp_text(self, f'Search in [{self.children[0].id}]', False)
            view.hint_frame.move(self.children[i].values[0].x, self.children[i].values[0].y)
            return self.children[i].search_value(value)

    def successor(self, remove=True):  # POT remove do ogarnięcia
        """
        Searches for successor in the tree starting in self.
        Removes the successor!
        :param remove: if True successor will be deleted, else not
        :return: for remove==True: tuple(successor, node from which successor was deleted)
                 for remove==False: value of the successor
        """
        first = self.values[0]
        view = self.tree.view
        view.hint_frame.draw(first.x, first.y)
        if self.is_leaf:
            view.draw_exp_text(self, f'Node [{self.id}] is a leaf, so first value is a successor')
            view.erase(hint_frame)
            return (self.values.pop(0), self) if remove else self.values[0].value
        else:
            view.draw_exp_text(self, f'Node [{self.id}] is not a leaf. Search for successor in a first child')
            view.hint_frame.move(self.children[0].values[0].x, self.children[0].values[0].y, True)
            view.erase(hint_frame)
            return self.children[0].successor(remove)

    # BPTNode specific methods below

    def split_child(self, i, full_node):
        """
        Splits full_node (i-th child of self) into self and new_node (new child of self with values >)
        :param i: position of full_node in self.children
        :param full_node: child of self
        :return: returns nothing
        """
        new_node = BPTNode(self.tree, full_node.is_leaf, self.x, self.y)
        md = self.tree.max_degree
        view = self.tree.view
        split_point = (md + 1) // 2
        # Rewrite values: full_node to new_node
        view.draw_exp_text(full_node, f'Rewrite {full_node.values[split_point - 1].value} to [{self.id}]')
        for j in range(0, (md - 1) // 2 + (0 if md % 2 else 1)):
            if split_point < len(full_node.values):
                new_node.values.insert(j, full_node.values[split_point])
                new_node.values[j].parent = new_node
                full_node.values.pop(split_point)
        new_node.x = new_node.values[0].x
        new_node.y = new_node.values[0].y
        if not full_node.is_leaf:
            # Rewrite children: full_node to new_node
            for j in range(0, len(new_node.values) + 1):
                if split_point < len(full_node.children):
                    new_node.children.insert(j, full_node.children[split_point])
                    full_node.children[split_point].parent = new_node
                    full_node.children.pop(split_point)
        self.children.insert(i + 1, new_node)
        new_node.parent = self
        # Move one value from full_node to self
        self.values.insert(i, full_node.values[len(full_node.values) - 1])
        self.values[i].parent = self
        # b+tree
        if full_node.is_leaf:
            tmp = mb.BalValue(full_node.values[len(full_node.values) - 1].value, new_node,
                              full_node.values[len(full_node.values) - 1].x,
                              full_node.values[len(full_node.values) - 1].y)
            view.draw_object(tmp, view.canvas_now)
            new_node.values.insert(0, tmp)
        # b+tree end
        full_node.values.pop(len(full_node.values) - 1)
        self.tree.root.update_positions()
        view.animate(self.tree.root)
        view.draw_exp_text(full_node, f'Values < {self.values[0].value} stay in [{full_node.id}] node')
        view.draw_exp_text(new_node, f'Values > {self.values[0].value} make new node [{new_node.id}]')
        view.draw_exp_text(self, f'Nodes [{full_node.id}] and [{new_node.id}] become '
                                 f'left and right children of [{self.id}]')

    def fix_delete(self, value):
        """
        Fixes the tree after the deletion operation.
        :return: returns nothing
        """
        min_val_degree = math.ceil(self.tree.max_degree / 2) - 1
        prev = self.parent
        view = self.tree.view
        self.tree.update_positions()
        view.animate(self.tree.root)
        # Node validates the tree constraints
        if len(self.values) < min_val_degree:
            view.draw_exp_text(self, f'Node [{self.id}] has not enough values')
            # Cases with root
            if self is self.tree.root and len(self.values) == 0 and len(self.children) > 0:
                view.draw_exp_text(self, f'Node [{self.id}] is a root. '
                                         f'New root is first child of [{self.id}]: [{self.children[0].id}]')
                self.tree.root = self.children[0]
                self.children[0].parent = None
                self.tree.root.update_positions()
                view.animate(self.tree.root)
                return
            elif self is self.tree.root and len(self.values) == 0 and len(self.children) == 0:
                view.draw_exp_text(self, f'Node [{self.id}] is a root. Root has no children. Tree is empty')
                self.tree.clear()
                return
            i = prev.children.index(self)
            # Cases with node
            if i - 1 >= 0 and len(prev.children[i - 1].values) > min_val_degree:
                view.draw_exp_text(self, f'Rewrite index {prev.children[i - 1].values[-1].value} '
                                         f'from [{prev.children[i - 1].id}] to [{self.id}]')
                self.values.insert(0, prev.children[i - 1].values[-1])
                prev.children[i - 1].values[-1].parent = self
                if not prev.children[i - 1].is_leaf:
                    view.draw_exp_text(f'Rewrite {prev.children[i - 1].children[-1].id} as first child of {self.id}')
                    prev.children[i - 1].children[-1].parent = self
                    self.children.insert(0, prev.children[i - 1].children[-1])
                    prev.children[i - 1].children.pop()
                    view.draw_exp_text(f'Change value ({self.values[0].value}) '
                                       f'in node [{self.id}] to successor of it\'s right child')
                    self.values[0].value = self.children[1].successor(False)
                prev.children[i - 1].values.pop()
                self.update_positions()
                view.animate(self.tree.root)
                view.draw_exp_text(f'Change value ({prev.values[i - 1].value}) '
                                   f'in node [{prev.id}] to successor of it\'s right child')
                prev.values[i - 1].value = prev.children[i].successor(False)
            elif i + 1 < len(prev.children) and len(prev.children[i + 1].values) > min_val_degree:
                view.draw_exp_text(self, f'Rewrite index {prev.children[i + 1].values[0].value} '
                                         f'from [{prev.children[i + 1].id}] to [{self.id}]')
                self.values.append(prev.children[i + 1].values[0])
                prev.children[i + 1].values[0].parent = self
                if not prev.children[i + 1].is_leaf:
                    prev.children[i + 1].children[0].parent = self
                    view.draw_exp_text(f'Rewrite {prev.children[i + 1].children[0].id} as last child of {self.id}')
                    self.children.append(prev.children[i + 1].children[0])
                    prev.children[i + 1].children.pop(0)
                    view.draw_exp_text(f'Change value ({self.values[0].value}) '
                                       f'in node [{self.id}] to successor of it\'s right child')
                    self.values[0].value = self.children[1].successor(False)
                prev.children[i + 1].values.pop(0)
                self.update_positions()
                view.animate(self.tree.root)
                view.draw_exp_text(f'Change value ({prev.values[i].value}) '
                                   f'in node [{prev.id}] to successor of it\'s right child')
                prev.values[i].value = prev.children[i + 1].successor(False)
            elif i - 1 >= 0 and len(prev.children[i - 1].values) == min_val_degree:
                if self.is_leaf:
                    view.erase(prev.values[i - 1].tag())
                    view.erase(f'Line{hash(prev.values[i - 1])}')
                    prev.children[i].parent = None
                    prev.children.pop(i)
                    prev.values[i - 1].parent = None
                    prev.values.pop(i - 1)
                    view.draw_exp_text(self, f'Rewrite values from [{self.id}] node to [{prev.id}] node')
                    view.draw_exp_text(self, f'Remove node [{self.id}]')
                    for v in self.values:
                        prev.children[i - 1].values.append(v)
                        v.parent = prev.children[i - 1]
                else:
                    prev.children.pop(i)
                    sibling = prev.children[i - 1]
                    prev.children.pop(i - 1)
                    # self values and children to prev
                    view.draw_exp_text(self, f'Rewrite values and children from [{self.id}] node to [{prev.id}] node')
                    for v in self.values:
                        prev.values.append(v)
                        v.parent = prev
                    for c in self.children:
                        prev.children.append(c)
                        c.parent = prev
                    # sibling values and children to prev
                    view.draw_exp_text(self,
                                       f'Rewrite values and children from [{sibling.id}] node to [{prev.id}] node')
                    for v in reversed(sibling.values):
                        prev.values.insert(0, v)
                        v.parent = prev
                    for c in reversed(sibling.children):
                        prev.children.insert(0, c)
                        c.parent = prev
                prev.update_positions()
                view.animate(self.tree.root)
            elif i + 1 < len(prev.children) and len(prev.children[i + 1].values) == min_val_degree:
                view.draw_exp_text(prev, f'Remove node {self.id}')
                view.draw_exp_text(self, f'Delete [{prev.values[i].value}] node')
                if self.is_leaf:
                    view.erase(prev.values[i].tag())
                    view.erase(f'Line{hash(prev.values[i])}')
                    prev.children[i].parent = None
                    prev.values[i].parent = None
                    prev.values.pop(i)
                    view.draw_exp_text(self, f'Rewrite values from [{self.id}] node to [{prev.id}] node')
                    view.draw_exp_text(self, f'Remove node [{self.id}]')
                    for v in reversed(self.values):
                        prev.children[i + 1].values.insert(0, v)
                        v.parent = prev.children[i + 1]
                    prev.children.pop(i)
                else:
                    sibling = prev.children[i + 1]
                    prev.children.pop(i + 1)
                    prev.children.pop(i)
                    # self values and children to prev
                    view.draw_exp_text(self, f'Rewrite values and children from [{self.id}] node to [{prev.id}] node')
                    for v in reversed(self.values):
                        prev.values.insert(0, v)
                        v.parent = prev
                    for c in reversed(self.children):
                        prev.children.insert(0, c)
                        c.parent = prev
                    # sibling values and children to prev
                    view.draw_exp_text(self,
                                       f'Rewrite values and children from [{sibling.id}] node to [{prev.id}] node')
                    for v in sibling.values:
                        prev.values.append(v)
                        v.parent = prev
                    for c in sibling.children:
                        prev.children.append(c)
                        c.parent = prev
                prev.update_positions()
                view.animate(self.tree.root)
            else:
                return
            prev.fix_delete(value)
        self.tree.update_positions()
        view.animate(self.tree.root)

    def min(self):
        curr = self
        while not curr.is_leaf:
            curr = curr.children[0]
        self.tree.view.draw_exp_text(curr, f'Min value is first element of '
                                           f'double-linked list of leaves: {curr.values[0].value}')

    def max(self):
        curr = self
        while not curr.is_leaf:
            curr = curr.children[-1]
        self.tree.view.draw_exp_text(curr, f'Max value is last element of '
                                           f'double-linked list of leaves: {curr.values[-1].value}')

    def mean(self, val_sum, counter):
        pass

    def median(self, tab):
        pass

    def insert_specific(self, value, i):
        pass


class BPTree(mb.BalTree):
    node_class = BPTNode

    def mean(self):
        if self.root is None:
            self.view.explanation.append(f'Tree is empty. Impossible to calculate mean of an empty tree')
        else:
            self.view.explanation.append(f'Calculate the mean value of the tree - traverse leaves')
            successors = self.root.successors()
            values = []
            for s in successors:
                if type(s) is mb.BalValue and s.parent.is_leaf:
                    values.append(s)
            self.view.hint_frame.draw(values[0].x, values[0].y)
            val_sum = 0
            counter = 0
            for v in values:
                if v != values[0]:
                    self.view.hint_frame.move(v.x, v.y)
                self.view.draw_exp_text(v, f'Add {v.value} to sum {val_sum} '
                                           f'and increase counter {counter} by 1')
                val_sum += v.value
                counter += 1
            self.view.draw_exp_text(self.root, f'Whole tree traversed. '
                                               f'Mean = {val_sum}/{counter} = {val_sum / counter}')

    def median(self):
        if self.root is None:
            self.view.explanation.append(f'Tree is empty. Impossible to calculate median of an empty tree')
        else:
            self.view.explanation.append(f'Calculate the median value of the tree - traverse leaves')
            successors = self.root.successors()
            values = []
            for s in successors:
                if type(s) is mb.BalValue and s.parent.is_leaf:
                    values.append(s)
            self.view.hint_frame.draw(values[0].x, values[0].y)
            tab = []
            for v in values:
                if v != values[0]:
                    self.view.hint_frame.move(v.x, v.y)
                self.view.draw_exp_text(v, f'Append {v.value} to tab {tab}')
                tab.append(v.value)
            self.view.draw_exp_text(self.root, f'Whole tree traversed. Values = {tab}. '
                                               f'Median = {statistics.median(tab)}')
