import keras.models
import keras.layers


# TODO
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
        return len([block for block in self.structure if self.structure[block]["type"] == "SUM" or self.structure[block]["type"] == "SUB" or self.structure[block]["type"] == "MULT" or self.structure[block]["type"] == "DIV"])

    def checkSequential(self):
        index = None

        while True:

            if index is not None:
                break

            tempInit = next(bl for bl in self.structure if self.structure[bl]["block"] is True and self.structure[bl]["FirstBlock"] is True)

            if tempInit is None:
                print("Error checking sequential structure for Keras. Exiting")
                quit()

            tempIndex = tempInit
            last = self.structure[tempIndex]["FinalBlock"]

            # Checks the integrity of the branch (aka it checks that it starts from an input and through all the middle arches and blocks
            # ends with a final block. If not it removes the first block of that branch. The first valid branch (input-> ...-> output)
            # will be considered as the valid network
            while last is False:

                if self.structure[tempIndex]["block"] is True:
                    tempIndex = next(block for block in self.structure if self.structure[block]["name"] == next(self.structure[tempIndex]["SuccArch"]))

                else:
                    tempIndex = next(block for block in self.structure if self.structure[block]["name"] == self.structure[tempIndex]["FinalBlock"])

                if self.structure[tempIndex]["block"] is True and self.structure[tempIndex]["FinalBlock"] is True:
                    last = True
                    index = tempInit

                elif self.structure[tempIndex]["block"] is True and self.structure[tempIndex]["FinalBlock"] is False and len(self.structure[tempIndex]["SuccArch"]) == 0:
                    break

            if last is False:
                self.structure.pop(tempInit)

        return index

    def prepareModel(self):
        structInput = []
        tempBlock = []

        if self.checkNumBranches() == 0:
            self.model = keras.models.Sequential()

        # TODO
        else:
            print("Error: only sequential networks currently supported. Exiting")
            quit()

        initBlockIndex = self.checkSequential()

        # ///////////

        for elem in [self.structure[block] for block in self.structure if self.structure[block]["block"] is True and
                                                          self.structure[block]["FirstBlock"] is True]:
            structInput.append()

    def setCost(self, cost):
        pass

    def setInputOutput(self, inputData, outputData):
        pass

    def saveModel(self):
        pass

    def run(self):
        pass


model = Sequential()

model.add(Convolution2D(32, 3, 3, activation='relu', input_shape=(1, 28, 28)))
model.add(Convolution2D(32, 3, 3, activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))
