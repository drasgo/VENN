import sklearn


# TODO
class FrameStructure:

    def __init__(self, numberInput, numberOutput, structure, structureName):
        self.ninput = numberInput
        self.noutput = numberOutput
        self.structure = structure.copy()
        self.name = structureName
        self.model = None
        self.cost = None
        self.input = None
        self.output = None

    def prepareModel(self):
        pass

    def setCost(self, cost):
        pass

    def setInputOutput(self, inputData, outputData):
        pass

    def saveModel(self):
        pass

    def run(self):
        pass
