import redblack_tree.rbt_model as rbt
import redblack_tree.rbt_view as v
import redblack_tree.rbt_controller as c

view = v.View(
    width=800,
    height=300,
    y_space=50,
    y_above=30,
    node_size=26,
    animation_time=1500,
    animation_unit=10,
    layout='double',
)

tree = rbt.RBTree(view)
controller = c.Controller(tree, view)
frame = view.create_GUI(controller, tree)
