import avlt.avl_model as avlt
import avlt.avl_view as v
import mvc_base.controller as c


view = v.AVLView(
    node_width=26,
    node_height=26,
    columns_to_skip=0
)

tree = avlt.AVLTree(view)
controller = c.Controller(tree, view)
frame = view.create_GUI(controller)
