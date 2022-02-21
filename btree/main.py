import btree.btree_model as bt
import btree.btree_view as v
import btree.btree_controller as c

view = v.View(
    node_size=38,
    node_height=17
)

tree = bt.BTree(3, view)
controller = c.Controller(tree, view)
frame = view.create_GUI(controller)
