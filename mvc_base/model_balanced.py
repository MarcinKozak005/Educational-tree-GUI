import abc

import mvc_base.model_multi_child as mc


class BalValue(mc.MCValue):

    def __init__(self, value, parent_node, x=0, y=0):
        super().__init__(value, parent_node, x, y)


class BalTree(mc.MCTree, abc.ABC):
    value_class = BalValue


class BalNode(mc.MCNode, abc.ABC):

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
        self.insert_and_fix(value, i)

    def print_node(self, indent=0):
        print('\t' * indent + f'{self.values}')
        for c in self.children:
            c.print_node(indent + 1)

    @abc.abstractmethod
    def split_child(self, i, full_node):
        pass
