from Gates.node import Node


class NotGateNode(Node):
    """NOT gate node"""

    def __init__(self, scene):
        super().__init__(scene, "NOT Gate", "NOT")

        # Add 1 input socket
        self.add_input_socket(0)

        # Add 1 output socket
        self.add_output_socket()

        # Set initial value
        self.value = 0

    def update_value(self):
        """Perform NOT logic operation"""
        if self.input_sockets:
            input_value = self.input_sockets[0].get_value()
            self.value = 1 if not input_value else 0
            self.output_sockets[0].set_value(self.value)
            self.update_connected_nodes()