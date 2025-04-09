from Gates.logicGateNode import LogicGateNode


class OrGateNode(LogicGateNode):
    """OR gate node"""

    def __init__(self, scene):
        super().__init__(scene, "OR Gate", "OR")

    def update_value(self):
        """Perform OR logic operation"""
        values = self.get_input_values()
        if len(values) >= 2:
            self.value = 1 if (values[0] or values[1]) else 0
            self.output_sockets[0].set_value(self.value)
            self.update_connected_nodes()