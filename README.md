# kNN Model for detection of atypical queries

Inside this repository we have two folders:

* **Individual Tests** (Logs created in test environment)

## Needed Tools and Libraries

* [Python 3](https://www.python.org/download/releases/3.0/)
* [Pip](https://pypi.org/project/pip/)
* [PyOD](https://pyod.readthedocs.io/en/latest/)
* [Spicy](https://pypi.org/project/spicy/)
* [Pandas](https://pandas.pydata.org/)
* [Numpy](https://numpy.org/)
* [Sckit_learn](https://scikit-learn.org/stable/)
* [Matplotlib](https://matplotlib.org/)

## Files Description

To summarize the operation I point out the following explanations of the files in the folders:

* **PrimerPaso.py**
  In this step, the data collection is carried out from the entered file, reading of transaction records, extraction of attributes and generation of new files. These files will contain the extracted transaction log data in a format set for the next step. The path of the log file to use is edited on Line 5.
* **SegundoPaso.py**
  A split of transaction log sets is performed, where files with a maximum of 5000 transaction logs each are generated.
* **TercerPaso.py**
  Each set of transaction records generated in the previous step is read, cleaning, transformation, data normalization and implementation of the kNN algorithm are performed. The result of this step is the generation of new files containing only the transaction logs identified as anomalies.
* **CuartoPaso.py**
  A text analysis of the query made to the database associated with the transaction record that was identified as an anomaly is performed. If any expression is recorded that reveals the existence of an attack or its attempt, the anomaly is recorded on the system server.
* **Executable.sh**
  File that executes all the mentioned files.

## Execution Steps       

We recommend updating the local packages before executing the project.

In your project root directory, run the update command:
```
$ npm update
```

For installing all dependencies, run the install commmand:
```
$ npm install -g npm@latest
```

For executing all og the files at once, run the command:
```
$ sh ejecutable.sh
```

For executing one file at the time, run the command:
```
$ py "Filename.py"
```

## Authors:

* Cesar Añasco: 	[cesar.anasco@epn.edu.ec](mailto:cesar.anasco@epn.edu.ec)
* Karen Morocho: 	[karen.morocho@epn.edu.ec](mailto:karen.morocho@epn.edu.ec)
