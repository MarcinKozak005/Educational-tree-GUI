import avlt.avl_model as avlt
import avlt.avl_view as avltv
import rbt.rbt_model as rbt
import rbt.rbt_view as rbtv
import structures_comparison.controller_comparison as c
import structures_comparison.view_comparison as v

view = v.ComparisonView()
controller = c.ComparisonController(view)
frame = view.create_GUI(controller, 'Comparison')

avlt_view = avltv.AVLView(
    node_width=26,
    node_height=26,
    columns_to_skip=0
)
avlt_view.create_GUI(controller, '')
avlt_view.canvas_now = view.canvas_top
avlt_tree = avlt.AVLTree(avlt_view)
controller.top_tree = avlt_tree

rbt_view = rbtv.RBTView(
    node_width=26,
    node_height=26,
    columns_to_skip=0
)
rbt_view.create_GUI(controller, '')
rbt_view.canvas_now = view.canvas_bottom
rbt_tree = rbt.RBTree(rbt_view)
controller.bottom_tree = rbt_tree

# initial_max_degree = 3
# bt_view = btv.BTView(
#     node_width=24,
#     node_height=18,
#     columns_to_skip=0,
#     current_max_degree=initial_max_degree
# )
# bt_view.create_GUI(controller, '')
# bt_view.canvas_now = view.canvas_bottom
# bt_tree = bt.BTree(bt_view, initial_max_degree)
# controller.bottom_tree = bt_tree

# rbt_view.short_animation_time = 500
# rbt_view.long_animation_time = 1000
# avlt_view.short_animation_time = 500
# avlt_view.long_animation_time = 1000
# bt_view.short_animation_time = 500
# bt_view.long_animation_time = 1000
