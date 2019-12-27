class WrapperTemplate:

    def __init__(self, numberInput, numberOutput, structure, structureName):
        self.ninput = numberInput
        self.noutput = numberOutput
        self.structure = structure.copy()
        self.name = structureName
        self.model = None
        self.cost = None
        self.inputTrain = None
        self.outputTrain = None
        self.inputTest = None
        self.outputTest = None
        self.isSequential = None
        self.optimizer = None
        self.loss_object = None

    # Override it
    def chooseActivation(self, activ):
        pass

    # Override it
    def chooseCost(self):
        pass

    # Override it
    def chooseOptimizer(self):
        pass

    # Override it
    def prepareModel(self):
        pass

    # Override it
    def saveModel(self):
        pass

    # Override it
    def run(self):
        pass

    # Override it
    def test(self):
        pass

    #
    # Gets input and output data. Don't touch it
    def setInputOutput(self, inputData, outputData, test):
        if test is False:
            self.inputTrain = inputData
            self.outputTrain = outputData
        else:
            self.inputTrain = inputData[:len(inputData)*0.6]
            self.inputTest = inputData[len(inputData)*0.6:]
            self.outputTrain = outputData[:len(inputData)*0.6]
            self.outputTest = outputData[len(inputData)*0.6:]

    # Sets which cost to use. Don't touch it
    def setCost(self, cost):
        self.cost = cost

    # Sets which optimizer to use. Don't touch it
    def setOptimizer(self, optim):
        self.optimizer = optim

    # Checks how many branches has the structure. Don't touch it
    def checkNumBranches(self, structure):
        # Check the numebr of aggregation blocks (aka sum, mult, div, sub blocks). Every aggregation block is a branch unified
        return len([block for block in structure if structure[block]["block"] is True and
                    (structure[block]["type"] == "SUM" or structure[block]["type"] == "SUB" or
                     structure[block]["type"] == "MULT" or structure[block]["type"] == "DIV")])

    # For sequential models. Don't touch it
    def returnFirstCompleteSequential(self, structure):
        index = None
        # print("in check sequential")
        while True:

            if index is not None:
                break

            tempInit = next(bl for bl in structure if
                            structure[bl]["block"] is True and structure[bl]["FirstBlock"] is True)
            # print("nome: " + self.structure[tempInit]["name"])
            if tempInit is None:
                print("Error checking sequential structure for Keras. Exiting")
                quit()

            tempIndex = tempInit
            last = structure[tempIndex]["LastBlock"]

            # Checks the integrity of the branch (aka it checks that it starts from an input and through all the middle arches and blocks
            # ends with a final block. If not it removes the first block of that branch. The first valid branch (input-> ...-> output)
            # will be considered as the valid network
            while last is False:

                if structure[tempIndex]["block"] is True:
                    # print("è blocco")
                    tempIndex = next(block for block in structure if any(
                        structure[block]["name"] == x for x in structure[tempIndex]["SuccArch"]))

                else:
                    # print("è arco")
                    tempIndex = next(block for block in structure if
                                     structure[block]["name"] == structure[tempIndex]["finalBlock"])

                if structure[tempIndex]["block"] is True and structure[tempIndex]["LastBlock"] is True:
                    # print("finito con final block")
                    last = True
                    index = tempInit

                elif structure[tempIndex]["block"] is True and structure[tempIndex]["LastBlock"] is False and \
                        len(structure[tempIndex]["SuccArch"]) == 0:
                    # print("finito senza final block")
                    break

            if last is False:
                # print("rimuovo questo primo elemento perchè questo branch non ha final block:: " + self.structure[tempInit]["name"])
                structure.pop(tempInit)

        return index

    # Returns next pair of arch-block. Don't touch it
    def getArchBlock(self, structure, index):
        while structure[index]["LastBlock"] is False:
            nextArchName = next(arch for arch in structure[index]["SuccArch"])
            nextArchIndex = next(key for key in structure if structure[key]["name"] == nextArchName)
            nextBlockName = structure[nextArchIndex]["finalBlock"]
            nextBlockIndex = next(key for key in structure if structure[key]["name"] == nextBlockName)
            # print("nuova coppia arco-blocco: " + nextArchName + " " + nextBlockName)
            index = nextBlockIndex
            yield nextArchIndex, nextBlockIndex
