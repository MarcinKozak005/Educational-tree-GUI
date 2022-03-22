import math
import tkinter as tk

import mvc_base.model as model
from core.constants import grey_node, hint_frame


class BPTree(model.Tree):

    def __init__(self, view, max_degree):
        super().__init__(view)
        if max_degree < 2:
            raise ValueError
        self.max_degree = max_degree

    def insert_value(self, value):
        if self.root is None:
            self.root = BPTNode(self, True, self.view.width // 2, self.view.y_space)
            self.view.explanation.append(f'Tree is empty. Create node [{self.root.id}] with value {value}')
            self.root.values.append(BPTValue(value, self.root))
        else:
            view = self.view
            view.explanation.append(f'Tree is not empty. Find insert place for {value}')
            view.canvas_now.create_rectangle(self.root.x - view.node_width // 2,
                                             self.root.y - view.node_height // 2 - view.y_above,
                                             self.root.x + view.node_width // 2,
                                             self.root.y + view.node_height // 2 - view.y_above,
                                             fill='grey', tags=grey_node)
            view.canvas_now.create_text(self.root.x, self.root.y - view.y_above, fill='white',
                                        text=value, tags=grey_node)
            self.root.insert_value(BPTValue(value, None, self.root.x, self.root.y - view.y_above))
        self.root.update_positions(True)

    def delete_value(self, value):
        search_result = self.root.search_value(value)
        if search_result:
            self.root.delete_value(value)

    def search_value(self, value):
        if self.root is None:
            self.view.explanation.append(f'Tree is empty. Value cannot be found')
        else:
            self.root.search_value(value)

    def search_value_no_GUI(self, value):
        if self.root is not None:
            return self.root.search_value_no_GUI(value)

    def clear(self):
        """ Additionally resets BPTNode.class_node_id """
        self.root = None
        BPTNode.class_node_id = ord('@')


class BPTValue(model.AnimatedObject):

    def __init__(self, value, parent_node, x=0, y=0):
        super().__init__(x, y, parent_node)
        self.value = value

    def tick(self, view, x_un, y_un):
        view.erase(f'Line{hash(self)}')
        if view.canvas_now.find_withtag(self.tag()):
            view.canvas_now.move(self.tag(), x_un, y_un)
        else:
            view.canvas_now.move(grey_node, x_un, y_un)
        self.x += x_un
        self.y += y_un
        index = self.parent.values.index(self)
        if not self.parent.is_leaf:
            if index < len(self.parent.children):
                view.draw_line(view.canvas_now, self, self.parent.children[index], tk.SW, tk.N)
            if index == len(self.parent.values) - 1 and index + 1 < len(self.parent.children):
                view.draw_line(view.canvas_now, self, self.parent.children[index + 1], tk.SE, tk.N)
            view.canvas_now.tag_lower('Line')

    def tag(self):
        return f'Value{hash(self)}'


class BPTNode(model.AnimatedObject, model.Node):
    class_node_id = ord('@')  # distinguishes nodes by using letters

    @staticmethod
    def get_id():
        BPTNode.class_node_id += 1
        if BPTNode.class_node_id == ord('['):
            BPTNode.class_node_id = ord('a')
        elif BPTNode.class_node_id == ord('{'):
            BPTNode.class_node_id = ord('A')
        return chr(BPTNode.class_node_id)

    def __init__(self, tree, is_leaf, x, y):
        model.AnimatedObject.__init__(self, x, y, None)
        model.Node.__init__(self, tree, 0, tree.view.width)
        self.is_leaf = is_leaf
        self.values = []
        self.children = []
        self.id = BPTNode.get_id()

    def tick(self, view, x_unit, y_unit):
        view.canvas_now.move(self.tag(), x_unit, y_unit)
        self.x += x_unit
        self.y += y_unit

    def tag(self):
        return f'Node{hash(self)}'

    def insert_value(self, value):
        """
        Inserts value in the node or calls insert on child node to which the value should be inserted
        :param value: value to insert
        :return: returns nothing
        """
        i = 0
        view = self.tree.view
        view.hint_frame.draw(self.values[0].x, self.values[0].y)
        # Search for a spot to insert new value
        while i < len(self.values) and value.value >= self.values[i].value:
            view.draw_exp_text(self.values[i],
                               f'[{self.id}]: {value.value} >= {self.values[i].value}, check next value',
                               False)
            view.hint_frame.move(self.values[i].x + view.node_width, self.values[i].y, True)
            i += 1
        # Show end-search reason
        if i < len(self.values):
            view.draw_exp_text(self.values[i], f'[{self.id}]: {value.value} < {self.values[i].value}, '
                                               f'insert before {self.values[i].value}', False)
            view.hint_frame.move(self.values[i].x - view.node_width // 2, self.values[i].y, True)
        else:
            view.draw_exp_text(self, f'No next value', False)
            view.hint_frame.move(self.values[-1].x + view.node_width // 2, self.values[-1].y, True)
        # Insert value
        if self.is_leaf:
            self.values.insert(i, value)
            value.x = self.x
            value.y = self.y - view.y_above
            self.values[i].parent = self
            view.draw_exp_text(self, f'Node [{self.id}] is a leaf. Insert {value.value} in the node [{self.id}]', False)
            self.tree.update_positions()
            view.animate(self)
        else:
            view.draw_exp_text(self, f'Insert value to a child node [{self.children[i].id}] of [{self.id}]', False)
            view.erase(hint_frame)
            view.move_object(grey_node, self.x, self.y, self.children[i].x, self.children[i].y)
            self.children[i].insert_value(value)
        # Fix b-tree constraints
        if len(self.values) == self.tree.max_degree:
            view.erase(hint_frame)
            view.draw_exp_text(self, f'Number of values in [{self.id}] == max_tree_degree. Start fixing process')
            self.fix_insert()

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
                view.draw_exp_text(parent.values[i], f'Change value ({parent.values[i].value}) '
                                                     f'in node [{parent.id}] to successor of it\'s right child')
                i = values.index(value)
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

    def search_value_no_GUI(self, value):
        """
        Searches for value in the node
        :param value: searched value
        :return: if found: tuple (node_with_value, position_of_value_in_node), else: None
        """
        i = 0
        while i < len(self.values) and value > self.values[i].value:
            i += 1
        if i < len(self.values) and value == self.values[i].value:
            return self, i
        if self.is_leaf:
            return None
        else:
            return self.children[i].search_value_no_GUI(value)

    def update_positions(self, static=False, width=None):
        view = self.tree.view
        if self.parent is not None:
            unit = (self.parent.r_edge - self.parent.l_edge) / (2 * len(self.parent.children))
            index = self.parent.children.index(self)
            self.x_next = self.parent.l_edge + unit + index * 2 * unit
            self.y_next = self.parent.y_next + view.y_space
            self.l_edge = self.x_next - unit
            self.r_edge = self.x_next + unit
        elif self.parent is None:
            self.x_next = view.width // 2 if width is None else width // 2
            self.y_next = view.y_space
            self.l_edge = 0
            self.r_edge = view.width if width is None else width
        # Values
        for i in range(len(self.values)):
            self.values[i].x_next = self.x_next - len(self.values) * self.tree.view.node_width // 2 + \
                                    self.tree.view.node_width // 2 + i * self.tree.view.node_width
            self.values[i].y_next = self.y_next
        if static:
            self.x = self.x_next
            self.y = self.y_next
            for v in self.values:
                v.x = v.x_next
                v.y = v.y_next
        if not self.is_leaf:
            for c in self.children:
                c.update_positions(static)

    def successors(self):
        result = []
        for c in self.children:
            result += c.successors()
        result.append(self)
        result += self.values
        return result

    def successor(self, remove=True):
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

    def print_node(self, indent=0):
        print('\t' * indent + f'{self.values}')
        for c in self.children:
            c.print_node(indent + 1)

    # BPNode specific methods below

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
            tmp = BPTValue(full_node.values[len(full_node.values) - 1].value, new_node,
                           full_node.values[len(full_node.values) - 1].x, full_node.values[len(full_node.values) - 1].y)
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

    def fix_insert(self):
        """
        Fixes the node to make it obey max_degree constraint of b-trees
        :return: returns nothing
        """
        if self.parent is not None:
            self.parent.split_child(self.parent.children.index(self), self)
        else:
            self.tree.view.draw_exp_text(self, f'Root has too much values. Create new root and split old one')
            s = BPTNode(self.tree, False, self.tree.view.width // 2, self.tree.view.y_space)
            s.children.insert(0, self.tree.root)
            self.tree.root.parent = s
            self.tree.root = s
            s.split_child(0, s.children[0])

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

    def predecessor(self):
        """
        Searches for predecessor in the tree starting in self.
        Removes the predecessor!
        :return: predecessor, node from which predecessor was deleted
        """
        last = self.values[-1]
        view = self.tree.view
        view.hint_frame.draw(last.x, last.y)
        if self.is_leaf:
            view.draw_exp_text(self, f'Node [{self.id}] is a leaf, last value is a predecessor')
            view.erase(hint_frame)
            return self.values.pop(-1), self
        else:
            view.draw_exp_text(self, f'Node [{self.id}] is not a leaf. Search for a predecessor in last child')
            view.hint_frame.move(self.children[-1].values[-1].x, self.children[-1].values[-1].y)
            view.erase(hint_frame)
            return self.children[-1].predecessor()
