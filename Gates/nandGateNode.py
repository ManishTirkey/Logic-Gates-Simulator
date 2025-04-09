from Gates.logicGateNode import LogicGateNode


class NandGateNode(LogicGateNode):
    """NAND gate node"""

    def __init__(self, scene):
        super().__init__(scene, "NAND Gate", "NAND")

    def update_value(self):
        """Perform NAND logic operation"""
        values = self.get_input_values()
        if len(values) >= 2:
            self.value = 0 if (values[0] and values[1]) else 1
            self.output_sockets[0].set_value(self.value)
            self.update_connected_nodes()