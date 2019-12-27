import json
import os
import ViCreNN.costants as costants


class NNStructure:

    def __init__(self, blocks=None, arrows=None):
        self.topology = {}
        self.file = costants.NNSTRUCTURE_FILE
        self.input = ""
        self.output = ""
        self.framework = None
        self.finalInput = []
        self.finalOutput = []
        self.numberInputs = 0
        self.numberOutputs = 0
        self.cost = ""
        self.optimizer = costants.OPTIMIZERS[0]
        self.frameStruct = None
        self.inputType = costants.INPUT_TYPE[0]

        if blocks is not None and arrows is not None:
            self.blocks = blocks[:]
            self.arrows = arrows[:]

    def setStructureFilename(self, name):
        if "." not in name:
            name = name + costants.STRUCTURE_EXTENSION
        self.file = name

    def setFramework(self, frame):
        self.framework = frame

    def setCostFunction(self, cost):
        self.cost = cost

    def setOptimizer(self, optim):
        self.optimizer = optim
        
    def setInputType(self, inputType):
        self.inputType = inputType

    def setInputOutput(self, inputData, outputData):
        self.input = inputData
        self.output = outputData

    def setInputOutputNumber(self, inputCount, outputCount):
        self.numberInputs = inputCount
        self.numberOutputs = outputCount

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

            if len(layer.SuccArch) > 0 and layer.layer.currentText() == "OUTPUT":
                print("blocco output ha archi successivi")
                return 0

        if not any(len(lay.PrevArch) == 0 for lay in self.blocks if lay.layer.text == "INPUT"):
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
            temp["name"] = str(block.objectName())
            temp["FirstBlock"] = True if len(block.PrevArch) == 0 else False and block.layer.currentText() == "INPUT"
            temp["LastBlock"] = True if len(block.SuccArch) == 0 else False and block.layer.currentText() == "OUTPUT"
            temp["PrevArch"] = [bl.objectName() for bl in block.PrevArch]
            temp["SuccArch"] = [bl.objectName() for bl in block.SuccArch]
            temp["type"] = str(block.layer.currentText())
            if str(block.layer.currentText()) == "LAYER":
                temp["neurons"] = str([int(s) for s in block.neurons.text().split() if s.isdigit()][0])
            temp["position"] = [block.x(), block.y(), block.height(), block.width()]
            return temp

        def getArrowProperties(arch):
            # print("in get arrow properties")
            temp = dict()
            temp["block"] = False
            temp["name"] = str(arch.objectName())
            temp["initBlock"] = arch.initBlock.objectName()
            temp["finalBlock"] = arch.finalBlock.objectName()
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

    def exportAs(self, run=False):
        if self.input != "" and self.output != "":
            self.prepareIOData()

        if self.numberInputs == 0 and self.numberOutputs == 0:
            print("Error preparing input/output data")
            return

        if self.framework.lower() == "tensorflow":
            import ViCreNN.nn.tensorflowWrapper as frameChosen
            nomeFile = self.framework.lower() + "-" + self.file.replace(costants.STRUCTURE_EXTENSION, costants.TENSORFLOW_EXTENSION)

        elif self.framework.lower() == "pytorch":
            import ViCreNN.nn.pytorchWrapper as frameChosen
            nomeFile = self.framework.lower() + "-" + self.file.replace(costants.STRUCTURE_EXTENSION, costants.PYTORCH_EXTENSION)

        elif self.framework.lower() == "keras":
            import ViCreNN.nn.kerasWrapper as frameChosen
            nomeFile = self.framework.lower() + "-" + self.file.replace(costants.STRUCTURE_EXTENSION, costants.KERAS_EXTENSION)

        elif self.framework.lower() == "fastai":
            import ViCreNN.nn.fastaiWrapper as frameChosen
            nomeFile = self.framework.lower() + "-" + self.file.replace(costants.STRUCTURE_EXTENSION, costants.FASTAI_EXTENSION)

        else:
            print("Error choosing framework: " + self.framework.lower())
            return

        self.frameStruct = frameChosen.FrameStructure(self.numberInputs, self.numberOutputs, structure=self.topology, structureName=nomeFile)

        if self.frameStruct.prepareModel() is False:
            print("Error preparing the Neural Network model with " + self.framework.lower() + " framework. Aborted")
            return

        if run is False:
            self.frameStruct.saveModel()

    def runAs(self, test=False):
        if self.frameStruct is None:
            self.exportAs(run=True)
        elif self.input != "" and self.output != "":
            self.prepareIOData()

        self.frameStruct.setCost(cost=self.cost)
        self.frameStruct.setOptimizer(optim=self.optimizer)
        self.frameStruct.setInputOutput(inputData=self.finalInput, outputData=self.finalOutput, test=test)

        if test is False:
            return self.frameStruct.run()

        else:
            return self.frameStruct.run() + "\n" + self.frameStruct.test()

    def prepareIOData(self):
        self.finalInput = self.splitInputOuput(inp=True)
        self.finalOutput = self.splitInputOuput(inp=False)

        if self.checkInputOutput(len(self.finalOutput), len(self.finalOutput)) is False:
            print("Number of input data is different of number of target data: Input:" +
                  str(len(self.finalInput)) + ", Output: " + str(len(self.finalOutput)))
            return

        elif self.finalInput.count("[") != self.finalInput.count("]"):
            print("Inconsistency with paretheses in input data. Numebr of [: " + str(self.finalInput.count("[")) +
                  "; number of ]:" + str(self.finalInput.count("]")))
            return

        elif self.finalOutput.count("[") != self.finalOutput.count("]"):
            print("Inconsistency with paretheses in output data. Numebr of [: " + str(self.finalOutput.count("[")) +
                  "; number of ]:" + str(self.finalOutput.count("]")))
            return

        self.numberInputs = len(self.finalInput[0])
        self.numberOutputs = len(self.finalOutput[0])

    # Split and flattens input and output data
    def splitInputOuput(self, inp):
        reference = self.input if inp else self.output

        if "[" in reference:
            par = "["
            counterpar = "]"
        elif "(" in reference:
            par = "("
            counterpar = ")"
        elif "{" in reference:
            par = "{"
            counterpar = "}"
        else:
            return reference.split(",")

        count = 0

        for x in reference:
            if x != par:
                break
            count += 1

        # This divides different inputs/outputs
        temp = reference.split(str(count * counterpar) + "," + str(count * par))
        lista = []
        
        # TODO
        # This flattens the data. This mustn't be performed if input data is for convo nets or recurrent nets
        
        # if self.type == "mlp":
        for x in temp:
            x = x.replace(counterpar, "")
            x = x.replace(par, "")
            lista.append(x.split(","))
        # elif self.type == "cnn":
        # ...
        # elif self.type == "rnn":
        # ...
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