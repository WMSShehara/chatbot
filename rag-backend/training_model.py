from fastapi import FastAPI, BackgroundTasks
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
from process_Data import get_data
import tensorflow as tf

app = FastAPI()

# Load the tokenizer and model globally
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
tokenizer.pad_token = tokenizer.eos_token
model = TFGPT2LMHeadModel.from_pretrained('gpt2')

# Global variable to track training status
training_status = {"status": "idle", "progress": 0}


def train_model():
    global training_status

    training_status["status"] = "training"
    training_status["progress"] = 0

    # Get data
    data = get_data()  # Should return a list of (question, answer) pairs
    questions = [question for question, _ in data]
    answers = [answer for _, answer in data]

    # Tokenize the data
    max_length = 512
    inputs = tokenizer(
        questions,
        truncation=True,
        padding='max_length',
        max_length=max_length,
        return_tensors='tf'
    )
    targets = tokenizer(
        answers,
        truncation=True,
        padding='max_length',
        max_length=max_length,
        return_tensors='tf'
    )

    input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']
    labels = targets['input_ids']

    # Replace padding tokens in labels with -100
    labels = tf.where(labels == tokenizer.pad_token_id, -100, labels)

    # Create dataset
    def generator():
        for i in range(len(input_ids)):
            yield {
                "input_ids": input_ids[i],
                "attention_mask": attention_mask[i],
                "labels": labels[i],
            }

    dataset = tf.data.Dataset.from_generator(
        generator,
        output_signature={
            "input_ids": tf.TensorSpec(shape=(max_length,), dtype=tf.int32),
            "attention_mask": tf.TensorSpec(shape=(max_length,), dtype=tf.int32),
            "labels": tf.TensorSpec(shape=(max_length,), dtype=tf.int32),
        },
    )

    batch_size = 8
    dataset = dataset.shuffle(len(data)).batch(batch_size).prefetch(tf.data.AUTOTUNE)

    optimizer = tf.keras.optimizers.Adam(learning_rate=5e-5)

    @tf.function
    def train_step(batch):
        with tf.GradientTape() as tape:
            outputs = model(
                input_ids=batch['input_ids'],
                attention_mask=batch['attention_mask'],
                labels=batch['labels'],
            )
            loss = outputs.loss

        gradients = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))
        return loss

    epochs = 3
    for epoch in range(epochs):
        print(f"Epoch {epoch + 1}/{epochs}")
        epoch_loss = 0
        for step, batch in enumerate(dataset):
            loss = train_step(batch)
            epoch_loss += loss

            # Update progress
            training_status["progress"] = (step + 1) / len(dataset) * 100

            if step % 10 == 0:
                print(f"Step {step}, Loss: {loss.numpy():.4f}")

        print(f"Epoch {epoch + 1} Loss: {epoch_loss / (step + 1):.4f}")

    training_status["status"] = "completed"
    training_status["progress"] = 100


@app.post("/train")
async def train_endpoint(background_tasks: BackgroundTasks):
    """Endpoint to start training."""
    if training_status["status"] == "training":
        return {"message": "Training is already in progress."}

    background_tasks.add_task(train_model)
    return {"message": "Training started."}


@app.get("/status")
async def status_endpoint():
    """Endpoint to check training status."""
    return training_status


@app.post("/generate")
async def generate_endpoint(input_text: str):
    """Endpoint to generate text using the trained model."""
    input_ids = tokenizer.encode(input_text, return_tensors="tf")
    output = model.generate(input_ids, max_length=100, num_return_sequences=1)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return {"response": response}
