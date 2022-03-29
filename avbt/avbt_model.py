import statistics

import mvc_base.model_aggregated as ma


class AVBTNode(ma.AggNode):
    class_node_id = ord('@')  # distinguishes nodes by using letters

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

    def mean(self, val_sum=None, counter=None):
        view = self.tree.view
        length = len(self.values)
        for i in range(length):
            if not self.is_leaf:
                view.draw_exp_text(self, f'Go to {i}. child of node [{self.id}]: node [{self.children[i].id}]')
                view.hint_frame.move(self.children[i].values[0].x, self.children[i].values[0].y)
                val_sum, counter = self.children[i].mean(val_sum, counter)
            if i != 0:
                view.hint_frame.move(self.values[i].x, self.values[i].y)
            view.draw_exp_text(self, f'Add {self.values[i].value}x{self.values[i].counter} to sum {val_sum} '
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

    def median(self, tab=None):
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


class AVBTree(ma.AggTree):
    node_class = AVBTNode

    def min(self):
        if self.root is None:
            self.view.explanation.append(f'Tree is empty. Impossible to calculate min of an empty tree')
        else:
            self.root.min()

    def max(self):
        if self.root is None:
            self.view.explanation.append(f'Tree is empty. Impossible to calculate max of an empty tree')
        else:
            self.root.max()

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
