from library import *
from theme.theme import THEMES, current_theme


class NodeListItem(QWidget):
    """Widget representing a node in the side panel"""

    def __init__(self, text, node_type, parent=None):
        super().__init__(parent)
        self.text = text
        self.node_type = node_type

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Set appearance
        self.setStyleSheet(
            f"background-color: {THEMES[current_theme]['node']}; color: {THEMES[current_theme]['text']}; border: 1px solid {THEMES[current_theme]['text']}; border-radius: 5px;")
        self.setMinimumHeight(40)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Start drag operation
            drag = QDrag(self)
            mime_data = QMimeData()

            # Store node type in mime data
            mime_data.setText(self.node_type)
            drag.setMimeData(mime_data)

            # Create thumbnail pixmap for drag
            pixmap = QPixmap(self.size())
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            self.render(painter)
            painter.end()
            drag.setPixmap(pixmap)

            # Set drag hot spot to cursor position
            drag.setHotSpot(event.pos())

            # Execute drag operation
            result = drag.exec_(Qt.CopyAction)

            # Prevent event propagation after drag
            event.accept()
        else:
            super().mousePressEvent(event)