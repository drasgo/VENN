import json
import os
import VENN.costants as costants


class NNStructure:
    def __init__(self):
        self.logger = None
        self.topology = {}
        self.file = costants.NNSTRUCTURE_FILE
        self.loadingFile = costants.NNSTRUCTURE_FILE
        self.input = ""
        self.output = ""
        self.framework = None
        self.finalInput = []
        self.finalOutput = []
        self.numberInputs = 0
        self.numberOutputs = 0
        self.loss = ""
        self.optimizer = costants.OPTIMIZERS[0]
        self.frameStruct = None
        self.inputType = costants.INPUT_TYPE[0]
        self.blocks = None
        self.arrows = None
        self.inputFile = ""
        self.outputFile = ""
        self.epochs = 1

    def setBlocksArrows(self, blocks, arrows):
        self.blocks = blocks[:]
        self.arrows = arrows[:]
        self.topology = {}

    def setStructureFilename(self, name):
        if "." not in name:
            name = name + costants.STRUCTURE_EXTENSION
        self.file = name

    def setLoadingStructureFilename(self, name):
        if name != "":
            self.loadingFile = name

    def setFramework(self, frame):
        self.framework = frame

    def setLossFunction(self, loss):
        print("loss: " + str(loss))
        if loss is not None and loss != "":
            self.loss = loss

    def setOptimizer(self, optim):
        print("optim: " + str(optim))
        self.optimizer = optim

    def setEpochs(self, epochs):
        print("epochs: " + str(epochs))
        self.epochs = epochs

    def setInputOutput(self, inputFile, outputFile):
        self.inputFile = inputFile
        self.outputFile = outputFile
        self.getIO()

    def setInputOutputNumber(self, inputCount, outputCount):
        self.numberInputs = inputCount
        self.numberOutputs = outputCount

    def setLogger(self, logger):
        self.logger = logger

    def restrictionSumSub(self, node):
        if node.layer.currentText() == "SUM" or node.layer.currentText() == "SUB":
            arch1 = node.PrevArch[0]
            arch2 = node.PrevArch[1]
            block1 = arch1.initBlock
            block2 = arch2.initBlock

            if self.restrictionSumSub(block1) == self.restrictionSumSub(block2):
                return True
            else:
                return False

        elif node.layer.currentText() == "MULT":
            arch1 = node.PrevArch[0]
            arch2 = node.PrevArch[1]
            block1 = arch1.initBlock
            block2 = arch2.initBlock

            return self.restrictionSumSub(block1) * self.restrictionSumSub(block2)

        elif node.layer.currentText() == "DENSE":
            try:
                return [int(s) for s in node.neurons.text().split() if s.isdigit()][0]
            except IndexError:
                pass

        elif node.layer.currentText() == "INPUT":
            if self.numberInputs == 0:
                self.prepareIOData()
            return self.numberInputs

        elif node.layer.currentText() == "BLANK":
            arch1 = node.PrevArch[0]
            block1 = arch1.initBlock
            return self.restrictionSumSub(block1)

        self.logger(
            "Error checking sum dimensionality: block "
            + node.objectName()
            + " not recognized - type "
            + node.layer.currentText(),
            "red",
        )

    def checkTopology(self):
        if len(self.blocks) < 2 or len(self.arrows) == 0:
            self.logger("There aren't enough blocks or arrows.", "red")
            return 0

        for layer in self.blocks:

            if layer.layer.currentText() == "DENSE" and not any(
                ch.isdigit() for ch in layer.neurons.text()
            ):
                self.logger(
                    "Dense layers needs number of neurons.: " + layer.neurons.text(),
                    "red",
                )
                return 0

            if len(layer.PrevArch) == 0 and len(layer.SuccArch) == 0:
                self.logger(
                    "Block "
                    + layer.objectName()
                    + " has no incoming nor outcoming arrows",
                    "red",
                )
                layer.__del__()
                return 0

            if len(layer.SuccArch) > 0 and layer.layer.currentText() == "OUTPUT":
                self.logger("Output block can't have outcoming arrows", "red")
                return 0

            if layer.layer.currentText() == "SUM" or layer.layer.currentText() == "SUB":
                if self.restrictionSumSub(layer) is False:
                    self.logger(
                        "Dimension of input blocks into "
                        + layer.objectName()
                        + " -type "
                        + layer.layer.currentText()
                        + "- are not the same",
                        "red",
                    )
                    return 0

        if not any(lay for lay in self.blocks if lay.layer.currentText() == "INPUT"):
            self.logger("Input block absent", "red")
            # self.logger("Number of prev arches: " + str([len(lay.PrevArch) for lay in self.blocks]), "red")
            return 0

        if len([lay for lay in self.blocks if lay.layer.currentText() == "INPUT"]) > 1:
            self.logger("Only one input block supported so far", "red")
            self.logger(
                "Number of input blocks: "
                + str(
                    len(
                        [
                            lay
                            for lay in self.blocks
                            if lay.layer.currentText() == "INPUT"
                        ]
                    )
                ),
                "red",
            )
            return 0

        if not any(lay for lay in self.blocks if lay.layer.currentText() == "OUTPUT"):
            self.logger("Output block absent", "red")
            # self.logger("Number of succ arches: " + str([len(lay.SuccArch) for lay in self.blocks]), "red")
            return 0

        if len([lay for lay in self.blocks if lay.layer.currentText() == "OUTPUT"]) > 1:
            self.logger("Only one output block supported", "red")
            self.logger(
                "Number of output blocks: "
                + str(
                    len(
                        [
                            lay
                            for lay in self.blocks
                            if lay.layer.currentText() == "OUTPUT"
                        ]
                    )
                ),
                "red",
            )
            return 0

        for arch in self.arrows:

            # if arch.name == "None":
            #     self.logger("funzione di attivazione è None in " + arch.objectName(), "red")
            #     return 0

            if arch.initBlock is None or arch.finalBlock is None:
                self.logger(
                    "Error with "
                    + arch.objectName()
                    + ": it's without previous or next block",
                    "red",
                )
                return 0

        return 1

    def commitTopology(self):

        initialIndex = 0

        def getBlockProperties(block):
            # self.logger("in get block properties")
            temp = dict()
            temp["block"] = True
            temp["name"] = str(block.objectName())
            temp["FirstBlock"] = (
                True
                if len(block.PrevArch) == 0
                else False and block.layer.currentText() == "INPUT"
            )
            temp["LastBlock"] = (
                True
                if len(block.SuccArch) == 0
                else False and block.layer.currentText() == "OUTPUT"
            )
            temp["PrevArch"] = [bl.objectName() for bl in block.PrevArch]
            temp["SuccArch"] = [bl.objectName() for bl in block.SuccArch]
            temp["type"] = str(block.layer.currentText())
            if str(block.layer.currentText()) in costants.BLOCK_LABELS:
                temp["neurons"] = str(
                    [int(s) for s in block.neurons.text().split() if s.isdigit()][0]
                )
            temp["size"] = [block.width(), block.height()]
            temp["pos"] = [block.x(), block.y()]
            return temp

        def getArrowProperties(arch):
            # self.logger("in get arrow properties")
            temp = dict()
            temp["block"] = False
            temp["name"] = str(arch.objectName())
            temp["initBlock"] = arch.initBlock.objectName()
            temp["finalBlock"] = arch.finalBlock.objectName()
            temp["activFunc"] = arch.name
            temp["size"] = [arch.width(), arch.height()]
            temp["pos"] = [arch.x(), arch.y()]
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

            if (
                initialIndex == 0
                or self.topology[str(initialIndex - 1)]["block"] is False
            ) and len(self.blocks) > 0:
                # self.logger(component.objectName())
                self.topology[str(initialIndex)] = getBlockProperties(component)
                # self.logger("index: " + str(initialIndex) + "; in block step")
                # self.logger(self.topology)
                self.blocks.remove(component)

                for arch in getNextArrow(component):
                    initialIndex = initialIndex + 1
                    # self.logger("In piu archi in uscita da blocco")
                    recursive(arch)

            elif (
                self.topology[str(initialIndex - 1)]["block"] is True
                and len(self.arrows) > 0
            ):
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
        if (
            len(self.finalInput) == 0
            and len(self.finalOutput) == 0
            and self.numberInputs == 0
            and self.numberOutputs == 0
        ):
            self.prepareIOData()

        if self.numberInputs == 0 and self.numberOutputs == 0:
            self.logger("Error preparing input/output data")
            return False

        if len(self.topology) == 0:
            self.commitTopology()

        if self.framework.lower() == "tensorflow":
            import VENN.nn.tensorflowWrapper as frameChosen

            nomeFile = (
                self.framework.lower()
                + "-"
                + self.file.replace(
                    costants.STRUCTURE_EXTENSION, costants.TENSORFLOW_EXTENSION
                )
            )

        elif self.framework.lower() == "pytorch":
            import VENN.nn.pytorchWrapper as frameChosen

            nomeFile = (
                self.framework.lower()
                + "-"
                + self.file.replace(
                    costants.STRUCTURE_EXTENSION, costants.PYTORCH_EXTENSION
                )
            )

        elif self.framework.lower() == "keras":
            import VENN.nn.kerasWrapper as frameChosen

            nomeFile = (
                self.framework.lower()
                + "-"
                + self.file.replace(
                    costants.STRUCTURE_EXTENSION, costants.KERAS_EXTENSION
                )
            )

        # elif self.framework.lower() == "fastai":
        #     import VENN.nn.fastaiWrapper as frameChosen
        #     nomeFile = self.framework.lower() + "-" + self.file.replace(costants.STRUCTURE_EXTENSION,
        #                                                                 costants.FASTAI_EXTENSION)

        else:
            self.logger("Error choosing framework: " + self.framework.lower(), "red")
            return False

        self.frameStruct = frameChosen.FrameStructure(
            self.numberInputs,
            self.numberOutputs,
            structure=self.topology,
            structureName=nomeFile,
            logger=self.logger,
        )

        if self.frameStruct.prepareModel() is False:
            self.logger(
                "Error preparing the Neural Network model with "
                + self.framework.lower()
                + " framework. Aborted",
                "red",
            )
            return False

        if run is False:
            self.frameStruct.saveModel()

        return True

    def runAs(self, test=False):
        if len(self.finalInput) == 0 and len(self.finalOutput) == 0:
            if self.prepareIOData() == 0:
                return "Error preparing input/output data", "red"

        if (
            self.loss != ""
            and self.optimizer != ""
            and isinstance(self.epochs, int)
            and self.epochs > 0
        ):
            self.frameStruct.setLoss(cost=self.loss)
            self.frameStruct.setOptimizer(optim=self.optimizer)
            self.frameStruct.setEpochs(epochs=self.epochs)
        else:
            return (
                "Error setting parameters. Check loss function, optimizer function and/or number of epochs",
                "red",
            )

        if self.frameStruct is None:
            if self.exportAs(run=True) is False:
                return "Error preparing structure pre-run with " + self.framework, "red"

        self.frameStruct.setInputOutput(
            inputData=self.finalInput, outputData=self.finalOutput, test=test
        )

        return self.frameStruct.run(), ""

    def getIO(self):
        with open(self.inputFile, "r") as f:
            for line in f.readlines():
                self.input = self.input + line

        with open(self.outputFile, "r") as f:
            for line in f.readlines():
                self.output = self.output + line

    def prepareIOData(self):
        if len(self.input) > 0:
            self.finalInput = self.splitInputOuput(inp=True)
        else:
            return 0

        if len(self.output) > 0:
            self.finalOutput = self.splitInputOuput(inp=False)
        else:
            return 0

        if self.checkInputOutput(len(self.finalInput), len(self.finalOutput)) is False:
            self.logger(
                "Number of input data is different of number of target data: Input:"
                + str(len(self.finalInput))
                + ", Output: "
                + str(len(self.finalOutput)),
                "red",
            )
            return 0

        elif self.finalInput.count("[") != self.finalInput.count("]"):
            self.logger(
                "Inconsistency with paretheses in input data. Numebr of [: "
                + str(self.finalInput.count("["))
                + "; number of ]:"
                + str(self.finalInput.count("]")),
                "red",
            )
            return 0

        elif self.finalOutput.count("[") != self.finalOutput.count("]"):
            self.logger(
                "Inconsistency with paretheses in output data. Numebr of [: "
                + str(self.finalOutput.count("["))
                + "; number of ]:"
                + str(self.finalOutput.count("]")),
                "red",
            )
            return 0

        elif len(self.finalInput) == 0 or len(self.finalOutput) == 0:
            self.logger("Input and/or output data not available.", "red")
            return 0

        self.numberInputs = len(self.finalInput[0])
        self.numberOutputs = len(self.finalOutput[0])

        return 1

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
        # if not CNN or RNN:
        for x in temp:
            x = x.replace(counterpar, "")
            x = x.replace(par, "")
            lista.append(x.split(","))
        # elif not any(self.topology[elem]["type"] == "CNN" for elem in self.topology if self.topology[elem]["block"] is True)::
        # ...
        # elif is RNN:
        # ...
        return lista

    def checkInputOutput(self, inputLen, outputLen):
        return True if inputLen == outputLen else False

    def loadTopology(self):
        if os.path.exists(self.loadingFile):
            with open(self.loadingFile, "r") as data:
                return json.load(data)
        else:
            self.logger("Previous structure not found", "red")
            return None
