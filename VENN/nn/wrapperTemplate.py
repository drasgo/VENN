class WrapperTemplate:

    def __init__(self, numberInput, numberOutput, structure, structureName, logger):
        self.ninput = numberInput
        self.noutput = numberOutput
        self.structure = structure.copy()
        self.name = structureName
        self.model = None
        self.inputTrain = None
        self.outputTrain = None
        self.inputTest = None
        self.outputTest = None
        self.isSequential = None
        self.loss = ""
        self.optimizer = ""
        self.loss_object = None
        self.optimizer_object = None
        self.epoch = 0
        self.logger = logger
        self.test = False

        self.prepareStructure()

    def chooseNode(self, layerType, **kwargs):
        """ Overriden for choosing the current layer in the wrappers."""
        pass

    def chooseActivation(self, activ):
        """ Overriden for choosing the current activation function in the wrappers."""
        pass

    def chooseLoss(self):
        """ Overriden for choosing the cost function in the wrappers."""
        pass

    def chooseOptimizer(self):
        """ Overriden for choosing the optimizer function in the wrappers."""
        pass

    def prepareModel(self):
        """ Overriden for preparing the sctructure of the model in the wrappers. This actually creates the model of the
        specified framework which later can be saved or used for run/test.
        """
        pass

    def saveModel(self):
        """ Overriden for saving in file the prepared model."""
        pass

    def run(self):
        """ Overriden for running the prepared model."""
        pass

    def dimensionalityChangeforMultiply(self, node, done):
        """ Overriden for commute the previous nodes which go into a mult special block [1]x[m] and [1]x[n] into [m]x[1]
        and [1]x[n], and reshape the resulting matrix [m]x[n] into a row vector 1x[m*n].
        """
        pass

    def multNode(self, inputNode1, inputNode2, name=""):
        """Overriden for implementing the multiplication operation support into the wrappers."""
        pass

    def sumNode(self, inputNode1, inputNode2, name=""):
        """Overriden for implementing the sum operation support into the wrappers."""
        pass

    def subNode(self, inputNode1, inputNode2, name=""):
        """Overriden for implementing the subtraction operation support into the wrappers."""
        pass

    def nodeSupport(self, node):
        """Overriden for guaranteeing the support of the current layer in the specified framework"""
        pass

    def functionSupport(self, activ):
        """Overriden for guaranteeing the support of the current activation function in the specified framework"""
        pass

    #
    def setInputOutput(self, inputData, outputData, test):
        """ Gets input and output data and divides it, if also testing is performed, into training and testing data.
        Don't touch it
        """
        self.test = test
        if self.test is False:
            self.inputTrain = inputData
            self.outputTrain = outputData
        else:
            self.inputTrain = inputData[:len(inputData) * 0.6]
            self.inputTest = inputData[len(inputData) * 0.6:]
            self.outputTrain = outputData[:len(inputData) * 0.6]
            self.outputTest = outputData[len(inputData) * 0.6:]

    def prepareStructure(self):
        """ Removes any blank block and any arch associated (for example in case of curved branches). Don't touch it"""
        toBeDeleted = []

        for element in self.structure:

            if self.structure[element]["block"] is True and self.structure[element]["type"] == "BLANK":
                tempNameSuccArch = self.structure[element]["SuccArch"]
                tempNamePrevArch = self.structure[element]["PrevArch"][0]
                tempPrevArch = next(key for key in self.structure if self.structure[key]["name"] == tempNamePrevArch)

                for arch in tempNameSuccArch:
                    tempSuccArch, nextBlock = self.getArchBlock(arch)
                    nextBlockName = self.structure[tempSuccArch]["finalBlock"]
                    self.structure[tempPrevArch]["finalBlock"] = nextBlockName
                    self.structure[nextBlock]["PrevArch"].remove(arch)
                    self.structure[nextBlock]["PrevArch"].append(tempNamePrevArch)
                    toBeDeleted.append(tempSuccArch)
                toBeDeleted.append(element)

        for elem in toBeDeleted:
            self.structure.pop(elem)

    def setLoss(self, loss):
        """ Sets which cost to use. Don't touch it"""
        self.loss = loss

    def setOptimizer(self, optim):
        """ Sets which optimizer to use. Don't touch it"""
        self.optimizer = optim

    def setEpochs(self, epochs):
        """ Sets number of epochs for training. Don't touch it."""
        self.epoch = epochs

    def checkNumBranches(self, structure):
        """ Checks how many branches the structure has. Don't touch it. (NOTE: now it's useless, to be deleted)"""
        # Check the numebr of aggregation blocks (aka sum, mult, div, sub blocks). Every aggregation block is a branch unified
        return len([block for block in structure if structure[block]["block"] is True and
                    (structure[block]["type"] == "SUM" or structure[block]["type"] == "SUB" or
                     structure[block]["type"] == "MULT")])

    def returnFirstCompleteDiagram(self, structure):
        """ Return first complete diagram input->output. Don't touch it"""
        index = None
        # self.logger("in check sequential")
        while True:

            if index is not None:
                break

            tempInit = next(bl for bl in structure if
                            structure[bl]["block"] is True and structure[bl]["type"] == "INPUT")
            # self.logger("nome: " + self.structure[tempInit]["name"])
            if tempInit is None:
                self.logger("Error checking sequential structure for. Exiting")
                quit()

            tempIndex = tempInit
            last = structure[tempIndex]["LastBlock"]

            # Checks the integrity of the branch (aka it checks that it starts from an input and through all the middle arches and blocks
            # ends with a final block. If not it removes the first block of that branch. The first valid branch (input-> ...-> output)
            # will be considered as the valid network
            while last is False:

                if structure[tempIndex]["block"] is True:
                    # self.logger("è blocco")
                    tempIndex = next(block for block in structure if any(
                        structure[block]["name"] == x for x in structure[tempIndex]["SuccArch"]))

                else:
                    # self.logger("è arco")
                    tempIndex = next(block for block in structure if
                                     structure[block]["name"] == structure[tempIndex]["finalBlock"])

                if structure[tempIndex]["block"] is True and structure[tempIndex]["type"] == "OUTPUT":
                    # self.logger("finito con final block")
                    last = True
                    index = tempInit

                elif structure[tempIndex]["block"] is True and structure[tempIndex]["type"] == "OUTPUT" and \
                        len(structure[tempIndex]["SuccArch"]) == 0:
                    # self.logger("finito senza final block")
                    break

            if last is False:
                # self.logger("rimuovo questo primo elemento perchè questo branch non ha final block:: " + self.structure[tempInit]["name"])
                structure.pop(tempInit)
        return index

    def getPair(self, index):
        """ Returns next pair of arch-block. It checks if the pass is sequential or if two branches are coming out from
        one block, which means that a special block will come up later on. Don't touch it
        """
        # It keeps going until either it gets to the last block or, just in case it is the recursive instance, the next
        # block it finds is a special block (aka mult/sum/sub), in which case stops itself, returning next arch = None,
        # next block = index (which is prev block) and special block = next block. Either way, the wrapper will always
        #  get nextArchIndex, nextBlockIndex, None if it is sequential or None, index, specName in case the current branch
        #  get to a special block. Note: max two branches can merge into one special block
        # print("in get pair")
        while self.structure[index]["type"] != "OUTPUT":

            # If there are more than 1 arches exiting the current block
            if len(self.structure[index]["SuccArch"]) > 1:
                specIndex = None
                # print("in succ arch maggiore di 1")
                # For each exiting arch exiting the current block
                for tempArchName in self.structure[index]["SuccArch"]:
                    archIndex, blockIndex = self.getArchBlock(tempArchName)
                    # If the next block from the current block is a special block (aka mult/add/sub) then return
                    # to the wrapper arch=None, the current index, the name of the special block.
                    # The wrapper is expected to put a control for checking if specName is not none, in which case it
                    # saves the prev index with as one of the enteing nodes into the special block
                    if self.structure[blockIndex]["type"] == "SUM" or \
                            self.structure[blockIndex]["type"] == "SUB" or \
                            self.structure[blockIndex]["type"] == "MULT":
                        # print("next block is special block")
                        specIndex = blockIndex
                        specName = self.structure[blockIndex]["name"]
                        yield None, index, specName

                    # If the next block is not a special one send it right away and then call itself again recursively
                    else:
                        yield archIndex, blockIndex, None
                        branches = self.getPair(blockIndex)

                        # Here the result from the recursive results are given. The expected behaviour is to go on until
                        # the control if the current block is a special block is met. Then the recursive function stops
                        # returning None, the previous index and the index of the special block
                        for nextArchIndex, nextBlockIndex, tempSpec in branches:
                            specIndex = tempSpec
                            # print("in get pair passing to wrapper block" + self.structure[nextBlockIndex]["name"])

                            # If the index of the special block is None get what is returned from the recursive function
                            #  and send it to the wrapper
                            if specIndex is None:
                                specName = None
                                # print("arch " + self.structure[nextArchIndex]["name"])
                            # If the index of the special block is not None then it is supposed to be the last cycle from
                            # the recursive function, which means that it sent back nextArchIndex = None,
                            # nextBlockIndex = index and specIndex = index of the special block. It is sent to the
                            # wrapper and then it continues.
                            else:
                                specName = self.structure[specIndex]["name"]
                                # print("block " + specName)
                            yield nextArchIndex, nextBlockIndex, specName

                # This is the last piece of code after the reunion of the two arches. The current index needs to be
                # updated to the index of the special block
                index = specIndex

            # Gets the next arch and block indeces from getArchBlock passing the arch name
            nextArchName = next(arch for arch in self.structure[index]["SuccArch"])
            nextArchIndex, nextBlockIndex = self.getArchBlock(nextArchName)

            # This should be true just if this piece is part of the recursion (if the found next block is a special block
            # the function stops itself, sending back nextArchIndex = None, nextBlockIndex = index (which is the prev
            # index) and special block = nextBlockIndex
            if self.structure[nextBlockIndex]["type"] == "SUM" or self.structure[nextBlockIndex]["type"] == "SUB" or \
                    self.structure[nextBlockIndex]["type"] == "MULT":
                # print("in sub, mult o sum in get pair")
                yield None, index, nextBlockIndex
                break

            # Updates the index and sends back to the wrapper the next arch-block pair
            index = nextBlockIndex
            # print("block " + self.structure[nextBlockIndex]["name"] + ", arch " + self.structure[nextArchIndex]["name"])
            yield nextArchIndex, nextBlockIndex, None

    def getArchBlock(self, archName):
        """Given an archName, it returns its index and its final block index. Don't touch it."""
        nextArchIndex = next(key for key in self.structure if self.structure[key]["name"] == archName)
        nextBlockName = self.structure[nextArchIndex]["finalBlock"]
        nextBlockIndex = next(key for key in self.structure if self.structure[key]["name"] == nextBlockName)
        return nextArchIndex, nextBlockIndex

    def computeSpecBlockDim(self, specBlockIndex):
        """Looks for the output dimensionality of the given special block: if it is a SUM/SUB block then the dimension
        is the same as either one of the two input blocks. If it is a MULT block the dimension is the multiplication
        of the dimension of two input blocks. It also checks if one (or both) of the previous blocks is a
         special block itself and continues recurrently. Don't touch it.
        """
        if self.structure[specBlockIndex]["type"] == "SUM" or self.structure[specBlockIndex]["type"] == "SUB" or \
                self.structure[specBlockIndex]["type"] == "MULT":
            archName1 = [elem for elem in self.structure[specBlockIndex]["PrevArch"]][0]
            archIndex1 = next(elem for elem in self.structure if self.structure[elem]["name"] == archName1)
            blockIndex1 = next(
                elem for elem in self.structure if
                self.structure[elem]["name"] == self.structure[archIndex1]["initBlock"])

            if self.structure[specBlockIndex]["type"] == "SUM" or self.structure[specBlockIndex]["type"] == "SUB":
                return self.computeSpecBlockDim(blockIndex1)

            elif self.structure[specBlockIndex]["type"] == "MULT":
                archName2 = [elem for elem in self.structure[specBlockIndex]["PrevArch"]][1]
                archIndex2 = next(elem for elem in self.structure if self.structure[elem]["name"] == archName2)
                blockIndex2 = next(
                    elem for elem in self.structure if
                    self.structure[elem]["name"] == self.structure[archIndex2]["initBlock"])

                return self.computeSpecBlockDim(blockIndex1) * self.computeSpecBlockDim(blockIndex2)
        else:

            if self.structure[specBlockIndex]["type"] == "DENSE":
                return int(self.structure[specBlockIndex]["neurons"])

            else:
                return self.ninput
