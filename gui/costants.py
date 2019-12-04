LINE_WIDTH = 25

ACTIVATION_FUNCTIONS = {"None": "cyan",
                        "Rectified Linear (ReLu)": "blue",
                        "Hyperbolic Tangent (Tanh)": "green",
                        "Exponential Linear (Elu)": "darkGreen",
                        "Log Softmax": "darkYellow",
                        "Sigmoid": "orange",
                        "Softmax": "red",
                        "Softplus": "darkRed",
                        "Other": "purple"}

FRAMEWORKS = ["TensorFlow", "PyTorch"]

BOX_PROPERTIES = ["LAYER", "INPUT", "OUTPUT", "SUM", "SUB", "MULT", "DIV", "BLANK", "COST"]

COST_FUNCTION = ["", "Mean Square Error (MSE)", "Cross Entropy", "OTHER"]

NNSTRUCTURE_FILE = "NNStructure.dr"

ARROW_DEFAULT_FUNC = "None"

blockSelected = "background-color: dimgray;"
blockUnSelected = "background-color: rgb(114, 159, 207);"

INPUT_OUTPUT_DATA_FILE_EXTENSION = "Text Files (*.txt, *.json, *.dat)"

STRUCTURE_EXTENSION = ".dr"

TENSORFLOW_EXTENSION = ".h5"

PYTORCH_EXTENSION = ".pyt"

KERAS_EXTENSION = ".ke"
SCIKIT_EXTENSION = ".sci"


def arrow_stylesheet(color=ACTIVATION_FUNCTIONS[ARROW_DEFAULT_FUNC]):
    return "border-color: black; background-color: " + color + ";"
