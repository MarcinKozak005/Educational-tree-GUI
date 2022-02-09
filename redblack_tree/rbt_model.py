class RBTree:
    def __init__(self):
        self.root = None

    class RBNode:
        def __init__(self, x, y, val, l_edge, r_edge, parent):
            self.val = val
            self.left = RBTree.RBLeaf()
            self.right = RBTree.RBLeaf()
            self.parent = parent
            # Canvas visualization connected
            self.x = x  # x-position of the node
            self.y = y  # y-position of the node
            self.l_edge = l_edge  # edges for nice tree visualization
            self.r_edge = r_edge  # edges for nice tree visualization
            self.color = 'red'
            # Animation connected
            self.x_next = x
            self.y_next = y

        def __getitem__(self, item):
            if item == 'left':
                return self.left
            elif item == 'right':
                return self.right

        def __setitem__(self, key, value):
            if key == 'left':
                self.left = value
            elif key == 'right':
                self.right = value

        def successors(self):
            result = []
            if type(self.left) is RBTree.RBNode:
                result += self.left.successors()
            if type(self.right) is RBTree.RBNode:
                result += self.right.successors()
            result.append(self)
            return result

    # Model
    class RBLeaf:
        color = 'black'

        def __init__(self):
            pass
