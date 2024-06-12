# beach-cleaning-hardware
Repository for hardware design and documentation


## Installation:

Clone repository, for this example we assume that the source code is located in folder `${HOME}/src`, paths used in the following need to be modified accordingly in case another folder structure is used:
```
cd ${HOME}
mkdir -p OIST_BC
cd OIST_BC
git clone git@github.com:okinawa-ai-beach-robot/beach-cleaning-hardware.git
````

To install the beachbot source package:
```
cd ${HOME}/OIST_BC/beach-cleaning-hardware/python-interface
pip install -e .
```

In case the package is installed on Jetson SBC, the OpenCV python package can be overshadowed by the public PIP one.
In this case, the hardware interface for the camera of the Jetson cann ot be opened.
To avoid using the public OpenCV package, uninstallation can be performed by:
```
pip uninstall opencv-python
``` 

### Setup of Enironment:
The *beachbot* python package assumes a environment variable **BEACHBOT_HOME** to be set and pointing to te base folder inlcuding dataset and model sub-folders.
In our case, we can modify the `.bachrc` file to define the base-path:
```
echo -e "export BEACHBOT_HOME=\"`echo $HOME`/OIST_BC/\"\n" >> ~/.bashrc
```

The current definition of the environment variable can be verified by:
```
echo $BEACHBOT_HOME
```


### Setup of Datasets:
It is assumed that datasets are located in the subfolder `${BEACHBOT_HOME}/Datasets/`.
Each dataset is stored in its own folder and contains:
- `valid/` subfolder containing validation samples
- `train/` subfolder containing training samples
- `test/` subfolder containing testing samples
- contains a `dataset.yaml` file with the dataset specifications
Each sample sub-folder (valid,train, and test) contain two furter subfolders:
- `labels/` includes a text file with bounding boxes (*\[xxx\].txt*) for each image in the `images` folder.
- `images/` includes a set of images (*\[xxx\].jpg*)

The data format of the bounding box is defined as sinple text file.
Each line encodes one bounding box of an object:
```
[cmass number (integer)] [x position of center of box (float)] [y position of center of box (float)] [width of box (float)] [height of box (float)]
```
As an example, the content of the file could be:
```
2 0.846875 0.3825 0.30625 0.2225
2 0.69140625 0.3695375 0.28515625 0.2109375
2 0.4912109375 0.3664125 0.349609375 0.2453125
2 0.26171875 0.3507875 0.298828125 0.2046875
2 0.1411171875 0.3375 0.2822265625 0.1843
```
Position and size is encoded relative to the image (value range 0-1), tha class mumber bust be in rage as defined in the the dataset definition file `dataset.yaml`.

#### Dataset import from Roboflow:
TODO


## How to Use:
Various examples of how to use the provided packages are located in the folder `${HOME}/OIST_BC/beach-cleaning-hardware/python-interface/tests`

### Evaluation of a trained model via web-ui:
```
cd ${HOME}/OIST_BC/beach-cleaning-hardware/python-interface/tests
python dataset_analyzer_ui.py 
```
It seems that the connection of the browser to the server is lost some times (TODO), in such case it may help to relod the browser window of to close and reopen a new tab.



