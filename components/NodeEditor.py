from Gates.andGateNode import AndGateNode
from Gates.nandGateNode import NandGateNode
from Gates.node import Node
from Gates.norGateNode import NorGateNode
from Gates.notGateNode import NotGateNode
from Gates.orGateNode import OrGateNode
from Gates.xnorGateNode import XnorGateNode
from Gates.xorGateNode import XorGateNode
from components.sockets.inputNode import InputNode
from components.sockets.outputNode import OutputNode
from components.wire import Wire
from library import *
from theme.theme import THEMES, current_theme


class NodeEditor(QGraphicsView):
    """Main node editor view"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # drag and drop
        self.setAcceptDrops(True)

        # Wire dragging state
        self.wire_dragging = False
        self.temp_wire = None

        # Setup view
        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)

        # Draw grid in background
        self.setBackgroundBrush(QBrush(QColor(THEMES[current_theme]["window"])))

        # Store nodes for saving/loading
        self.nodes = []

    def clear_scene(self):
        """Clear the scene and reset state"""
        # Remove all items
        self.scene.clear()
        self.nodes = []
        self.wire_dragging = False
        self.temp_wire = None

    def create_node(self, node_type, pos=None):
        """Create a new node of the specified type"""
        if pos is None:
            pos = QPointF(self.width() / 2, self.height() / 2)

        node = None
        if node_type == "INPUT":
            node = InputNode(self.scene)
        elif node_type == "OUTPUT":
            node = OutputNode(self.scene, can_write=False)
        elif node_type == "OUTPUT_WRITE":
            node = OutputNode(self.scene, can_write=True)
        elif node_type == "AND":
            node = AndGateNode(self.scene)
        elif node_type == "OR":
            node = OrGateNode(self.scene)
        elif node_type == "NOT":
            node = NotGateNode(self.scene)
        elif node_type == "NAND":
            node = NandGateNode(self.scene)
        elif node_type == "NOR":
            node = NorGateNode(self.scene)
        elif node_type == "XOR":
            node = XorGateNode(self.scene)
        elif node_type == "XNOR":
            node = XnorGateNode(self.scene)

        if node:
            node.setPos(pos)
            self.scene.addItem(node)
            self.nodes.append(node)
            return node

        return None

    def dragEnterEvent(self, event):
        """Handle drag enter event"""
        if event.mimeData().hasText():
            event.setAccepted(True)
            event.acceptProposedAction()
        else:
            event.setAccepted(False)

    def dragMoveEvent(self, event):
        """Handle drag move event"""
        if event.mimeData().hasText():
            event.setAccepted(True)
            event.acceptProposedAction()
        else:
            event.setAccepted(False)

    def dropEvent(self, event):
        """Handle drop event"""
        if event.mimeData().hasText():
            # Get the node type from mime data
            node_type = event.mimeData().text()

            # Convert the drop position to scene coordinates
            pos = self.mapToScene(event.pos())

            # Create the node at the drop position
            self.create_node(node_type, pos)

            # Accept the drop action
            event.acceptProposedAction()

            # Debug
            print(f"Node of type {node_type} created at position {pos.x()}, {pos.y()}")

        # Ensure the event is marked as handled
        event.accept()

    def mouseMoveEvent(self, event):
        if self.wire_dragging and self.temp_wire:
            # Update temp wire endpoint while dragging
            scene_pos = self.mapToScene(event.pos())
            line = self.temp_wire.line()
            self.temp_wire.setLine(line.x1(), line.y1(), scene_pos.x(), scene_pos.y())

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.wire_dragging:
            if self.temp_wire:
                # If wire was not connected to an input, remove it
                pass
            # handle the wire connection

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:

            # Delete selected items
            # add latter key-event
            # debugging adding global key event

            print("trying to delete the selected item")

            for item in self.scene.selectedItems():
                if isinstance(item, Node):
            # Remove connected wires first
                    pass


    def wheelEvent(self, event):
        # Zoom in/out with mouse wheel
        zoom_factor = 1.2

        if event.angleDelta().y() > 0:
            # Zoom in
            self.scale(zoom_factor, zoom_factor)
        else:
            # Zoom out
            self.scale(1 / zoom_factor, 1 / zoom_factor)

    def get_data(self):
        """Get serializable data for saving"""
        data = {
            "nodes": [],
            "connections": []
        }

        # Save nodes
        for i, node in enumerate(self.nodes):
            node_data = {
                "id": i,
                "type": node.node_type,
                "pos": [node.pos().x(), node.pos().y()],
            }

            # Save additional data for input nodes
            if node.node_type == "INPUT":
                node_data["value"] = node.value

            data["nodes"].append(node_data)

        # Save connections
        for node in self.nodes:
            node_id = self.nodes.index(node)

            for i, socket in enumerate(node.input_sockets):
                if socket.wire and socket.wire.start_socket:
                    start_node = socket.wire.start_socket.node
                    start_socket_id = start_node.output_sockets.index(socket.wire.start_socket)
                    start_node_id = self.nodes.index(start_node)

                    connection = {
                        "from_node": start_node_id,
                        "from_socket": start_socket_id,
                        "to_node": node_id,
                        "to_socket": i
                    }

                    data["connections"].append(connection)

        return data

    def load_data(self, data):
        """Load from serialized data"""
        self.clear_scene()

        # Create nodes
        nodes_map = {}  # Map saved node IDs to actual node objects

        for node_data in data["nodes"]:
            node = self.create_node(node_data["type"], QPointF(node_data["pos"][0], node_data["pos"][1]))
            nodes_map[node_data["id"]] = node

            # Load additional data for input nodes
            if node_data["type"] == "INPUT" and "value" in node_data:
                node.set_value(str(node_data["value"]))

        # Create connections
        # make connection latter

        # needs to debug

        # for conn in data["connections"]:
        #     from_node = nodes_map.get(conn["from_node"])
        #     to_node = nodes_map.get(conn["to_node"])
        #
        #     if from_node and to_node:
        #         # Create wire between nodes
        #         try:
        #             from_socket = from_node.output_sockets[conn["from_socket"]]
        #             to_socket = to_node.input_sockets[conn["to_socket"]]
        #
        #             wire = Wire(from_socket, to_socket)
        #             self.scene.addItem(wire)
        #
        #             # Update socket references
        #             to_socket.wire = wire
        #
        #             # Update values
        #             to_node.update_value()
        #         except IndexError:
        #             print("Error: Socket index out of range")
        #
        # # Update all nodes
        # for node in self.nodes:
        #     node.update_value()
