from Gates.node import Node
from library import *


class InputNode(Node):
    """Node with a text input for manual value entry"""

    def __init__(self, scene):
        super().__init__(scene, "Input", "INPUT")
        self.value = 0

        # Adjust height for the input field
        self.height = 80
        self.setRect(0, 0, self.width, self.height)

        # Add output socket
        self.add_output_socket()

        # Add input field (will be handled by the node editor view)
        self.input_value_item = QGraphicsTextItem("0", self)
        self.input_value_item.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.input_value_item.setPos(self.width // 2 - 10, 50)

    def set_value(self, value):
        """Set the node's value from UI interaction"""
        try:
            self.value = int(value)
            # Ensure it's binary
            self.value = 1 if self.value else 0
            self.input_value_item.setPlainText(str(self.value))

            # Update output socket
            if self.output_sockets:
                self.output_sockets[0].set_value(self.value)

            # Update connected nodes
            self.update_connected_nodes()
        except ValueError:
            # Reset to previous value if invalid input
            self.input_value_item.setPlainText(str(self.value))

    def update_value(self):
        """Update the output value based on the input field"""
        try:
            self.value = int(self.input_value_item.toPlainText())
            # Ensure it's binary
            self.value = 1 if self.value else 0

            # Update output socket
            if self.output_sockets:
                self.output_sockets[0].set_value(self.value)

            # Update connected nodes
            self.update_connected_nodes()
        except ValueError:
            # Reset to default value if invalid input
            self.value = 0
            self.input_value_item.setPlainText("0")

            if self.output_sockets:
                self.output_sockets[0].set_value(0)

            self.update_connected_nodes()