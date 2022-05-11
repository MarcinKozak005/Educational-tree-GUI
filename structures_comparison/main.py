import avlt.avl_model as avlt
import avlt.avl_view as avltv
import rbt.rbt_model as rbt
import rbt.rbt_view as rbtv
import structures_comparison.controller_comparison as c
import structures_comparison.view_comparison as v

view = v.ComparisonView()
controller = c.ComparisonController(view)

rbt_view = rbtv.RBTView(
    node_width=26,
    node_height=26,
    columns_to_skip=0
)
rbt_view.create_GUI(controller, '')
rbt_view.canvas_now = view.canvas_top
rbt_tree = rbt.RBTree(rbt_view)
controller.top_tree = rbt_tree
view.animation_controller.view1 = rbt_view

avlt_view = avltv.AVLView(
    node_width=26,
    node_height=26,
    columns_to_skip=0
)
avlt_view.create_GUI(controller, '')
avlt_view.canvas_now = view.canvas_bottom
avlt_tree = avlt.AVLTree(avlt_view)
controller.bottom_tree = avlt_tree
view.animation_controller.view2 = avlt_view

frame = view.create_GUI(controller, 'Comparison')
rbt_view.canvas_now = view.canvas_top
avlt_view.canvas_now = view.canvas_bottom
