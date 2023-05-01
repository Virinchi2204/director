import glob
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, LSTM, Embedding
from keras.preprocessing.text import Tokenizer



# combine all scripts into a single text
script_files = glob.glob("C:/Users/virin/hackathongbp/Scripts/*.txt")
combined_text = ""
for file in script_files:
    with open(file, encoding="utf8") as f:
        text = f.read()
        combined_text += text + "\n"

# create tokenizer and generate sequences
tokenizer = Tokenizer()
tokenizer.fit_on_texts([combined_text])
sequences = tokenizer.texts_to_sequences([combined_text])[0]

# create input and output sequences
seq_length = 50
inputs = []
outputs = []
for i in range(seq_length, len(sequences)):
    inputs.append(sequences[i-seq_length:i])
    outputs.append(sequences[i])

# pad sequences
inputs_padded = tf.keras.utils.pad_sequences(inputs, maxlen=seq_length, truncating='pre')
outputs_categorical = np.array(outputs)
outputs_categorical = np.eye(len(tokenizer.word_index)+1)[outputs_categorical]

# define model
vocab_size = len(tokenizer.word_index) + 1
model = Sequential()
model.add(Embedding(input_dim=vocab_size, output_dim=100, input_length=seq_length))
model.add(LSTM(units=100, return_sequences=True))
model.add(LSTM(units=100))
model.add(Dense(units=vocab_size, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# train model
model.fit(inputs_padded, outputs_categorical, epochs=10, batch_size=64)

# generate new text
seed_text = "Batman"
for i in range(50):
    # encode seed text
    seed_sequence = tokenizer.texts_to_sequences([seed_text])[0]
    seed_padded = tf.keras.utils.pad_sequences([seed_sequence], maxlen=seq_length, truncating='pre')

    # predict next word
    prediction = model.predict(seed_padded)[0]
    index = np.argmax(prediction)

    # convert index back to word
    word = ""
    for w, i in tokenizer.word_index.items():
        if i == index:
            word = w
            break

    # add predicted word to seed text
    seed_text += " " + word

print(seed_text)



"""
import os
import openai

# Set OpenAI API key
openai.api_key = "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"

# Define the file paths for the three scripts
file_paths = ["Scripts/batman_begins.txt", "Scripts/tdk.txt", "Scripts/tdk_returns.txt"]

# Read the contents of each script file
script_text = ""
for file_path in file_paths:
    with open(file_path, "r", encoding="utf-8") as file:
        script_text += file.read()

# Get user prompt
prompt = input("Enter a prompt for the new script: ")

# Generate a new script based on the provided scripts and the user prompt
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=script_text + prompt,
    max_tokens=4000,
    n=1,
    stop=None,
    temperature=0.5
)

# Print and save the generated script
generated_script = response.choices[0].text
print(generated_script)

# Save the generated script to the Scripts folder
with open("Scripts/generated_script.txt", "w", encoding="utf-8") as file:
    file.write(generated_script)
"""