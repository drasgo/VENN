from tensorflow import keras
from tensorflow.keras import layers


class FrameStructure:

    def __init__(self, inputData, outputData, structure):
        self.input = inputData
        self.output = outputData
        self.structure = structure

    def prepareModel(self):
        structInput = []
        structMiddle = []
        prevBlockProp = {}

        for element in [block for block in self.structure if block["block"] is True and block["FirstBlock"]]:
            structInput.append(keras.Input(shape=(len(self.input[0])), name=["input"]))
            structMiddle.append(keras.Input(shape=(len(self.input[0])), name=["input"]))
            prevBlockProp[element["name"]] = {"name": element["name"], "succarch": element["SuccArch"]}
            self.structure.remove(element)

        final = False
        while len(self.structure) != 0 and final is False:
            for element in structInput:
                temp = structMiddle[structInput.index(element)]
                temp, prevBlockProp[structInput.index(element)], final = self.createLayer(temp, prevBlockProp[structInput.index(element)],
                                        [(structMiddle[i], prevBlockProp[i]) for i in range(len(structMiddle) - 1)
                                         if structMiddle[i] is not temp])

    # TODO
    #  la variabile otherbranches serve per implementare successivamente i blocchi mult add sub div e blank
    def createLayer(self, prevLayer, prevBlockProp, otherBranches):
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

        return layers.Dense(neurons, activation=self.chooseActivation(activFunc), name=blockName)(prevLayer), \
                            {"name": blockName, "succarch": block["SuccArch"]}, block["FinalBlock"]

    def chooseActivation(self, activ):
        pass

    def saveModel(self):
        pass





inputs = keras.Input(shape=(784,), name='digits')
x = layers.Dense(64, activation='relu', name='dense_1')(inputs)
x = layers.Dense(64, activation='relu', name='dense_2')(x)
outputs = layers.Dense(10, activation='softmax', name='predictions')(x)

model = keras.Model(inputs=inputs, outputs=outputs, name='3_layer_mlp')
model.summary()
