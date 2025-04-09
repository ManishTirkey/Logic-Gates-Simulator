from Gates.logicGateNode import LogicGateNode


class XnorGateNode(LogicGateNode):
    """XNOR gate node"""

    def __init__(self, scene):
        super().__init__(scene, "XNOR Gate", "XNOR")

    def update_value(self):
        """Perform XNOR logic operation"""
        values = self.get_input_values()
        if len(values) >= 2:
            self.value = 1 if (values[0] == values[1]) else 0
            self.output_sockets[0].set_value(self.value)
            self.update_connected_nodes()