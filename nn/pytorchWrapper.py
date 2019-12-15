import torch
import torch.nn as nn
import gui.costants as costants
from torchsummary import summary


# TODO
class FrameStructure(nn.Module):

    def __init__(self, numberInput, numberOutput, structure, structureName):
        super(FrameStructure, self).__init__()
        self.ninput = numberInput
        self.noutput = numberOutput
        self.structure = structure.copy()
        self.name = structureName
        self.model = None
        self.cost = None
        self.input = None
        self.output = None
        self.isSequential = True
        self.archs = list()
        self.blocks = list()

    def prepareModel(self):
        # TODO
        #  Implement multiple branches
        if costants.checkNumBranches(self.structure) == 0:
            self.isSequential = True
        else:
            print("Error in Pytorch: only sequential networks currently supported. Exiting")
            return False

        initBlockIndex = costants.returnFirstCompleteSequential(self.structure)
        inNeurons = self.ninput
        outNeurons = inNeurons

        self.model = nn.Sequential()
        self.model.add_module("blockInput", torch.nn.Linear(inNeurons, outNeurons))

        for arch, block in costants.getArchBlock(self.structure, initBlockIndex):

            if self.structure[block]["LastBlock"] is False:
                outNeurons = int(self.structure[block]["neurons"])
            else:
                outNeurons = self.noutput

            self.model.add_module("arch" + self.structure[arch]["name"], self.chooseActivation(self.structure[arch]["activFunc"]))
            self.model.add_module("block" + self.structure[block]["name"], torch.nn.Linear(inNeurons, outNeurons))

            inNeurons = outNeurons

    def forward(self, x):
        return self.model.forward(x)

    def setCost(self, cost):
        self.cost = cost

    # TODO
    def chooseCost(self):
        pass

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
            print("Error selecting activation function " + activ + " in Pytorch. Quitting")
            quit()

    def setInputOutput(self, inputData, outputData):
        pass

    def saveModel(self):
        torch.save(self.model, "test.txt")
        summary(self.model, (self.ninput,))

    # TODO
    def run(self):
        pass
