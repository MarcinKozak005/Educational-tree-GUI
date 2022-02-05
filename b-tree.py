class BTreeNode:
    def __init__(self, max_degree, is_leaf):
        self.max_degree = max_degree  # if max degree <3 then ...
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []

    def search(self, key):
        i = 0
        while i <= len(self.keys) and key > self.keys[i]:
            i += 1
        if i <= len(self.keys) and key == self.keys[i]:
            return self, i
        if self.is_leaf:
            return None
        else:
            return self.children[i].search(key)

    def split_child(self, i, y):
        """
        Splits y (i-th children of self) into self and z (new child of self with keys >)
        :param i: position of y in self.children
        :param y: children of self
        :return: returns nothing
        """
        z = BTreeNode(self.max_degree, y.is_leaf)
        # Rewrite keys. y to z
        for j in range(0, (self.max_degree - 1) // 2):
            if (y.max_degree + 1) // 2 <= len(y.keys) - 1:
                z.keys.insert(j, y.keys[(y.max_degree + 1) // 2])
                y.keys.pop((y.max_degree + 1) // 2)
        if not y.is_leaf:
            # Rewrite children. y to z
            for j in range(0, (self.max_degree + 1) // 2):
                if (y.max_degree + 1) // 2 <= len(y.children) - 1:
                    z.children.insert(j, y.children[(y.max_degree + 1) // 2])
                    y.children.pop((y.max_degree + 1) // 2)
        self.children.insert(i + 1, z)
        self.keys.insert(i, y.keys[len(y.keys) - 1])
        y.keys.pop(len(y.keys) - 1)

    def insert(self, k, prev=None, self_i=None):
        global btree_root
        i = 0
        if self.is_leaf:
            while i < len(self.keys) and k > self.keys[i]:
                i += 1
            self.keys.insert(i, k)
            # fixing
            if len(self.keys) == btree_root.max_degree:
                self.fixing(prev, self_i)
        elif not self.is_leaf:
            while i < len(self.keys) and k > self.keys[i]:
                i += 1
            self.children[i].insert(k, self, i)
            if len(self.keys) == btree_root.max_degree:
                self.fixing(prev, self_i)

    def fixing(self, prev, self_i):
        global btree_root
        if prev is not None:
            prev.split_child(self_i, self)
        else:
            s = BTreeNode(btree_root.max_degree, False)
            s.children.insert(0, btree_root)
            btree_root = s
            s.split_child(0, s.children[0])

    def print(self, indent=0):
        print('\t'*indent + f"{self.keys}")
        for c in self.children:
            c.print(indent+1)


btree_root = None
btree_root = BTreeNode(3, True)
numbers = [5, 4, 1, 9, 6, 3, 6, 8, 3, 1, 2, 5, 7]

# for x in numbers:
#     btree_root.insert(x)
#     print(f'Inserting {x}')
#     btree_root.print()
#     print('---')

for x in range(1, 15):
    btree_root.insert(x)
    btree_root.print()
    print('---')

print('asdas')
