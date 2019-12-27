import torch
import torch.nn as nn
from torchsummary import summary
from ViCreNN.nn.wrapperTemplate import WrapperTemplate


# TODO
class FrameStructure(WrapperTemplate, nn.Module):

    def __init__(self, numberInput, numberOutput, structure, structureName):
        nn.Module.__init__(self)
        WrapperTemplate.__init__(self, numberInput, numberOutput, structure, structureName)

    def prepareModel(self):
        # TODO
        #  Implement multiple branches
        if self.checkNumBranches(self.structure) == 0:
            self.isSequential = True
        else:
            print("Error in Pytorch: only sequential networks currently supported. Exiting")
            return False

        initBlockIndex = self.returnFirstCompleteSequential(self.structure)
        inNeurons = self.ninput
        outNeurons = inNeurons

        self.model = nn.Sequential()
        self.model.add_module("blockInput", torch.nn.Linear(inNeurons, outNeurons))

        for arch, block in self.getArchBlock(self.structure, initBlockIndex):

            if self.structure[block]["LastBlock"] is False:
                outNeurons = int(self.structure[block]["neurons"])
            else:
                outNeurons = self.noutput

            self.model.add_module("arch" + self.structure[arch]["name"], self.chooseActivation(self.structure[arch]["activFunc"]))
            self.model.add_module("block" + self.structure[block]["name"], torch.nn.Linear(inNeurons, outNeurons))

            inNeurons = outNeurons

    def forward(self, x):
        return self.model.forward(x)

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

    def saveModel(self):
        torch.save(self.model, "test.txt")
        summary(self.model, (self.ninput,))

    # TODO
    def run(self):
        pass
