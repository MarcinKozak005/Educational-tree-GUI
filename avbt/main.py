import avbt.avbt_model as avbt
import avbt.avbt_view as v
import mvc_base.controller as c

initial_max_degree = 3

view = v.AVBTView(
    node_width=24,
    node_height=18,
    columns_to_skip=2,
    current_max_degree=initial_max_degree
)

tree = avbt.AVBTree(view, initial_max_degree)
controller = c.Controller(tree, view)
frame = view.create_GUI(controller, 'AVB-tree')
