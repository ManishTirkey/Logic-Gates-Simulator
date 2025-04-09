from Gates.node import Node


class LogicGateNode(Node):
    """Base class for logic gate nodes"""

    def __init__(self, scene, title, node_type):
        super().__init__(scene, title, node_type)

        # Add 2 input sockets for most logic gates
        self.add_input_socket(0)
        self.add_input_socket(1)

        # Add 1 output socket
        self.add_output_socket()

        # Set initial value
        self.value = 0

    def get_input_values(self):
        """Get values from input sockets"""
        values = []
        for socket in self.input_sockets:
            values.append(socket.get_value())
        return values