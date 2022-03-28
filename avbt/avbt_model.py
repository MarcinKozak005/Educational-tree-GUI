import mvc_base.model_aggregated as ma


class AVBTNode(ma.AggNode):
    class_node_id = ord('@')  # distinguishes nodes by using letters


class AVBTree(ma.AggTree):
    node_class = AVBTNode
