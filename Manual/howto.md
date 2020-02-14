### <a name="documentation"></a> Documentation

To automatically generate the documentation run on the terminal the following command:

<b>pdoc --html path/to/project/directory</b>

This will generate a folder called html with the documentation. Note: this can be done only if you already installed the pdoc package through pip3.


### <a name="howto"></a> How to use

<img src="https://www.github.com/drasgo/VENN/blob/master/Manua/VENN.jpg" />

<br /><br />
Let's take a look at the gui of the tool, as shown in the above picture: we can tell right away that there are essentially four distinct areas.

In the upper left corner we can see the an area where we can specify various options relative to the run/test mode: the input and output data we want to train the model with, the epochs number for the training session and the loss and optimizer functions we want to use. The only thing which needs to be modified right away is the number of values for each input and each output -aka their dimensionalities. We are coming back to this later on.


In the lower left corner we can see the logger, which will show us every possible problem or useful piece of information regarding the completion of a task - such as the creation of a model, or the export of the model into a framework, or so on.


In the lower right corner we can find the various options: saving and loading a structure with a personalized name - specified in the "structure name" label - or with the standard NNStructure name, export the model into one of the available frameworks and run and/or test the exported model with the specified framework. Remember that, if a model is successfully exported and/or trained, than it is automatically saved for rapid exportation and deployment.


Finally we can find in the upper right corner the main window where we are actually going to graphically create our network.
