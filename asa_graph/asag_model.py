import math
import statistics

import mvc_base.model_aggregated as ma


class ASAGNode(ma.AggNode):
    class_node_id = ord('@')  # distinguishes nodes by using letters

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
                removed_node.rewrite()
                self.fix_delete()
        elif value in values:
            i = values.index(value)
            if counts[i] > 1:
                view.draw_exp_text(self.values[i], f'Reduce value counter by 1 to {self.values[i].counter - 1}')
                self.values[i].counter -= 1
                return
            # No None handling cause each non leaf node always has prev and next
            removed_node = self.values[i]
            prev_val = removed_node.prev_value
            prev_val_parent = prev_val.parent
            next_val = removed_node.next_value
            next_val_parent = next_val.parent
            removed_node.rewrite()
            if len(prev_val_parent.values) > min_val_degree:
                view.draw_exp_text(removed_node, f'Remove value {removed_node.value}')
                # Different destination y that usually, since [counter] below the node also needs to disappear
                view.move_object(removed_node.tag(), removed_node.x, removed_node.y,
                                 removed_node.x, -1.5 * view.node_height)
                view.draw_exp_text(prev_val_parent, f'Move value {prev_val.value} to [{self.id}] node')
                self.values[i] = prev_val
                self.values[i].parent = self
                prev_val_parent.values.remove(prev_val)
                view.draw_exp_text(prev_val_parent, f'Fix [{prev_val_parent.id}] node')
                view.erase(f'Line{hash(removed_node)}')
                prev_val_parent.fix_delete()
            elif len(next_val_parent.values) > min_val_degree:
                view.draw_exp_text(removed_node, f'Remove value {removed_node.value}')
                # Different destination y that usually, since [counter] below the node also needs to disappear
                view.move_object(removed_node.tag(), removed_node.x, removed_node.y,
                                 removed_node.x, -1.5 * view.node_height)
                view.draw_exp_text(next_val_parent, f'Move value {next_val.value} to [{self.id}] node')
                self.values[i] = next_val
                self.values[i].parent = self
                next_val_parent.values.remove(next_val)
                view.draw_exp_text(next_val_parent, f'Fix [{next_val_parent.id}] node')
                view.erase(f'Line{hash(removed_node)}')
                next_val_parent.fix_delete()
            elif len(prev_val_parent.values) == min_val_degree:
                view.draw_exp_text(removed_node, f'Remove value {removed_node.value}')
                # Different destination y that usually, since [counter] below the node also needs to disappear
                view.move_object(removed_node.tag(), removed_node.x, removed_node.y,
                                 removed_node.x, -1.5 * view.node_height)
                view.draw_exp_text(prev_val_parent, f'Move value {prev_val.value} to [{self.id}] node')
                self.values[i] = prev_val
                self.values[i].parent = self
                prev_val_parent.values.remove(prev_val)
                view.draw_exp_text(prev_val_parent, f'Fix [{prev_val_parent.id}] node')
                view.erase(f'Line{hash(removed_node)}')
                prev_val_parent.fix_delete()
            elif len(next_val_parent.values) == min_val_degree:
                view.draw_exp_text(removed_node, f'Remove value {removed_node.value}')
                # Different destination y that usually, since [counter] below the node also needs to disappear
                view.move_object(removed_node.tag(), removed_node.x, removed_node.y,
                                 removed_node.x, -1.5 * view.node_height)
                view.draw_exp_text(prev_val_parent, f'Move value {next_val.value} to [{self.id}] node')
                self.values[i] = next_val
                self.values[i].parent = self
                next_val_parent.values.remove(next_val)
                view.draw_exp_text(next_val_parent, f'Fix [{next_val_parent.id}] node')
                view.erase(f'Line{hash(removed_node)}')
                next_val_parent.fix_delete()
            else:
                view.draw_exp_text(self, f'Merge node [{prev_val_parent.id}] value {self.values[i].value} '
                                         f'and node [{next_val_parent.id}]')
                prev_val_parent.values.append(self.values[i])
                self.values[i].parent = prev_val_parent
                for v in next_val_parent.values:
                    v.parent = prev_val_parent
                    prev_val_parent.values.append(v)
                prev_val_parent.children.extend(next_val_parent.children)
                for c in next_val_parent.children:
                    c.parent = prev_val_parent
                view.erase(f'Line{hash(self.values[i])}')
                self.values.pop(i)
                # self.children.pop(i + 1)
                self.tree.update_positions()
                view.animate(self.tree.root)
                prev_val_parent.delete_value(value)
                self.fix_delete()
        # Search for a value to delete
        else:
            i = 0
            while i < len(self.values) and value > self.values[i].value:
                i += 1
            self.children[i].delete_value(value)

    def fix_delete(self):
        """
        Fixes the tree after the deletion operation.
        :return: returns nothing
        """
        min_val_degree = math.ceil(self.tree.max_degree / 2) - 1
        prev = self.parent
        next_to_fix = prev
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
            elif self is self.tree.root and len(self.values) + 1 == len(self.children):
                return
            if len(self.values) > min_val_degree or self.is_leaf:
                prev_val = self.get_prev(0)
                next_val = self.get_next(0)
                prev2_val = None if prev_val is None else prev_val.prev_value
                next2_val = None if next_val is None else next_val.next_value
                prev_val_parent = None if prev_val is None else prev_val.parent
                next_val_parent = None if next_val is None else next_val.parent
                # Cases with node
                if prev_val is not None and prev2_val is not None and len(prev2_val.parent.values) > min_val_degree:
                    tmp = prev_val_parent == prev2_val.parent
                    i = prev_val_parent.values.index(prev_val)
                    view.draw_exp_text(self,
                                       f'Rewrite value {prev_val.value} from [{prev_val_parent.id}] to [{self.id}]')
                    self.values.insert(0, prev_val)
                    prev_val.parent = self
                    prev_val_parent.values.remove(prev_val)
                    self.update_positions()
                    view.animate(self.tree.root)
                    if not tmp:
                        view.draw_exp_text(prev_val_parent, f'Too much children compared to values. '
                                                            f'Rewrite {prev2_val.value} from '
                                                            f'[{prev2_val.parent.id}] to [{prev_val_parent.id}]')
                        prev_val_parent.values.insert(i, prev2_val)
                        prev2_val.parent.values.remove(prev2_val)
                        next_to_fix = prev2_val.parent
                        prev2_val.parent = prev_val_parent
                elif next_val is not None and next2_val is not None and len(next2_val.parent.values) > min_val_degree:
                    tmp = next_val_parent == next2_val.parent
                    i = next_val_parent.values.index(next_val)
                    view.draw_exp_text(self, f'Rewrite value {next_val.value} from [{prev.id}] to [{self.id}]')
                    self.values.append(next_val)
                    next_val.parent = self
                    next_val_parent.values.remove(next_val)
                    self.update_positions()
                    view.animate(self.tree.root)
                    if not tmp:
                        view.draw_exp_text(next_val_parent, f'Too much children compared to values. '
                                                            f'Rewrite {next2_val.value} from '
                                                            f'[{next2_val.parent.id}] to [{next_val_parent.id}]')
                        next_val_parent.values.insert(i, next2_val)
                        next2_val.parent.values.remove(next2_val)
                        next_to_fix = next2_val.parent
                        next2_val.parent = next_val_parent
                elif prev_val is not None and prev2_val is not None and len(prev2_val.parent.values) == min_val_degree \
                        and self.parent == prev2_val.parent.parent:
                    i = prev_val_parent.values.index(prev_val)
                    view.draw_exp_text(prev, f'Rewrite value {prev_val.value} '
                                             f'from [{prev_val_parent.id}] to [{prev2_val.parent.id}]')
                    prev2_val.parent.values.append(prev_val)
                    prev_val.parent = prev2_val.parent
                    view.draw_exp_text(self, f'Rewrite values and children from [{self.id}] to [{prev2_val.parent.id}]')
                    for n in self.children:
                        n.parent = prev2_val.parent
                    prev2_val.parent.children.extend(self.children)
                    for v in self.values:
                        v.parent = prev2_val.parent
                        prev2_val.parent.values.append(v)
                    view.draw_exp_text(self, f'Delete [{self.id}] node')
                    view.erase(self.tag())
                    prev_val_parent.values.pop(i)
                    self.parent.children.remove(self)
                    next_to_fix = prev_val_parent
                elif next_val is not None and next2_val is not None and len(next2_val.parent.values) == min_val_degree \
                        and self.parent == next2_val.parent.parent:
                    i = next_val_parent.values.index(next_val)
                    view.draw_exp_text(prev, f'Rewrite value {next_val.value} '
                                             f'from [{next_val_parent.id}] to [{next2_val.parent.id}]')
                    next2_val.parent.values.insert(0, next_val)
                    next_val.parent = next2_val.parent
                    view.draw_exp_text(self, f'Rewrite values and children from [{self.id}] to [{next2_val.parent.id}]')
                    for c in reversed(self.children):
                        next2_val.parent.children.insert(0, c)
                        c.parent = next2_val.parent
                    for v in reversed(self.values):
                        v.parent = next2_val.parent
                        next2_val.parent.values.insert(0, v)
                    view.draw_exp_text(self, f'Delete [{self.id}] node')
                    view.erase(self.tag())
                    next_val_parent.values.pop(i)
                    self.parent.children.remove(self)
                    next_to_fix = next_val_parent
                else:
                    return
            # len(self.values) <= min_degree
            elif prev is not None:
                i = prev.children.index(self)
                if i - 1 >= 0 and len(prev.children[i - 1].values) > min_val_degree:
                    view.draw_exp_text(self,
                                       f'Rewrite value {prev.values[i - 1].value} from [{prev.id}] to [{self.id}]')
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
                    view.draw_exp_text(self,
                                       f'Rewrite values and children from [{self.id}] to [{prev.children[i - 1].id}]')
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
                    view.draw_exp_text(self,
                                       f'Rewrite values and children from [{self.id}] to [{prev.children[i + 1].id}]')
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
            if next_to_fix is not None:
                next_to_fix.fix_delete()

    def in_order(self):
        if self.is_leaf:
            return self.values
        else:
            result = []
            i = 0
            for i in range(len(self.values)):
                result += self.children[i].in_order()
                result.append(self.values[i])
            result += self.children[i + 1].in_order()
            return result

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
        view = self.tree.view
        next_value = self.get_next(i)
        prev_value = self.get_prev(i)
        value.next_value = next_value
        value.prev_value = prev_value
        if prev_value is not None:
            prev_value.next_value = value
        if next_value is not None:
            next_value.prev_value = value
        view.draw_exp_text(self, f'Update next neighbour connections: '
                                 f'next([{value.value}]) is [{None if next_value is None else next_value.value}] and '
                                 f'prev([{value.value}]) is [{None if prev_value is None else prev_value.value}]')


