LINE_WIDTH = 25

ACTIVATION_FUNCTIONS = {"None": "white",
                        "Linear": "cyan",
                        "Rectified Linear (ReLu)": "blue",
                        "Hyperbolic Tangent (Tanh)": "green",
                        "Hard Hyperbolic Tangent (HardTanh)": "darkGreen",
                        "Exponential Linear (Elu)": "yellow",
                        "Log Softmax": "darkYellow",
                        "Sigmoid": "orange",
                        "Hard Sigmoid": "darkOrange",
                        "Softmax": "red",
                        "Softplus": "darkRed",
                        "Other": "purple"}

FRAMEWORKS = ["TensorFlow", "PyTorch", "Keras", "FastAI"]

BOX_PROPERTIES = ["LAYER", "INPUT", "OUTPUT", "SUM", "SUB", "MULT", "DIV", "BLANK"]

COST_FUNCTION = ["", "Mean Square Error (MSE)", "Cross Entropy", "OTHER"]

OPTIMIZERS = ["Adam"]

INPUT_TYPE = ["normal", "cnn", "rnn"]

ARROW_DEFAULT_FUNC = "None"

blockSelected = "background-color: dimgray;"
blockUnSelected = "background-color: rgb(114, 159, 207);"

INPUT_OUTPUT_DATA_FILE_EXTENSION = "Text Files (*.txt, *.json, *.dat)"

NNSTRUCTURE_FILE = "NNStructure.dr"

STRUCTURE_EXTENSION = ".dr"

TENSORFLOW_EXTENSION = ".h5"

PYTORCH_EXTENSION = ".pyt"

KERAS_EXTENSION = ".ke"

FASTAI_EXTENSION = ".fai"

IMAGE_EXTENSION = ".png"


def arrow_stylesheet(color=ACTIVATION_FUNCTIONS[ARROW_DEFAULT_FUNC]):
    return "border-color: black; background-color: " + color + ";"
