import redblack_tree.rbt_model as rbt
import redblack_tree.rbt_view as v
import redblack_tree.rbt_controller as c

view = v.View(
    node_size=26,
)

tree = rbt.RBTree(view)
controller = c.Controller(tree, view)
frame = view.create_GUI(controller)
