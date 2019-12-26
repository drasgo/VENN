from tensorflow import keras
from tensorflow import GradientTape
from tensorflow.keras import layers
import gui.costants as costants
from nn.wrapperTemplate import WrapperTemplate


class FrameStructure(WrapperTemplate):

    def __init__(self, numberInput, numberOutput, structure, structureName):
        super(FrameStructure, self).__init__(numberInput, numberOutput, structure, structureName)

    def prepareModel(self):
        # TODO
        #  Implement multiple branches
        if self.checkNumBranches(self.structure) == 0:
            self.isSequential = True

        else:
            print("Error in Keras: only sequential networks currently supported. Exiting")
            return False

        initBlockIndex = self.returnFirstCompleteSequential(self.structure)

        inputNode = keras.Input(shape=(self.ninput,), name="input")
        outputNode = None
        initIndex = True

        for arch, block in self.getArchBlock(self.structure, initBlockIndex):

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

    def saveModel(self):
        if self.model is not None:
            self.model.summary()

        else:
            self.prepareModel()
            self.model.summary()

        self.model.save(self.name)
        keras.utils.plot_model(self.model, self.name + costants.IMAGE_EXTENSION)

    # TODO
    def run(self):
        train_loss = keras.metrics.Mean(name='train_loss')
        train_accuracy = keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')

        with GradientTape() as tape:
            predictions = self.model(self.input)
            loss = self.loss_object(self.output, predictions)
            gradients = tape.gradient(loss, self.model.trainable_variables)
            self.optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))

        train_loss(loss)
        train_accuracy(self.output, predictions)

    # TODO
    def chooseCost(self):
        self.loss_object = keras.losses.SparseCategoricalCrossentropy()

    # TODO
    def chooseOptimizer(self):
        self.optimizer = keras.optimizers.Adam()

    # TODO
    def test(self):
        pass

    # TODO
    def chooseBlock(self, block):
        pass
