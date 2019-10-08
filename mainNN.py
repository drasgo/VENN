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
        print([lay.objectName() for lay in self.blocks])

        if len(self.blocks) < 2 or len(self.arrows) == 0:
            print("non ci sono abbastanza blocchi o abbastanza frecce")
            return 0

        for layer in self.blocks:

            if not any(ch.isdigit() for ch in layer.neurons.text()):
                print("non ci sono numeri in blocco: " + layer.neurons.text())
                return 0

            if len(layer.PrevArch) == 0 and len(layer.SuccArch) == 0:
                print("non ci sono arco precedente o successivo in blocco " + layer.objectName())
                return 0

        if not any(len(lay.PrevArch) == 0 for lay in self.blocks):
            print("non c'è blocco iniziale")
            print("number of prev arches: " + str([len(lay.PrevArch) for lay in self.blocks]))
            return 0

        if not any(len(lay.SuccArch) == 0 for lay in self.blocks):
            print("non c'è blocco finale")
            print("number of succ arches: " + str([len(lay.SuccArch) for lay in self.blocks]))
            return 0

        for arch in self.arrows:

            if arch.name == "None":
                print("funzione di attivazione è None in " + arch.objectName())
                return 0

            if arch.initBlock is None or arch.finalBlock is None:
                print("blocco iniziale o finale è None in arco " + arch.objectName())
                return 0

        return 1

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