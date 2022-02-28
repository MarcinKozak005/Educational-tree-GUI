import btree.btree_model as bt
import btree.btree_view as v
import btree.btree_controller as c

initial_max_degree = 3

view = v.BTView(
    node_width=24,
    node_height=18,
    columns_to_skip=2,
    current_max_degree=initial_max_degree
)

tree = bt.BTree(initial_max_degree, view)
controller = c.Controller(tree, view)
frame = view.create_GUI(controller)
