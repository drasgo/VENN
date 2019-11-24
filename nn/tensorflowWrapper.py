from tensorflow import keras
from tensorflow.keras import layers


class FrameStructure:

    def __init__(self, numberInput, numberOutput, structure):
        self.ninput = numberInput
        self.noutput = numberOutput
        self.structure = structure
        self.model = None

    def prepareModel(self):
        structInput = []
        structMiddle = []
        prevBlockProp = {}
        finalBlock = None
        finalLayer = None
        # print([self.structure[block] for block in self.structure])
        for element in [block for block in self.structure if self.structure[block]["block"] is True and self.structure[block]["FirstBlock"]]:
            structInput.append(keras.Input(shape=(self.ninput, ), name="input"))
            structMiddle.append(keras.Input(shape=(self.ninput, ), name="input"))
            prevBlockProp[self.structure[element]["name"]] = {"name": self.structure[element]["name"], "succarch": self.structure[element]["SuccArch"]}
            self.structure.pop(element)

        final = False
        while len(self.structure) != 0 and final is False:
            for element in structInput:
                temp = structMiddle[structInput.index(element)]
                # print("temp " + str(temp))
                # print("element " + str(element))
                # print("structuinput.index[element]" + str(structInput.index(element)))
                # print("prevblockprop " + str(prevBlockProp))
                # print("list(prevblockprop.values())[structinput.index[element] " + str(list(prevBlockProp.values())[structInput.index(element)]))
                final = self.createLayer(temp, list(prevBlockProp.values())[structInput.index(element)])
                                         #, [(structMiddle[i], prevBlockProp[i]) for i in range(len(structMiddle)) if
                                         #  structMiddle[i] is not temp])
                if final is False:
                    temp, prevBlockProp[structInput.index(element)] = \
                        self.createLayer(temp, list(prevBlockProp.values())[structInput.index(element)])
                                         # , [(structMiddle[i], prevBlockProp[i]) for i in range(len(structMiddle)) if
                                         #  structMiddle[i] is not temp])
                else:
                    finalBlock = self.createLayer(temp, list(prevBlockProp.values())[structInput.index(element)])
                                         # , [(structMiddle[i], prevBlockProp[i]) for i in range(len(structMiddle)) if
                                         #  structMiddle[i] is not temp])
                    finalLayer = temp

        output = layers.Dense(self.noutput, activation=self.chooseCost(finalBlock["cost"]), name="output")(finalLayer)
        self.model = keras.Model(inputs=structInput[0], outputs=output)

    # TODO
    #  la variabile otherbranches serve per implementare successivamente i blocchi mult add sub div e blank
    # Add in arguments otherbranches
    def createLayer(self, prevLayer, prevBlockProp):
        index = 0
        for elem in self.structure:
            if elem["name"] == prevBlockProp["succarch"]:
                break
            index += 1
        arch = self.structure[str(index)]
        activFunc = arch["activFunc"]
        blockName = arch["finalBlock"]

        index = 0
        for elem in self.structure:
            if elem["name"] == blockName:
                break
            index += 1
        block = self.structure[str(index)]
        neurons = 0

        if block["type"] == "LAYER":
            neurons = block["neurons"]
        #     TODO
        #     elif block["type"] == "SUM"/"SUB"/"MULT"/"DIV"/"BLANK":

        yield block["final"]

        if block["final"] is False:
            return layers.Dense(neurons, activation=self.chooseActivation(activFunc), name=blockName)(prevLayer), \
           {"name": blockName, "succarch": block["SuccArch"]}, block["FinalBlock"]

        else:
            return block

    def chooseActivation(self, activ):
        if activ == "Tanh":
            return "relu"
        # TODO
        # Add activation function
        else:
            return None

    def chooseCost(self, cost):
        if cost == "MSE":
            return None
        elif cost == "CROSSENTROPY":
            return "softmax"

    def saveModel(self):
        if self.model is not None:
            self.model.summary()
        else:
            self.prepareModel()
            self.model.summary()

#
# inputs = keras.Input(shape=(784,), name='digits')
# x = layers.Dense(64, activation='relu', name='dense_1')(inputs)
# x = layers.Dense(64, activation='relu', name='dense_2')(x)
# outputs = layers.Dense(10, activation='softmax', name='predictions')(x)
#
# model = keras.Model(inputs=inputs, outputs=outputs, name='3_layer_mlp')
# model.summary()
