# TODO: Support selections that are not rectangular
# TODO: Support non-8-bit color depth
from PyQt5.QtWidgets import *
from krita import *

NO_LABEL = 0
GREEN_LABEL = 2


def unset_all_blue_labels():
    document = Krita.instance().activeDocument()

    if document is None:
        return

    def recurse(node):
        if node.colorLabel() == GREEN_LABEL:
            node.setColorLabel(NO_LABEL)

        children = node.childNodes()

        if children:
            for child in children:
                recurse(child)

    recurse(document.rootNode())


def set_color_labels_recursively(node):
    node.setColorLabel(GREEN_LABEL)

    if node.parentNode() and node != Krita.instance().activeDocument().rootNode():
        set_color_labels_recursively(node.parentNode())


def list_layers_colorizing_selection():
    document = Krita.instance().activeDocument()

    if document is None:
        return []

    selection = document.selection()

    if selection is None:
        return []

    return LayerFinder(document, selection).find_layers()


class LayerFinder:
    def __init__(self, document, selection):
        self.document = document
        self.selection = selection

        assert self.document is not None
        assert self.selection is not None

    def find_layers(self):
        def recurse(node):
            children = node.childNodes()

            if children and node.visible():
                return [x for child in children for x in recurse(child)]
            elif not children and self.node_affects(node):
                return [node]
            else:
                return []

        return recurse(self.document.rootNode())

    def node_affects(self, node):
        return ColorizingNodeChecker(node, self.selection).is_colorizing()


class ColorizingNodeChecker:
    def __init__(self, node, selection):
        self.node = node
        self.selection = selection

        assert not self.node.childNodes()

    def is_colorizing(self):
        return (
            self.node.visible()
            and self.node.opacity() != 0
            and self.overlapping_region_has_opaque_pixels()
        )

    def overlapping_region_has_opaque_pixels(self):
        overlapping = self.overlapping_region()

        (ox, oy, ow, oh) = (
            overlapping.x(),
            overlapping.y(),
            overlapping.width(),
            overlapping.height(),
        )

        bytes = self.node.pixelData(ox, oy, ow, oh)

        for i in range(0, bytes.size(), 4):
            chunk = tuple([ord(x) for x in bytes[i : i + 4]])

            if chunk[3] != 0:
                return True

        return False

    def overlapping_region(self):
        (sx, sy, sw, sh) = (
            self.selection.x(),
            self.selection.y(),
            self.selection.width(),
            self.selection.height(),
        )

        selectionRect = QRect(sx, sy, sw, sh)

        rect = self.node.bounds()

        return rect.intersected(selectionRect)


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
        unset_all_blue_labels()

        document = Krita.instance().activeDocument()

        if document is None:
            return

        selection = document.selection()

        layers = list_layers_colorizing_selection()

        [set_color_labels_recursively(layer) for layer in layers]

    def canvasChanged(self, canvas):
        pass


Krita.instance().addExtension(LayerFinderExtension(Krita.instance()))
