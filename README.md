# motion-correct

## Motivation
Face recognition APIs like Microsoft Azure are developed for the general purpose. This application is intended to improve recognition accuracy for a classroom setting (where we have a given group of people that generally stay in the same position throughout the class). In this kind of situation, because of the consistency of position, it is possible to obtain a better recognition accuracy. This application is developed to extract the position information from API returned face recognition result and use the consistency of position assumption to improve accuracy.


## Installation

## Test Case

### Instruction

### Result
| Data Set | Data Count | Original Accuracy | Improved Accuracy |
| --- | --- | --- | --- |
| Training Set 2018-01-03&18 | 1693 | 0.7732 | 0.8771 |
| Test Set 2018-01-09 | 1693 | 0.7732 | 0.8771 |
| Test Set 2018-01-09 | 345 | 0.4783 | 0.5913 |
| Test Set 2018-01-09 | 525 | 0.6267 | 0.6933 |
| Test Set 2018-01-09 | 792 | 0.7980 | 0.8573 |
In this test set example 

## Directory Tree
```bash
├── motion-correct
│   ├── data
│   │   ├──azure_face_recognition_result_data.json # Sample test data.
│   │   ├──group1.csv # Similarity table for group 1.
│   │   └──group5.csv # Similarity table for group 5.
│   ├── __init__.py
│   ├── automaton.py # Automaton class, represent the model in a frame, used
│   │                # to support the build of location model.
│   ├── build.py # Build location model.
│   ├── collection.py # Collection class, connect automaton class across frames,
│   │                 # used to support the build of location model.
│   ├── convert.py # Normalize and add dummy variables to convert the matched result
│   │              # into vector to feed the neural network.
│   ├── data.py # Obtain data from JSON or SQL database.
│   ├── main.py # Main file, run main.py to run the program.
│   ├── match.py # The trough the data and perform match between the data and the model.
│   ├── model.weights.best.hdf5 # Best rate for the trained network.
│   ├── network.py # Build the neural network.
│   ├── parameter.py # Parameter setting.
│   ├── predict.py # Run the trained neural network to predict on the input data.
│   ├── similarity.py # Convert the predicted confidence on one face to all faces
│   │                 # using the similarity table.
│   └── test.py # Generate precision and accuracy table for testing purposes.
├── README.md # This file.
└── setup.py # Setup file for this Python package.
```

## Key Concepts

### Trusted Area


### Frame Filling


## Design Flow

### Overview
The algorithm takes input Microsoft Azure face recognition data in `data.py`. Then process the data and build trusted area model using the build function in `build.py`. The function finds face recognition results that do not move (same face found at close by location in a range of time) with the help from `Automaton` and `Collection` class. Next, in `match.py`, the algorithm matches the face recognition results back to all the trusted area model that is confirmed to be valid. The match function will trust all the face recognition results that can be matched into a valid model, and generate a snapshot of which models and faces are matched in each frame. The data are processed in `convert.py` before sending to convolutional neural network in `network.py` to decide which possible face is the closest match to an unconfirmed recognition result, and `predict.py` translate the network outputs into final results.

### Trusted Area Model

### Convolutional Neural Network



## Reference & Extension
Dalong, Y. & Qingge, J. (2017). Multiple Object Tracking Algorithm via Collaborative Motion Status Estimation. Retrieved from http://www.jsjkx.com/jsjkx/ch/reader/view_abstract.aspx?file_no=201711A032
