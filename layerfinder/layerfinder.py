# TODO: Support selections that are not rectangular
# TODO: Support non-8-bit color depth
from PyQt5.QtWidgets import *
from krita import *


def node_affects(node, selection):
    assert not node.childNodes()

    if not node.visible():
        return False

    if node.opacity() == 0:
        return False

    (sx, sy, sw, sh) = (
        selection.x(),
        selection.y(),
        selection.width(),
        selection.height(),
    )

    selectionRect = QRect(sx, sy, sw, sh)

    rect = node.bounds()

    overlappinf = rect.intersected(selectionRect)

    (ox, oy, ow, oh) = (
        overlappinf.x(),
        overlappinf.y(),
        overlappinf.width(),
        overlappinf.height(),
    )

    bytes = node.pixelData(ox, oy, ow, oh)

    for i in range(0, bytes.size(), 4):
        chunk = tuple([ord(x) for x in bytes[i : i + 4]])

        if chunk[3] != 0:
            return True

    return False


class LayerFinderDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layer finder")

        self.label = QLabel("")

        self.find_button = QPushButton("Find")
        self.find_button.clicked.connect(self.run)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.find_button)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setWidget(self.widget)

    def createActions(self, window):
        action = window.createAction(
            "layerfinder", "Find layers colorizing the selection"
        )
        action.triggered.connect(self.run)

    def run(self):
        document = Krita.instance().activeDocument()

        if document is None:
            self.show_message("There is no active document")
            return

        selection = document.selection()

        layers = self.find_layers(document.rootNode(), selection)

        names = [self.track_parents(layer) for layer in layers]

        if names:
            self.show_message("Layers:\n" + "\n".join(names))
        else:
            self.show_message("No layers found")

    def canvasChanged(self, canvas):
        pass

    def find_layers(self, node, selection):
        layers = []

        children = node.childNodes()

        if children:
            for child in children:
                layers += self.find_layers(child, selection)
        else:
            if node_affects(node, selection):
                layers = [node]

        return layers

    def show_message(self, message):
        self.label.setText(message)

    def track_parents(self, node):
        s = node.name()

        while (
            node.parentNode() and node != Krita.instance().activeDocument().rootNode()
        ):
            node = node.parentNode()
            s = node.name() + " --> " + s

        return s


Krita.instance().addDockWidgetFactory(
    DockWidgetFactory("layerfinder", DockWidgetFactoryBase.DockRight, LayerFinderDocker)
)
