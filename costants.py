LINE_WIDTH = 25

ACTIVATION_FUNCTIONS = {"None": "white",
                        "Tanh": "blue",
                        "Linear": "red",
                        "Other": "orange"}

BOX_PROPERTIES = ["LAYER", "SUM", "SUB", "MULT", "DIV", "BLANK"]

NNSTRUCTURE_FILE = "NNStructure.nn"

ARROW_DEFAULT_FUNC = "None"


def arrow_stylesheet(color=ACTIVATION_FUNCTIONS[ARROW_DEFAULT_FUNC]):
    return "border-color: black; background-color: " + color + ";"
