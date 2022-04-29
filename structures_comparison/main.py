import structures_comparison.controller_comparison as c
import structures_comparison.view_comparison as v

view = v.ComparisonView()
controller = c.ComparisonController(view)
frame = view.create_GUI(controller, 'Comparison')
