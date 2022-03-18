import math
import tkinter as tk

import core.root as r
import mvc_base.model as model


class BTree(model.Tree):

    def __init__(self, view, max_degree):
        super().__init__(view)
        if max_degree < 2:
            raise ValueError
        self.max_degree = max_degree

    def insert_value(self, value):
        if self.root is None:
            self.root = BTNode(self, True, self.view.width // 2, self.view.y_space)
            self.view.explanation.append(f'Tree is empty')
            self.root.values.append(BTValue(value, self.root))
            self.view.explanation.append(f'Added value {value} in node [{self.root.id}]')
        else:
            view = self.view
            view.explanation.append(f'Tree is not empty, looking for insert place for {value}')
            view.canvas_now.create_rectangle(self.root.x - view.node_width // 2,
                                             self.root.y - view.node_height // 2 - view.y_above,
                                             self.root.x + view.node_width // 2,
                                             self.root.y + view.node_height // 2 - view.y_above,
                                             fill='grey', tags=r.grey_node)
            view.canvas_now.create_text(self.root.x, self.root.y - view.y_above, fill='white',
                                        text=value, tags=r.grey_node)
            self.root.insert_value(BTValue(value, None, self.root.x, self.root.y - view.y_above))
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
        """ Additionally resets BTNode.class_node_id """
        self.root = None
        BTNode.class_node_id = ord('@')


class BTValue(model.AnimatedObject):

    def __init__(self, value, parent_node, x=0, y=0):
        super().__init__(x, y, parent_node)
        self.value = value

    def tick(self, view, x_un, y_un):
        view.erase(f'Line{hash(self)}')
        if view.canvas_now.find_withtag(self.tag()):
            view.canvas_now.move(self.tag(), x_un, y_un)
        else:
            view.canvas_now.move(r.grey_node, x_un, y_un)
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


class BTNode(model.AnimatedObject, model.Node):
    class_node_id = ord('@')

    @staticmethod
    def get_id():
        BTNode.class_node_id += 1
        if BTNode.class_node_id == ord('['):
            BTNode.class_node_id = ord('a')
        elif BTNode.class_node_id == ord('{'):
            BTNode.class_node_id = ord('A')
        return chr(BTNode.class_node_id)

    def __init__(self, tree, is_leaf, x, y):
        model.AnimatedObject.__init__(self, x, y, None)
        model.Node.__init__(self, tree, 0, tree.view.width)
        self.is_leaf = is_leaf
        self.values = []
        self.children = []
        self.id = BTNode.get_id()

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
        while i < len(self.values) and value.value > self.values[i].value:
            view.draw_exp_text(self.values[i], f'[{self.id}]: {value.value} > {self.values[i].value}, check next value',
                               False)
            view.hint_frame.move(self.values[i].x + view.node_width, self.values[i].y, True)
            i += 1
        if i < len(self.values):
            view.draw_exp_text(self.values[i], f'[{self.id}]: {value.value} < {self.values[i].value}, '
                                               f'insert to previous', False)
            view.hint_frame.move(self.values[i].x - view.node_width // 2, self.values[i].y, True)
        else:
            view.draw_exp_text(self, f'No next value', False)
            view.hint_frame.move(self.values[-1].x + view.node_width // 2, self.values[-1].y, True)
        if self.is_leaf:
            self.values.insert(i, value)
            value.x = self.x
            value.y = self.y - view.y_above
            self.values[i].parent = self
            view.draw_exp_text(self, f'Node [{self.id}] is a leaf. Inserting {value.value} in the node [{self.id}]',
                               False)
            self.tree.update_positions()
            view.animate(self)
        else:
            view.draw_exp_text(self, f'Insert value to a children node [{self.children[i].id}] of [{self.id}]', False)
            view.erase(r.hint_frame)
            view.move_object(r.grey_node, self.x, self.y, self.children[i].x, self.children[i].y)
            self.children[i].insert_value(value)
        if len(self.values) == self.tree.max_degree:
            view.erase(r.hint_frame)
            view.draw_exp_text(self, f'Number of values in [{self.id}] == max b-tree degree. Start fixing')
            self.fix_insert()

    def delete_value(self, value):
        min_val_degree = math.ceil(self.tree.max_degree / 2) - 1
        values = [self.values[i].value for i in range(len(self.values))]
        view = self.tree.view
        if self.is_leaf and value in values:
            i = values.index(value)
            removed_node = self.values.pop(i)
            view.erase(removed_node.tag())
            self.fix_delete()
        elif value in values:
            i = values.index(value)
            if len(self.children[i].values) > min_val_degree:
                view.draw_exp_text(self.children[i], f'Node [{self.children[i].id}] has > {min_val_degree} values. '
                                                     f'Looking for the predecessor of {value}')
                view.erase(self.values[i].tag())
                view.erase(f'Line{hash(self.values[i])}')
                self.values[i], to_fix = self.children[i].predecessor()
                self.values[i].parent = self
                to_fix.fix_delete()
            elif len(self.children[i + 1].values) > min_val_degree:
                view.draw_exp_text(self.children[i], f'Node [{self.children[i + 1].id}] has > {min_val_degree} values.'
                                                     f'Looking for the successor of {value}')
                view.erase(self.values[i].tag())
                view.erase(f'Line{hash(self.values[i])}')
                self.values[i], to_fix = self.children[i + 1].successor()
                self.values[i].parent = self
                to_fix.fix_delete()
            else:
                view.draw_exp_text(self, f'Merge nodes [{self.children[i].id}] and [{self.children[i + 1].id}]')
                self.children[i].values.append(BTValue(value, self.children[i]))
                for v in self.children[i + 1].values:
                    v.parent = self.children[i]
                    self.children[i].values.append(v)
                self.children[i].children.extend(self.children[i + 1].children)
                for c in self.children[i + 1].children:
                    c.parent = self.children[i]
                view.erase(self.values[i].tag())
                view.erase(f'Line{hash(self.values[i])}')
                self.values.pop(i)
                self.children.pop(i + 1)
                self.children[i].delete_value(value)
                self.fix_delete()
        else:
            i = 0
            while i < len(self.values) and value > self.values[i].value:
                i += 1
            self.children[i].delete_value(value)

    def search_value(self, value):
        """
        Searches for value in the node
        :param value: searched value
        :return: if found: tuple (node_with_value, position_of_value_in_node), else: None
        """
        i = 0
        view = self.tree.view
        view.hint_frame.draw(self.values[0].x, self.values[0].y)
        while i < len(self.values) and value > self.values[i].value:
            view.draw_exp_text(self.values[i], f'[{self.id}]: {value} > {self.values[i].value}, check next value',
                               False)
            view.hint_frame.move(self.values[i].x + view.node_width, self.values[i].y, True)
            i += 1
        if i < len(self.values) and value == self.values[i].value:
            view.draw_exp_text(self, f'Value found in node [{self.id}]')
            view.erase(r.hint_frame)
            return self, i
        if self.is_leaf:
            view.draw_exp_text(self, f'Value not found')
            view.erase(r.hint_frame)
            return None
        else:
            if i < len(self.values):
                view.draw_exp_text(self.values[i], f'[{self.id}]: {value} < {self.values[i].value}, '
                                                   f'search in [{self.children[i].id}]', False)
            else:
                view.draw_exp_text(self, f'No next value', False)
                view.draw_exp_text(self, f'Search value in a children node [{self.children[i].id}] of [{self.id}]',
                                   False)
            if i != 0:
                view.hint_frame.move(self.values[i - 1].x, self.values[i - 1].y, True)
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

    def successor(self):
        """
        Searches for successor in the tree starting in self.
        Removes the successor!
        :return: successor, node from which successor was deleted
        """
        first = self.values[0]
        view = self.tree.view
        view.hint_frame.draw(first.x, first.y)
        if self.is_leaf:
            view.draw_exp_text(self, f'Node [{self.id}] is a leaf, first value is a successor')
            return self.values.pop(0), self
        else:
            view.draw_exp_text(self, f'Node [{self.id}] is not a leaf, search for successor in a first child')
            view.hint_frame.move(self.children[0].values[0].x, self.children[0].values[0].y, True)
            view.erase(r.hint_frame)
            return self.children[0].successor()

    def print_node(self, indent=0):
        print('\t' * indent + f'{self.values}')
        for c in self.children:
            c.print_node(indent + 1)

    # BNode specific methods below

    def split_child(self, i, full_node):
        """
        Splits full_node (i-th children of self) into self and new_node (new child of self with values >)
        :param i: position of full_node in self.children
        :param full_node: children of self
        :return: returns nothing
        """
        new_node = BTNode(self.tree, full_node.is_leaf, self.x, self.y)
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
            for j in range(0, split_point):
                if split_point < len(full_node.children):
                    new_node.children.insert(j, full_node.children[split_point])
                    full_node.children[split_point].parent = new_node
                    full_node.children.pop(split_point)
        self.children.insert(i + 1, new_node)
        new_node.parent = self
        # Move one value from full_node to self
        self.values.insert(i, full_node.values[len(full_node.values) - 1])
        self.values[i].parent = self
        full_node.values.pop(len(full_node.values) - 1)
        self.tree.root.update_positions()
        view.animate(self.tree.root)
        view.draw_exp_text(full_node, f'Values < {self.values[0].value} stays in [{full_node.id}] node')
        view.draw_exp_text(new_node, f'Values > {self.values[0].value} makes new node [{new_node.id}]')
        view.draw_exp_text(self, f'Nodes [{full_node.id}] and [{new_node.id}] become a children of [{self.id}]')

    def fix_insert(self):
        """
        Fixes the node to make it obey max_degree constraint of b-trees
        :return: returns nothing
        """
        if self.parent is not None:
            self.parent.split_child(self.parent.children.index(self), self)
        else:
            self.tree.view.draw_exp_text(self, f'Root has too much values. Create new root and split old one')
            s = BTNode(self.tree, False, self.tree.view.width // 2, self.tree.view.y_space)
            s.children.insert(0, self.tree.root)
            self.tree.root.parent = s
            self.tree.root = s
            s.split_child(0, s.children[0])

    def fix_delete(self):
        """
        Fixes the tree after the deletion operation.
        :return: returns nothing
        """
        min_val_degree = math.ceil(self.tree.max_degree / 2) - 1
        prev = self.parent
        view = self.tree.view
        if len(self.values) < min_val_degree:
            view.draw_exp_text(self, f'Node [{self.id}] has not enough values')
            if self is self.tree.root and len(self.children) > 0:
                view.draw_exp_text(self, f'Node [{self.id}] is a root.'
                                         f'New root is first child of [{self.id}]: [{self.children[0].id}]')
                self.tree.root = self.children[0]
                self.children[0].parent = None
                self.tree.root.update_positions()
                view.animate(self.tree.root)
                return
            elif self is self.tree.root and len(self.children) == 0:
                view.draw_exp_text(self, f'Node [{self.id}] is a root. Root has no children. Tree is empty')
                self.tree.root = None
                return
            i = prev.children.index(self)
            if i - 1 >= 0 and len(prev.children[i - 1].values) > min_val_degree:
                view.draw_exp_text(self, f'Rewrite value {prev.values[i - 1].value} from [{prev.id}] to [{self.id}]')
                self.values.insert(0, prev.values[i - 1])
                prev.values[i - 1].parent = self
                prev.values.pop(i - 1)
                self.update_positions()
                view.animate(self.tree.root)
                view.draw_exp_text(prev, f'Too much children compared to values. '
                                         f'Rewrite {prev.children[i - 1].values[-1].value} from '
                                         f'[{prev.children[i - 1].id}] to [{prev.id}]')
                prev.values.insert(i - 1, prev.children[i - 1].values[-1])
                prev.children[i - 1].values[-1].parent = prev
                prev.children[i - 1].values.pop()
                if prev.children[i - 1].children:
                    self.children.insert(0, prev.children[i - 1].children[-1])
                    prev.children[i - 1].children[-1].parent = self
                    prev.children[i - 1].children.pop()
            elif i + 1 < len(prev.children) and len(prev.children[i + 1].values) > min_val_degree:
                view.draw_exp_text(self, f'Rewrite value {prev.values[i].value} from [{prev.id}] to [{self.id}]')
                self.values.append(prev.values[i])
                prev.values[i].parent = self
                prev.values.pop(i)
                self.update_positions()
                view.animate(self.tree.root)
                view.draw_exp_text(prev, f'Too much children compared to values. '
                                         f'Rewrite {prev.children[i + 1].values[0].value} from '
                                         f'[{prev.children[i + 1].id}] to [{prev.id}]')
                prev.values.insert(i, prev.children[i + 1].values[0])
                prev.children[i + 1].values[0].parent = prev
                prev.children[i + 1].values.pop(0)
                if prev.children[i + 1].children:
                    self.children.append(prev.children[i + 1].children[0])
                    prev.children[i + 1].children[0].parent = self
                    prev.children[i + 1].children.pop(0)
            elif i - 1 >= 0 and len(prev.children[i - 1].values) == min_val_degree:
                view.draw_exp_text(prev, f'Rewrite value {prev.values[i - 1].value} '
                                         f'from [{prev.id}] to [{prev.children[i - 1].id}]')
                view.draw_exp_text(self, f'Rewrite values from [{self.id}] to [{prev.children[i - 1].id}]')
                view.draw_exp_text(self, f'Delete [{self.id}] node')
                prev.children[i - 1].values.append(prev.values[i - 1])
                prev.values[i - 1].parent = prev.children[i - 1]
                # Unnecessary?
                for n in self.children:
                    n.parent = prev.children[i - 1]
                prev.children[i - 1].children.extend(self.children)
                # End unnecessary
                for v in self.values:
                    v.parent = prev.children[i - 1]
                    prev.children[i - 1].values.append(v)
                prev.values.pop(i - 1)
                prev.children.pop(i)
            elif i + 1 < len(prev.children) and len(prev.children[i + 1].values) == min_val_degree:
                view.draw_exp_text(prev, f'Rewrite value {prev.values[i].value} from [{prev.id}] to [{self.id}]')
                view.draw_exp_text(self, f'Rewrite values from [{self.id}] to [{prev.children[i + 1].id}]')
                view.draw_exp_text(self, f'Delete [{prev.children[i + 1].id}] node')
                prev.children[i + 1].values.insert(0, prev.values[i])
                prev.values[i].parent = prev.children[i + 1]
                # Unnecessary?
                for n in prev.children[i + 1].children:
                    n.parent = self
                prev.children[i + 1].children.extend(self.children)
                # End unnecessary
                for v in reversed(self.values):
                    v.parent = prev.children[i + 1]
                    prev.children[i + 1].values.insert(0, v)
                prev.values.pop(i)
                prev.children.pop(i)
            else:
                return
            prev.fix_delete()
        self.tree.update_positions()
        view.animate(self.tree.root)

    def predecessor(self):
        """
        Searches for predecessor in the tree starting in self.
        Removes the predecessor!
        :return: predecessor, node from which predecessor was deleted
        """
        last = self.values[-1]
        self.tree.view.hint_frame.draw(last.x, last.y)
        if self.is_leaf:
            self.tree.view.draw_exp_text(self, f'Node [{self.id}] is a leaf, last value is a predecessor')
            return self.values.pop(-1), self
        else:
            self.tree.view.draw_exp_text(self, f'Node [{self.id}] is not a leaf, search for predecessor in last child')
            self.tree.view.hint_frame.move(self.children[-1].values[-1].x, self.children[-1].values[-1].y)
            self.tree.view.erase(r.hint_frame)
            return self.children[-1].predecessor()