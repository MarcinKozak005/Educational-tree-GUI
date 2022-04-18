import copy
import statistics

import mvc_base.model_aggregated as ma


class AVBPTNode(ma.AggNode):
    class_node_id = ord('@')  # distinguishes nodes by using letters

    def __init__(self, tree, is_leaf, x, y):
        super().__init__(tree, is_leaf, x, y)
        self.prev_value = None
        self.next_value = None

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


class AVBPTree(ma.AggTree):
    value_class = ma.LinkAggValue
    node_class = AVBPTNode

    def __deepcopy__(self, memo):
        cp = AVBPTree(self.view, self.max_degree)
        cp.root = copy.deepcopy(self.root, memo)
        return cp

    def mean(self):
        if self.root is None:
            self.view.explanation.append(f'Tree is empty. Impossible to calculate mean of an empty tree')
        else:
            self.view.explanation.append(f'Calculate the mean value of the tree - traverse leaves')
            successors = self.root.successors()
            values = []
            for s in successors:
                if type(s) is ma.AggValue:
                    values.append(s)
            self.view.hint_frame.draw(values[0].x, values[0].y)
            val_sum = 0
            counter = 0
            values.sort(key=lambda x: x.value)
            for v in values:
                if v != values[0]:
                    self.view.hint_frame.move(v.x, v.y)
                self.view.draw_exp_text(v, f'Add {v.value}x{v.counter} to sum {val_sum} '
                                           f'and increase counter {counter} by {v.counter}')
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
                if type(s) is ma.AggValue:
                    values.append(s)
            self.view.hint_frame.draw(values[0].x, values[0].y)
            tab = []
            values.sort(key=lambda x: x.value)
            for v in values:
                if v != values[0]:
                    self.view.hint_frame.move(v.x, v.y)
                self.view.draw_exp_text(v, f'Append {v.value} ({v.counter} times) to tab {tab}')
                tab.append([v.value] * v.counter)
            self.view.draw_exp_text(self.root, f'Whole tree traversed. Values = {tab}. '
                                               f'Median = {statistics.median(tab)}')
