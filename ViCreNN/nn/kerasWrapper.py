import keras
import ViCreNN.costants as costants
from ViCreNN.nn.wrapperTemplate import WrapperTemplate
import sys


class FrameStructure(WrapperTemplate):

    def __init__(self, numberInput, numberOutput, structure, structureName, logger):
        super(FrameStructure, self).__init__(numberInput, numberOutput, structure, structureName, logger)
        self.frame = "Keras"

    def prepareModel(self, called=False):
        # Check if this function is called from keras wrapper or from tensorflow wrapper
        if called is True:
            if "keras" in sys.modules:
                del sys.modules["keras"]
            from tensorflow import keras
        else:
            import keras

        # Input Block
        initBlockIndex = self.returnFirstCompleteDiagram(self.structure)

        inputNode = keras.Input(shape=(self.ninput,), name="input")
        outputNode = None

        # nodes dictionary keeps track of every block as keras node
        nodes = {self.structure[initBlockIndex]["name"]: inputNode}
        # merge dictionary keeps track of the two branches associated to one special block
        merge = {}

        getP = self.getPair(initBlockIndex)

        # starts getting the next arch-block pair
        for arch, block, specBlock in getP:

            # Merging two branches
            if specBlock is not None:
                if specBlock not in merge:
                    merge[specBlock] = nodes[self.structure[block]["name"]]
                    continue

                else:
                    specIndex = next(ind for ind in self.structure if self.structure[ind]["name"] == specBlock)
                    layerT = self.chooseNode(self.structure[specIndex]["type"])
                    outputNode = layerT(name=specBlock)([outputNode, merge[specBlock]])
                    merge.pop(specBlock)
                    nodes[specBlock] = outputNode
                    continue

            # If it's not merging than it is a regular block and it needs regular activation function and block type
            layerT = self.chooseNode(self.structure[block]["type"])
            activationFunc = self.chooseActivation(self.structure[arch]["activFunc"])

            # Check if layer typer is valid
            if layerT is None:
                self.logger(
                    "Layer type " + self.structure[block]["name"] + " not supported in " + self.frame + ". Skipping layer")
                continue

            # Check if Activation function is valid
            if activationFunc is None:
                self.logger("Activation function" + str(
                    self.structure[arch]["activFunc"]) + " not supported in " + self.frame + ". Skipping layer")
                continue

            tempOut = nodes[self.structure[arch]["initBlock"]]

            # Last block
            if self.structure[block]["type"] == "OUTPUT":
                outputNode = layerT(self.noutput, activation=activationFunc,
                                    name="Output")(tempOut)
            # Mid blocks
            else:
                outputNode = layerT(int(self.structure[block]["neurons"]), activation=activationFunc,
                                    name=(str(self.structure[block]["name"])))(tempOut)

            nodes[self.structure[block]["name"]] = outputNode

        self.model = keras.Model(inputs=inputNode, outputs=outputNode)

    def saveModel(self):
        if self.model is None:
            self.prepareModel()

        self.model.save(self.name)
        keras.utils.plot_model(self.model, to_file=self.name + costants.IMAGE_EXTENSION)

    def chooseNode(self, layerType):
        if layerType == "DENSE" or layerType == "OUTPUT":
            return keras.layers.Dense
        elif layerType == "SUM":
            return keras.layers.Add
        elif layerType == "SUB":
            return keras.layers.Subtract
        elif layerType == "MULT":
            return keras.layers.Multiply
        elif layerType == "DROPOUT":
            return keras.layers.Dropout
        elif layerType == "POOLING":
            return None
        elif layerType == "CNN":
            return None
        else:
            return None

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
            return None

    def chooseCost(self):
        if self.cost == "Mean Absolute Error (MAE)":
            self.loss_object = "mean_absolute_error"
        if self.cost == "Mean Absolute Percentage Error (MAPE)":
            self.loss_object = "mean_absolute_percentage_error"
        elif self.cost == "Mean Squared Error (MSE)":
            self.loss_object = "mean_squared_error"
        elif self.cost == "Mean Squared Logarithmic Error (MSLE)":
            self.loss_object = "mean_squared_logarithmic_error"
        elif self.cost == "Hinge":
            self.loss_object = "categorical_hinge"
        elif self.cost == "Huber":
            self.loss_object = "huber_loss"
        elif self.cost == "Logaritmic Cosine (LogCosh)":
            self.loss_object = "logcosh"
        elif self.cost == "Poisson":
            self.loss_object = "poisson"
        elif self.cost == "Binary Cross Entropy (BCE)":
            self.loss_object = "binary_crossentropy"
        elif self.cost == "Categorical Cross Entropy":
            self.loss_object = "categorical_crossentropy"
        elif self.cost == "Kullback-Leibler (KLDivergence)":
            self.loss_object = "kullback_leibler_divergence"
        elif self.cost == "Sparse Categorical Cross Entropy":
            self.loss_object = "sparse_categorical_crossentropy"
        elif self.cost == "Cosine Similarity":
            self.loss_object = "cosine_proximity"
        else:
            self.loss_object = None

    def chooseOptimizer(self):
        if self.optimizer == "Adam":
            self.optimizer_object = keras.optimizers.Adam
        elif self.optimizer == "SGD":
            self.optimizer_object = keras.optimizers.SGD
        elif self.optimizer == "Adadelta":
            self.optimizer_object = keras.optimizers.Adadelta
        elif self.optimizer == "Adagrad":
            self.optimizer_object = keras.optimizers.Adagrad
        elif self.optimizer == "Adamax":
            self.optimizer_object = keras.optimizers.Adamax
        elif self.optimizer == "Nadam":
            self.optimizer_object = keras.optimizers.Nadam
        elif self.optimizer == "RMSprop":
            self.optimizer_object = keras.optimizers.RMSprop
        else:
            self.optimizer_object = None

    def run(self):
        self.chooseCost()
        self.chooseOptimizer()

        if self.loss_object is None:
            return "Error choosing cost function in Keras: " + self.cost + " not available in Keras"
        if self.optimizer_object is None:
            return "Error choosing optimizer in Keras: " + self.optimizer + " not available in Keras"

        self.model.compile(loss=self.loss_object, optimizer=self.optimizer_object, metrics=['accuracy'])
        history = self.model.fit(self.inputTrain, self.outputTrain, epochs=self.epoch)

        return "Train --> Loss: " + str(history.history["loss"]) + ", Accuracy: " + str(history.history["acc"])

    def test(self):
        score = self.model.evaluate(self.inputTest, self.outputTest, verbose=0)
        return "Test --> Loss: " + str(score[0]) + ", Accuracy: " + str(score[1])
