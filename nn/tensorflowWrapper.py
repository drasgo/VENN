from tensorflow import keras
from tensorflow.keras import layers
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

    def prepareModel(self):
        structInput = []
        structMiddle = []
        prevBlockProp = {}
        output = None

        for element in [block for block in self.structure if
                        self.structure[block]["block"] is True and self.structure[block]["FirstBlock"]]:
            temp = keras.Input(shape=(self.ninput,), name="input")
            structInput.append(temp)
            structMiddle.append(temp)
            prevBlockProp[str(element)] = {"name": self.structure[element]["name"], "succarch": self.structure[element]["SuccArch"]}

        final = False
        while len(self.structure) != 0 and final is False:
            for index in range(len(structInput)):

                createLayerFunc = self.createLayer(structMiddle[index], prevBlockProp[str(index)])
                # , [(structMiddle[i], prevBlockProp[i]) for i in range(len(structMiddle)) if  structMiddle[i] is not temp])

                blockArches = False

                while blockArches is False:
                    final, blockArches = next(createLayerFunc)

                    if final is False:
                        structMiddle[index], prevBlockProp[str(index)] = next(createLayerFunc)
                    else:
                        output = next(createLayerFunc)

        self.model = keras.Model(inputs=structInput[0], outputs=output)

    # TODO
    #  la variabile otherbranches serve per implementare successivamente i blocchi mult add sub div e blank
    # Add in arguments otherbranchesq
    # Find arch-> block (for current layer)+ return current block -> next arch (for next layer)
    def createLayer(self, prevLayer, prevBlockProp):
        index = None

        # Find current arch
        for elem in self.structure:
            index = elem

            if any(arch for arch in prevBlockProp["succarch"] if self.structure[elem]["name"] == arch):
                prevBlockProp["succarch"].remove(next(arch for arch in prevBlockProp["succarch"] if self.structure[elem]["name"] == arch))
                break

        # current arch
        arch = self.structure[index]
        # print(arch)

        if arch["block"] is True:
            print("Error converting structure to tensorflow")
            quit()

        # find current arch activ function
        activFunc = arch["activFunc"]

        # find current block infos
        index = None
        for elem in self.structure:
            index = elem
            if self.structure[elem]["name"] == arch["finalBlock"]:
                break

        # current block infos
        block = self.structure[str(index)]

        # find next arch
        succArch = block["SuccArch"]

        # find current block neurons number
        neurons = 0
        if block["type"] == "LAYER":
            neurons = int(block["neurons"])
        elif block["type"] == "OUTPUT":
            neurons = self.noutput
        #     TODO
        #     elif block["type"] == "SUM"/"SUB"/"MULT"/"DIV"/"BLANK":

        yield block["LastBlock"], True if len(prevBlockProp["succarch"]) == 0 else False

        if block["LastBlock"] is False:
            yield layers.Dense(neurons, activation=self.chooseActivation(activFunc), name=block["name"])(prevLayer), \
                   {"name": block["name"], "succarch": succArch} if len(prevBlockProp["succarch"]) == 0 else prevBlockProp

        else:
            yield layers.Dense(neurons, activation=self.chooseActivation(activFunc), name=block["name"])(prevLayer)

    def chooseActivation(self, activ):
        if activ == "Hyperbolic Tangent (Tanh)":
            return 'tanh'
        elif activ == "Softmax":
            return 'softmax'
        elif activ == "Rectified Linear (ReLu)":
            return "relu"
        elif activ == "Exponential Linear (Elu)":
            return "elu"
        elif activ == "Log Softmax":
            return "log_softmax"
        elif activ == "Sigmoid":
            return "sigmoid"
        elif activ == "Softplus":
            return "softplus"
        elif activ == "Linear":
            return "linear"
        elif activ == "Hard Sigmoid":
            return "hard_sigmoid"
        else:
            print("Error selecting activation function " + activ + " in Tensorflow. Quitting")
            quit()

    def setCost(self, cost):
        self.cost = cost

    def setInputOuptut(self, inputData, outputData):
        self.input = inputData
        self.output = outputData

    def saveModel(self):
        if self.model is not None:
            self.model.summary()

        else:
            self.prepareModel()
            self.model.summary()

        self.model.save(self.name)
        keras.utils.plot_model(self.model, self.name + costants.IMAGE_EXTENSION)

    def run(self):
        pass
