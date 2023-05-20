# TODO: Support selections that are not rectangular
# TODO: Support non-8-bit color depth
from krita import *


def show_message(message):
    QMessageBox.information(QWidget(), "Layer finder", message)


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


class LayerFinderExtension(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction(
            "layerfinder", "Find layers colorizing the selection"
        )
        action.triggered.connect(self.run)

    def run(self):
        document = Krita.instance().activeDocument()

        if document is None:
            show_message("There is no active document")
            return

        selection = document.selection()

        self.recur(document.rootNode(), selection)

    def recur(self, node, selection):
        children = node.childNodes()

        if children:
            for child in children:
                self.recur(child, selection)
        else:
            if node_affects(node, selection):
                show_message("Layer {} affects the selection".format(node.name()))


Krita.instance().addExtension(LayerFinderExtension(Krita.instance()))
