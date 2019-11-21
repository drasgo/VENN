import json
import os
import gui.costants as costants


class NNStructure:

    def __init__(self, blocks=None, arrows=None, inputData="", outputData=""):
        self.topology = {}
        self.file = costants.NNSTRUCTURE_FILE
        self.input = inputData
        self.output = outputData
        self.framework = None
        self.inputTarget = {}

        if blocks is not None and arrows is not None:
            self.blocks = blocks[:]
            self.arrows = arrows[:]

    def setStructureFilename(self, name):
        self.file = name

    def setFramework(self, frame):
        self.framework = frame

    def checkTopology(self):
        # print([lay.objectName() for lay in self.blocks])

        if len(self.blocks) < 2 or len(self.arrows) == 0:
            print("non ci sono abbastanza blocchi o abbastanza frecce")
            return 0

        for layer in self.blocks:

            if layer.layer.currentText() == "LAYER" and not any(ch.isdigit() for ch in layer.neurons.text()):
                print("non ci sono numeri in blocco: " + layer.neurons.text())
                return 0

            if len(layer.PrevArch) == 0 and len(layer.SuccArch) == 0:
                print("non ci sono arco precedente o successivo in blocco " + layer.objectName())
                layer.__del__()
                return 0

        if not any(len(lay.PrevArch) == 0 for lay in self.blocks):
            print("initial block absent")
            print("number of prev arches: " + str([len(lay.PrevArch) for lay in self.blocks]))
            return 0

        if not any(len(lay.SuccArch) == 0 for lay in self.blocks):
            print("final block absent")
            print("number of succ arches: " + str([len(lay.SuccArch) for lay in self.blocks]))
            return 0

        for arch in self.arrows:

            # if arch.name == "None":
            #     print("funzione di attivazione è None in " + arch.objectName())
            #     return 0

            if arch.initBlock is None or arch.finalBlock is None:
                print("blocco iniziale o finale è None in arco " + arch.objectName())
                return 0

        return 1

    def commitTopology(self):

        initialIndex = 0

        def getBlockProperties(block):
            # print("in get block properties")
            temp = dict()
            temp["block"] = True
            temp["name"] = "saved" + str(block.objectName())
            temp["PrevArch"] = ["saved" + bl.objectName() for bl in block.PrevArch]
            temp["SuccArch"] = ["saved" + bl.objectName() for bl in block.SuccArch]
            temp["type"] = str(block.layer.currentText())
            if str(block.layer.currentText()) == "LAYER":
                temp["neurons"] = str([int(s) for s in block.neurons.text().split() if s.isdigit()][0])
            if str(block.layer.currentText()) == "COST":
                temp["cost"] = str(block.cost.currentText())
            temp["position"] = [block.x(), block.y(), block.height(), block.width()]
            return temp

        def getArrowProperties(arch):
            # print("in get arrow properties")
            temp = dict()
            temp["block"] = False
            temp["name"] = "saved" + str(arch.objectName())
            temp["initBlock"] = "saved" + arch.initBlock.objectName()
            temp["finalBlock"] = "saved" + arch.finalBlock.objectName()
            temp["activFunc"] = arch.name
            temp["position"] = [arch.x(), arch.y(), arch.width(), arch.height()]
            return temp

        def getNextArrow(block):
            if block.block is True:
                # print("in get next arrow")
                return block.SuccArch

        def getNextBlock(arch):
            if arch.block is False:
                # print("in get next block")
                return arch.finalBlock

        def recursive(component):
            nonlocal initialIndex

            if (initialIndex == 0 or self.topology[str(initialIndex-1)]["block"] is False) and len(self.blocks) > 0:
                # print(component.objectName())
                self.topology[str(initialIndex)] = getBlockProperties(component)
                # print("index: " + str(initialIndex) + "; in block step")
                # print(self.topology)
                self.blocks.remove(component)

                for arch in getNextArrow(component):
                    initialIndex = initialIndex + 1
                    # print("In piu archi in uscita da blocco")
                    recursive(arch)

            elif self.topology[str(initialIndex-1)]["block"] is True and len(self.arrows) > 0:
                self.topology[str(initialIndex)] = getArrowProperties(component)
                # print("index: " + str(initialIndex) + "; in arrow step")
                # print(self.topology)
                self.arrows.remove(component)
                initialIndex = initialIndex + 1
                recursive(getNextBlock(component))

        for first in [fi for fi in self.blocks if len(fi.PrevArch) == 0]:
            recursive(first)

    def saveTopology(self):
        if len(self.topology) == 0:
            self.commitTopology()

        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.topology, f, indent=4)

    def exportAs(self):
        if self.input != "" and self.output != "":
            self.prepareIOData()

        if len(self.inputTarget) == 0:
            print("Error preparing input/target data while exporting structure into " + self.framework)
            return

        if self.framework.lowercase() == "tensorflow":
            import nn.tensorflowWrapper as frame
        else:
            import nn.pytorchWrapper as frame

        frameStruc = frame.FrameStructure

    def prepareIOData(self):
        inputList = self.splitInputOuput(inp=True)
        outputList = self.splitInputOuput(inp=False)

        if self.checkInputOutput(len(inputList), len(outputList)) is False:
            print("Number of input data is different of number of target data: Input:" +
                  str(len(inputList)) + ", Output: " + str(len(outputList)))
            return

        for index in range(len(inputList) - 1):
            self.inputTarget[inputList[index]] = outputList[index]

    def splitInputOuput(self, inp):
        reference = self.input if inp else self.output
        if "[" not in reference:
            return reference.split(",")
        else:
            temp = reference.split("],[")
            lista = []
            for x in temp:
                temp1 = x.replace("]", "")
                temp1 = temp1.replace("[", "")
                lista.append(temp1.split(","))
            return lista

    def checkInputOutput(self, inputLen, outputLen):
        return True if inputLen == outputLen else False

    def loadTopology(self):
        if os.path.exists(self.file):
            with open(self.file, "r") as data:
                # print(str(data))
                loaded = json.load(data)
        else:
            print("Previous structure not found")
            loaded = None

        return loaded
