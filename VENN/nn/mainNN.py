import json
import os
import VENN.costants as costants


class NNStructure:

    def __init__(self, blocks=None, arrows=None):
        self.logger = None
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
        self.blocks = None
        self.arrows = None

    def setBlocksArrows(self, blocks, arrows):
        self.blocks = blocks[:]
        self.arrows = arrows[:]
        self.topology = {}

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

    def setLogger(self, logger):
        self.logger = logger

    def checkTopology(self):
        # self.logger([lay.objectName() for lay in self.blocks])

        if len(self.blocks) < 2 or len(self.arrows) == 0:
            self.logger("non ci sono abbastanza blocchi o abbastanza frecce", "red")
            return 0

        for layer in self.blocks:

            if layer.layer.currentText() == "LAYER" and not any(ch.isdigit() for ch in layer.neurons.text()):
                self.logger("non ci sono numeri in blocco: " + layer.neurons.text(), "red")
                return 0

            if len(layer.PrevArch) == 0 and len(layer.SuccArch) == 0:
                self.logger("non ci sono arco precedente o successivo in blocco " + layer.objectName(), "red")
                layer.__del__()
                return 0

            if len(layer.SuccArch) > 0 and layer.layer.currentText() == "OUTPUT":
                self.logger("blocco output ha archi successivi", "red")
                return 0

        if not any(lay for lay in self.blocks if lay.layer.currentText() == "INPUT"):
            self.logger("Input block absent", "red")
            self.logger("Number of prev arches: " + str([len(lay.PrevArch) for lay in self.blocks]), "red")
            return 0

        if len([lay for lay in self.blocks if lay.layer.currentText() == "INPUT"]) > 1:
            self.logger("Only one input block supported so far", "red")
            self.logger("Number of input blocks: " + str(len([lay for lay in self.blocks if lay.layer.currentText() == "INPUT"])), "red")

        if not any(lay for lay in self.blocks if lay.layer.currentText() == "OUTPUT"):
            self.logger("Output block absent", "red")
            self.logger("Number of succ arches: " + str([len(lay.SuccArch) for lay in self.blocks]), "red")
            return 0

        if len([lay for lay in self.blocks if lay.layer.currentText() == "OUTPUT"]) > 1:
            self.logger("Only one output block supported so far", "red")
            self.logger("Number of output blocks: " + str(len([lay for lay in self.blocks if lay.layer.currentText() == "OUTPUT"])), "red")

        for arch in self.arrows:

            if arch.name == "None":
                self.logger("funzione di attivazione è None in " + arch.objectName(), "red")
                return 0

            if arch.initBlock is None or arch.finalBlock is None:
                self.logger("blocco iniziale o finale è None in arco " + arch.objectName(), "red")
                return 0

        return 1

    def commitTopology(self):

        initialIndex = 0

        def getBlockProperties(block):
            # self.logger("in get block properties")
            temp = dict()
            temp["block"] = True
            temp["name"] = str(block.objectName())
            temp["FirstBlock"] = True if len(block.PrevArch) == 0 else False and block.layer.currentText() == "INPUT"
            temp["LastBlock"] = True if len(block.SuccArch) == 0 else False and block.layer.currentText() == "OUTPUT"
            temp["PrevArch"] = [bl.objectName() for bl in block.PrevArch]
            temp["SuccArch"] = [bl.objectName() for bl in block.SuccArch]
            temp["type"] = str(block.layer.currentText())
            if str(block.layer.currentText()) == "DENSE":
                temp["neurons"] = str([int(s) for s in block.neurons.text().split() if s.isdigit()][0])
            temp["position"] = [block.x(), block.y(), block.height(), block.width()]
            return temp

        def getArrowProperties(arch):
            # self.logger("in get arrow properties")
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
                # self.logger("in get next arrow")
                return block.SuccArch

        def getNextBlock(arch):
            if arch.block is False:
                # self.logger("in get next block")
                return arch.finalBlock

        def recursive(component):
            nonlocal initialIndex

            if (initialIndex == 0 or self.topology[str(initialIndex - 1)]["block"] is False) and len(self.blocks) > 0:
                # self.logger(component.objectName())
                self.topology[str(initialIndex)] = getBlockProperties(component)
                # self.logger("index: " + str(initialIndex) + "; in block step")
                # self.logger(self.topology)
                self.blocks.remove(component)

                for arch in getNextArrow(component):
                    initialIndex = initialIndex + 1
                    # self.logger("In piu archi in uscita da blocco")
                    recursive(arch)

            elif self.topology[str(initialIndex - 1)]["block"] is True and len(self.arrows) > 0:
                self.topology[str(initialIndex)] = getArrowProperties(component)
                # self.logger("index: " + str(initialIndex) + "; in arrow step")
                # self.logger(self.topology)
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

        self.logger("Model saved!")

    def exportAs(self, run=False):
        if self.input != "" and self.output != "":
            self.prepareIOData()

        if self.numberInputs == 0 and self.numberOutputs == 0:
            self.logger("Error preparing input/output data")
            return

        if len(self.topology) == 0:
            self.commitTopology()

        if self.framework.lower() == "tensorflow":
            import ViCreNN.nn.tensorflowWrapper as frameChosen
            nomeFile = self.framework.lower() + "-" + self.file.replace(costants.STRUCTURE_EXTENSION,
                                                                        costants.TENSORFLOW_EXTENSION)

        elif self.framework.lower() == "pytorch":
            import ViCreNN.nn.pytorchWrapper as frameChosen
            nomeFile = self.framework.lower() + "-" + self.file.replace(costants.STRUCTURE_EXTENSION,
                                                                        costants.PYTORCH_EXTENSION)

        elif self.framework.lower() == "keras":
            import ViCreNN.nn.kerasWrapper as frameChosen
            nomeFile = self.framework.lower() + "-" + self.file.replace(costants.STRUCTURE_EXTENSION,
                                                                        costants.KERAS_EXTENSION)

        # elif self.framework.lower() == "fastai":
        #     import ViCreNN.nn.fastaiWrapper as frameChosen
        #     nomeFile = self.framework.lower() + "-" + self.file.replace(costants.STRUCTURE_EXTENSION,
        #                                                                 costants.FASTAI_EXTENSION)

        else:
            self.logger("Error choosing framework: " + self.framework.lower(), "red")
            return

        self.frameStruct = frameChosen.FrameStructure(self.numberInputs, self.numberOutputs, structure=self.topology,
                                                      structureName=nomeFile, logger=self.logger)

        if self.frameStruct.prepareModel() is False:
            self.logger(
                "Error preparing the Neural Network model with " + self.framework.lower() + " framework. Aborted", "red")
            return

        if run is False:
            self.frameStruct.saveModel()
            self.logger("Model saved using " + self.framework)

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
            self.logger("Number of input data is different of number of target data: Input:" +
                        str(len(self.finalInput)) + ", Output: " + str(len(self.finalOutput)), "red")
            return

        elif self.finalInput.count("[") != self.finalInput.count("]"):
            self.logger("Inconsistency with paretheses in input data. Numebr of [: " + str(self.finalInput.count("[")) +
                        "; number of ]:" + str(self.finalInput.count("]")), "red")
            return

        elif self.finalOutput.count("[") != self.finalOutput.count("]"):
            self.logger(
                "Inconsistency with paretheses in output data. Numebr of [: " + str(self.finalOutput.count("[")) +
                "; number of ]:" + str(self.finalOutput.count("]")), "red")
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
                return json.load(data)
        else:
            self.logger("Previous structure not found", "red")
            return None
