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
        self.isSequential = None

    def prepareModel(self):
        # TODO
        #  Implement multiple branches
        if costants.checkNumBranches(self.structure) == 0:
            self.isSequential = True

        else:
            print("Error in Keras: only sequential networks currently supported. Exiting")
            return False

        initBlockIndex = costants.returnFirstCompleteSequential(self.structure)

        inputNode = keras.Input(shape=(self.ninput,), name="input")
        outputNode = None
        initIndex = True

        for arch, block in costants.getArchBlock(self.structure, initBlockIndex):

            if initIndex is True:
                outputNode = inputNode
                initIndex = False

            if self.structure[block]["LastBlock"]:
                neurons = self.noutput
            else:
                neurons = int(self.structure[block]["neurons"])

            outputNode = layers.Dense(neurons, activation=self.chooseActivation(self.structure[arch]["activFunc"]),
                                      name=("block" + str(self.structure[block]["name"])))(outputNode)

        self.model = keras.Model(inputs=inputNode, outputs=outputNode)
    
    # TODO
    def chooseBlock(self, block):
        pass
    
    def chooseActivation(self, activ):
        if activ.lower() in "Hyperbolic Tangent (Tanh)".lower():
            return 'tanh'
        elif activ.lower() in "Softmax".lower():
            return 'softmax'
        elif activ.lower() in "Rectified Linear (ReLu)".lower():
            return "relu"
        elif activ.lower() in "Exponential Linear (Elu)".lower():
            return "elu"
        elif activ.lower() in "Log Softmax".lower():
            return "log_softmax"
        elif activ.lower() in "Sigmoid".lower():
            return "sigmoid"
        elif activ.lower() in "Softplus".lower():
            return "softplus"
        elif activ.lower() in "Linear".lower():
            return "linear"
        elif activ.lower() in "Hard Sigmoid".lower():
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
