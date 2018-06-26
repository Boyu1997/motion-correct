# motion-correct

## Installation

## Directory Tree
```bash
├── motion-correct
│   ├── data
│   │   ├──azure_face_recognition_result_data.json # Sample test data.
│   │   ├──group1.csv # Similarity table for group 1.
│   │   └──group5.csv # Similarity table for group 5.
│   ├── __init__.py
│   ├── automaton.py # Automaton class, represent the model in a frame, used
|   |                # to support the build of location model.
│   ├── build.py # Build location model.
│   ├── collection.py # Collection class, connect automaton class across frames,
|   |                 # used to support the build of location model.
│   ├── convert.py # Normalize and add dummy variables to convert the matched result
|   |              # into vector to feed the neural network.
│   ├── data.py # Obtain data from JSON or SQL database.
│   ├── main.py # Main file, run main.py to run the program.
│   ├── match.py # The trough the data and perform match between the data and the model.
│   ├── model.weights.best.hdf5 # Best rate for the trained network.
│   ├── network.py # Build the neural network.
│   ├── parameter.py # Parameter setting.
│   ├── predict.py # Run the trained neural network to predict on the input data.
│   ├── similarity.py # Convert the predicted confidence on one face to all faces
|   |                 # using the similarity table.
│   └── test.py # Generate precision and accuracy table for testing purposes.
├── README.md # This file.
└── setup.py # Setup file for this Python package.
```

## Reference & Extension
Dalong, Y. & Qingge, J. (2017). Multiple Object Tracking Algorithm via Collaborative Motion Status Estimation. Retrieved from http://www.jsjkx.com/jsjkx/ch/reader/view_abstract.aspx?file_no=201711A032
