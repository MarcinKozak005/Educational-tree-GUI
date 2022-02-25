class BTree:
    def __init__(self, max_degree, view):
        if max_degree < 2:
            raise ValueError
        self.max_degree = max_degree
        self.root = None
        self.view = view

    def insert_value(self, value):
        if self.root is None:
            self.root = BTree.BTreeNode(self, True, self.view.width // 2, self.view.y_space, 0, self.view.width)
            self.view.explanation.append(f'Tree is empty')
            self.root.values.append(BTree.BTreeNode.BValue(value, self.root))
            self.view.explanation.append(f'Added value {value} in node [{self.root.id}]')
        else:
            view = self.view
            view.explanation.append(f'Tree is not empty, looking for insert place for {value}')
            view.canvas_now.create_rectangle(self.root.x - view.node_width // 2,
                                             self.root.y - view.node_height // 2 - view.y_above,
                                             self.root.x + view.node_width // 2,
                                             self.root.y + view.node_height // 2 - view.y_above,
                                             fill='red', tags=f'grey_node')
            view.canvas_now.create_text(self.root.x, self.root.y - view.y_above, fill='white',
                                        text=value, tags=f'grey_node')
            self.root.insert(BTree.BTreeNode.BValue(value, None, self.root.x, self.root.y - view.y_above))
        self.root.update_positions(True)

    def print_tree(self):
        self.root.print_node()

    def search_value(self, value):
        if self.root is None:
            self.view.explanation.append(f'Tree is empty. Value cannot be found')
        else:
            self.root.search_value(value)

    def delete_value(self, value):
        self.root.delete_value(value)

    def update_positions(self, static=False, width=None):
        if self.root is not None:
            self.root.update_positions(static, width)

    class BTreeNode:

        class_node_id = 64

        @staticmethod
        def get_id():
            BTree.BTreeNode.class_node_id += 1
            return chr(BTree.BTreeNode.class_node_id)

        def __init__(self, tree, is_leaf, x, y, l_edge, r_edge):
            self.tree = tree
            self.is_leaf = is_leaf
            self.values = []
            self.children = []
            self.parent = None
            # Canvas visualization connected
            self.x = x  # x-position of the node
            self.y = y  # y-position of the node
            self.l_edge = l_edge  # edges for nice visualization
            self.r_edge = r_edge  # edges for nice visualization
            self.x_next = x
            self.y_next = y
            self.id = self.get_id()

        def search_value(self, value):
            """
            Searches for value in the node
            :param value: searched value
            :return: if found: tuple (node_with_value, position_of_value_in_node),
                     else None
            """
            i = 0
            self.tree.view.canvas_now.create_rectangle(self.values[0].x - self.tree.view.node_width // 2,
                                                       self.values[0].y - self.tree.view.node_height // 2,
                                                       self.values[0].x + self.tree.view.node_width // 2,
                                                       self.values[0].y + self.tree.view.node_height // 2,
                                                       outline='red', tags='hint_frame')
            while i < len(self.values) and value > self.values[i].value:
                self.tree.view.draw_exp_text(self.values[i],
                                             f'[{self.id}]: {value} > {self.values[i].value}, check next value',
                                             False)
                self.tree.view.move_object('hint_frame', self.values[i].x, self.values[i].y,
                                           self.values[i].x + self.tree.view.node_width, self.values[i].y)
                i += 1
            if i < len(self.values) and value == self.values[i].value:
                self.tree.view.draw_exp_text(self, f'Value found')
                self.tree.view.canvas_now.delete('hint_frame')
                return self, i
            if self.is_leaf:
                self.tree.view.draw_exp_text(self, f'Value not found')
                self.tree.view.canvas_now.delete('hint_frame')
                return None
            else:
                if i < len(self.values):
                    self.tree.view.draw_exp_text(self.values[i],
                                                 f'[{self.id}]: {value} < {self.values[i].value}, search in [{self.children[i].id}]',
                                                 False)
                else:
                    self.tree.view.draw_exp_text(self, f'No next value', False)
                    self.tree.view.move_object('hint_frame', self.values[i - 1].x + self.tree.view.node_width,
                                               self.values[i - 1].y, self.values[i - 1].x,
                                               self.values[i - 1].y)
                    self.tree.view.draw_exp_text(self,
                                                 f'Search value in a children node [{self.children[i].id}] of [{self.id}]',
                                                 False)
                self.tree.view.move_object('hint_frame', self.values[i - 1].x, self.values[i - 1].y,
                                           self.children[i].values[0].x, self.children[i].values[0].y)
                return self.children[i].search_value(value)

        def split_child(self, i, full_node):
            """
            Splits full_node (i-th children of self) into self and new_node (new child of self with values >)
            :param i: position of full_node in self.children
            :param full_node: children of self
            :return: returns nothing
            """
            new_node = BTree.BTreeNode(self.tree, full_node.is_leaf, self.x, self.y, 0, 0)
            md = self.tree.max_degree
            split_point = (md + 1) // 2
            # Rewrite values: full_node to new_node
            self.tree.view.draw_exp_text(full_node,
                                         f'Rewrite values and children > {full_node.values[split_point - 1].value}'
                                         f' from [{full_node.id}] to [{new_node.id}]'
                                         f' and {full_node.values[split_point - 1].value} to [{self.id}]')
            for j in range(0, (md - 1) // 2):
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
            self.tree.view.animate_values_movement(self.tree.root)

        def insert(self, value):
            """
            Inserts value in the node or calls insert on child node to which value should be inserted
            :param value: inserted value
            :return: returns nothing
            """
            i = 0
            self.tree.view.canvas_now.create_rectangle(self.values[0].x - self.tree.view.node_width // 2,
                                                       self.values[0].y - self.tree.view.node_height // 2,
                                                       self.values[0].x + self.tree.view.node_width // 2,
                                                       self.values[0].y + self.tree.view.node_height // 2,
                                                       outline='red', tags='hint_frame')
            while i < len(self.values) and value.value > self.values[i].value:
                self.tree.view.draw_exp_text(self.values[i],
                                             f'[{self.id}]: {value.value} > {self.values[i].value}, check next value',
                                             False)
                self.tree.view.move_object('hint_frame', self.values[i].x, self.values[i].y,
                                           self.values[i].x + self.tree.view.node_width, self.values[i].y)
                i += 1
            if i < len(self.values):
                self.tree.view.draw_exp_text(self.values[i],
                                             f'[{self.id}]: {value.value} < {self.values[i].value}, insert to previous',
                                             False)
            else:
                self.tree.view.draw_exp_text(self, f'No next value', False)
            if self.is_leaf:
                self.values.insert(i, value)
                value.x = self.x
                value.y = self.y - self.tree.view.y_above
                self.values[i].parent = self
                self.tree.view.move_object('hint_frame', self.values[i - 1].x + self.tree.view.node_width,
                                           self.values[i - 1].y, self.values[i - 1].x + self.tree.view.node_width // 2,
                                           self.values[i - 1].y)
                self.tree.view.draw_exp_text(self,
                                             f'Node [{self.id}] is a leaf. Inserting {value.value} in the node [{self.id}]',
                                             False)
                self.tree.update_positions()
                self.tree.view.animate_values_movement(self)
            else:
                self.tree.view.move_object('hint_frame', self.values[i - 1].x + self.tree.view.node_width,
                                           self.values[i - 1].y, self.values[i - 1].x + self.tree.view.node_width // 2,
                                           self.values[i - 1].y)
                self.tree.view.draw_exp_text(self,
                                             f'Insert value to a children node [{self.children[i].id}] of [{self.id}]',
                                             False)
                self.tree.view.canvas_now.delete('hint_frame')
                self.tree.view.move_object('grey_node', self.x, self.y, self.children[i].x, self.children[i].y)
                self.children[i].insert(value)
            if len(self.values) == self.tree.max_degree:
                self.tree.view.canvas_now.delete('hint_frame')
                self.tree.view.draw_exp_text(self,
                                             f'Number of values in [{self.id}] == max b-tree degree. Start fixing')
                self.fix_insert()

        def fix_insert(self):
            """
            Fixes the node to make it obey max_degree constraint of b-trees
            :return: returns nothing
            """
            if self.parent is not None:
                self.parent.split_child(self.parent.children.index(self), self)
            else:
                self.tree.view.draw_exp_text(self, f'Root has too much values. Create new root and split old one')
                s = BTree.BTreeNode(self.tree, False, self.tree.view.width // 2, self.tree.view.y_space, 0,
                                    self.tree.view.width)
                s.children.insert(0, self.tree.root)
                self.tree.root.parent = s
                self.tree.root = s
                s.split_child(0, s.children[0])

        def fix_delete(self):
            """
            Fixes the tree after the deletion operation.
            :return: returns nothing
            """
            prev = self.parent
            if not self.values:
                if self is self.tree.root:
                    self.tree.root = self.children[0]
                    return
                i = prev.children.index(self)
                if i - 1 >= 0 and len(prev.children[i - 1].values) > 1:
                    self.values.insert(0, prev.values[i - 1])
                    prev.values[i - 1] = prev.children[i - 1].values[-1]
                    if prev.children[i - 1].children:
                        self.children.insert(0, prev.children[i - 1].children[-1])
                        prev.children[i - 1].children[-1].parent = self
                        prev.children[i - 1].children.pop()
                    prev.children[i - 1].values.pop()
                elif i + 1 < len(prev.children) and len(prev.children[i + 1].values) > 1:
                    self.values.append(prev.values[i])
                    prev.values[i] = prev.children[i + 1].values[0]
                    if prev.children[i + 1].children:
                        self.children.append(prev.children[i + 1].children[0])
                        prev.children[i + 1].children[0].parent = self
                        prev.children[i + 1].children.pop(0)
                    prev.children[i + 1].values.pop(0)
                elif i - 1 >= 0 and len(prev.children[i - 1].values) == 1:
                    prev.children[i - 1].values.append(prev.values[i - 1])
                    prev.children[i - 1].values.extend(self.values)
                    for n in self.children:
                        n.parent = prev.children[i - 1]
                    prev.children[i - 1].children.extend(self.children)
                    prev.values.pop(i - 1)
                    prev.children.pop(i)
                elif i + 1 < len(prev.children) and len(prev.children[i + 1].values) == 1:
                    self.values.append(prev.values[i])
                    self.values.extend(prev.children[i + 1].values)
                    for n in prev.children[i + 1].children:
                        n.parent = self
                    self.children.extend(prev.children[i + 1].children)
                    prev.values.pop(i)
                    prev.children.pop(i + 1)
                else:
                    return
                prev.fix_delete()

        def delete_value(self, value):
            if self.is_leaf and value in self.values:
                self.values.remove(value)
                self.fix_delete()
            elif value in self.values:
                i = self.values.index(value)
                if len(self.children[i].values) > 1:
                    self.values[i], to_fix = self.children[i].predecessor()
                    to_fix.fix_delete()
                elif len(self.children[i + 1].values) > 1:
                    self.values[i], to_fix = self.children[i + 1].successor()
                    to_fix.fix_delete()
                else:
                    self.children[i].values.append(value)
                    self.children[i].values.extend(self.children[i + 1].values)
                    self.children[i].children.extend(self.children[i + 1].children)
                    self.values.remove(value)
                    self.children.pop(i + 1)
                    self.children[i].delete_value(value)
                    self.fix_delete()
            else:
                i = 0
                while i < len(self.values) and value > self.values[i]:
                    i += 1
                self.children[i].delete_value(value)

        def predecessor(self):
            """
            Searches for predecessor in the tree starting in self.
            Removes the predecessor!
            :return: predecessor, node from which predecessor was deleted
            """
            if self.is_leaf:
                return self.values.pop(-1), self
            else:
                return self.children[-1].predecessor()

        def successor(self):
            """
            Searches for successor in the tree starting in self.
            Removes the successor!
            :return: successor, node from which successor was deleted
            """
            if self.is_leaf:
                return self.values.pop(0), self
            else:
                return self.children[0].successor()

        def print_node(self, indent=0):
            print('\t' * indent + f"{self.values}")
            for c in self.children:
                c.print_node(indent + 1)

        def update_positions(self, static=False, width=None):
            """
            Updates the node's positions
            :param static: True means there will be no animation, False means there will be an animation
            :param width: width of canvas for updating positions
            :return: returns nothing
            """
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
                self.values[i].x_next = \
                    self.x_next - len(self.values) * self.tree.view.node_width // 2 + \
                    self.tree.view.node_width // 2 + i * self.tree.view.node_width
                self.values[i].y_next = self.y_next
            # Node

            # Node end?
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
            # Nodes and values
            result = []
            for c in self.children:
                result += c.successors()
            result.append(self)
            result += self.values
            return result

        class BValue:
            def __init__(self, value, parent_node=None, x=0, y=0):
                self.value = value
                self.parent = parent_node
                self.x = x
                self.y = y
                # Animation connected
                self.x_next = 0
                self.y_next = 0

# Code below was used to test b-tree (model) behaviour before the addition of GUI/View
# if __name__ == "__main__":
#     t = BTree(3)
#     numbers = [5, 4, 1, 9, 6, 3, 6, 8, 3, 1, 2, 5, 7]
#     to_delete = [14, 1, 8, 4, 9, 3]
#
#     for _ in range(1, 15):
#         t.insert_value(_)
#     t.print_tree()
#
#     print("Deletion")
#     for _ in to_delete:
#         print('---')
#         t.delete_value(_)
#         t.print_tree()
#
#     w = BTree(3)
#     for _ in [1, 2, 3]:
#         w.insert_value(_)
#     w.print_tree()
#     print('---')
#     w.delete_value(2)
#     w.print_tree()
