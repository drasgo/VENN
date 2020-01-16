from tensorflow import keras
from tensorflow import GradientTape
import tensorflow as tf
from tensorflow.keras import layers
import ViCreNN.costants as costants
from ViCreNN.nn.wrapperTemplate import WrapperTemplate


class FrameStructure(WrapperTemplate):

    def __init__(self, numberInput, numberOutput, structure, structureName, logger):
        super(FrameStructure, self).__init__(numberInput, numberOutput, structure, structureName, logger)

    def prepareModel(self):
        # TODO
        #  Implement multiple branches
        if self.checkNumBranches(self.structure) == 0:
            self.isSequential = True

        else:
            self.logger("Error in Keras: only sequential networks currently supported")
            return False

        initBlockIndex = self.returnFirstCompleteSequential(self.structure)

        inputNode = keras.Input(shape=(self.ninput,), name="input")
        outputNode = None
        initIndex = True

        for arch, block in self.getArchBlock(self.structure, initBlockIndex):
            activationFunc = self.chooseActivation(self.structure[arch]["activFunc"])
            layerT = self.chooseNode(self.structure[block]["type"])

            if layerT is None:
                continue

            elif activationFunc is None:
                self.logger("Error choosing activation function in TensorFlow: " +
                            str(self.structure[arch]["activFunc"]) + " not available in TensorFlow")
                return False

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

    def chooseNode(self, layerType):
        if layerType == "LAYER":
            return layers.Dense
        elif layerType == "SUM":
            return layers.Add
        elif layerType == "SUB":
            return layers.Subtract
        elif layerType == "MULT":
            return layers.Multiply
        elif layerType == "DROPOUT":
            return layers.Dropout
        else:
            return None

    def saveModel(self):
        if self.model is not None:
            self.model.summary()

        else:
            self.prepareModel()
            self.model.summary()

        self.model.save(self.name)
        keras.utils.plot_model(self.model, self.name + costants.IMAGE_EXTENSION)

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
            return None

    def chooseCost(self):
        if self.cost == "Mean Absolute Error (MAE)":
            self.loss_object = keras.losses.MeanAbsoluteError
        if self.cost == "Mean Absolute Percentage Error (MAPE)":
            self.loss_object = keras.losses.MeanAbsolutePercentageError
        elif self.cost == "Mean Squared Error (MSE)":
            self.loss_object = keras.losses.MeanSquaredError
        elif self.cost == "Mean Squared Logarithmic Error (MSLE)":
            self.loss_object = keras.losses.MeanSquaredLogarithmicError
        elif self.cost == "Hinge":
            self.loss_object = keras.losses.Hinge
        elif self.cost == "Huber":
            self.loss_object = keras.losses.Huber
        elif self.cost == "Logaritmic Cosine (LogCosh)":
            self.loss_object = keras.losses.LogCosh
        elif self.cost == "Poisson":
            self.loss_object = keras.losses.Poisson
        elif self.cost == "Binary Cross Entropy (BCE)":
            self.loss_object = keras.losses.BinaryCrossentropy
        elif self.cost == "Categorical Cross Entropy":
            self.loss_object = keras.losses.CategoricalCrossentropy
        elif self.cost == "Kullback-Leibler (KLDivergence)":
            self.loss_object = keras.losses.KLDivergence
        elif self.cost == "Sparse Categorical Cross Entropy":
            self.loss_object = keras.losses.SparseCategoricalCrossentropy
        elif self.cost == "Cosine Similarity":
            self.loss_object = keras.losses.CosineSimilarity
        elif self.cost == "Log-Likelihood":
            self.loss_object = tf.nn.log_poisson_loss
        else:
            self.loss_object = None

    def chooseOptimizer(self):
        if self.optimizer == "Adam":
            self.optimizer_object = keras.optimizers.Adam
        elif self.optimizer == "SDG":
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
        elif self.optimizer == "Ftrl":
            self.optimizer_object = keras.optimizers.Ftrl
        else:
            self.optimizer_object = None

    def run(self):
        train_loss = keras.metrics.Mean(name='train_loss')
        train_accuracy = keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')

        self.chooseCost()
        self.chooseOptimizer()

        if self.loss_object is None:
            return "Error choosing cost function in TensorFlow: " + self.cost + " not available in TensorFlow"
        if self.optimizer_object is None:
            return "Error choosing optimizer in TensorFlow: " + self.optimizer + " not available in TensorFlow"

        with GradientTape() as tape:
            for epoch in range(self.epoch):
                predictions = self.model(self.inputTrain)
                loss = self.loss_object(self.outputTrain, predictions)
                gradients = tape.gradient(loss, self.model.trainable_variables)
                self.optimizer_object.apply_gradients(zip(gradients, self.model.trainable_variables))

        train_loss(loss)
        train_accuracy(self.outputTrain, predictions)

        return "Train --> Loss: " + str(train_loss.result()) + ", Accuracy: " + str(train_accuracy.result() * 100)

    def test(self):
        test_loss = keras.metrics.Mean(name='test_loss')
        test_accuracy = keras.metrics.SparseCategoricalAccuracy(name='test_accuracy')

        predictions = self.model(self.inputTest)
        t_loss = self.loss_object(self.outputTest, predictions)

        test_loss(t_loss)
        test_accuracy(self.outputTest, predictions)

        return "Test --> Loss: " + str(test_loss.result()) + ", Accuracy: " + str(test_accuracy.result() * 100)
