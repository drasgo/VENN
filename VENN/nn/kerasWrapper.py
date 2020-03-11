import sys
from VENN.nn.wrapperTemplate import WrapperTemplate
import VENN.costants as costants


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

        inputNode = keras.Input(shape=(1, self.ninput), name="input")
        outputNode = None

        # nodes dictionary keeps track of every block as keras node
        nodes = {self.structure[initBlockIndex]["name"]: inputNode}
        # merge dictionary keeps track of the two branches associated to one special block
        merge = {}

        getP = self.getPair(initBlockIndex)

        # TODO
        # TODO
        # For implementing multiple inputs support here needs to be
        # for initBlockIndex in self.returnFirstCompleteDiagram(self.structure): ...
        # which is a generator function which yields for every connected input. Then a control needs to be
        # inserted for checking if a specific block is already in the dictionary nodes, in which case it exits the
        # loop because it means that it is the second (or anyway not the first) cycle  and this branch just reconnected
        # to the other already prepared branch.
        # starts getting the next arch-block pair
        for arch, block, specBlock in getP:

            # Merging two branches
            if specBlock is not None:
                if specBlock not in merge:
                    merge[specBlock] = nodes[self.structure[block]["name"]]
                    continue

                else:
                    specIndex = next(ind for ind in self.structure if self.structure[ind]["name"] == specBlock)
                    tempNode = nodes[self.structure[block]["name"]]

                    outputNode = self.chooseNode(self.structure[specIndex]["type"], inputNode1=merge[specBlock],
                                                 inputNode2=tempNode, name=specBlock)
                    if outputNode is None:
                        self.logger("Aborting creation of model with " + self.frame)
                        self.model = None
                        return False
                    merge.pop(specBlock)
                    nodes[specBlock] = outputNode
                    continue

            # Check if layer type is valid
            if self.nodeSupport(self.structure[block]["type"]) is False:
                self.logger("Error. Layer type " + self.structure[block]["name"] +
                            " not supported in " + self.frame + ".")
                self.model = None
                return False
            # Check if Activation function is valid
            if self.functionSupport(self.structure[arch]["activFunc"]) is False:
                # if self.structure[arch]["activFunc"] != "None":
                self.logger("Error. Activation function " + str(self.structure[arch]["activFunc"]) +
                            " not supported in " + self.frame + ".")
                self.model = None
                return False

            # If it's not merging than it is a regular block and it needs regular activation function and block type
            layerT = self.chooseNode(self.structure[block]["type"])
            activationFunc = self.chooseActivation(self.structure[arch]["activFunc"])
            tempOut = nodes[self.structure[arch]["initBlock"]]

            # Last block
            if self.structure[block]["type"] == "OUTPUT":
                outputNode = layerT(self.noutput, activation=activationFunc,
                                    name="Output")(tempOut)
            # Mid blocks
            else:
                outputNode = layerT(int(self.structure[block]["neurons"]), activation=activationFunc,
                                    name=str(self.structure[block]["name"]))(tempOut)

            nodes[self.structure[block]["name"]] = outputNode

        self.model = keras.Model(inputs=inputNode, outputs=outputNode)

    def nodeSupport(self, node):
        if node == "DENSE" or node == "SUM" or node == "SUB" or node == "MULT" or \
                node == "DROPOUT" or node == "POOLING" or node == "CNN" or node == "INPUT" or node == "OUTPUT":
            return True
        else:
            return False

    def functionSupport(self, activ):
        if activ in "Hyperbolic Tangent (Tanh)" or activ in "Softmax" or activ in "Rectified Linear (ReLu)" or \
                activ in "Exponential Linear (Elu)" or activ in "Sigmoid" or activ in "Softplus" \
                or activ in "Linear" or activ in "Hard Sigmoid" or activ in "Softmax":
            return True
        else:
            return False

    def chooseNode(self, layerType, **kwargs):
        from keras import layers
        if layerType == "DENSE" or layerType == "OUTPUT":
            return layers.Dense
        elif layerType == "SUM":
            return self.sumNode(inputNode1=kwargs["inputNode1"], inputNode2=kwargs["inputNode2"], name=kwargs["name"])
        elif layerType == "SUB":
            return self.subNode(inputNode1=kwargs["inputNode1"], inputNode2=kwargs["inputNode2"], name=kwargs["name"])
        elif layerType == "MULT":
            return self.multNode(inputNode1=kwargs["inputNode1"], inputNode2=kwargs["inputNode2"], name=kwargs["name"])
        elif layerType == "DROPOUT":
            return layers.Dropout
        elif layerType == "POOLING":
            return None
        elif layerType == "CNN":
            return None
        else:
            return None

    def dimensionalityChangeforMultiply(self, node, done=False):
        """It changes the shape of the given node. If it is called before the multiplication, it just inverts the two
                dimensions ([1]x[m] -> [m]x[1]). If it is called after the multiplication, the tensor will be reshaped from
                [m]x[n] -> [1]x[m*n]
                """
        from keras import backend

        if done is False:
            return backend.reshape(node, [backend.shape(node)[0], backend.shape(node)[2], 1])
        else:
            return backend.reshape(node, [backend.shape(node)[0], 1, backend.shape(node)[1] * backend.shape(node)[2]])

    def multNode(self, inputNode1, inputNode2, name=""):
        from keras import layers

        return self.dimensionalityChangeforMultiply(
            layers.multiply([self.dimensionalityChangeforMultiply(inputNode1), inputNode2], name=name), True)

    def sumNode(self, inputNode1, inputNode2, name=""):
        from keras import layers

        if inputNode1.shape() != inputNode2.shape():
            self.logger("dimensionality error with " + str(inputNode1) + " and " + str(inputNode2) + " in pytorch")
            return None
        return layers.add([inputNode1, inputNode2], name=name)

    def subNode(self, inputNode1, inputNode2, name=""):
        from keras import layers

        if inputNode1.shape() != inputNode2.shape():
            self.logger("dimensionality error with " + str(inputNode1) + " and " + str(inputNode2) + " in pytorch")
            return None
        return layers.subtract([inputNode1, inputNode2], name=name)

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

    def chooseLoss(self):
        if self.loss == "Mean Absolute Error (MAE)":
            self.loss_object = "mean_absolute_error"
        if self.loss == "Mean Absolute Percentage Error (MAPE)":
            self.loss_object = "mean_absolute_percentage_error"
        elif self.loss == "Mean Squared Error (MSE)":
            self.loss_object = "mean_squared_error"
        elif self.loss == "Mean Squared Logarithmic Error (MSLE)":
            self.loss_object = "mean_squared_logarithmic_error"
        elif self.loss == "Hinge":
            self.loss_object = "categorical_hinge"
        elif self.loss == "Huber":
            self.loss_object = "huber_loss"
        elif self.loss == "Logaritmic Cosine (LogCosh)":
            self.loss_object = "logcosh"
        elif self.loss == "Poisson":
            self.loss_object = "poisson"
        elif self.loss == "Binary Cross Entropy (BCE)":
            self.loss_object = "binary_crossentropy"
        elif self.loss == "Categorical Cross Entropy":
            self.loss_object = "categorical_crossentropy"
        elif self.loss == "Kullback-Leibler (KLDivergence)":
            self.loss_object = "kullback_leibler_divergence"
        elif self.loss == "Sparse Categorical Cross Entropy":
            self.loss_object = "sparse_categorical_crossentropy"
        elif self.loss == "Cosine Similarity":
            self.loss_object = "cosine_proximity"
        else:
            self.loss_object = None

    def chooseOptimizer(self):
        from keras import optimizers

        if self.optimizer == "Adam":
            self.optimizer_object = optimizers.Adam
        elif self.optimizer == "SGD":
            self.optimizer_object = optimizers.SGD
        elif self.optimizer == "Adadelta":
            self.optimizer_object = optimizers.Adadelta
        elif self.optimizer == "Adagrad":
            self.optimizer_object = optimizers.Adagrad
        elif self.optimizer == "Adamax":
            self.optimizer_object = optimizers.Adamax
        elif self.optimizer == "Nadam":
            self.optimizer_object = optimizers.Nadam
        elif self.optimizer == "RMSprop":
            self.optimizer_object = optimizers.RMSprop
        else:
            self.optimizer_object = None

    def saveModel(self):
        from keras import utils

        if self.model is None:
            self.logger("Error saving model with " + self.frame)

        self.model.save(self.name)
        self.logger("Model saved with " + self.frame)
        self.model.summary(print_fn=self.logger)
        utils.plot_model(self.model, to_file=self.name + costants.IMAGE_EXTENSION)

    def run(self):
        self.chooseLoss()
        self.chooseOptimizer()

        if self.loss_object is None:
            return "Error choosing cost function in Keras: " + self.loss + " not available in Keras"
        if self.optimizer_object is None:
            return "Error choosing optimizer in Keras: " + self.optimizer + " not available in Keras"

        self.model.compile(loss=self.loss_object, optimizer=self.optimizer_object, metrics=['accuracy'])
        history = self.model.fit(self.inputTrain, self.outputTrain, epochs=self.epoch)

        # Save trained

        result = "Train --> Loss: " + str(history.history["loss"]) + ", Accuracy: " + str(history.history["acc"])

        if self.test is True:
            score = self.model.evaluate(self.inputTest, self.outputTest, verbose=0)
            result = result + "Test --> Loss: " + str(score[0]) + ", Accuracy: " + str(score[1])

        self.saveModel()

        self.logger("Trained " + self.frame + " model saved correctly!")

        return result
