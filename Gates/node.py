from components.sockets.sockets import Socket
from components.wire import Wire
from library import *
from theme.theme import THEMES, current_theme


class Node(QGraphicsRectItem):
    """Base class for all node types"""

    def __init__(self, scene, title="Node", node_type="base"):
        super().__init__()
        self.scene = scene
        self.title = title
        self.node_type = node_type
        self.width = 140
        self.height = 100
        self.input_sockets = []
        self.output_sockets = []

        self.init_ui()

    def init_ui(self):
        # Set appearance
        self.setRect(0, 0, self.width, self.height)
        self.setPen(QPen(QColor(THEMES[current_theme]["text"]), 1))
        self.setBrush(QBrush(QColor(THEMES[current_theme]["node"])))
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)

        # Add title
        self.title_item = QGraphicsTextItem(self.title, self)
        self.title_item.setDefaultTextColor(QColor(THEMES[current_theme]["text"]))
        self.title_item.setPos(10, 5)

        # Add type label
        self.type_item = QGraphicsTextItem(self.node_type, self)
        self.type_item.setDefaultTextColor(QColor(THEMES[current_theme]["text"]))
        self.type_item.setPos(10, 25)
        font = QFont()
        font.setItalic(True)
        self.type_item.setFont(font)

    def add_input_socket(self, socket_id=0):
        """Add an input socket to the node"""
        socket = Socket(self, is_input=True, socket_id=socket_id)
        y_pos = 50 + socket_id * 20
        socket.setPos(0, y_pos)
        self.input_sockets.append(socket)

        # Add label
        label = QGraphicsTextItem(f"In {socket_id}", self)
        label.setDefaultTextColor(QColor(THEMES[current_theme]["text"]))
        label.setPos(15, y_pos - 7)

        return socket

    def add_output_socket(self, socket_id=0):
        """Add an output socket to the node"""
        socket = Socket(self, is_input=False, socket_id=socket_id)
        y_pos = 50 + socket_id * 20
        socket.setPos(self.width, y_pos)
        self.output_sockets.append(socket)

        # Add label
        label = QGraphicsTextItem(f"Out {socket_id}", self)
        label.setDefaultTextColor(QColor(THEMES[current_theme]["text"]))
        label.setPos(self.width - 50, y_pos - 7)

        return socket

    def update_connected_nodes(self):
        """Update nodes connected to this node's outputs"""
        for socket in self.output_sockets:
            for item in self.scene.items():
                if isinstance(item, Wire) and item.start_socket == socket and item.end_socket:
                    item.end_socket.node.update_value()

    def update_value(self):
        """Calculate and update the node's output value"""
        # To be implemented by subclasses
        pass

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange and hasattr(self, 'scene'):
            # Update wires when node is moved
            for socket in self.input_sockets + self.output_sockets:
                if socket.wire:
                    socket.wire.update_position()

                # Also update wires that start from this socket
                if not socket.is_input:
                    for item in self.scene.items():
                        if isinstance(item, Wire) and item.start_socket == socket:
                            item.update_position()

        return super().itemChange(change, value)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Bring node to front
            self.setZValue(10)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Return to normal z-value
            self.setZValue(0)
        super().mouseReleaseEvent(event)
