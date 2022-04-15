import abc
import math

import core.root as r
import mvc_base.model_multi_child as mc
from core.constants import hint_frame


class AggValue(mc.MCValue):

    def __init__(self, value, parent_node, x=0, y=0):
        super().__init__(value, parent_node, x, y)
        self.counter = 1


class LinkValue(AggValue):
    def __init__(self, value, parent_node, x=0, y=0):
        super().__init__(value, parent_node, x, y)
        self.prev_value = None
        self.next_value = None

    def rewrite(self):
        if self.prev_value is not None:
            self.prev_value.next_value = self.next_value
        if self.next_value is not None:
            self.next_value.prev_value = self.prev_value


class AggTree(mc.MCTree, abc.ABC):
    pass


class AggNode(mc.MCNode, abc.ABC):

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
        while i < len(self.values) and value.value > self.values[i].value:
            view.draw_exp_text(self.values[i], f'[{self.id}]: {value.value} > {self.values[i].value}, check next value',
                               False)
            view.hint_frame.move(self.values[i].x + view.node_width, self.values[i].y, True)
            i += 1
        # Value is already present in the tree
        if i < len(self.values) and value.value == self.values[i].value:
            view.draw_exp_text(self,
                               f'Increase counter of value ({self.values[i].value}) to {self.values[i].counter + 1}',
                               False)
            self.values[i].counter += 1
            return
        elif i < len(self.values):
            view.draw_exp_text(self.values[i], f'[{self.id}]: {value.value} < {self.values[i].value}, '
                                               f'insert before {self.values[i].value}', False)
            view.hint_frame.move(self.values[i].x - view.node_width // 2, self.values[i].y, True)
        else:
            view.draw_exp_text(self, f'No next value', False)
            view.hint_frame.move(self.values[-1].x + view.node_width // 2, self.values[-1].y, True)
        self.insert_and_fix(value, i)

    def delete_value(self, value):
        min_val_degree = math.ceil(self.tree.max_degree / 2) - 1
        values = [self.values[i].value for i in range(len(self.values))]
        counts = [self.values[i].counter for i in range(len(self.values))]
        view = self.tree.view
        if self.is_leaf and value in values:
            i = values.index(value)
            if counts[i] > 1:
                view.draw_exp_text(self.values[i], f'Reduce value counter by 1 to {self.values[i].counter - 1}')
                self.values[i].counter -= 1
            else:
                removed_node = self.values.pop(i)
                view.draw_exp_text(removed_node, f'Remove value {removed_node.value}')
                # Different destination y that usually, since [counter] below the node also needs to disappear
                view.move_object(removed_node.tag(), removed_node.x, removed_node.y,
                                 removed_node.x, -1.5 * view.node_height)
                self.fix_delete()
        elif value in values:
            i = values.index(value)
            if counts[i] > 1:
                view.draw_exp_text(self.values[i], f'Reduce value counter by 1 to {self.values[i].counter - 1}')
                self.values[i].counter -= 1
                return
            if len(self.children[i].values) > min_val_degree and self.children[i].is_leaf \
                    or not self.children[i].is_leaf:
                removed_node = self.values[i]
                view.draw_exp_text(removed_node, f'Remove value {removed_node.value}')
                # Different destination y that usually, since [counter] below the node also needs to disappear
                view.move_object(removed_node.tag(), removed_node.x, removed_node.y,
                                 removed_node.x, -1.5 * view.node_height)
                view.draw_exp_text(self.children[i], f'Find predecessor of {value} in [{self.children[i].id}] node')
                self.values[i], to_fix = self.children[i].predecessor()
                self.values[i].parent = self
                view.draw_exp_text(to_fix, f'Value {self.values[i].value} goes to node {self.id}')
                view.erase(f'Line{hash(removed_node)}')
                to_fix.fix_delete()
            elif len(self.children[i + 1].values) > min_val_degree and self.children[i + 1].is_leaf \
                    or not self.children[i + 1].is_leaf:
                removed_node = self.values[i]
                view.draw_exp_text(removed_node, f'Remove value {removed_node.value}')
                # Different destination y that usually, since [counter] below the node also needs to disappear
                view.move_object(removed_node.tag(), removed_node.x, removed_node.y,
                                 removed_node.x, -1.5 * view.node_height)
                view.draw_exp_text(self.children[i + 1],
                                   f'Find successor of {value} in [{self.children[i + 1].id}] node')
                self.values[i], to_fix = self.children[i + 1].successor()
                self.values[i].parent = self
                view.draw_exp_text(to_fix, f'Value {self.values[i].value} goes to node {self.id}')
                view.erase(f'Line{hash(removed_node)}')
                to_fix.fix_delete()
            else:
                view.draw_exp_text(self, f'Merge node [{self.children[i].id}] value {self.values[i].value} '
                                         f'and node [{self.children[i + 1].id}]')
                self.children[i].values.append(self.values[i])
                self.values[i].parent = self.children[i]
                for v in self.children[i + 1].values:
                    v.parent = self.children[i]
                    self.children[i].values.append(v)
                self.children[i].children.extend(self.children[i + 1].children)
                for c in self.children[i + 1].children:
                    c.parent = self.children[i]
                view.erase(f'Line{hash(self.values[i])}')
                self.values.pop(i)
                self.children.pop(i + 1)
                self.tree.update_positions()
                view.animate(self.tree.root)
                self.children[i].delete_value(value)
                self.fix_delete()
        # Search for a value to delete
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
            return None
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

    def print_node(self, indent=0):
        print('\t' * indent + f'{self.values}')
        for c in self.children:
            c.print_node(indent + 1)

    # AggNode specific methods below

    def split_child(self, i, full_node):
        """
        Splits full_node (i-th child of self) into self and new_node (new child of self with values >)
        :param i: position of full_node in self.children
        :param full_node: child of self
        :return: returns nothing
        """
        new_node = self.tree.node_class(self.tree, full_node.is_leaf, self.x, self.y)
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
        view.draw_exp_text(full_node, f'Values < {self.values[0].value} stay in [{full_node.id}] node')
        view.draw_exp_text(new_node, f'Values > {self.values[0].value} make new node [{new_node.id}]')
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

    def get_next(self, position, mode=r.Mode.value):
        """
        Get the next_value - such that after sorting values next_value would be just after self
        :param position: position of node/value we want to get next of
        :param mode: Mode.value or Mode.node
        :return: returns next_value or None if it's not found
        """

        def get_next_help(node):
            if node.parent is not None:
                return node.parent.get_next(node.parent.children.index(node), r.Mode.node)
            else:
                return None

        if mode == r.Mode.value:
            if self.is_leaf:
                if position + 1 < len(self.values):
                    return self.values[position + 1]
                # search in nodes above
                else:
                    return get_next_help(self)
            else:
                return self.children[position + 1].get_next(-1, r.Mode.value)
        elif mode == r.Mode.node:
            if position < len(self.values):
                return self.values[position]
            # search in nodes above
            else:
                return get_next_help(self)

    def get_prev(self, position, mode=r.Mode.value):
        """
        Get the prev_value - such that after sorting values prev_value would be just before self
        :param position: position of node/value we want to get next of
        :param mode: Mode.value or Mode.node
        :return: returns prev_value or None if it's not found
        """

        def get_prev_help(node):
            if node.parent is not None:
                return node.parent.get_prev(node.parent.children.index(node), r.Mode.node)
            else:
                return None

        if mode == r.Mode.value:
            if self.is_leaf:
                if position - 1 >= 0:
                    return self.values[position - 1]
                # search in nodes above
                else:
                    return get_prev_help(self)
            else:
                return self.children[position].get_prev(len(self.children[position].values), r.Mode.value)
        elif mode == r.Mode.node:
            if position != 0:
                return self.values[position - 1]
            # search in nodes above
            else:
                return get_prev_help(self)
