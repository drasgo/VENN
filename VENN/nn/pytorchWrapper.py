import torch
import torch.nn as nn
from torchsummary import summary
from VENN.nn.wrapperTemplate import WrapperTemplate


class FrameStructure(WrapperTemplate):
    def __init__(self, numberInput, numberOutput, structure, structureName, logger):
        WrapperTemplate.__init__(
            self, numberInput, numberOutput, structure, structureName, logger
        )
        self.frame = "Pytorch"

    def prepareModel(self):
        self.model = torchModel(self)
        if self.model.ready is False:
            self.model = None
            return False

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
            or activ == "Log Softmax"
            or activ == "Sigmoid"
            or activ == "Softplus"
            or activ == "Linear"
            or activ == "Hard Hyperbolic Tangent(HardTanh)"
        ):
            return True
        else:
            return False

    def chooseNode(self, layerType, **kwargs):
        if layerType == "DENSE" or layerType == "OUTPUT":
            return torch.nn.Linear(int(kwargs["inputDim"]), int(kwargs["outputDim"]))
        elif layerType == "SUM":
            return self.sumNode(
                inputNode1=kwargs["inputNode1"], inputNode2=kwargs["inputNode2"]
            )
        elif layerType == "SUB":
            return self.subNode(
                inputNode1=kwargs["inputNode1"], inputNode2=kwargs["inputNode2"]
            )
        elif layerType == "MULT":
            return self.multNode(
                inputNode1=kwargs["inputNode1"], inputNode2=kwargs["inputNode2"]
            )
        elif layerType == "DROPOUT":
            # return torch.nn.Dropout
            return None
        elif layerType == "POOLING":
            # return torch.nn.AvgPool1d
            return None
        elif layerType == "CNN":
            # return torch.nn.Conv1d
            return None
        else:
            return None

    def dimensionalityChangeforMultiply(self, node, done=False):
        """It changes the shape of the given node. If it is called before the multiplication, it just inverts the two
        dimensions ([1]x[m] -> [m]x[1]). If it is called after the multiplication, the tensor will be reshaped from
        [m]x[n] -> [1]x[m*n]
        """
        if done is False:
            return node.view(list(node.size())[0], list(node.size())[2], 1)
        else:
            return node.reshape(
                list(node.size())[0], 1, list(node.size())[1] * list(node.size())[2]
            )

    def sumNode(self, inputNode1, inputNode2, name=""):
        if inputNode1.size() != inputNode2.size():
            self.logger(
                "dimensionality error with "
                + str(inputNode1)
                + " and "
                + str(inputNode2)
                + " in pytorch"
            )
            return None
        return inputNode1 + inputNode2

    def subNode(self, inputNode1, inputNode2, name=""):
        if inputNode1.size() != inputNode2.size():
            self.logger(
                "dimensionality error with "
                + str(inputNode1)
                + " and "
                + str(inputNode2)
                + " in pytorch"
            )
            return None
        return inputNode1 - inputNode2

    def multNode(self, inputNode1, inputNode2, name=""):
        return self.dimensionalityChangeforMultiply(
            self.dimensionalityChangeforMultiply(inputNode1) * inputNode2, True
        )

    def chooseActivation(self, activ):
        if activ == "Hyperbolic Tangent (Tanh)":
            return nn.Tanh()
        elif activ == "Softmax":
            return nn.Softmax()
        elif activ == "Rectified Linear (ReLu)":
            return torch.nn.ReLU()
        elif activ == "Exponential Linear (Elu)":
            return torch.nn.ELU()
        elif activ == "Log Softmax":
            return nn.LogSoftmax()
        elif activ == "Sigmoid":
            return nn.Sigmoid()
        elif activ == "Softplus":
            return nn.Softplus()
        elif activ == "Linear":
            return nn.Threshold(-9999999, 0)
        elif activ == "Hard Hyperbolic Tangent (HardTanh)":
            return nn.Hardtanh()
        else:
            return None

    def chooseLoss(self):
        if self.loss == "Mean Square Error (MSE)":
            self.loss_object = torch.nn.MSELoss
        elif self.loss == "Mean Absolute Error (MAE)":
            self.loss_object = torch.nn.L1Loss
        elif self.loss == "Categorical Cross Entropy":
            self.loss_object = torch.nn.CrossEntropyLoss
        elif self.loss == "Kullback-Leibler (KLDivergence)":
            self.loss_object = torch.nn.KLDivLoss
        elif self.loss == "Hinge":
            self.loss_object = torch.nn.HingeEmbeddingLoss
        elif self.loss == "Cosine Similarity":
            self.loss_object = torch.nn.CosineSimilarity
        elif self.loss == "Binary Cross Entropy (BCE)":
            self.loss_object = torch.nn.BCELoss
        elif self.loss == "Soft Margin Loss (SML)":
            self.loss_object = torch.nn.SoftMarginLoss
        elif self.loss == "Poisson Negative Log-Likelihood":
            self.loss_object = torch.nn.PoissonNLLLoss
        elif self.loss == "Negative Log-Likelihood":
            self.loss_object = torch.nn.NLLLoss
        else:
            self.loss_object = None

    def chooseOptimizer(self):
        if self.optimizer == "Adam":
            self.optimizer_object = torch.optim.Adam
        elif self.optimizer == "SDG":
            self.optimizer_object = torch.optim.SGD
        elif self.optimizer == "Adadelta":
            self.optimizer_object = torch.optim.Adadelta
        elif self.optimizer == "Adagrad":
            self.optimizer_object = torch.optim.Adagrad
        elif self.optimizer == "Adamax":
            self.optimizer_object = torch.optim.Adamax
        elif self.optimizer == "RMSprop":
            self.optimizer_object = torch.optim.RMSprop
        else:
            self.optimizer_object = None

    def saveModel(self):
        if self.model is None:
            self.logger("Error saving model with " + self.frame)
            return

        self.logger("Model saved with " + self.frame)

        torch.save(self.model, self.name)
        self.logger(self.model)
        summary(self.model, (1, self.ninput))

    def run(self):
        self.chooseLoss()
        self.chooseOptimizer()

        if self.loss_object is None:
            return (
                "Error choosing cost function in PyTorch: "
                + self.loss
                + " not available in Pytorch"
            )
        if self.optimizer_object is None:
            return (
                "Error choosing optimizer in Pytorch: "
                + self.optimizer
                + " not available in Pytorch"
            )

        optimizer = self.optimizer_object(self.model.parameters(), lr=0.01)
        self.model.train()

        modelLoss = None
        correct = 0

        for epoch in range(self.epoch):
            optimizer.zero_grad()  # Forward pass
            y_pred = self.model(self.inputTrain)  # Compute Loss
            loss = self.loss_object(y_pred.squeeze(), self.outputTrain)
            loss.backward()
            optimizer.step()
            for pred, train in (y_pred, self.outputTrain):
                if pred == train:
                    correct = correct + 1

        result = (
            "Train --> Loss: "
            + str(modelLoss.item())
            + ", Accuracy: "
            + str((correct / len(self.outputTrain)) * 100)
        )

        if self.test is True:
            self.model.eval()
            y_pred = self.model(self.inputTest)
            after_train = self.loss_object(y_pred.squeeze(), self.outputTest)

            correct = 0
            for pred, test in (y_pred, self.outputTest):
                if pred == test:
                    correct = correct + 1

            result = (
                result
                + "Test --> Loss: "
                + str(after_train.item())
                + ", Accuracy: "
                + str((correct / len(self.outputTest)) * 100)
            )

        self.saveModel()

        self.logger("Trained " + self.frame + " model saved correctly!")

        return result


