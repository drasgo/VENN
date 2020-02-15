### <a name="howto"></a> How to use
<br />
<img src="Images/VENN.jpg" />

<br /><br />
Let's take a look at the gui of the tool, as shown in the above picture: we can tell right away that there are essentially four distinct areas.

In the upper left corner we can see the an area where we can specify various options relative to the run/test mode: the input and output data we want to train the model with, the epochs number for the training session and the loss and optimizer functions we want to use. The only thing which needs to be modified right away is the number of values for each input and each output -aka their dimensionalities. We are coming back to this later on.


In the lower left corner we can see the logger, which will show us every possible problem or useful piece of information regarding the completion of a task - such as the creation of a model, or the export of the model into a framework, or so on.


In the lower right corner we can find the various options: saving and loading a structure with a personalized name - specified in the "structure name" label - or with the standard NNStructure name, export the model into one of the available frameworks and run and/or test the exported model with the specified framework. Remember that, if a model is successfully exported and/or trained, than it is automatically saved for rapid exportation and deployment.


Finally we can find in the upper right corner the main window where we are actually going to graphically create our network.


#### <a name="dragdrop"></a> Drag n' Drop


<br />
<img src="Images/dragndrop.gif" />
<br /><br />

As you can see from the gif above, in the upper right corner we have an empty space where we can easily drag and drop blocks. We right-click and drag the empty template block in the lower left corner of this space, dropping it wherever we feel like. After dropping it, a new block is created, which let's us choose its behavior. It can be:

* Input
* Output
* Dense - or fully connected -
* Pooling
* Convolution
* Sum
* Multiplication
* Subtraction
* Dropout
* Blank


Later on we are going to discuss this differentiation.

Right-clicking an existing block we can drag n' drop as many times as we want, allowing us the modify and replace the blocks as we design our network.

Left-clicking the block it allows us to select it. One a block is selected it changes color to a light gray. Right clicking anywhere in the empty space allow us to unselect it. If we select another block after selecting the first one, it creates automatically a blank arch between them. Selecting the arch let's us change its attribute by selecting the wanted activation function from the drop down box placed on the right of the template block, as shown in the below gif.

<br />

<img src="Images/archcreat.gif" />

<br /><br />

We can decide which activation function the selected arrow has to have among the following currently available:

*  : no activation function
* Linear
* Rectified Linear - or ReLu -
* Hyperbolic Tangent - or Tanh -
* Hard Hyperbolic Tangent - or HardTanh -
* Exponential Linear - or Elu -
* Sigmoid
* Hard Sigmoid
* Softmax
* Softplus
* Log Softmax



### <a name="frames"></a>Frameworks supported

....


#### <a name="tensor"></a>TensorFlow


...


#### <a name="keras"></a>Keras


....


#### <a name="pytorch"></a>Pytorch


....
