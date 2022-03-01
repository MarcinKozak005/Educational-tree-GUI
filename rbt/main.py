import rbt.rbt_model as rbt
import rbt.rbt_view as v
import mvc_base.controller as c

view = v.RBTView(
    node_width=26,
    node_height=26,
    columns_to_skip=0
)

tree = rbt.RBTree(view)
controller = c.Controller(tree, view)
frame = view.create_GUI(controller)
