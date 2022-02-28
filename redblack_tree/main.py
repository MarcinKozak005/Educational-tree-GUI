import redblack_tree.rbt_model as rbt
import redblack_tree.rbt_view as v
import redblack_tree.rbt_controller as c

view = v.RBView(
    node_width=26,
    node_height=26,
    columns_to_skip=0
)

tree = rbt.RBTree(view)
controller = c.Controller(tree, view)
frame = view.create_GUI(controller)
