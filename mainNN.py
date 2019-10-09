import gui


class NNStructure:

    def __init__(self, blocks=None, arrows=None, file=None):
        self.topology = {}
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
                layer.__del__()
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

        initialIndex = 0
        blockIndex = 0
        arrowIndex = 0

        def getBlockProperties(block):
            nonlocal blockIndex
            print("in get block properties")
            temp = dict()
            temp["block"] = True
            temp["name"] = str(blockIndex) + "block"
            temp["prevArch"] = block.PrevArch.objectName()
            temp["SuccArch"] = block.SuccArch.objectName()
            temp["neurons"] = [int(s) for s in block.neurons.text().split() if s.isdigit()]
            blockIndex = blockIndex + 1
            return temp

        def getArrowProperties(arch):
            nonlocal arrowIndex
            print("in get arrow properties")
            temp = dict()
            temp["block"] = False
            temp["name"] = str(arrowIndex) + "arch"
            temp["initBlock"] = arch.initBlock.objectName()
            temp["finalBlock"] = arch.finalBlock.objectName()
            temp["activFunc"] = arch.name
            arrowIndex = arrowIndex + 1
            return temp

        def getNextArrow(block):
            if block.block is True:
                print("in get next arrow")
                return block.SuccArch

        def getNextBlock(arch):
            if arch.block is False:
                print("in get next block")
                return arch.finalBlock

        def recursive(component):
            nonlocal initialIndex

            if (initialIndex == 0 or self.topology[str(initialIndex-1)]["block"] is False) and len(self.blocks) > 0:
                self.topology[str(initialIndex)] = getBlockProperties(component)
                print("index: " + str(initialIndex) + "; in block step")
                print(self.topology)
                self.blocks.remove(component)

                for arch in getNextArrow(component):
                    initialIndex = initialIndex + 1
                    print("In piu archi in uscita da blocco")
                    recursive(arch)

            elif self.topology[str(initialIndex-1)]["block"] is True and len(self.arrows) > 0:
                self.topology[str(initialIndex)] = getArrowProperties(component)
                print("index: " + str(initialIndex) + "; in arrow step")
                print(self.topology)
                self.arrows.remove(component)
                initialIndex = initialIndex + 1
                recursive(getNextBlock(component))

        for first in [fi for fi in self.blocks if len(fi.PrevArch) == 0]:
            recursive(first)

    def saveTopology(self):
        pass

    def exportAs(self, framework):
        pass

    def loadTopology(self):
        pass

    def importTopology(self):
        pass
