# import fastai
from ViCreNN.nn.pytorchWrapper import FrameStructure as PyTFrame


# FastAI actually uses Pytorch models and runs those models in its own way.
# So the models are created using Pytorch and then it will handle the run
class FrameStructure(PyTFrame):

    def __init__(self, numberInput, numberOutput, structure, structureName, logger):
        super(FrameStructure, self).__init__(numberInput, numberOutput, structure, structureName, logger)

    def prepareModel(self):
        super(FrameStructure, self).prepareModel()

    # TODO
    def chooseCost(self):
        pass

    # TODO
    def run(self):
        pass