class ASAGraph(ma.AggTree):
    value_class = ma.LinkValue
    node_class = ASAGNode

    def mean(self):
        if self.root is None:
            self.view.explanation.append(f'Tree is empty. Impossible to calculate mean of an empty tree')
        else:
            curr_node = self.root
            while not curr_node.is_leaf:
                curr_node = curr_node.children[0]
            curr_val = curr_node.values[0]
            counter, val_sum = 0, 0
            while True:
                self.view.hint_frame.draw(curr_val.x, curr_val.y)
                self.view.draw_exp_text(curr_val, f'Add {curr_val.value}x{curr_val.counter} to sum {val_sum} '
                                                  f'and increase counter {counter} by {curr_val.counter}')
                val_sum += curr_val.value * curr_val.counter
                counter += curr_val.counter
                if curr_val.next_value is not None:
                    self.view.hint_frame.move(curr_val.next_value.x, curr_val.next_value.y)
                    curr_val = curr_val.next_value
                else:
                    break
            self.view.draw_exp_text(curr_val, f'Whole tree traversed. Mean = {val_sum}/{counter} = {val_sum / counter}')

    def median(self):
        view = self.view
        if self.root is None:
            view.explanation.append(f'Tree is empty. Impossible to calculate median of an empty tree')
        else:
            curr_node = self.root
            while not curr_node.is_leaf:
                curr_node = curr_node.children[0]
            curr_val = curr_node.values[0]
            tab = []
            while True:
                view.hint_frame.draw(curr_val.x, curr_val.y)
                view.draw_exp_text(curr_val, f'Append {curr_val.value} ({curr_val.counter} times) to tab {tab}')
                tab.append(curr_val.value)
                if curr_val.next_value is not None:
                    view.hint_frame.move(curr_val.next_value.x, curr_val.next_value.y)
                    curr_val = curr_val.next_value
                else:
                    break
            view.draw_exp_text(curr_val, f'Whole tree traversed. Values = {tab}. Median = {statistics.median(tab)}')
