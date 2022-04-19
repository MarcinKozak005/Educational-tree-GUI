import copy
import math
import statistics

import mvc_base.model_balanced as mb
from core.constants import hint_frame


class BTNode(mb.BalNode):

    def delete_value(self, value):
        node, pos = self.search_value(value)
        if node is not None and pos is not None:
            min_val_degree = math.ceil(node.tree.max_degree / 2) - 1
            values = [node.values[i].value for i in range(len(node.values))]
            view = node.tree.view
            if node.is_leaf and value in values:
                i = values.index(value)
                removed_elem = node.values.pop(i)
                view.draw_exp_text(removed_elem, f'Remove value {removed_elem.value}')
                view.move_object(removed_elem.tag(), removed_elem.x, removed_elem.y, removed_elem.x, -view.node_height)
                node.fix_delete()
            elif value in values:
                i = values.index(value)
                if len(node.children[i].values) > min_val_degree and node.children[i].is_leaf \
                        or not node.children[i].is_leaf:
                    removed_elem = node.values[i]
                    view.draw_exp_text(removed_elem, f'Remove value {removed_elem.value}')
                    view.move_object(removed_elem.tag(), removed_elem.x, removed_elem.y, removed_elem.x,
                                     -view.node_height)
                    view.draw_exp_text(node.children[i], f'Find predecessor of {value} in [{node.children[i].id}] node')
                    node.values[i], to_fix = node.children[i].predecessor()
                    node.values[i].parent = node
                    view.draw_exp_text(to_fix, f'Value {node.values[i].value} goes to node {node.id}')
                    view.erase(f'Line{hash(removed_elem)}')
                    to_fix.fix_delete()
                elif len(node.children[i + 1].values) > min_val_degree and node.children[i + 1].is_leaf \
                        or not node.children[i + 1].is_leaf:
                    removed_elem = node.values[i]
                    view.draw_exp_text(removed_elem, f'Remove value {removed_elem.value}')
                    view.move_object(removed_elem.tag(), removed_elem.x, removed_elem.y, removed_elem.x,
                                     -view.node_height)
                    view.draw_exp_text(node.children[i + 1],
                                       f'Find successor of {value} in [{node.children[i + 1].id}] node')
                    node.values[i], to_fix = node.children[i + 1].successor()
                    node.values[i].parent = node
                    view.draw_exp_text(to_fix, f'Value {node.values[i].value} goes to node {node.id}')
                    view.erase(f'Line{hash(removed_elem)}')
                    to_fix.fix_delete()
                else:
                    view.draw_exp_text(node, f'Merge node [{node.children[i].id}] value {node.values[i].value} '
                                             f'and node [{node.children[i + 1].id}]')
                    node.children[i].values.append(node.values[i])
                    node.values[i].parent = node.children[i]
                    for v in node.children[i + 1].values:
                        v.parent = node.children[i]
                        node.children[i].values.append(v)
                    node.children[i].children.extend(node.children[i + 1].children)
                    for c in node.children[i + 1].children:
                        c.parent = node.children[i]
                    view.erase(f'Line{hash(node.values[i])}')
                    node.values.pop(i)
                    node.children.pop(i + 1)
                    node.tree.update_positions()
                    view.animate(node.tree.root)
                    node.children[i].delete_value(value)
                    node.fix_delete()

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
        if i < len(self.values) and value == self.values[i].value:
            view.draw_exp_text(self, f'Value {value} found in node [{self.id}] in place {i}')
            view.erase(hint_frame)
            return self, i
        # Not found strings
        if self.is_leaf:
            exp_string = f'No more values.' if i >= len(self.values) else f'{value} < {self.values[i].value}.'
            view.draw_exp_text(self, f'[{self.id}]: {exp_string}  [{self.id}] is a leaf. Value {value} not found')
            view.erase(hint_frame)
            return None, None
        # Search in child
        else:
            # Show appropriate explanation string
            if i < len(self.values):
                view.draw_exp_text(self.values[i], f'[{self.id}]: {value} < {self.values[i].value}', False)
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
            view.draw_exp_text(self, f'Node [{self.id}] is a leaf, so first value is a successor')
            view.erase(hint_frame)
            return self.values.pop(0), self
        else:
            view.draw_exp_text(self, f'Node [{self.id}] is not a leaf. Search for successor in a first child')
            view.hint_frame.move(self.children[0].values[0].x, self.children[0].values[0].y, True)
            view.erase(hint_frame)
            return self.children[0].successor()

    # BTNode specific methods below

    def split_child(self, i, full_node):
        """
        Splits full_node (i-th child of self) into self and new_node (new child of self with values >)
        :param i: position of full_node in self.children
        :param full_node: child of self
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
        full_node.values.pop(len(full_node.values) - 1)
        self.tree.root.update_positions()
        view.animate(self.tree.root)
        view.draw_exp_text(full_node, f'Values < {self.values[i].value} stay in [{full_node.id}] node')
        view.draw_exp_text(new_node, f'Values > {self.values[i].value} make new node [{new_node.id}]')
        view.draw_exp_text(self, f'Nodes [{full_node.id}] and [{new_node.id}] become '
                                 f'left and right children of [{self.id}]')

    def fix_delete(self):
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
                prev.children[i - 1].values.append(prev.values[i - 1])
                prev.values[i - 1].parent = prev.children[i - 1]
                view.draw_exp_text(self, f'Rewrite values and children from [{self.id}] to [{prev.children[i - 1].id}]')
                for n in self.children:
                    n.parent = prev.children[i - 1]
                prev.children[i - 1].children.extend(self.children)
                for v in self.values:
                    v.parent = prev.children[i - 1]
                    prev.children[i - 1].values.append(v)
                view.draw_exp_text(self, f'Delete [{self.id}] node')
                view.erase(self.tag())
                prev.values.pop(i - 1)
                prev.children.pop(i)
            elif i + 1 < len(prev.children) and len(prev.children[i + 1].values) == min_val_degree:
                view.draw_exp_text(prev, f'Rewrite value {prev.values[i].value} '
                                         f'from [{prev.id}] to [{prev.children[i + 1].id}]')
                prev.children[i + 1].values.insert(0, prev.values[i])
                prev.values[i].parent = prev.children[i + 1]
                view.draw_exp_text(self, f'Rewrite values and children from [{self.id}] to [{prev.children[i + 1].id}]')
                for c in reversed(self.children):
                    prev.children[i + 1].children.insert(0, c)
                    c.parent = prev.children[i + 1]
                for v in reversed(self.values):
                    v.parent = prev.children[i + 1]
                    prev.children[i + 1].values.insert(0, v)
                view.draw_exp_text(self, f'Delete [{self.id}] node')
                view.erase(self.tag())
                prev.values.pop(i)
                prev.children.pop(i)
            else:
                return
            prev.fix_delete()

    def min(self):
        view = self.tree.view
        view.explanation.append(f'Search the minimal value of the tree')
        curr = self.tree.root
        view.hint_frame.draw(curr.values[0].x, curr.values[0].y)
        while not curr.is_leaf:
            view.draw_exp_text(curr, f'Node [{curr.id}] has children. Search for min in the first child')
            view.hint_frame.move(curr.children[0].values[0].x, curr.children[0].values[0].y)
            curr = curr.children[0]
        view.draw_exp_text(curr, f'Node [{curr.id}] has no children. '
                                 f'The min value is it\'s first value {curr.values[0].value}')

    def max(self):
        view = self.tree.view
        view.explanation.append(f'Search the maximal value of the tree')
        curr = self.tree.root
        view.hint_frame.draw(curr.values[-1].x, curr.values[-1].y)
        while not curr.is_leaf:
            view.draw_exp_text(curr, f'Node [{curr.id}] has children. Search for max in the last child')
            view.hint_frame.move(curr.children[-1].values[-1].x, curr.children[-1].values[-1].y)
            curr = curr.children[-1]
        view.draw_exp_text(curr, f'Node [{curr.id}] has no children. '
                                 f'The max value is it\'s last value {curr.values[-1].value}')

    def mean(self, val_sum, counter):
        view = self.tree.view
        length = len(self.values)
        for i in range(length):
            if not self.is_leaf:
                view.draw_exp_text(self, f'Go to {i}. child of node [{self.id}]: node [{self.children[i].id}]')
                view.hint_frame.move(self.children[i].values[0].x, self.children[i].values[0].y)
                val_sum, counter = self.children[i].mean(val_sum, counter)
            if i != 0:
                view.hint_frame.move(self.values[i].x, self.values[i].y)
            view.draw_exp_text(self, f'Add {self.values[i].value} to sum {val_sum} '
                                     f'and increase counter {counter} by 1')
            val_sum += self.values[i].value
            counter += 1
        if not self.is_leaf:
            view.draw_exp_text(self, f'Go to {length}. child of node [{self.id}]: node [{self.children[length].id}]')
            view.hint_frame.move(self.children[length].values[0].x, self.children[length].values[0].y)
            val_sum, counter = self.children[length].mean(val_sum, counter)
        if self.parent is not None:
            pos_in_parent = self.parent.children.index(self) if self.parent.children.index(self) != len(
                self.parent.children) - 1 \
                else len(self.parent.children) - 2
            view.hint_frame.move(self.parent.values[pos_in_parent].x, self.parent.values[pos_in_parent].y)
        return val_sum, counter

    def median(self, tab):
        view = self.tree.view
        length = len(self.values)
        for i in range(length):
            if not self.is_leaf:
                view.draw_exp_text(self, f'Go to {i}. child of node [{self.id}]: node [{self.children[i].id}]')
                view.hint_frame.move(self.children[i].values[0].x, self.children[i].values[0].y)
                tab = self.children[i].median(tab)
            if i != 0:
                view.hint_frame.move(self.values[i].x, self.values[i].y)
            view.draw_exp_text(self, f'Append {self.values[i].value} to tab {tab}')
            tab.append(self.values[i].value)
        if not self.is_leaf:
            view.draw_exp_text(self, f'Go to {length}. child of node [{self.id}]: node [{self.children[length].id}]')
            view.hint_frame.move(self.children[length].values[0].x, self.children[length].values[0].y)
            tab = self.children[length].median(tab)
        if self.parent is not None:
            pos_in_parent = self.parent.children.index(self) if self.parent.children.index(self) != len(
                self.parent.children) - 1 \
                else len(self.parent.children) - 2
            view.hint_frame.move(self.parent.values[pos_in_parent].x, self.parent.values[pos_in_parent].y)
        return tab

    def insert_specific(self, value, i):
        pass


class BTree(mb.BalTree):
    value_class = mb.BalValue
    node_class = BTNode

    def __deepcopy__(self, memo):
        cp = BTree(self.view, self.max_degree)
        cp.root = copy.deepcopy(self.root, memo)
        return cp

    def mean(self):
        if self.root is None:
            self.view.explanation.append(f'Tree is empty. Impossible to calculate mean of an empty tree')
        else:
            self.view.explanation.append(f'Calculate the mean value of the tree - traverse tree in order')
            self.view.hint_frame.draw(self.root.values[0].x, self.root.values[0].y)
            val_sum, counter = self.root.mean(0, 0)
            self.view.draw_exp_text(self.root, f'Whole tree traversed. '
                                               f'Mean = {val_sum}/{counter} = {val_sum / counter}')

    def median(self):
        if self.root is None:
            self.view.explanation.append(f'Tree is empty. Impossible to calculate median of an empty tree')
        else:
            self.view.explanation.append(f'Calculate the median of the tree - traverse tree in order')
            self.view.hint_frame.draw(self.root.values[0].x, self.root.values[0].y)
            tab = self.root.median([])
            self.view.draw_exp_text(self.root,
                                    f'Whole tree traversed. Values = {tab}. Median = {statistics.median(tab)}')
