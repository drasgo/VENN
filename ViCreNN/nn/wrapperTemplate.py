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
        self.cost = ""
        self.optimizer = ""
        self.loss_object = None
        self.optimizer_object = None
        self.epoch = 0
        self.logger = logger
        self.prepareStructure()

    def chooseActivation(self, activ):
        """ Override it"""
        pass

    def chooseCost(self):
        """ Override it"""
        pass

    def chooseOptimizer(self):
        """ Override it"""
        pass

    def prepareModel(self):
        """ Override it"""
        pass

    def saveModel(self):
        """ Override it"""
        pass

    def run(self):
        """ Override it"""
        pass

    def test(self):
        """ Override it"""
        pass

    #
    def setInputOutput(self, inputData, outputData, test):
        """ Gets input and output data. Don't touch it"""
        if test is False:
            self.inputTrain = inputData
            self.outputTrain = outputData
        else:
            self.inputTrain = inputData[:len(inputData)*0.6]
            self.inputTest = inputData[len(inputData)*0.6:]
            self.outputTrain = outputData[:len(inputData)*0.6]
            self.outputTest = outputData[len(inputData)*0.6:]

    # TODO: remove any blank block and any arch associated (for example in case of curved branches)
    def prepareStructure(self):
        toBeDeleted = []

        for element in self.structure:

            if self.structure[element]["block"] is True and self.structure[element]["type"] == "BLANK":
                tempNameSuccArch = self.structure[element]["SuccArch"]
                tempNamePrevArch = self.structure[element]["PrevArch"][0]
                tempPrevArch = next(key for key in self.structure if self.structure[key]["name"] == tempNamePrevArch)

                for arch in tempNameSuccArch:
                    tempSuccArch = next(key for key in self.structure if self.structure[key]["name"] == arch)
                    nextBlockName = self.structure[tempSuccArch]["finalBlock"]
                    nextBlock = next(key for key in self.structure if self.structure[key]["name"] == nextBlockName)
                    self.structure[tempPrevArch]["finalBlock"] = nextBlockName
                    self.structure[nextBlock]["PrevArch"].remove(arch)
                    self.structure[nextBlock]["PrevArch"].append(tempNamePrevArch)
                    toBeDeleted.append(tempSuccArch)
                toBeDeleted.append(element)

        for elem in toBeDeleted:
            self.structure.pop(elem)

    def setCost(self, cost):
        """ Sets which cost to use. Don't touch it"""
        self.cost = cost

    def setOptimizer(self, optim):
        """ Sets which optimizer to use. Don't touch it"""
        self.optimizer = optim

    def setEpochs(self, epochs):
        """ Sets number of epochs for training"""
        self.epoch = epochs

    def checkNumBranches(self, structure):
        """ Checks how many branches has the structure. Don't touch it"""
        # Check the numebr of aggregation blocks (aka sum, mult, div, sub blocks). Every aggregation block is a branch unified
        return len([block for block in structure if structure[block]["block"] is True and
                    (structure[block]["type"] == "SUM" or structure[block]["type"] == "SUB" or
                     structure[block]["type"] == "MULT" or structure[block]["type"] == "DIV")])

    def returnFirstCompleteSequential(self, structure):
        """ For sequential models. Don't touch it"""
        index = None
        # self.logger("in check sequential")
        while True:

            if index is not None:
                break

            tempInit = next(bl for bl in structure if
                            structure[bl]["block"] is True and structure[bl]["FirstBlock"] is True)
            # self.logger("nome: " + self.structure[tempInit]["name"])
            if tempInit is None:
                self.logger("Error checking sequential structure for Keras. Exiting")
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

                if structure[tempIndex]["block"] is True and structure[tempIndex]["LastBlock"] is True:
                    # self.logger("finito con final block")
                    last = True
                    index = tempInit

                elif structure[tempIndex]["block"] is True and structure[tempIndex]["LastBlock"] is False and \
                        len(structure[tempIndex]["SuccArch"]) == 0:
                    # self.logger("finito senza final block")
                    break

            if last is False:
                # self.logger("rimuovo questo primo elemento perchè questo branch non ha final block:: " + self.structure[tempInit]["name"])
                structure.pop(tempInit)

        return index

    def getArchBlock(self, structure, index):
        """ Returns next pair of arch-block. Don't touch it"""
        while structure[index]["LastBlock"] is False:
            nextArchName = next(arch for arch in structure[index]["SuccArch"])
            nextArchIndex = next(key for key in structure if structure[key]["name"] == nextArchName)
            nextBlockName = structure[nextArchIndex]["finalBlock"]
            nextBlockIndex = next(key for key in structure if structure[key]["name"] == nextBlockName)
            # self.logger("nuova coppia arco-blocco: " + nextArchName + " " + nextBlockName)
            index = nextBlockIndex
            yield nextArchIndex, nextBlockIndex
