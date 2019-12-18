LINE_WIDTH = 25

ACTIVATION_FUNCTIONS = {"None": "white",
                        "Linear": "cyan",
                        "Rectified Linear (ReLu)": "blue",
                        "Hyperbolic Tangent (Tanh)": "green",
                        "Hard Hyperbolic Tangent(HardTanh)": "darkGreen",
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

# Neural Network framework structure costant functions


def checkNumBranches(structure):
    # Check the numebr of aggregation blocks (aka sum, mult, div, sub blocks). Every aggregation block is a branch unified
    return len([block for block in structure if structure[block]["block"] is True and
                (structure[block]["type"] == "SUM" or structure[block]["type"] == "SUB" or
                 structure[block]["type"] == "MULT" or structure[block]["type"] == "DIV")])


def returnFirstCompleteSequential(structure):
    index = None
    # print("in check sequential")
    while True:

        if index is not None:
            break

        tempInit = next(bl for bl in structure if
                        structure[bl]["block"] is True and structure[bl]["FirstBlock"] is True)
        # print("nome: " + self.structure[tempInit]["name"])
        if tempInit is None:
            print("Error checking sequential structure for Keras. Exiting")
            quit()

        tempIndex = tempInit
        last = structure[tempIndex]["LastBlock"]

        # Checks the integrity of the branch (aka it checks that it starts from an input and through all the middle arches and blocks
        # ends with a final block. If not it removes the first block of that branch. The first valid branch (input-> ...-> output)
        # will be considered as the valid network
        while last is False:

            if structure[tempIndex]["block"] is True:
                # print("è blocco")
                tempIndex = next(block for block in structure if any(
                    structure[block]["name"] == x for x in structure[tempIndex]["SuccArch"]))

            else:
                # print("è arco")
                tempIndex = next(block for block in structure if
                                 structure[block]["name"] == structure[tempIndex]["finalBlock"])

            if structure[tempIndex]["block"] is True and structure[tempIndex]["LastBlock"] is True:
                # print("finito con final block")
                last = True
                index = tempInit

            elif structure[tempIndex]["block"] is True and structure[tempIndex]["LastBlock"] is False and \
                    len(structure[tempIndex]["SuccArch"]) == 0:
                # print("finito senza final block")
                break

        if last is False:
            # print("rimuovo questo primo elemento perchè questo branch non ha final block:: " + self.structure[tempInit]["name"])
            structure.pop(tempInit)

    return index


def getArchBlock(structure, index):
    while structure[index]["LastBlock"] is False:
        nextArchName = next(arch for arch in structure[index]["SuccArch"])
        nextArchIndex = next(key for key in structure if structure[key]["name"] == nextArchName)
        nextBlockName = structure[nextArchIndex]["finalBlock"]
        nextBlockIndex = next(key for key in structure if structure[key]["name"] == nextBlockName)
        # print("nuova coppia arco-blocco: " + nextArchName + " " + nextBlockName)
        index = nextBlockIndex
        yield nextArchIndex, nextBlockIndex
