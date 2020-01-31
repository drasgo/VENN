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
        initBlockIndex = self.returnFirstCompleteDiagram(self.structure)

        inputNode = keras.Input(shape=(self.ninput,), name="input")
        outputNode = None

        nodes = {self.structure[initBlockIndex]["name"]: inputNode}
        merge = {}

        getP = self.getPair(initBlockIndex)

        for arch, block, specBlock in getP:
            layerT = self.chooseNode(self.structure[block]["type"])
            print("\n\n\n indici: blocco --> " + str(block) + ", arco --> " + str(arch))
            print("CURRENT STEP: BLOCK --> " + str(self.structure[block]["name"]) + ", SPECIAL BLOCK --> " + str(specBlock))
            # Merging two branches
            if specBlock is not None:
                if specBlock not in merge:
                    print("saved in merge output node with key " + specBlock)

                    merge[specBlock] = nodes[self.structure[block]["name"]]
                    continue

                else:
                    print("nodo 1: " + str(outputNode) + ", nodo 2 :" + str(merge[specBlock]))
                    outputNode = keras.layers.add([outputNode, merge[specBlock]])
                    merge.pop(specBlock)
                    # specIndex = next(ind for ind in self.structure if self.structure[ind]["name"] == specBlock)
                    print("special node computed and spec block " + specBlock + " loaded in nodes dictionary")
                    nodes[specBlock] = outputNode
                    continue
            # If it's not merging than it is a regular block and it needs an activation function
            else:
                activationFunc = self.chooseActivation(self.structure[arch]["activFunc"])
            print("ARCH --> " + str(self.structure[arch]["name"]))

            # Layer type not supported
            if layerT is None:
                continue

            # Activation function not supported
            if activationFunc is None:
                self.logger("Error choosing activation function in TensorFlow: " +
                            str(self.structure[arch]["activFunc"]) + " not available in TensorFlow")
                return False

            tempOut = nodes[self.structure[arch]["initBlock"]]

            # Last block
            if self.structure[block]["type"] == "OUTPUT":
                print("in output node ")
                outputNode = layerT(self.noutput, activation=activationFunc,
                                    name="Output")(tempOut)

            else:
                print("mid structure")
                outputNode = layerT(int(self.structure[block]["neurons"]), activation=activationFunc,
                                    name=(str(self.structure[block]["name"])))(tempOut)

            nodes[self.structure[block]["name"]] = outputNode

        self.model = keras.Model(inputs=inputNode, outputs=outputNode)

    def saveModel(self):
        if self.model is not None:
            self.model.summary()

        else:
            self.prepareModel()
            self.model.summary()

        self.model.save(self.name)
        keras.utils.plot_model(self.model, self.name + costants.IMAGE_EXTENSION)
        # self.logger("Model saved with Tensorflow")

    def chooseNode(self, layerType):
        if layerType == "DENSE" or layerType == "OUTPUT":
            return layers.Dense
        elif layerType == "SUM":
            return layers.add
        elif layerType == "SUB":
            return layers.subtract
        elif layerType == "MULT":
            return layers.multiply
        elif layerType == "DROPOUT":
            return layers.Dropout
        elif layerType == "POOLING":
            return None
        elif layerType == "CNN":
            return None
        else:
            return None

    def chooseActivation(self, activ):
        if activ.lower() == "Hyperbolic Tangent (Tanh)".lower():
            return 'tanh'
        elif activ.lower() == "Softmax".lower():
            return 'softmax'
        elif activ.lower() == "Rectified Linear (ReLu)".lower():
            return "relu"
        elif activ.lower() == "Exponential Linear (Elu)".lower():
            return "elu"
        elif activ.lower() == "Log Softmax".lower():
            return "log_softmax"
        elif activ.lower() == "Sigmoid".lower():
            return "sigmoid"
        elif activ.lower() == "Softplus".lower():
            return "softplus"
        elif activ.lower() == "Linear".lower():
            return "linear"
        elif activ.lower() == "Hard Sigmoid".lower():
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
