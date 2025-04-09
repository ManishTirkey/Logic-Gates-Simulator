from Gates.node import Node
from library import *
from theme.theme import THEMES, current_theme


class OutputNode(Node):
    """Node that displays output from connected nodes"""

    def __init__(self, scene, can_write=False):
        title = "Output (Write)" if can_write else "Output"
        super().__init__(scene, title, "OUTPUT")
        self.can_write = can_write
        self.value = 0

        # Add input socket
        self.add_input_socket()

        # Add output display
        self.output_value_item = QGraphicsTextItem("0", self)
        self.output_value_item.setDefaultTextColor(QColor(THEMES[current_theme]["text"]))
        self.output_value_item.setPos(self.width // 2 - 5, 50)

        if can_write:
            # Additional height for write button (will be handled by node editor view)
            self.height = a = 100
            self.setRect(0, 0, self.width, self.height)

    def update_value(self):
        """Update the node's display value based on input"""
        if self.input_sockets:
            self.value = self.input_sockets[0].get_value()
            self.output_value_item.setPlainText(str(self.value))

    def write_to_file(self, filename):
        """Write the output value to a file"""
        if self.can_write:
            with open(filename, 'w') as f:
                f.write(f"Output value: {self.value}\n")
            return True
        return False
