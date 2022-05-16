import copy
import statistics

import mvc_base.model_aggregated as ma


class AVBTNode(ma.AggNode):

    def min(self):
        view = self.tree.view
        view.explanation.append(f'Search the minimal value of the tree')
        curr = self.tree.root
        view.hint_frame.draw(curr.values[0].x, curr.values[0].y)
        while not curr.is_leaf:
            view.draw_exp_text(curr, f'Node [{curr.id}] has children. Search for min value in 0. child')
            view.hint_frame.move(curr.children[0].x, curr.children[0].y)
            curr = curr.children[0]
        view.draw_exp_text(curr, f'Node [{curr.id}] has no children. '
                                 f'It\'s first value {curr.values[0].value} is the min value of the tree')

    def max(self):
        view = self.tree.view
        view.explanation.append(f'Search the maximal value of the tree')
        curr = self.tree.root
        view.hint_frame.draw(curr.values[-1].x, curr.values[-1].y)
        while not curr.is_leaf:
            view.draw_exp_text(curr, f'Node [{curr.id}] has children. Search for max value in last child')
            view.hint_frame.move(curr.children[-1].x, curr.children[-1].y)
            curr = curr.children[-1]
        view.draw_exp_text(curr, f'Node [{curr.id}] has no children. '
                                 f'It\'s last value {curr.values[-1].value} is the max value of the tree')

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
            view.draw_exp_text(self, f'Add {self.values[i].value} ({self.values[i].counter} times) to sum {val_sum} '
                                     f'and increase counter {counter} by {self.values[i].counter}')
            val_sum += self.values[i].value * self.values[i].counter
            counter += self.values[i].counter
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
            view.draw_exp_text(self, f'Append {self.values[i].value} ({self.values[i].counter} times) to tab {tab}')
            tab.extend(self.values[i].counter * [self.values[i].value])
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


class AVBTree(ma.AggTree):
    value_class = ma.AggValue
    node_class = AVBTNode

    def __deepcopy__(self, memo):
        cp = AVBTree(self.view, self.max_degree)
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
