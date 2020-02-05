import torch
import torch.nn as nn
from torchsummary import summary
from ViCreNN.nn.wrapperTemplate import WrapperTemplate


class FrameStructure(WrapperTemplate):

    def __init__(self, numberInput, numberOutput, structure, structureName, logger):
        # nn.Module.__init__(self)
        WrapperTemplate.__init__(self, numberInput, numberOutput, structure, structureName, logger)
        self.frame = "Pytorch"

    def prepareModel(self):
        self.model = torchModel(self)

    # def forward(self, x=None):
    #     if x is None:
    #         x = torch.zeros([1, self.ninput])
    #
    #     initBlockIndex = self.returnFirstCompleteDiagram(self.structure)
    #     inputDim = self.ninput
    #
    #     # nodes dictionary keeps track of every block as keras node
    #     nodes = {self.structure[initBlockIndex]["name"]: torch.nn.Linear(self.ninput, inputDim)(x)}
    #     # merge dictionary keeps track of the two branches associated to one special block
    #     merge = {}
    #     outputNode = None
    #     getP = self.getPair(initBlockIndex)
    #
    #     # TODO: nota: non ci sono nodi per l'ingresso e l'uscita della rete neurale, quindi bisogna settare il primo
    #     # TODO: (i primi nel caso in cui l'input sia subito smezzato) blocco con la granddezzo dell'input size e primo/i blocchi
    #     # TODO:  e lo stesso vale per l'ultimo blocco prima della'output
    #     # starts getting the next arch-block pair
    #     for arch, block, specBlock in getP:
    #
    #         # Merging two branches
    #         if specBlock is not None:
    #             if specBlock not in merge:
    #                 merge[specBlock] = nodes[self.structure[block]["name"]]
    #                 continue
    #
    #             else:
    #                 specIndex = next(ind for ind in self.structure if self.structure[ind]["name"] == specBlock)
    #                 layerT = self.chooseNode(self.structure[specIndex]["type"])
    #                 tempBlock = nodes[self.structure[block]["name"]]
    #                 outputBlock = layerT(inputNode=tempBlock, outputNode=merge[specBlock])
    #                 merge.pop(specBlock)
    #                 nodes[specBlock] = outputBlock
    #                 continue
    #
    #         # Check if layer type is valid
    #         if self.nodeSupport(self.structure[block]["type"]) is False:
    #             self.logger("Layer type " + self.structure[block][
    #                     "name"] + " not supported in " + self.frame + ". Skipping layer")
    #             continue
    #
    #         # Check if Activation function is valid
    #         if self.functionSupport(self.structure[arch]["activFunc"]) is False:
    #             self.logger("Activation function" + str(
    #                 self.structure[arch]["activFunc"]) + " not supported in " + self.frame + ". Skipping layer")
    #             continue
    #
    #         if self.structure[block]["type"] == "OUTPUT":
    #             outputDim = self.noutput
    #         else:
    #             outputDim = self.structure[block]["neurons"]
    #
    #         # If it's not merging than it is a regular block and it needs regular activation function and block type
    #         layerT = self.chooseNode(self.structure[block]["type"], inputDim=inputDim, outputDim=outputDim)
    #         activationFunc = self.chooseActivation(self.structure[arch]["activFunc"])()
    #
    #         tempBlock = nodes[self.structure[arch]["initBlock"]]
    #         # print(str(tempBlock))
    #         # print(str(activationFunc))
    #         outputNode = activationFunc(tempBlock)
    #
    #         # Mid blocks. If this is the last block then the result is the data from passed through the last activation
    #         # function (there are no input nor output blocks so the result is just the output data, not saved anywhere)
    #         if self.structure[block]["type"] == "OUTPUT":
    #             return outputNode
    #         else:
    #             outputBlock = layerT(outputNode)
    #             nodes[self.structure[block]["name"]] = outputBlock
    #             # print(str(outputBlock))
    #             inputDim = self.structure[block]["neurons"]
    #         # if x is None:

    def saveModel(self):
        if self.model is None:
            self.prepareModel()

        print("Model's state_dict:")
        for param_tensor in self.model.state_dict():
            print(param_tensor, "\t", self.model.state_dict()[param_tensor].size())

        torch.save(self.model, self.name)
        print(self.model)
        repr(self.model)
        summary(self.model, (1, self.ninput))

    def nodeSupport(self, node):
        if node == "DENSE" or node == "SUM" or node == "SUB" or node == "MULT" or \
                node == "DROPOUT" or node == "POOLING" or node == "CNN" or node == "INPUT" or node == "OUTPUT":
            return True
        else:
            return False

    def functionSupport(self, activ):
        if activ == "Hyperbolic Tangent (Tanh)" or activ == "Softmax" or activ == "Rectified Linear (ReLu)" or \
                activ == "Exponential Linear (Elu)" or activ == "Log Softmax" or activ == "Sigmoid" or activ == "Softplus" \
                or activ == "Linear" or activ == "Hard Hyperbolic Tangent(HardTanh)":
            return True
        else:
            return False

    def chooseNode(self, layerType, **kwargs):
        if layerType == "DENSE" or layerType == "OUTPUT":
            return torch.nn.Linear(int(kwargs["inputDim"]), int(kwargs["outputDim"]))
        elif layerType == "SUM":
            # return self.sumNode(inputNode=kwargs["inputNode"], outputNode=kwargs["outputNode"])
            return self.sumNode
        elif layerType == "SUB":
            # return self.subNode(inputNode=kwargs["inputNode"], outputNode=kwargs["outputNode"])
            return self.subNode
        elif layerType == "MULT":
            return self.multNode
            # return self.multNode(inputNode=kwargs["inputNode"], outputNode=kwargs["outputNode"])
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

    def sumNode(self, inputNode, outputNode):
        return inputNode + outputNode

    def subNode(self, inputNode, outputNode):
        return inputNode - outputNode

    # TODO mult
    def multNode(self, inputNode, outputNode):
        return inputNode * outputNode

    def chooseActivation(self, activ):
        if activ == "Hyperbolic Tangent (Tanh)":
            return nn.Tanh
        elif activ == "Softmax":
            return nn.Softmax
        elif activ == "Rectified Linear (ReLu)":
            return nn.ReLU
        elif activ == "Exponential Linear (Elu)":
            return nn.ELU
        elif activ == "Log Softmax":
            return nn.LogSoftmax
        elif activ == "Sigmoid":
            return nn.Sigmoid
        elif activ == "Softplus":
            return nn.Softplus
        elif activ == "Linear":
            return nn.Linear
        elif activ == "Hard Hyperbolic Tangent(HardTanh)":
            return nn.Hardtanh
        else:
            return None

    def chooseCost(self):
        if self.cost == "Mean Square Error (MSE)":
            self.loss_object = torch.nn.MSELoss
        elif self.cost == "Mean Absolute Error (MAE)":
            self.loss_object = torch.nn.L1Loss
        elif self.cost == "Categorical Cross Entropy":
            self.loss_object = torch.nn.CrossEntropyLoss
        elif self.cost == "Kullback-Leibler (KLDivergence)":
            self.loss_object = torch.nn.KLDivLoss
        elif self.cost == "Hinge":
            self.loss_object = torch.nn.HingeEmbeddingLoss
        elif self.cost == "Cosine Similarity":
            self.loss_object = torch.nn.CosineSimilarity
        elif self.cost == "Binary Cross Entropy (BCE)":
            self.loss_object = torch.nn.BCELoss
        elif self.cost == "Soft Margin Loss (SML)":
            self.loss_object = torch.nn.SoftMarginLoss
        elif self.cost == "Poisson Negative Log-Likelihood":
            self.loss_object = torch.nn.PoissonNLLLoss
        elif self.cost == "Negative Log-Likelihood":
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

    def run(self):
        self.chooseCost()
        self.chooseOptimizer()

        if self.loss_object is None:
            return "Error choosing cost function in PyTorch: " + self.cost + " not available in Pytorch"
        if self.optimizer_object is None:
            return "Error choosing optimizer in Pytorch: " + self.optimizer + " not available in Pytorch"

        optimizer = self.optimizer_object(self.model.parameters(), lr=0.01)
        self.model.train()

        loss = None
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

        return "Train --> Loss: " + str(loss.item()) + ", Accuracy: " + str((correct / len(self.outputTrain)) * 100)

    def test(self):
        self.model.eval()
        y_pred = self.model(self.inputTest)
        after_train = self.loss_object(y_pred.squeeze(), self.outputTest)

        correct = 0
        for pred, test in (y_pred, self.outputTest):
            if pred == test:
                correct = correct + 1

        return "Test --> Loss: " + str(after_train.item()) + ", Accuracy: " + str(
            (correct / len(self.outputTest)) * 100)


