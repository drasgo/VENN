from tensorflow.keras import utils, losses, optimizers, metrics
from tensorflow import GradientTape
from tensorflow import nn
from tensorflow.keras import layers
import ViCreNN.costants as costants
from ViCreNN.nn.kerasWrapper import FrameStructure as kerasWrapper


class FrameStructure(kerasWrapper):

    def __init__(self, numberInput, numberOutput, structure, structureName, logger):
        kerasWrapper.__init__(self, numberInput, numberOutput, structure, structureName, logger)
        self.frame = "TensorFlow"

    def prepareModel(self, called=False):
        kerasWrapper.prepareModel(self, True)

    def saveModel(self):
        if self.model is not None:
            self.model.summary()

        else:
            self.prepareModel()
            self.model.summary()

        self.model.save(self.name)
        utils.plot_model(self.model, self.name + costants.IMAGE_EXTENSION)
        # self.logger("Model saved with Tensorflow")

    def nodeSupport(self, node):
        if node == "DENSE" or node == "SUM" or node == "SUB" or node == "MULT" or \
                node == "DROPOUT" or node == "POOLING" or node == "CNN" or node == "INPUT" or node == "OUTPUT":
            return True
        else:
            return False

    def functionSupport(self, activ):
        if activ == "Hyperbolic Tangent (Tanh)" or activ == "Softmax" or activ == "Rectified Linear (ReLu)" or \
                activ == "Exponential Linear (Elu)" or activ == "Sigmoid" or activ == "Softplus" \
                or activ == "Linear" or activ == "Hard Sigmoid" or activ == "Softmax" or activ == "Log Softmax":
            return True
        else:
            return False

    def chooseNode(self, layerType, **kwargs):
        if layerType == "DENSE" or layerType == "OUTPUT":
            return layers.Dense
        elif layerType == "SUM":
            return layers.Add
        elif layerType == "SUB":
            return layers.Subtract
        elif layerType == "MULT":
            return layers.Multiply
        elif layerType == "DROPOUT":
            return layers.Dropout
        elif layerType == "POOLING":
            return None
        elif layerType == "CNN":
            return None
        else:
            return None

    def chooseActivation(self, activ):
        tempActiv = kerasWrapper.chooseActivation(self, activ)
        if tempActiv is not None:
            return tempActiv
        else:
            if activ.lower() == "Log Softmax".lower():
                return "log_softmax"
            else:
                return None

    def chooseCost(self):
        if self.cost == "Mean Absolute Error (MAE)":
            self.loss_object = losses.MeanAbsoluteError
        if self.cost == "Mean Absolute Percentage Error (MAPE)":
            self.loss_object = losses.MeanAbsolutePercentageError
        elif self.cost == "Mean Squared Error (MSE)":
            self.loss_object = losses.MeanSquaredError
        elif self.cost == "Mean Squared Logarithmic Error (MSLE)":
            self.loss_object = losses.MeanSquaredLogarithmicError
        elif self.cost == "Hinge":
            self.loss_object = losses.Hinge
        elif self.cost == "Huber":
            self.loss_object = losses.Huber
        elif self.cost == "Logaritmic Cosine (LogCosh)":
            self.loss_object = losses.LogCosh
        elif self.cost == "Poisson":
            self.loss_object = losses.Poisson
        elif self.cost == "Binary Cross Entropy (BCE)":
            self.loss_object = losses.BinaryCrossentropy
        elif self.cost == "Categorical Cross Entropy":
            self.loss_object = losses.CategoricalCrossentropy
        elif self.cost == "Kullback-Leibler (KLDivergence)":
            self.loss_object = losses.KLDivergence
        elif self.cost == "Sparse Categorical Cross Entropy":
            self.loss_object = losses.SparseCategoricalCrossentropy
        elif self.cost == "Cosine Similarity":
            self.loss_object = losses.CosineSimilarity
        elif self.cost == "Log-Likelihood":
            self.loss_object = nn.log_poisson_loss
        else:
            self.loss_object = None

    def chooseOptimizer(self):
        if self.optimizer == "Adam":
            self.optimizer_object = optimizers.Adam
        elif self.optimizer == "SDG":
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
        elif self.optimizer == "Ftrl":
            self.optimizer_object = optimizers.Ftrl
        else:
            self.optimizer_object = None

    def run(self):
        train_loss = metrics.Mean(name='train_loss')
        train_accuracy = metrics.SparseCategoricalAccuracy(name='train_accuracy')

        self.chooseCost()
        self.chooseOptimizer()

        if self.loss_object is None:
            return "Error choosing cost function in " + self.frame + ": " + self.cost + " not available in TensorFlow"
        if self.optimizer_object is None:
            return "Error choosing optimizer in " + self.frame + ": " + self.optimizer + " not available in TensorFlow"

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
        test_loss = metrics.Mean(name='test_loss')
        test_accuracy = metrics.SparseCategoricalAccuracy(name='test_accuracy')

        predictions = self.model(self.inputTest)
        t_loss = self.loss_object(self.outputTest, predictions)

        test_loss(t_loss)
        test_accuracy(self.outputTest, predictions)

        return "Test --> Loss: " + str(test_loss.result()) + ", Accuracy: " + str(test_accuracy.result() * 100)
