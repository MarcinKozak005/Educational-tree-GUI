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

        def print_node(self, indent=0):
            print('\t'*indent + f"{self.keys}")
            for c in self.children:
                c.print_node(indent+1)


btree_root = BTree(3)
numbers = [5, 4, 1, 9, 6, 3, 6, 8, 3, 1, 2, 5, 7]

# for x in numbers:
#     btree_root.insert(x)
#     print(f'Inserting {x}')
#     btree_root.print()
#     print('---')

for x in range(1, 15):
    btree_root.insert_key(x)
    btree_root.print_tree()
    print('---')

