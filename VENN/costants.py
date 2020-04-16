LINE_WIDTH = 25

ACTIVATION_FUNCTIONS = {"": "white",
                        "Linear": "cyan",
                        "Rectified Linear (ReLu)": "blue",
                        "Hyperbolic Tangent (Tanh)": "green",
                        "Hard Hyperbolic Tangent (HardTanh)": "darkGreen",
                        "Exponential Linear (Elu)": "yellow",
                        "Sigmoid": "orange",
                        "Hard Sigmoid": "darkOrange",
                        "Softmax": "red",
                        "Softplus": "darkRed",
                        "Log Softmax": "purple"}

FRAMEWORKS = {"TensorFlow": "tensorflow",
              "PyTorch": "torch",
              "Keras": "keras"}
# , "FastAI": "fastai"}

BOX_PROPERTIES = ["DENSE",
                  "CONV2D",
                  "CONV3D",
                  "POOLING",
                  "DROPOUT",
                  "INPUT",
                  "OUTPUT",
                  "SUM",
                  "SUB",
                  "MULT",
                  "CONC",
                  "BLANK"]

COST_FUNCTION = ["",
                 "Mean Absolute Error (MAE)",
                 "Mean Absolute Percentage Error (MAPE)",
                 "Mean Squared Error (MSE)",
                 "Mean Squared Logarithmic Error (MSLE)",
                 "Binary Cross Entropy (BCE)",
                 "Soft Margin Loss (SML)",
                 "Log-Likelihood",
                 "Negative Log-Likelihood",
                 "Hinge",
                 "Huber",
                 "Logaritmic Cosine (LogCosh)",
                 "Poisson",
                 "Poisson Negative Log-Likelihood",
                 "Categorical Cross Entropy",
                 "Sparse Categorical Cross Entropy",
                 "Kullback-Leibler (KLDivergence)",
                 "Cosine Similarity"]

OPTIMIZERS = ["",
              "Adam",
              "Adadelta",
              "Adagrad",
              "Adamax",
              "Nadam",
              "RMSprop",
              "Ftrl",
              "SDG"]

BLOCK_LABELS = {"DENSE": "Neurons: ",
                "CNN": "Kernel: ",
                "POOLING": "Pooling: ",
                "DROPOUT": "Dropout: "}

INPUT_TYPE = ["normal", "cnn", "rnn"]

ARROW_DEFAULT_FUNC = ""

blockSelected = "background-color: dimgray;"
blockUnSelected = "background-color: rgb(114, 159, 207);"

INPUT_OUTPUT_DATA_FILE_EXTENSION = "Text Files (*.txt *.json *.dat)"

NNSTRUCTURE_FILE = "NNStructure.dr"

STRUCTURE_DATA_FILE_EXTENSION = "VENN Files (*.dr)"

STRUCTURE_EXTENSION = ".dr"

TENSORFLOW_EXTENSION = ".h5"

PYTORCH_EXTENSION = ".pyt"

KERAS_EXTENSION = ".ke"

# FASTAI_EXTENSION = ".fai"

IMAGE_EXTENSION = ".png"


NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]


def arrow_stylesheet(color=ACTIVATION_FUNCTIONS[ARROW_DEFAULT_FUNC]):
    return "border-color: black; background-color: " + color + ";"
