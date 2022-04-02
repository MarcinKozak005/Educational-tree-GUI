import asa_graph.asag_model as asag
import asa_graph.asag_view as v
import mvc_base.controller as c

initial_max_degree = 3

view = v.ASAGView(
    node_width=24,
    node_height=18,
    columns_to_skip=2,
    current_max_degree=initial_max_degree
)

graph = asag.ASAGraph(view, initial_max_degree)
controller = c.Controller(graph, view)
frame = view.create_GUI(controller, 'ASA-Graph+tree')
