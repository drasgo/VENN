# VENN
Visual Editor tool for Neural Network development training and deployment

To use this project you have to install:

- PyQt5
- (Optional) tensorflow
- (Optional) torch torchvision (Pytorch)
- (Optional) keras
- (Optional) pdoc (Documentation)

# WIKI

To generate documentation run on the terminal

pdoc --html path/to/project/directory

This will generate a folder called html with the documentation

How to.. : https://www.github.com/drasgo/ViCreNN/blob/master/howto.md



# TODO

- aggiungere scelte per optimizer ed epochs
- modificare il controllo pre salvataggio modello aggiungendo il fatto che i due nodi prima di un sub/sub devono avere la stessa dimensione + rimuovere controllo di arco none
- togliere finestre in cui contenere i dati di input e output, lasciando solo la finestra con il nome del file
- spostare le finestre per decidere epoch. ninput, noutput, cost, optimizer, percorso file input e percorso file output a destra
- rimuovere scelta del tipo di dati, spostando e aumentando la finestra del logger verso sinistra
- aggiungere possibilità di inserire più nodi di input (quindi recuperando l'input da più file esterni)

- add graphical resize if window is resized
- add test/run option
- add epoch label
- graphical refactor
- add more advanced settings
- add recursive full support
- add convolution support
- add famous models prefab
- general bugfix
- comments
- Double check for cost/loss/activation/optimization functions for all frameworks





-----------------------------------
ALTRO PROGETTO: programma che prende un modello gia addestrato in tensorflow, pytorch, keras o altri e un dato di input restituisce l'output. Può anche prendere più input computando tutti i vari output
