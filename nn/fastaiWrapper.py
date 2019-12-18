import fastai
import nn.pytorchWrapper


# FastAI actually uses Pytorch models and runs those models in its own way.
# So the models are created using Pytorch and then it will handle the run
class FrameStructure(nn.pytorchWrapper.FrameStructure):

    def __init__(self, numberInput, numberOutput, structure, structureName):
        super(FrameStructure, self).__init__(numberInput, numberOutput, structure, structureName)
        self.ninput = numberInput
        self.noutput = numberOutput
        self.structure = structure.copy()
        self.name = structureName
        self.model = None
        self.cost = None
        self.input = None
        self.output = None

    # Need to override for fastAI usage
    def run(self):
        pass
