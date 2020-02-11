# VENN How-To and Usage

This program is a Visual Editor of Neural Network.

## What is a Neural Network?

A neural network is a statistical model which, given a specific input, returns an output which can correspond to:
* the percentage of how likely the input is part of a specific class - this network is called classifier -;
* the possible result of a generalized function which the network tries to approximate - this network is called function approximator -;
* divide the input in possible groups - or segments - of data - this network is called cluster and performs an action called segmentation.

These are the main types of neural networks, which are then specialized into serving a specific purpose.

A network is divided in layers and arches. The mathematical meaning of every pair of layer-arch considering the most common type of layer, the fully-connected -or dense - layer, is:
 * Given that an arch correspond to a mathematical function -activation_function-
 * Given that a layer is formed by a weight matrix -w_matrix- and a bias matrix -b_matrix-


 out_matrix = activation_function(in_matrix*w_matrix + b_matrix)

 Where:

 * in_matrix is the input matrix which goes into the given arch;
 * out_matrix is the output matrix of the layer.


 This n-th layer of the model's output is the n+1-th layer of the model's input, and viceversa this layer's input is the n-1-th layer of the model's output.  

 A computation can be done in training mode or in testing mode: the first part a feed forward is the same, but the training mode also performs afterwards a process of back propagation.

 ### Feed Forward

Feed forward is the process of giving a neural network an input matrix which contains the data that the neural network should be able to generalize for finding an appropriate result.
Through this step-by-step process the input are going to be computed - passed though activation functions, multiplied with the layers' weight matrices and added with the layers' bias matrices.

Let's consider for example a three layers model. This model is formed as follows:

*   The input, in_matrix, is a [1]x[m] row-matrix
*   The output, out_matrix, is row-vector of 4 values where, ideally, one of the values is 1 and the other ones are 0s. (For this reason this network is an example of a classifier, where there are 4 possible classes and the sum of the values in the output vector, the percentages of membership to each class, needs to be 1)
* the hidden layer - every layer between the input and the output layers. In this case it is just one - has a weight matrix, w_matrix, [1]x[k], which means that this layer has k neurons, and a bias matrix, b_matrix, [n]x[k]

 ### Back Propagation



 ## VENN

 Given this quick and oversimplified explanation of what a neural network is, let's dive into this tool.
