import keras
import ViCreNN.costants as costants
from ViCreNN.nn.wrapperTemplate import WrapperTemplate


class FrameStructure(WrapperTemplate):

    def __init__(self, numberInput, numberOutput, structure, structureName, logger):
        super(FrameStructure, self).__init__(numberInput, numberOutput, structure, structureName, logger)

    def prepareModel(self):

        # TODO
        #  Implement multiple branches
        if self.checkNumBranches(self.structure) == 0:
            self.model = keras.models.Sequential()
            self.isSequential = True
        else:
            self.logger("Error in Keras: only sequential networks currently supported. Exiting")
            return False

        initBlockIndex = self.returnFirstCompleteSequential(self.structure)

        for arch, block in self.getArchBlock(self.structure, initBlockIndex):

            if initBlockIndex is not None:
                self.logger("nodi in input: " + str(self.ninput))
                self.model.add(keras.layers.Dense(int(self.structure[block]["neurons"]),
                                                  activation=self.chooseActivation(self.structure[arch]["activFunc"]),
                                                  input_dim=int(self.ninput)))
                initBlockIndex = None

            elif self.structure[block]["LastBlock"] is True:
                self.model.add(keras.layers.Dense(int(self.noutput),
                                                  activation=self.chooseActivation(self.structure[arch]["activFunc"])))
                self.logger("rete finita")

            else:
                self.model.add(keras.layers.Dense(int(self.structure[block]["neurons"]),
                                                  activation=self.chooseActivation(self.structure[arch]["activFunc"])))
                self.logger("nodi in " + self.structure[block]["name"] + ": " + str(self.structure[block]["neurons"]))

    def chooseActivation(self, activ):
        if activ.lower() in "Linear".lower():
            return "linear"
        elif activ.lower() in "Rectified Linear (ReLu)".lower():
            return "relu"
        elif activ.lower() in "Hyperbolic Tangent (Tanh)".lower():
            return "tanh"
        elif activ.lower() in "Exponential Linear (Elu)".lower():
            return "elu"
        elif activ.lower() in "Hard Sigmoid".lower():
            return "hard_sigmoid"
        elif activ.lower() in "Sigmoid".lower():
            return "sigmoid"
        elif activ.lower() in "Softmax".lower():
            return "softmax"
        elif activ.lower() in "Softplus".lower():
            return "softplus"
        elif activ.lower() in "Other".lower():
            self.logger("Not supported activation function: " + activ + " in Keras. Quitting")
            quit()

    #  TODO
    def chooseCost(self):
        pass

    def saveModel(self):
        if self.model is None:
            self.prepareModel()

        self.model.save(self.name)
        keras.utils.plot_model(self.model, to_file=self.name + costants.IMAGE_EXTENSION)

    # TODO
    def run(self):
        pass
