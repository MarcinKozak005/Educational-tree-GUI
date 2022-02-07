class BTree:
    def __init__(self, max_degree):
        self.max_degree = max_degree  # errors with wrong max_degree
        self.root = self.BTreeNode(self, True)

    def insert_key(self, k):
        self.root.insert(k)

    def print_tree(self):
        self.root.print_node()

    def search(self, key):
        self.root.search(key)

    def delete(self, key):
        self.root.delete(key)

    class BTreeNode:
        def __init__(self, tree, is_leaf):
            self.tree = tree
            self.is_leaf = is_leaf
            self.keys = []
            self.children = []

        def search(self, key):
            """
            Searches for key in the node
            :param key: searched key
            :return: if found: tuple (node_with_key, position_of_key_in_node),
                     else None
            """
            i = 0
            while i <= len(self.keys) and key > self.keys[i]:
                i += 1
            if i <= len(self.keys) and key == self.keys[i]:
                return self, i
            if self.is_leaf:
                return None
            else:
                return self.children[i].search(key)

        def split_child(self, i, full_node):
            """
            Splits full_node (i-th children of self) into self and z (new child of self with keys >)
            :param i: position of full_node in self.children
            :param full_node: children of self
            :return: returns nothing
            """
            new_node = BTree.BTreeNode(self.tree, full_node.is_leaf)
            md = self.tree.max_degree
            split_point = (md + 1) // 2
            # Rewrite keys: full_node to new_node
            for j in range(0, (md - 1) // 2):
                if split_point < len(full_node.keys):
                    new_node.keys.insert(j, full_node.keys[split_point])
                    full_node.keys.pop(split_point)
            if not full_node.is_leaf:
                # Rewrite children: full_node to new_node
                for j in range(0, split_point):
                    if split_point < len(full_node.children):
                        new_node.children.insert(j, full_node.children[split_point])
                        full_node.children.pop(split_point)
            self.children.insert(i + 1, new_node)
            # Move one key from full_node to self
            self.keys.insert(i, full_node.keys[len(full_node.keys) - 1])
            full_node.keys.pop(len(full_node.keys) - 1)

        def insert(self, k, prev=None, self_i=None):
            """
            Inserts key k in the node or calls insert on child node to which k should be inserted
            :param k: inserted key
            :param prev: parent of self
            :param self_i: position of self in children list of prev
            :return: returns nothing
            """
            i = 0
            while i < len(self.keys) and k > self.keys[i]:
                i += 1
            if self.is_leaf:
                self.keys.insert(i, k)
            else:
                self.children[i].insert(k, self, i)
            if len(self.keys) == self.tree.max_degree:
                self.fixing(prev, self_i)

        def fixing(self, prev, self_i):
            """
            Fixes the node to make it obey max_degree constraint of b-trees
            :param prev: parent of self
            :param self_i: position of self in children list of prev
            :return: returns nothing
            """
            if prev is not None:
                prev.split_child(self_i, self)
            else:
                s = BTree.BTreeNode(self.tree, False)
                s.children.insert(0, self.tree.root)
                self.tree.root = s
                s.split_child(0, s.children[0])

        def delete(self, key):
            # 1
            if self.is_leaf and key in self.keys:
                self.keys.remove(key)
            # 2
            elif key in self.keys:
                i = self.keys.index(key)
                # a
                if len(self.children[i].keys) > 1:
                    self.keys[i] = self.children[i].predecessor()
                    self.children[i].delete(self.keys[i])
                # b
                elif len(self.children[i + 1].keys) > 1:
                    self.keys[i] = self.children[i + 1].successor()
                    self.children[i + 1].delete(self.keys[i])
                # c
                else:
                    self.children[i].keys.append(key)
                    self.children[i].keys.extend(self.children[i + 1].keys)
                    self.children[i].children.extend(self.children[i + 1].children)
                    self.keys.remove(key)
                    self.children.pop(i + 1)
                    self.children[i].delete(key)
            # 3
            else:
                i = 0
                while i < len(self.keys) and key > self.keys[i]:
                    i += 1
                # a
                if len(self.children[i].keys) > 1:
                    self.children[i].delete(key)
                elif len(self.children[i].keys) == 1 and \
                        i - 1 >= 0 and len(self.children[i - 1].keys) > 1:
                    self.children[i].keys.insert(0, self.keys[i - 1])
                    self.keys[i - 1] = self.children[i - 1].keys[-1]
                    if self.children[i - 1].children:
                        self.children[i].children.insert(0, self.children[i - 1].children[-1])
                        self.children[i - 1].children.pop()
                    self.children[i - 1].keys.pop()
                    self.children[i].delete(key)
                elif len(self.children[i].keys) == 1 and \
                        i + 1 < len(self.children) and len(self.children[i + 1].keys) > 1:
                    self.children[i].keys.append(self.keys[i])
                    self.keys[i] = self.children[i + 1].keys[0]
                    if self.children[i + 1].children:
                        self.children[i].children.append(self.children[i + 1].children[0])
                        self.children[i + 1].children.pop(0)
                    self.children[i + 1].keys.pop(0)
                    self.children[i].delete(key)
                # b
                elif len(self.children[i].keys) == 1 and \
                        i - 1 >= 0 and len(self.children[i - 1].keys) == 1:
                    self.children[i - 1].keys.append(self.keys[i - 1])
                    self.children[i - 1].keys.extend(self.children[i].keys)
                    self.children[i - 1].children.extend(self.children[i].children)
                    self.keys.pop(i - 1)
                    self.children.pop(i)
                    self.children[i - 1].delete(key)
                elif len(self.children[i].keys) == 1 and \
                        i + 1 < len(self.children) and len(self.children[i + 1].keys) == 1:
                    self.children[i].keys.append(self.keys[i])
                    self.children[i].keys.extend(self.children[i + 1].keys)
                    self.children[i].children.extend(self.children[i + 1].children)
                    self.keys.pop(i)
                    self.children.pop(i + 1)
                    self.children[i].delete(key)

        def predecessor(self):
            if self.is_leaf:
                return self.keys[-1]
            else:
                return self.children[-1].predecessor()

        def successor(self):
            if self.is_leaf:
                return self.keys[0]
            else:
                return self.children[0].successor()

        def print_node(self, indent=0):
            print('\t' * indent + f"{self.keys}")
            for c in self.children:
                c.print_node(indent + 1)


tree = BTree(3)
numbers = [5, 4, 1, 9, 6, 3, 6, 8, 3, 1, 2, 5, 7]
to_delete = [14, 1, 8, 4, 9, 3]

# for x in numbers:
#     btree_root.insert(x)
#     print(f'Inserting {x}')
#     btree_root.print()
#     print('---')

for x in range(1, 15):
    tree.insert_key(x)
tree.print_tree()
print("Deletion")
for x in to_delete:
    print('---')
    tree.delete(x)
    tree.print_tree()
