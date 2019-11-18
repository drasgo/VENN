LINE_WIDTH = 25

ACTIVATION_FUNCTIONS = {"None": "white",
                        "Tanh": "blue",
                        "Linear": "red",
                        "Other": "orange"}

BOX_PROPERTIES = ["LAYER", "SUM", "SUB", "MULT", "DIV", "BLANK", "COST"]

COST_FUNCTION = ["MSE", "OTHER"]

NNSTRUCTURE_FILE = "NNStructure.dr"

ARROW_DEFAULT_FUNC = "None"

blockSelected = "background-color: dimgray;"
blockUnSelected = "background-color: rgb(114, 159, 207);"


def arrow_stylesheet(color=ACTIVATION_FUNCTIONS[ARROW_DEFAULT_FUNC]):
    return "border-color: black; background-color: " + color + ";"
