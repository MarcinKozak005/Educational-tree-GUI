class BTree:
    def __init__(self, max_degree):
        if max_degree < 2:
            raise ValueError
        self.max_degree = max_degree
        self.root = self.BTreeNode(self, True)

    def insert_key(self, k):
        self.root.insert(k)

    def print_tree(self):
        self.root.print_node()

    def search(self, key):
        self.root.search(key)

    def delete_key(self, key):
        self.root.delete_key(key)

    class BTreeNode:
        def __init__(self, tree, is_leaf):
            self.tree = tree
            self.is_leaf = is_leaf
            self.keys = []
            self.children = []
            self.parent = None

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
                        full_node.children[split_point].parent = new_node
                        full_node.children.pop(split_point)
            self.children.insert(i + 1, new_node)
            new_node.parent = self
            # Move one key from full_node to self
            self.keys.insert(i, full_node.keys[len(full_node.keys) - 1])
            full_node.keys.pop(len(full_node.keys) - 1)

        def insert(self, k):
            """
            Inserts key k in the node or calls insert on child node to which k should be inserted
            :param k: inserted key
            :return: returns nothing
            """
            i = 0
            while i < len(self.keys) and k > self.keys[i]:
                i += 1
            if self.is_leaf:
                self.keys.insert(i, k)
            else:
                self.children[i].insert(k)
            if len(self.keys) == self.tree.max_degree:
                self.fix_insert()

        def fix_insert(self):
            """
            Fixes the node to make it obey max_degree constraint of b-trees
            :return: returns nothing
            """
            if self.parent is not None:
                self.parent.split_child(self.parent.children.index(self), self)
            else:
                s = BTree.BTreeNode(self.tree, False)
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
            if not self.keys:
                if self is self.tree.root:
                    self.tree.root = self.children[0]
                    return
                i = prev.children.index(self)
                if i - 1 >= 0 and len(prev.children[i - 1].keys) > 1:
                    self.keys.insert(0, prev.keys[i - 1])
                    prev.keys[i - 1] = prev.children[i - 1].keys[-1]
                    if prev.children[i - 1].children:
                        self.children.insert(0, prev.children[i - 1].children[-1])
                        prev.children[i - 1].children[-1].parent = self
                        prev.children[i - 1].children.pop()
                    prev.children[i - 1].keys.pop()
                elif i + 1 < len(prev.children) and len(prev.children[i + 1].keys) > 1:
                    self.keys.append(prev.keys[i])
                    prev.keys[i] = prev.children[i + 1].keys[0]
                    if prev.children[i + 1].children:
                        self.children.append(prev.children[i + 1].children[0])
                        prev.children[i + 1].children[0].parent = self
                        prev.children[i + 1].children.pop(0)
                    prev.children[i + 1].keys.pop(0)
                elif i - 1 >= 0 and len(prev.children[i - 1].keys) == 1:
                    prev.children[i - 1].keys.append(prev.keys[i - 1])
                    prev.children[i - 1].keys.extend(self.keys)
                    for n in self.children:
                        n.parent = prev.children[i - 1]
                    prev.children[i - 1].children.extend(self.children)
                    prev.keys.pop(i - 1)
                    prev.children.pop(i)
                elif i + 1 < len(prev.children) and len(prev.children[i + 1].keys) == 1:
                    self.keys.append(prev.keys[i])
                    self.keys.extend(prev.children[i + 1].keys)
                    for n in prev.children[i + 1].children:
                        n.parent = self
                    self.children.extend(prev.children[i + 1].children)
                    prev.keys.pop(i)
                    prev.children.pop(i + 1)
                else:
                    return
                prev.fix_delete()

        def delete_key(self, key):
            if self.is_leaf and key in self.keys:
                self.keys.remove(key)
                self.fix_delete()
            elif key in self.keys:
                i = self.keys.index(key)
                if len(self.children[i].keys) > 1:
                    self.keys[i], to_fix = self.children[i].predecessor()
                    to_fix.fix_delete()
                elif len(self.children[i + 1].keys) > 1:
                    self.keys[i], to_fix = self.children[i + 1].successor()
                    to_fix.fix_delete()
                else:
                    self.children[i].keys.append(key)
                    self.children[i].keys.extend(self.children[i + 1].keys)
                    self.children[i].children.extend(self.children[i + 1].children)
                    self.keys.remove(key)
                    self.children.pop(i + 1)
                    self.children[i].delete_key(key)
                    self.fix_delete()
            else:
                i = 0
                while i < len(self.keys) and key > self.keys[i]:
                    i += 1
                self.children[i].delete_key(key)

        def predecessor(self):
            """
            Searches for predecessor in the tree starting in self.
            Removes the predecessor!
            :return: predecessor, node from which predecessor was deleted
            """
            if self.is_leaf:
                return self.keys.pop(-1), self
            else:
                return self.children[-1].predecessor()

        def successor(self):
            """
            Searches for successor in the tree starting in self.
            Removes the successor!
            :return: successor, node from which successor was deleted
            """
            if self.is_leaf:
                return self.keys.pop(0), self
            else:
                return self.children[0].successor()

        def print_node(self, indent=0):
            print('\t' * indent + f"{self.keys}")
            for c in self.children:
                c.print_node(indent + 1)


t = BTree(3)
numbers = [5, 4, 1, 9, 6, 3, 6, 8, 3, 1, 2, 5, 7]
to_delete = [14, 1, 8, 4, 9, 3]

for x in range(1, 15):
    t.insert_key(x)
t.print_tree()

print("Deletion")
for x in to_delete:
    print('---')
    t.delete_key(x)
    t.print_tree()

w = BTree(3)
for x in [1, 2, 3]:
    w.insert_key(x)
w.print_tree()
print('---')
w.delete_key(2)
w.print_tree()
