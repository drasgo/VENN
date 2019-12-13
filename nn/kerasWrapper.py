import keras
import gui.costants as costants


class FrameStructure:

    def __init__(self, numberInput, numberOutput, structure, structureName):
        self.ninput = numberInput
        self.noutput = numberOutput
        self.structure = structure.copy()
        self.name = structureName
        self.model = None
        self.cost = None
        self.input = None
        self.output = None
        self.model = None

    def checkNumBranches(self):
        # Check the numebr of aggregation blocks (aka sum, mult, div, sub blocks). Every aggregation block is a branch unified
        return len([block for block in self.structure if self.structure[block]["block"] is True and
                    (self.structure[block]["type"] == "SUM" or self.structure[block]["type"] == "SUB" or
                     self.structure[block]["type"] == "MULT" or self.structure[block]["type"] == "DIV")])

    def checkSequential(self):
        index = None
        # print("in check sequential")
        while True:

            if index is not None:
                break

            tempInit = next(bl for bl in self.structure if
                            self.structure[bl]["block"] is True and self.structure[bl]["FirstBlock"] is True)
            # print("nome: " + self.structure[tempInit]["name"])
            if tempInit is None:
                print("Error checking sequential structure for Keras. Exiting")
                quit()

            tempIndex = tempInit
            last = self.structure[tempIndex]["LastBlock"]

            # Checks the integrity of the branch (aka it checks that it starts from an input and through all the middle arches and blocks
            # ends with a final block. If not it removes the first block of that branch. The first valid branch (input-> ...-> output)
            # will be considered as the valid network
            while last is False:

                if self.structure[tempIndex]["block"] is True:
                    # print("è blocco")
                    tempIndex = next(block for block in self.structure if any(
                        self.structure[block]["name"] == x for x in self.structure[tempIndex]["SuccArch"]))

                else:
                    # print("è arco")
                    tempIndex = next(block for block in self.structure if
                                     self.structure[block]["name"] == self.structure[tempIndex]["finalBlock"])

                if self.structure[tempIndex]["block"] is True and self.structure[tempIndex]["LastBlock"] is True:
                    # print("finito con final block")
                    last = True
                    index = tempInit

                elif self.structure[tempIndex]["block"] is True and self.structure[tempIndex]["LastBlock"] is False and \
                        len(self.structure[tempIndex]["SuccArch"]) == 0:
                    # print("finito senza final block")
                    break

            if last is False:
                # print("rimuovo questo primo elemento perchè questo branch non ha final block:: " + self.structure[tempInit]["name"])
                self.structure.pop(tempInit)

        return index

    def prepareModel(self):

        if self.checkNumBranches() == 0:
            self.model = keras.models.Sequential()

        else:
            print("Error: only sequential networks currently supported. Exiting")
            quit()

        initBlockIndex = self.checkSequential()

        for arch, block in self.getArchBlock(initBlockIndex):

            if initBlockIndex is not None:
                print("nodi in input: " + str(self.ninput))
                self.model.add(keras.layers.Dense(int(self.structure[block]["neurons"]),
                                                  activation=self.chooseActivation(self.structure[arch]["activFunc"]),
                                                  input_dim=int(self.ninput)))
                initBlockIndex = None

            elif self.structure[block]["LastBlock"] is True:
                self.model.add(keras.layers.Dense(int(self.noutput),
                                                  activation=self.chooseActivation(self.structure[arch]["activFunc"])))
                print("rete finita")

            else:
                self.model.add(keras.layers.Dense(int(self.structure[block]["neurons"]),
                                                  activation=self.chooseActivation(self.structure[arch]["activFunc"])))
                print("nodi in " + self.structure[block]["name"] + ": " + str(self.structure[block]["neurons"]))

    def getArchBlock(self, index):
        while self.structure[index]["LastBlock"] is False:
            nextArchName = next(arch for arch in self.structure[index]["SuccArch"])
            nextArchIndex = next(key for key in self.structure if self.structure[key]["name"] == nextArchName)
            nextBlockName = self.structure[nextArchIndex]["finalBlock"]
            nextBlockIndex = next(key for key in self.structure if self.structure[key]["name"] == nextBlockName)
            print("nuova coppia arco-blocco: " + nextArchName + " " + nextBlockName)
            index = nextBlockIndex
            yield nextArchIndex, nextBlockIndex

    def chooseActivation(self, activ):
        if activ == "Linear":
            return "linear"
        elif activ == "Rectified Linear (ReLu)":
            return "relu"
        elif activ == "Hyperbolic Tangent (Tanh)":
            return "tanh"
        elif activ == "Exponential Linear (Elu)":
            return "elu"
        elif activ == "Hard Sigmoid":
            return "hard_sigmoid"
        elif activ == "Sigmoid":
            return "sigmoid"
        elif activ == "Softmax":
            return "softmax"
        elif activ == "Softplus":
            return "softplus"
        elif activ == "Other":
            print("Not supported activation function: " + activ + " in Keras. Quitting")
            quit()

    def setCost(self, cost):
        pass

    def setInputOutput(self, inputData, outputData):
        pass

    def saveModel(self):
        if self.model is None:
            self.prepareModel()

        self.model.save(self.name)
        keras.utils.plot_model(self.model, to_file=self.name + costants.IMAGE_EXTENSION)

    def run(self):
        pass
