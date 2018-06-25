from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten, Dropout
from keras.layers import Conv2D
from keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt
import numpy as np

def conv_net(X, y, X_test, y_test):
    # expected input data shape: (batch_size, timesteps, data_dim)
    model = Sequential()

    model.add(Conv2D(filters=64, kernel_size=[1,4], activation='relu', input_shape=(X.shape[1], X.shape[2], X.shape[3])))

    model.add(Flatten())

    model.add(Dense(128, activation='relu'))

    model.add(Dropout(0.2))

    model.add(Dense(32, activation='relu'))

    model.add(Dropout(0.2))

    model.add(Dense(y.shape[1], activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    model.summary()

    checkpointer = ModelCheckpoint(filepath='model.weights.best.hdf5', verbose=0, save_best_only=True)
    history = model.fit(X, y, epochs=300, verbose=0, callbacks=[checkpointer], validation_split=0.2)


    # load the weight for the best validation accuracy
    model.load_weights('model.weights.best.hdf5')

    '''
    # load the best weight
    predictions = model.predict_proba(X)
    print ("X for entry 500", np.array(X[500]).reshape(X.shape[1], 4))
    print ("y for entry 500", y[500])
    print ("Prediction for entry 500", predictions[500])
    '''

    # Scoring the model
    train_score = model.evaluate(X, y)
    print("\nTraining Set Accuracy: ", train_score[-1])
    test_score = model.evaluate(X_test, y_test)
    print("\nTest Set Accuracy: ", test_score[-1])

    '''
    # summarize history for lost
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    # summarize history for accuracy
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    '''


    return model
