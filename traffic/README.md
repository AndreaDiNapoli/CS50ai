# README file for the Traffic CS50ai project
### Author: Andrea Di Napoli
<br>

## Preparation
After implementing the load_data function, I started by implementing the simpliest neural network model possible and tested with the small grsrb database.
I did not care about accuracy, but I was just looking for a functioning modelling function.

    model = tf.keras.models.Sequential([
    
    # Flatten units
    tf.keras.layers.Flatten(),

    # Add output layer with 1 unit for category, with softmax activation
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
    )

    return model

This basic mode works with this results: <br>
*11/11 - 0s - loss: 0.2374 - accuracy: 0.9911 - 110ms/epoch - 10ms/step*

<br>

## Test
### Test 1:
I kept the same neural model, but using the full database

**MODEL**

    model = tf.keras.models.Sequential([
    
    # Flatten units
    tf.keras.layers.Flatten(),

    # Add output layer with 1 unit for category, with softmax activation
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
    )

    return model

**RESULTS**

*333/333 - 0s - loss: 51.3749 - accuracy: 0.7659 - 265ms/epoch - 797us/step*
<br>
<br>

### Test 2:
Time for some optimization! <br>
First, I'm gonna try some convoulation <br>
Flattening a 30x30 image does not seem a great idea, so first of all I'm gonna try to apply some pooling <br>

**MODEL**

    model = tf.keras.models.Sequential([
    
    # Convolutional layer. Learn 32 filters using a 3x3 kernel
    tf.keras.layers.Conv2D(
        32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
    ),

    # Max-pooling layer, using 2x2 pool size
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    
    # Flatten units
    tf.keras.layers.Flatten(),

    # Add output layer with 1 unit for category, with softmax activation
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
    )

    return model

**RESULTS**

*333/333 - 0s - loss: 0.8053 - accuracy: 0.8891 - 470ms/epoch - 1ms/step*
<br>
<br>

### Test 3:
Test 2 results were getting better, but 0.889 accuracy is not enough.
I noticed that accuracy while learning is very high (0.975) so it may be the case the mode is overfitting?
That seems reasonable since we have no hidden layers and so no dropouts!
Let's give a try adding some!

**MODEL**

    model = tf.keras.models.Sequential([
    
    # Convolutional layer. Learn 32 filters using a 3x3 kernel
    tf.keras.layers.Conv2D(
        32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
    ),

    # Max-pooling layer, using 2x2 pool size
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    
    # Flatten units
    tf.keras.layers.Flatten(),

    # Add a hidden layer with dropout
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.5),

    # Add output layer with 1 unit for category, with softmax activation
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

**RESULTS**

*333/333 - 1s - loss: 3.5077 - accuracy: 0.0542 - 549ms/epoch - 2ms/step*
<br>
<br>

### Test 4:
Test 3 results was way worse for some reason!
I guess I was right thinking about overfitting for test2, so maybe test3 solve that and now my accuracy is low.
Adding convoultion helped a lot, I'll try add some more steps of that (no need for pooling, I think. Number of "pixels" is low enough)

**MODEL**

    model = tf.keras.models.Sequential([
    
    # Convolutional layer. Learn 32 filters using a 3x3 kernel
    tf.keras.layers.Conv2D(
        32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
    ),

    # Max-pooling layer, using 2x2 pool size
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    # Convolutional layer. Learn 32 filters using a 3x3 kernel
    tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),
    
    # Convolutional layer. Learn 32 filters using a 3x3 kernel
    tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),

    # Flatten units
    tf.keras.layers.Flatten(),

    # Add a hidden layer with dropout
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.5),


    # Add output layer with 1 unit for category, with softmax activation
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

**RESULTS**

*333/333 - 1s - loss: 0.1187 - accuracy: 0.9737 - 663ms/epoch - 2ms/step*
<br>
<br>

### Final testing:
Test 4 was WAY better, 0.9737 is great!
I'll make some more swift test to see if it can be improved, keeping only summary note here.

<ul>
    <li>Increasing the filters of convoulition dropped down the accuracy</li>
    <li>Adding another hidden layer lower accuracy but let me think that the reason was lower learning, I'll try add some epoch</li>
    <li>Adding epochs (20) helped a lot, but accurasy is still lower than test 4. I think there's still room for training improvement</li>
    <li>Reaching 40 epoch results in accuracy: 0.9782! Not really much better, but maybe the model is more robust now</li>
    <li>Trying some more pooling to see if we can optimize</li>
</ul>
<br>

**FINAL MODEL**

    model = tf.keras.models.Sequential([
    
    # Convolutional layer. Learn 32 filters using a 3x3 kernel
    tf.keras.layers.Conv2D(
        32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
    ),

    # Max-pooling layer, using 2x2 pool size
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    # Convolutional layer. Learn 32 filters using a 3x3 kernel
    tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),
    
    # Convolutional layer. Learn 32 filters using a 3x3 kernel
    tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),

    # Max-pooling layer, using 2x2 pool size
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    # Flatten units
    tf.keras.layers.Flatten(),

    # Add a hidden layer with dropout
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.5),

    # Add a hidden layer with dropout
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.5),


    # Add output layer with 1 unit for category, with softmax activation
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

**RESULTS**

*333/333 - 1s - loss: 0.1044 - accuracy: 0.9791 - 740ms/epoch - 2ms/step*
<br>
<br>