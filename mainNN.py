import gui


class NNStructure:

    def __init__(self, blocks=None, arrows=None, file=None):
        if file is not None:
            self.file = file
            self.importTopology()
        elif blocks is not None and arrows is not None:
            self.blocks = blocks
            self.arrows = arrows

    def checkTopology(self):
        pass

    def commitTopology(self):
        pass

    def saveTopology(self):
        pass

    def exportAs(self, framework):
        pass

    def loadTopology(self):
        pass

    def importTopology(self):
        pass