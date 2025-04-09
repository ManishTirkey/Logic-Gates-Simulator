from library import *
from theme.theme import THEMES, current_theme


class Wire(QGraphicsLineItem):
    """Represents a connection between two sockets"""

    def __init__(self, start_socket=None, end_socket=None):
        super().__init__()
        self.start_socket = start_socket
        self.end_socket = end_socket

        # Set appearance
        self.setPen(QPen(QColor(THEMES[current_theme]["wire"]), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        self.setZValue(1)

        # Update position based on sockets
        self.update_position()

    def update_position(self):
        """Update the wire's position based on connected sockets"""
        if self.start_socket:
            start_pos = self.start_socket.scenePos()

            if self.end_socket:
                end_pos = self.end_socket.scenePos()
                self.setPen(
                    QPen(QColor(THEMES[current_theme]["wire_connected"]), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            else:
                end_pos = self.line().p2()

            self.setLine(start_pos.x(), start_pos.y(), end_pos.x(), end_pos.y())
