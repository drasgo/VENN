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
            self.logger("Error in Keras: only sequential networks currently supported")
            return False

        initBlockIndex = self.returnFirstCompleteSequential(self.structure)

        for arch, block in self.getArchBlock(self.structure, initBlockIndex):
            activationFunc = self.chooseActivation(self.structure[arch]["activFunc"])

            if activationFunc is None:
                self.logger(
                    "Error choosing activation function in Keras: " + str(self.structure[arch]["activFunc"]) + " not available in Keras")
                return False

            if initBlockIndex is not None:
                self.model.add(keras.layers.Dense(int(self.structure[block]["neurons"]),
                                                  activation=self.chooseActivation(self.structure[arch]["activFunc"]),
                                                  input_shape=int(self.ninput, )))
                initBlockIndex = None

            if self.structure[block]["LastBlock"]:
                neurons = self.noutput

            else:
                neurons = int(self.structure[block]["neurons"])

            self.model.add(
                keras.layers.Dense(neurons, activation=self.chooseActivation(self.structure[arch]["activFunc"])))

    def saveModel(self):
        if self.model is None:
            self.prepareModel()

        self.model.save(self.name)
        keras.utils.plot_model(self.model, to_file=self.name + costants.IMAGE_EXTENSION)

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
