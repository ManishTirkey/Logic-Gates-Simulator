from library import *
from components.wire import Wire
from theme.theme import THEMES, current_theme


class Socket(QGraphicsEllipseItem):
    """Represents an input or output socket on a node"""

    def __init__(self, parent=None, is_input=True, socket_id=0):
        super().__init__(-6, -6, 12, 12, parent)
        self.is_input = is_input
        self.socket_id = socket_id
        self.node = parent
        self.wire = None
        self.value = 0  # 0 or 1 for binary logic

        # Set appearance
        self.setPen(QPen(QColor(THEMES[current_theme]["socket"]), 1))
        self.setBrush(QBrush(QColor(THEMES[current_theme]["socket"])))
        self.setAcceptHoverEvents(True)
        self.setZValue(2)

    def hoverEnterEvent(self, event):
        self.setPen(QPen(QColor(THEMES[current_theme]["wire_connected"]), 2))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setPen(QPen(QColor(THEMES[current_theme]["socket"]), 1))
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Create new wire or connect existing one
            view = self.scene().views()[0]
            if not view.temp_wire and not (self.is_input and self.wire):
                # Start new wire from this socket
                start_pos = self.scenePos()
                end_pos = event.scenePos()

                if self.is_input:
                    # Wires can't start from inputs
                    return

                view.temp_wire = Wire(self, None)
                view.temp_wire.setLine(start_pos.x(), start_pos.y(), end_pos.x(), end_pos.y())
                self.scene().addItem(view.temp_wire)
                view.wire_dragging = True
            elif view.temp_wire and self.is_input and not self.wire:
                # Connect wire to this input socket
                start_socket = view.temp_wire.start_socket
                if start_socket.node != self.node:  # Prevent connecting to same node
                    self.connect_wire(view.temp_wire)
                    view.wire_dragging = False
                    view.temp_wire = None

                    # Update values through the network
                    self.node.update_value()
            elif self.wire and self.is_input:
                # Disconnect existing wire
                wire = self.wire
                self.disconnect_wire()
                self.scene().removeItem(wire)

                # Update values through the network
                self.node.update_value()

        super().mousePressEvent(event)

    def connect_wire(self, wire):
        """Connect a wire to this socket"""
        if self.is_input and not self.wire:
            wire.end_socket = self
            wire.update_position()
            self.wire = wire
            return True
        return False

    def disconnect_wire(self):
        """Disconnect wire from this socket"""
        if self.wire:
            if self.is_input:
                self.wire.end_socket = None
            else:
                # Find all wires starting from this output
                for wire in self.scene().items():
                    if isinstance(wire, Wire) and wire.start_socket == self:
                        if wire.end_socket:
                            wire.end_socket.wire = None
                        wire.start_socket = None
                        wire.end_socket = None
                        self.scene().removeItem(wire)
            self.wire = None
            return True
        return False

    def get_value(self):
        """Get the current value of this socket"""
        if self.is_input:
            if self.wire and self.wire.start_socket:
                return self.wire.start_socket.get_value()
            return 0  # Default value if not connected
        else:
            return self.value

    def set_value(self, value):
        """Set the value of this socket"""
        self.value = 1 if value else 0

