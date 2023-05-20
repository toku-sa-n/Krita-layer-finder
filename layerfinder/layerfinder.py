from krita import *


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
        QMessageBox.information(QWidget(), "Hello", "Hello World!")


Krita.instance().addExtension(LayerFinderExtension(Krita.instance()))
