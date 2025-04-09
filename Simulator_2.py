from components.NodeEditor import NodeEditor
from components.nodeListItem import NodeListItem
from components.sockets.outputNode import OutputNode
from library import *
from theme.theme import THEMES, current_theme


class LogicNodesApp(QMainWindow):
    """Main window"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Logic Nodes")
        self.setGeometry(100, 100, 1200, 800)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create tab widget for multiple node editors
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        main_layout.addWidget(self.tab_widget)

        # Create menu bar
        self.create_menu_bar()

        # Create side panel with node list - do this BEFORE applying a theme
        self.create_side_panel()

        # Create first editor tab
        self.new_editor()

        # Apply theme - now the dock widget exists
        # self.apply_theme(current_theme)

    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_editor)
        file_menu.addAction(new_action)

        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu("Edit")

        undo_action = QAction("Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        # Undo functionality would be implemented here
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        # Redo functionality would be implemented here
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction("Cut", self)
        cut_action.setShortcut("Ctrl+X")
        # Cut functionality would be implemented here
        edit_menu.addAction(cut_action)

        copy_action = QAction("Copy", self)
        copy_action.setShortcut("Ctrl+C")
        # Copy functionality would be implemented here
        edit_menu.addAction(copy_action)

        paste_action = QAction("Paste", self)
        paste_action.setShortcut("Ctrl+V")
        # Paste functionality would be implemented here
        edit_menu.addAction(paste_action)

        delete_action = QAction("Delete", self)
        delete_action.setShortcut("Delete")
        # Add delete functionality handled by NodeEditor
        edit_menu.addAction(delete_action)

        # Window menu
        window_menu = menubar.addMenu("Window")

        theme_menu = window_menu.addMenu("Theme")

        # Theme actions
        # for theme_name in THEMES.keys():
        #     theme_action = QAction(theme_name, self)
        #     theme_action.triggered.connect(lambda checked, theme=theme_name: self.apply_theme(theme))
        #     theme_menu.addAction(theme_action)

    def create_side_panel(self):
        """Create the side panel with node list"""
        # Create dock widget
        dock = QDockWidget("Nodes", self)
        dock.setObjectName("NodesDock")
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        # Create widget for dock
        dock_widget = QWidget()
        dock_layout = QVBoxLayout(dock_widget)

        # Add node items
        node_items = [
            ("Input", "INPUT"),
            ("Output", "OUTPUT"),
            ("Output (Write)", "OUTPUT_WRITE"),
            ("AND Gate", "AND"),
            ("OR Gate", "OR"),
            ("NOT Gate", "NOT"),
            ("NAND Gate", "NAND"),
            ("NOR Gate", "NOR"),
            ("XOR Gate", "XOR"),
            ("XNOR Gate", "XNOR")
        ]

        for text, node_type in node_items:
            item = NodeListItem(text, node_type)
            dock_layout.addWidget(item)

        # Add stretch to bottom
        dock_layout.addStretch()

        # Set dock widget
        dock.setWidget(dock_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    def new_editor(self):
        """Create a new editor tab"""
        editor = NodeEditor()
        tab_index = self.tab_widget.addTab(editor, "Untitled")
        self.tab_widget.setCurrentIndex(tab_index)

        # Connect to handle custom events for output nodes
        # Use a direct connection to the handler, not a lambda
        editor.scene.selectionChanged.connect(self.handle_selection_change)

    def handle_selection_change(self):
        """Handle selection changes in the editor"""
        # Get the sender (scene) and find the editor
        scene = self.sender()
        if not scene:
            return

        # Find the editor that contains this scene
        editor = None
        for i in range(self.tab_widget.count()):
            tab_editor = self.tab_widget.widget(i)
            if hasattr(tab_editor, 'scene') and tab_editor.scene == scene:
                editor = tab_editor
                break

        if not editor:
            return

        for item in scene.selectedItems():
            if isinstance(item, OutputNode) and item.can_write:
                # Add a write button to the node if it doesn't have one
                if not hasattr(item, "write_button"):
                    button = QGraphicsTextItem("Save to file", item)
                    button.setPos(10, 70)
                    button.setDefaultTextColor(QColor(THEMES[current_theme]["text"]))
                    # Make interactive
                    button.setTextInteractionFlags(Qt.TextEditorInteraction)
                    # Store reference
                    item.write_button = button
                    # Use a safer way to connect the event
                    item.write_button.mousePressEvent = lambda event, node=item: self.write_output_to_file(node)

    def write_output_to_file(self, node):
        if isinstance(node, OutputNode) and node.can_write:
            filename, _ = QFileDialog.getSaveFileName(self, "Save Output", "", "Text Files (*.txt)")
            if filename:
                node.write_to_file(filename)

    def close_tab(self, index):
        # Get the editor before removing the tab
        editor = self.tab_widget.widget(index)

        # Disconnect signals if it's a NodeEditor
        if isinstance(editor, NodeEditor) and editor.scene:
            editor.scene.selectionChanged.disconnect()

        # Now remove the tab
        self.tab_widget.removeTab(index)

        # If no tabs left, create a new one
        if self.tab_widget.count() == 0:
            self.new_editor()

    def get_current_editor(self):
        current_widget = self.tab_widget.currentWidget()
        if isinstance(current_widget, NodeEditor):
            return current_widget
        return None

    def open_file(self):
        """Open a saved node editor file"""
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Logic Nodes Files (*.ln);;All Files (*)")
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)

                # Create new editor and load data
                editor = NodeEditor()
                editor.load_data(data)

                # Add as new tab
                tab_name = os.path.basename(filename)
                tab_index = self.tab_widget.addTab(editor, tab_name)
                self.tab_widget.setCurrentIndex(tab_index)

                # Connect selection handler
                editor.scene.selectionChanged.connect(lambda: self.handle_selection_change(editor))
            except Exception as e:
                print(f"Error opening file: {e}")

    def save_file(self):
        """Save the current editor state to a file"""
        editor = self.get_current_editor()
        if editor:
            filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Logic Nodes Files (*.ln);;All Files (*)")
            if filename:
                # Make sure it has the correct extension
                if not filename.endswith(".ln"):
                    filename += ".ln"

                try:
                    # Get data from editor
                    data = editor.get_data()

                    # Save to file
                    with open(filename, 'w') as f:
                        json.dump(data, f, indent=2)

                    # Update tab name
                    tab_name = os.path.basename(filename)
                    self.tab_widget.setTabText(self.tab_widget.currentIndex(), tab_name)
                except Exception as e:
                    print(f"Error saving file: {e}")

    # def apply_theme(self, theme_name):
    #     """Apply the selected theme to the application"""
    #     global current_theme
    #     if theme_name in THEMES:
    #         current_theme = theme_name
    #
    #         # Update application style
    #         self.setStyleSheet(f"""
    #                     QMainWindow, QWidget {{ background-color: {THEMES[current_theme]['window']}; color: {THEMES[current_theme]['text']}; }}
    #                     QTabWidget::pane {{ border: 1px solid {THEMES[current_theme]['panel']}; }}
    #                     QTabBar::tab {{ background-color: {THEMES[current_theme]['panel']}; color: {THEMES[current_theme]['text']};
    #                                    padding: 5px; border: 1px solid {THEMES[current_theme]['panel']}; }}
    #                     QTabBar::tab:selected {{ background-color: {THEMES[current_theme]['node']}; }}
    #                     QDockWidget {{ background-color: {THEMES[current_theme]['panel']}; color: {THEMES[current_theme]['text']}; }}
    #                     QMenuBar, QMenu {{ background-color: {THEMES[current_theme]['panel']}; color: {THEMES[current_theme]['text']}; }}
    #                     QAction {{ color: {THEMES[current_theme]['text']}; }}
    #                 """)
    #
    #         # Update side panel
    #         for i in range(self.findChild(QDockWidget, "").widget().layout().count()):
    #             item = self.findChild(QDockWidget, "").widget().layout().itemAt(i)
    #             if item and item.widget() and isinstance(item.widget(), NodeListItem):
    #                 item.widget().setStyleSheet(f"""
    #                             background-color: {THEMES[current_theme]['node']};
    #                             color: {THEMES[current_theme]['text']};
    #                             border: 1px solid {THEMES[current_theme]['text']};
    #                             border-radius: 5px;
    #                         """)
    #
    #         # Update editors
    #         for i in range(self.tab_widget.count()):
    #             editor = self.tab_widget.widget(i)
    #             if isinstance(editor, NodeEditor):
    #                 # Update view background
    #                 editor.setBackgroundBrush(QBrush(QColor(THEMES[current_theme]["window"])))
    #
    #                 # Update all nodes and wires
    #                 for item in editor.scene.items():
    #                     if isinstance(item, Node):
    #                         item.setPen(QPen(QColor(THEMES[current_theme]["text"]), 1))
    #                         item.setBrush(QBrush(QColor(THEMES[current_theme]["node"])))
    #
    #                         # Update text items
    #                         if hasattr(item, "title_item"):
    #                             item.title_item.setDefaultTextColor(QColor(THEMES[current_theme]["text"]))
    #                         if hasattr(item, "type_item"):
    #                             item.type_item.setDefaultTextColor(QColor(THEMES[current_theme]["text"]))
    #                         if hasattr(item, "output_value_item"):
    #                             item.output_value_item.setDefaultTextColor(QColor(THEMES[current_theme]["text"]))
    #                         if hasattr(item, "write_button"):
    #                             item.write_button.setDefaultTextColor(QColor(THEMES[current_theme]["text"]))
    #
    #                         # Update sockets
    #                         for socket in item.input_sockets + item.output_sockets:
    #                             socket.setPen(QPen(QColor(THEMES[current_theme]["socket"]), 1))
    #                             socket.setBrush(QBrush(QColor(THEMES[current_theme]["socket"])))
    #
    #                     elif isinstance(item, Wire):
    #                         if item.end_socket:
    #                             item.setPen(
    #                                 QPen(QColor(THEMES[current_theme]["wire_connected"]), 2, Qt.SolidLine, Qt.RoundCap,
    #                                      Qt.RoundJoin))
    #                         else:
    #                             item.setPen(QPen(QColor(THEMES[current_theme]["wire"]), 2, Qt.SolidLine, Qt.RoundCap,
    #                                              Qt.RoundJoin))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogicNodesApp()
    window.show()
    sys.exit(app.exec_())
