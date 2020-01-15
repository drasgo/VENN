# TODO Implement FASTAI. Problem: obscure data management (if not from file?) and error initializing Learner
# from fastai import basic_train
# from ViCreNN.nn.pytorchWrapper import FrameStructure as PyTFrame
#
#
# # FastAI actually uses Pytorch models and runs those models in its own way.
# # So the models are created using Pytorch and then it will handle the run
# class FrameStructure(PyTFrame):
#
#     def __init__(self, numberInput, numberOutput, structure, structureName, logger):
#         super(FrameStructure, self).__init__(numberInput, numberOutput, structure, structureName, logger)
#
#     def prepareModel(self):
#         super(FrameStructure, self).prepareModel()
#
#     # TODO
#     def chooseCost(self):
#         pass
#
#     def chooseOptimizer(self):
#         pass
#
#     # TODO
#     def run(self):
#         self.chooseCost()
#         self.chooseOptimizer()
#
#         if self.loss_object is None:
#             return "Error choosing cost function in FastAI: " + self.cost + " not available in FastAI"
#         if self.optimizer_object is None:
#             return "Error choosing optimizer in FastAI: " + self.optimizer + " not available in FastAI"
#
#         data = basic_train.ItemList(items=self.inputTrain, label_cls=self.outputTrain)
#         datab = basic_train.DataBunch(data)
#         learner = basic_train.Learner(datab, model=self.model, loss_func=self.optimizer_object, metrics=accuracy)
#
#     def test(self):
#         pass
