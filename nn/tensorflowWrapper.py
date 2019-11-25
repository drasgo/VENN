from tensorflow import keras
from tensorflow.keras import layers
import pprint


class FrameStructure:

    def __init__(self, numberInput, numberOutput, structure):
        self.ninput = numberInput
        self.noutput = numberOutput
        self.structure = structure.copy()
        self.model = None

    def prepareModel(self):
        structInput = []
        structMiddle = []
        prevBlockProp = {}
        finalBlock = {}
        finalLayer = None
        pprint.pprint(self.structure, indent=4)
        for element in [block for block in self.structure if
                        self.structure[block]["block"] is True and self.structure[block]["FirstBlock"]]:

            structInput.append(keras.Input(shape=(self.ninput,), name="input"))
            structMiddle.append(keras.Input(shape=(self.ninput,), name="input"))
            prevBlockProp[element] = {"name" : self.structure[element]["name"], "succarch": self.structure[element]["SuccArch"]}
            # pprint.pprint(str(prevBlockProp))
            self.structure.pop(element)

        final = False
        while len(self.structure) != 0 and final is False:
            for element in structInput:

                temp = structMiddle[structInput.index(element)]

                createLayerFunc = self.createLayer(temp, prevBlockProp[element])
                # , [(structMiddle[i], prevBlockProp[i]) for i in range(len(structMiddle)) if  structMiddle[i] is not temp])

                blockArches = False

                while blockArches is False:

                    final, blockArches = next(createLayerFunc)

                    if final is False:
                        temp, prevBlockProp[element] = next(createLayerFunc)
                        print("prevBlockProp:")
                        pprint.pprint(prevBlockProp)
                    else:
                        finalBlock = next(createLayerFunc)
                        finalLayer = temp

        output = layers.Dense(self.noutput, activation=self.chooseCost(finalBlock["cost"]), name="output")(finalLayer)
        self.model = keras.Model(inputs=structInput[0], outputs=output)

    # TODO
    #  la variabile otherbranches serve per implementare successivamente i blocchi mult add sub div e blank
    # Add in arguments otherbranches
    # Find arch-> block (for current layer)+ return current block -> next arch (for next layer)
    def createLayer(self, prevLayer, prevBlockProp):
        index = None
        print("\nin create layer")
        pprint.pprint(str(prevBlockProp))

        # Find current arch
        for elem in self.structure:
            index = elem

            if any(arch for arch in prevBlockProp["succarch"] if self.structure[elem]["name"] == arch):
                prevBlockProp["succarch"].remove(next(arch for arch in prevBlockProp["succarch"] if self.structure[elem]["name"] == arch))
                break

        arch = self.structure[index]
        if arch["block"] is True:
            print("Error converting structure to tensorflow")
            quit()

        activFunc = arch["activFunc"]
        # find current block
        blockName = prevBlockProp["name"]
        # find next arch
        succArch = next(self.structure[arch]["name"] for arch in self.structure if self.structure[arch]["block"]
                        is False and self.structure[arch]["initBlock"] == blockName)

        index = None
        for elem in self.structure:
            index = elem
            if self.structure[elem]["name"] == blockName:
                break

        # current block infos
        block = self.structure[str(index)]
        neurons = 0

        if block["type"] == "LAYER":
            neurons = int(block["neurons"])
        #     TODO
        #     elif block["type"] == "SUM"/"SUB"/"MULT"/"DIV"/"BLANK":

        # print("block[final] " + str(block["final"]))

        pprint.pprint(str(prevLayer))
        pprint.pprint(str(prevBlockProp))
        print("num archi succ " + str(len(prevBlockProp["succarch"])))
        print("curr block " + blockName)
        print("curr arch " + arch["name"])
        print("succ arch " + str(succArch))

        yield block["LastBlock"], True if len(prevBlockProp["succarch"]) == 0 else False

        if block["LastBlock"] is False:
            yield layers.Dense(neurons, activation=self.chooseActivation(activFunc), name=blockName)(prevLayer), \
                   {"name": blockName, "succarch": succArch} if len(prevBlockProp["succarch"]) == 0 else prevBlockProp

        else:
            # print("block in create layer " + str(block))
            yield block

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
