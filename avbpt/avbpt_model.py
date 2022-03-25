import mvc_base.model_aggregated as ma


class AVBPTNode(ma.AggNode):
    class_node_id = ord('@')  # distinguishes nodes by using letters

    def in_order(self):
        if self.is_leaf:
            return self.values
        else:
            result = []
            for i in range(len(self.values)):
                result += self.children[i].in_order()
                result.append(self.values[i])
            result += self.children[i + 1].in_order()
            return result


class AVBPTree(ma.AggTree):
    node_class = AVBPTNode