class torchModel(nn.Module):

    def __init__(self, parent):
        super(torchModel, self).__init__()
        self.parent = parent
        self.activs = nn.ModuleDict()
        self.nodes = nn.ModuleDict()
        for node in list(elem for elem in self.parent.structure if self.parent.structure[elem]["block"] is True):
            print("nodo corrente: " + self.parent.structure[node]["name"])
            # Check if layer type is valid
            if self.parent.nodeSupport(self.parent.structure[node]["type"]) is False:
                self.parent.logger("Layer type " + self.parent.structure[node][
                    "name"] + " not supported in " + self.parent.frame + ". Skipping layer")
                continue

            # If it is not a mult sum or sub block create normal block
            if self.parent.structure[node]["type"] != "SUM" and self.parent.structure[node]["type"] != "SUB" and \
                    self.parent.structure[node]["type"] != "MULT":
                print("se nodo " + str(self.parent.structure[node]["name"]) + " non è mult/add/sub")
                # if it is not an input or output, which don't require proper blocks, create normal block
                if self.parent.structure[node]["type"] != "INPUT":
                    print("se nodo " + str(self.parent.structure[node]["name"] + " non è input"))
                    prevArchInd = next(elem for elem in self.parent.structure if
                                       self.parent.structure[elem]["name"] in self.parent.structure[node]["PrevArch"])

                    prevBlockInd = next(elem for elem in self.parent.structure if
                                        self.parent.structure[elem]["name"] == self.parent.structure[prevArchInd][
                                            "initBlock"])
                    if self.parent.structure[prevBlockInd]["type"] == "INPUT":
                        inputDim = self.parent.ninput
                    else:
                        if self.parent.structure[prevBlockInd]["type"] != "SUM" and \
                                self.parent.structure[prevBlockInd]["type"] != "SUB" and \
                                self.parent.structure[prevBlockInd]["type"] != "MULT":
                            inputDim = self.parent.structure[prevBlockInd]["neurons"]
                        else:
                            inputDim = self.parent.computeSpecBlockDim(specBlockIndex=node)
                    if self.parent.structure[node]["type"] == "OUTPUT":
                        layerType = "DENSE"
                        outputDim = self.parent.noutput
                    else:
                        layerType = self.parent.structure[node]["type"]
                        outputDim = self.parent.structure[node]["neurons"]

                    layerT = self.chooseNode(layerType=layerType, inputDim=inputDim, outputDim=outputDim)
                    self.nodes.add_module(self.parent.structure[node]["name"], layerT)
                    print("layer appena creato: " + str(layerT))
            else:
                print("in nodo " + self.parent.structure[node]["name"] + "")
                # layerT = self.chooseNode(layerType=self.parent.structure[node]["type"])
                # self.nodes.add_module(self.parent.structure[node]["name"], layerT)
        print("creazione  funzioni attivazione")
        for arch in list(elem for elem in self.parent.structure if self.parent.structure[elem]["block"] is False):
            # Check if Activation function is valid
            if self.parent.functionSupport(self.parent.structure[arch]["activFunc"]) is False:
                self.parent.logger("Activation function" + str(self.parent.structure[arch][
                                                                   "activFunc"]) + " not supported in " + self.parent.frame + ". Skipping layer")
                continue
            tempActiv = self.chooseActivation(self.parent.structure[arch]["activFunc"])()
            print("funzione attivazione creato: " + str(
                self.parent.chooseActivation(self.parent.structure[arch]["activFunc"])))
            self.activs.add_module(self.parent.structure[arch]["name"], tempActiv)
        print("fine inizializzazione classe")

        print("risultato finale: blocchi: " + str(self.nodes) + ", archi: " + str(self.activs))

    def forward(self, x):

        initBlockIndex = self.parent.returnFirstCompleteDiagram(self.parent.structure)
        # inputDim = self.parent.ninput
        # outputDim = self.parent.ninput

        # nodes dictionary keeps track of every block as keras node
        nodes = {self.parent.structure[initBlockIndex]["name"]: x}
        # merge dictionary keeps track of the two branches associated to one special block
        merge = {}
        outputNode = None
        getP = self.parent.getPair(initBlockIndex)

        # starts getting the next arch-block pair
        for arch, block, specBlock in getP:

            # Merging two branches
            if specBlock is not None:
                if specBlock not in merge:
                    merge[specBlock] = nodes[self.parent.structure[block]["name"]]
                    continue

                else:
                    specIndex = next(
                        ind for ind in self.parent.structure if self.parent.structure[ind]["name"] == specBlock)
                    # layerT = self.nodes[self.parent.structure[specIndex]["name"]]
                    tempBlock = nodes[self.parent.structure[block]["name"]]
                    outputBlock = self.chooseNode(layerType=self.parent.structure[specIndex]["type"],
                                                  inputNode1=tempBlock, inputNode2=merge[specBlock])
                    merge.pop(specBlock)
                    nodes[specBlock] = outputBlock
                    continue

            # If it's not merging than it is a regular block and it needs regular activation function and block type

            activationFunc = self.activs[self.parent.structure[arch]["name"]]
            print("presa funzione attivazione " + str(self.parent.structure[arch]["name"]) + " ossia: " + str(
                activationFunc))

            tempBlock = nodes[self.parent.structure[arch]["initBlock"]]

            outputNode = activationFunc(tempBlock)
            # print("funzione attivazione dopo passaggio dati " + str(outputNode))
            # print("dati passati: " + str(tempBlock))

            # Mid blocks. If this is the last block then the result is the data from passed through the last activation
            # function (there are no input nor output blocks so the result is just the output data, not saved anywhere)
            if self.parent.structure[block]["type"] == "OUTPUT":
                return outputNode
            else:

                layerT = self.nodes[self.parent.structure[block]["name"]]
                print("preso blocco " + str(self.parent.structure[block]["name"]) + " ossia: " + str(layerT))
                outputBlock = layerT(outputNode)
                # print("nodo dopo passaggio dati " + str(outputBlock))
                nodes[self.parent.structure[block]["name"]] = outputBlock

    def chooseNode(self, layerType, **kwargs):
        if layerType == "DENSE" or layerType == "OUTPUT":
            return torch.nn.Linear(int(kwargs["inputDim"]), int(kwargs["outputDim"]))
        elif layerType == "SUM":
            # return self.sumNode(inputNode=kwargs["inputNode"], outputNode=kwargs["outputNode"])
            return self.sumNode(inputNode1=kwargs["inputNode1"], inputNode2=kwargs["inputNode2"])
        elif layerType == "SUB":
            # return self.subNode(inputNode=kwargs["inputNode"], outputNode=kwargs["outputNode"])
            return self.subNode(inputNode1=kwargs["inputNode1"], inputNode2=kwargs["inputNode2"])
        elif layerType == "MULT":
            return self.multNode(inputNode1=kwargs["inputNode1"], inputNode2=kwargs["inputNode2"])
            # return self.multNode(inputNode=kwargs["inputNode"], outputNode=kwargs["outputNode"])
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

    def sumNode(self, inputNode1, inputNode2):
        return inputNode1 + inputNode2

    def subNode(self, inputNode1, inputNode2):
        return inputNode1 - inputNode2

    # TODO mult
    def multNode(self, inputNode1, inputNode2):
        return inputNode1 * inputNode2

    def chooseActivation(self, activ):
        if activ == "Hyperbolic Tangent (Tanh)":
            return nn.Tanh
        elif activ == "Softmax":
            return nn.Softmax
        elif activ == "Rectified Linear (ReLu)":
            return torch.nn.ReLU
        elif activ == "Exponential Linear (Elu)":
            return torch.nn.ELU
        elif activ == "Log Softmax":
            return nn.LogSoftmax
        elif activ == "Sigmoid":
            return nn.Sigmoid
        elif activ == "Softplus":
            return nn.Softplus
        elif activ == "Linear":
            return nn.Linear
        elif activ == "Hard Hyperbolic Tangent(HardTanh)":
            return nn.Hardtanh
        else:
            return None
