from tensorflow.keras import utils, losses, optimizers, metrics
from tensorflow import GradientTape
from tensorflow import nn
from tensorflow import reshape
from tensorflow import shape
from tensorflow.keras import layers
import VENN.costants as costants
from VENN.nn.kerasWrapper import FrameStructure as kerasWrapper


class FrameStructure(kerasWrapper):
    def __init__(self, numberInput, numberOutput, structure, structureName, logger):
        kerasWrapper.__init__(
            self, numberInput, numberOutput, structure, structureName, logger
        )
        self.frame = "TensorFlow"

    def prepareModel(self, called=False):
        return kerasWrapper.prepareModel(self, True)

    def nodeSupport(self, node):
        if (
            node == "DENSE"
            or node == "SUM"
            or node == "SUB"
            or node == "MULT"
            or node == "DROPOUT"
            or node == "POOLING"
            or node == "CNN"
            or node == "INPUT"
            or node == "OUTPUT"
        ):
            return True
        else:
            return False

    def functionSupport(self, activ):
        if (
            activ == "Hyperbolic Tangent (Tanh)"
            or activ == "Softmax"
            or activ == "Rectified Linear (ReLu)"
            or activ == "Exponential Linear (Elu)"
            or activ == "Sigmoid"
            or activ == "Softplus"
            or activ == "Linear"
            or activ == "Hard Sigmoid"
            or activ == "Softmax"
            or activ == "Log Softmax"
        ):
            return True
        else:
            return False

    def chooseNode(self, layerType, **kwargs):
        if layerType == "DENSE" or layerType == "OUTPUT":
            return layers.Dense
        elif layerType == "SUM":
            return self.sumNode(
                inputNode1=kwargs["inputNode1"],
                inputNode2=kwargs["inputNode2"],
                name=kwargs["name"],
            )
        elif layerType == "SUB":
            return self.subNode(
                inputNode1=kwargs["inputNode1"],
                inputNode2=kwargs["inputNode2"],
                name=kwargs["name"],
            )
        elif layerType == "MULT":
            return self.multNode(
                inputNode1=kwargs["inputNode1"],
                inputNode2=kwargs["inputNode2"],
                name=kwargs["name"],
            )
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
        if done is False:
            return reshape(node, [shape(node)[0], shape(node)[2], 1])
        else:
            return reshape(node, [shape(node)[0], 1, shape(node)[1] * shape(node)[2]])

    def multNode(self, inputNode1, inputNode2, name=""):
        return self.dimensionalityChangeforMultiply(
            layers.multiply(
                [self.dimensionalityChangeforMultiply(inputNode1), inputNode2],
                name=name,
            ),
            True,
        )

    def sumNode(self, inputNode1, inputNode2, name=""):
        if inputNode1.shape() != inputNode2.shape():
            self.logger(
                "dimensionality error with "
                + str(inputNode1)
                + " and "
                + str(inputNode2)
                + " in pytorch"
            )
            return None
        return layers.add([inputNode1, inputNode2], name=name)

    def subNode(self, inputNode1, inputNode2, name=""):
        if inputNode1.shape() != inputNode2.shape():
            self.logger(
                "dimensionality error with "
                + str(inputNode1)
                + " and "
                + str(inputNode2)
                + " in pytorch"
            )
            return None
        return layers.subtract([inputNode1, inputNode2], name=name)

    def chooseActivation(self, activ):
        tempActiv = kerasWrapper.chooseActivation(self, activ)
        if tempActiv is not None:
            return tempActiv
        else:
            if activ.lower() == "Log Softmax".lower():
                return "log_softmax"
            else:
                return None

    def chooseLoss(self):
        if self.loss == "Mean Absolute Error (MAE)":
            self.loss_object = losses.MeanAbsoluteError
        if self.loss == "Mean Absolute Percentage Error (MAPE)":
            self.loss_object = losses.MeanAbsolutePercentageError
        elif self.loss == "Mean Squared Error (MSE)":
            self.loss_object = losses.MeanSquaredError
        elif self.loss == "Mean Squared Logarithmic Error (MSLE)":
            self.loss_object = losses.MeanSquaredLogarithmicError
        elif self.loss == "Hinge":
            self.loss_object = losses.Hinge
        elif self.loss == "Huber":
            self.loss_object = losses.Huber
        elif self.loss == "Logaritmic Cosine (LogCosh)":
            self.loss_object = losses.LogCosh
        elif self.loss == "Poisson":
            self.loss_object = losses.Poisson
        elif self.loss == "Binary Cross Entropy (BCE)":
            self.loss_object = losses.BinaryCrossentropy
        elif self.loss == "Categorical Cross Entropy":
            self.loss_object = losses.CategoricalCrossentropy
        elif self.loss == "Kullback-Leibler (KLDivergence)":
            self.loss_object = losses.KLDivergence
        elif self.loss == "Sparse Categorical Cross Entropy":
            self.loss_object = losses.SparseCategoricalCrossentropy
        elif self.loss == "Cosine Similarity":
            self.loss_object = losses.CosineSimilarity
        elif self.loss == "Log-Likelihood":
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

    def saveModel(self):

        if self.model is None:
            self.logger("Error saving model with " + self.frame)
            return

        self.logger("Model saved with " + self.frame)
        self.model.summary()
        self.model.summary(print_fn=self.logger)
        self.model.save(self.name)
        utils.plot_model(self.model, self.name + costants.IMAGE_EXTENSION)

    def run(self):
        train_loss = metrics.Mean(name="train_loss")
        train_accuracy = metrics.SparseCategoricalAccuracy(name="train_accuracy")

        self.chooseLoss()
        self.chooseOptimizer()

        if self.loss_object is None:
            return (
                "Error choosing cost function in "
                + self.frame
                + ": "
                + self.loss
                + " not available in TensorFlow"
            )
        if self.optimizer_object is None:
            return (
                "Error choosing optimizer in "
                + self.frame
                + ": "
                + self.optimizer
                + " not available in TensorFlow"
            )

        with GradientTape() as tape:
            for epoch in range(self.epoch):
                predictions = self.model(self.inputTrain)
                loss = self.loss_object(self.outputTrain, predictions)
                gradients = tape.gradient(loss, self.model.trainable_variables)
                self.optimizer_object.apply_gradients(
                    zip(gradients, self.model.trainable_variables)
                )

        train_loss(loss)
        train_accuracy(self.outputTrain, predictions)

        result = (
            "Train --> Loss: "
            + str(train_loss.result())
            + ", Accuracy: "
            + str(train_accuracy.result() * 100)
        )

        if self.test is True:
            test_loss = metrics.Mean(name="test_loss")
            test_accuracy = metrics.SparseCategoricalAccuracy(name="test_accuracy")

            predictions = self.model(self.inputTest)
            t_loss = self.loss_object(self.outputTest, predictions)

            test_loss(t_loss)
            test_accuracy(self.outputTest, predictions)

            result = (
                result
                + "Test --> Loss: "
                + str(test_loss.result())
                + ", Accuracy: "
                + str(test_accuracy.result() * 100)
            )

        self.saveModel()

        self.logger("Trained " + self.frame + " model saved correctly!")

        return result
