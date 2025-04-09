from Gates.logicGateNode import LogicGateNode


class NorGateNode(LogicGateNode):
    """NOR gate node"""

    def __init__(self, scene):
        super().__init__(scene, "NOR Gate", "NOR")

    def update_value(self):
        """Perform NOR logic operation"""
        values = self.get_input_values()
        if len(values) >= 2:
            self.value = 0 if (values[0] or values[1]) else 1
            self.output_sockets[0].set_value(self.value)
            self.update_connected_nodes()