class torchModel(nn.Module):
    """This class implements the creation and connection of block modules and arch modules. Unless the sequential model
        is used, the process of creation instantiation modules and connection of the latter needs to be done in the
        __init__function and the forward function accordingly. This cannot be done in the FrameStructure class to avoid
        confusion when calling the prepareModel function. Now, when prepareModel is called, a torchModel object is called
        and saved, which contains every information for the model structure.
        """

    def __init__(self, parent):
        """In this function every block and arch module is created and saved in self.nodes and self.activs ModuleDicts accordingly."""
        super(torchModel, self).__init__()
        self.parent = parent
        self.ready = False
        self.structure = parent.structure
        # node and archs modules are saved here
        self.activs = nn.ModuleDict()
        self.nodes = nn.ModuleDict()

        # Iters on every block in the structure
        for node in list(
            elem for elem in self.structure if self.structure[elem]["block"] is True
        ):

            # Check if layer type is valid
            if self.parent.nodeSupport(self.structure[node]["type"]) is False:
                self.parent.logger(
                    "Layer type "
                    + self.structure[node]["name"]
                    + " not supported in "
                    + self.parent.frame
                    + "."
                )
                return

            # If it is not a mult sum or sub block
            if (
                self.structure[node]["type"] != "SUM"
                and self.structure[node]["type"] != "SUB"
                and self.structure[node]["type"] != "MULT"
            ):

                # if it is not an input , which doesn't require proper block, create normal block
                if self.structure[node]["type"] != "INPUT":
                    # Looks for the previous block (through the previous arch) to find the input dimension
                    prevArchInd = next(
                        elem
                        for elem in self.structure
                        if self.structure[elem]["name"]
                        in self.structure[node]["PrevArch"]
                    )
                    prevBlockInd = next(
                        elem
                        for elem in self.structure
                        if self.structure[elem]["name"]
                        == self.structure[prevArchInd]["initBlock"]
                    )

                    # If the previous block is input then the input dimension is equel to self.ninput
                    if self.structure[prevBlockInd]["type"] == "INPUT":
                        inputDim = self.parent.ninput

                    else:
                        if (
                            self.structure[prevBlockInd]["type"] != "SUM"
                            and self.structure[prevBlockInd]["type"] != "SUB"
                            and self.structure[prevBlockInd]["type"] != "MULT"
                        ):
                            inputDim = self.structure[prevBlockInd]["neurons"]
                        # If the previous block is a special block than it calls the computeSpecBlockDim, which looks
                        # for the output dimension of that block, which differs accordingly if the special block is
                        # sub/sum or mult
                        else:
                            inputDim = self.parent.computeSpecBlockDim(
                                specBlockIndex=prevBlockInd
                            )

                    if self.structure[node]["type"] == "OUTPUT":
                        layerType = "DENSE"
                        outputDim = self.parent.noutput

                    else:
                        layerType = self.structure[node]["type"]
                        outputDim = self.structure[node]["neurons"]

                    layerT = self.parent.chooseNode(
                        layerType=layerType, inputDim=inputDim, outputDim=outputDim
                    )
                    self.nodes.add_module(self.structure[node]["name"], layerT)

        for arch in list(
            elem for elem in self.structure if self.structure[elem]["block"] is False
        ):
            # Check if Activation function is valid
            if self.parent.functionSupport(self.structure[arch]["activFunc"]) is False:
                self.parent.logger(
                    "Activation function "
                    + str(self.structure[arch]["activFunc"])
                    + " not supported in "
                    + self.parent.frame
                    + "."
                )
                return

            tempActiv = self.parent.chooseActivation(self.structure[arch]["activFunc"])
            self.activs.add_module(self.structure[arch]["name"], tempActiv)

        self.ready = True

    def forward(self, x):
        initBlockIndex = self.parent.returnFirstCompleteDiagram(self.structure)

        # nodes dictionary keeps track of every block as keras node
        nodes = {self.structure[initBlockIndex]["name"]: x}

        # merge dictionary keeps track of the two branches associated to one special block
        merge = {}

        getP = self.parent.getPair(initBlockIndex)
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
                # If it is the first time seeing a block that goes into a precise special block than it is saved in merge
                if specBlock not in merge:
                    merge[specBlock] = nodes[self.structure[block]["name"]]
                    continue
                # If a second block goes into a specific special block then the first one is gathered and the operation
                # is performed with the gethered one and the current one. After the computation, this precise special
                # block is removed from the dictionary in which it was saved with the previous block
                else:
                    specIndex = next(
                        ind
                        for ind in self.structure
                        if self.structure[ind]["name"] == specBlock
                    )
                    tempBlock = nodes[self.structure[block]["name"]]
                    outputBlock = self.parent.chooseNode(
                        layerType=self.structure[specIndex]["type"],
                        inputNode1=merge[specBlock],
                        inputNode2=tempBlock,
                    )
                    if outputBlock is None:
                        self.logger("Aborting creation of model with " + self.frame)
                        return None

                    merge.pop(specBlock)
                    nodes[specBlock] = outputBlock
                    continue

            # If it's not merging than it is a regular block and it needs regular activation function and block type.
            # The activation function is taken from the ModuleDict prepared in __init__ and it is passed with the block
            # saved from the previous iteration in the nodes dictionary
            activationFunc = self.activs[self.structure[arch]["name"]]
            tempBlock = nodes[self.structure[arch]["initBlock"]]
            outputNode = activationFunc(tempBlock)

            # If this is the last block then the result is the data from passed through the last activation
            # function (there are no input nor output blocks so the result is just the output data). Otherwise the data
            # passed through the activatio function is passed through the next block and temporarly saved in the nodes
            # dictionary using its name as key
            if self.structure[block]["type"] == "OUTPUT":
                layerT = self.nodes[self.structure[block]["name"]]
                outputBlock = layerT(outputNode)
                return outputBlock
            else:

                layerT = self.nodes[self.structure[block]["name"]]
                outputBlock = layerT(outputNode)
                nodes[self.structure[block]["name"]] = outputBlock
