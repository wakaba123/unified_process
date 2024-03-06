import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

print("TensorFlow version:", tf.__version__)

IMG_SIZE = 28

class Model(tf.Module):

    def __init__(self):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Flatten(input_shape=(
                IMG_SIZE, IMG_SIZE), name='flatten'),
            tf.keras.layers.Dense(128, activation='relu', name='dense_1'),
            tf.keras.layers.Dense(10, name='dense_2')
        ])

        self.model.compile(
            optimizer='sgd',
            loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True))

    # The `train` function takes a batch of input images and labels.
    @tf.function(input_signature=[
        tf.TensorSpec([None, IMG_SIZE, IMG_SIZE], tf.float32),
        tf.TensorSpec([None, 10], tf.float32),
    ])
    def train(self, x, y):
        with tf.GradientTape() as tape:
            prediction = self.model(x)
            loss = self.model.loss(y, prediction)
        gradients = tape.gradient(loss, self.model.trainable_variables)
        self.model.optimizer.apply_gradients(
            zip(gradients, self.model.trainable_variables))
        result = {"loss": loss}
        return result

    @tf.function(input_signature=[
        tf.TensorSpec([None, IMG_SIZE, IMG_SIZE], tf.float32),
    ])
    def infer(self, x):
        logits = self.model(x)
        probabilities = tf.nn.softmax(logits, axis=-1)
        return {
            "output": probabilities,
            "logits": logits
        }

    @tf.function(input_signature=[tf.TensorSpec(shape=[], dtype=tf.string)])
    def save(self, checkpoint_path):
        tensor_names = [weight.name for weight in self.model.weights]
        tensors_to_save = [weight.read_value()
                           for weight in self.model.weights]
        tf.raw_ops.Save(
            filename=checkpoint_path, tensor_names=tensor_names,
            data=tensors_to_save, name='save')
        return {
            "checkpoint_path": checkpoint_path
        }

    @tf.function(input_signature=[tf.TensorSpec(shape=[], dtype=tf.string)])
    def restore(self, checkpoint_path):
        restored_tensors = {}
        for var in self.model.weights:
            restored = tf.raw_ops.Restore(
                file_pattern=checkpoint_path, tensor_name=var.name, dt=var.dtype,
                name='restore')
            var.assign(restored)
            restored_tensors[var.name] = restored
        return restored_tensors

fashion_mnist = tf.keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

train_images = (train_images / 255.0).astype(np.float32)
test_images = (test_images / 255.0).astype(np.float32)
train_labels = tf.keras.utils.to_categorical(train_labels)
test_labels = tf.keras.utils.to_categorical(test_labels)

NUM_EPOCHS = 100
BATCH_SIZE = 100
epochs = np.arange(1, NUM_EPOCHS + 1, 1)
losses = np.zeros([NUM_EPOCHS])
m = Model()

train_ds = tf.data.Dataset.from_tensor_slices((train_images, train_labels))
train_ds = train_ds.batch(BATCH_SIZE)

for i in range(NUM_EPOCHS):
  for x,y in train_ds:
    result = m.train(x, y)

  losses[i] = result['loss']
  if (i + 1) % 10 == 0:
    print(f"Finished {i+1} epochs")
    print(f"  loss: {losses[i]:.3f}")

# Save the trained weights to a checkpoint.
m.save('/tmp/model.ckpt')

plt.plot(epochs, losses, label='Pre-training')
plt.ylim([0, max(plt.ylim())])
plt.xlabel('Epoch')
plt.ylabel('Loss [Cross Entropy]')
plt.legend()
plt.show()

SAVED_MODEL_DIR = "saved_model"

tf.saved_model.save(
    m,
    SAVED_MODEL_DIR,
    signatures={
        'train':
            m.train.get_concrete_function(),
        'infer':
            m.infer.get_concrete_function(),
        'save':
            m.save.get_concrete_function(),
        'restore':
            m.restore.get_concrete_function(),
    })

# Convert the model
converter = tf.lite.TFLiteConverter.from_saved_model(SAVED_MODEL_DIR)
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS,  # enable TensorFlow Lite ops.
    tf.lite.OpsSet.SELECT_TF_OPS  # enable TensorFlow ops.
]
converter.experimental_enable_resource_variables = True
tflite_model = converter.convert()

interpreter = tf.lite.Interpreter(model_content=tflite_model)
interpreter.allocate_tensors()

infer = interpreter.get_signature_runner("infer")

logits_original = m.infer(x=train_images[:1])['logits'][0]
logits_lite = infer(x=train_images[:1])['logits'][0]

print(logits_original , logits_lite)