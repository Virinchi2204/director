import speech_recognition as sr
import openai
import pyttsx3
import os
openai.api_key= os.environ["OPENAI_API_KEY"]#"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"

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize speech recognition engine
r = sr.Recognizer()

# Define a function to generate ChatGPT response
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=prompt, max_tokens=4000, n=1,stop=None,temperature=0.5
    )
    return response.choices[0].text

def get_input():
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said: " + text)
            return text
        except:
            print("Sorry, I could not understand your speech input. Please enter text instead.")
            speak("Sorry, I could not understand your speech input. Please enter text instead.")
            text = input("Enter text input: ")
            return text
# Define a function to generate voice output
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize conversation
print("Hello, I'm Alfred Pennyworth. How can I assist you?")
speak("Hello, I'm Alfred Pennyworth. How can I assist you?")

# Conversation loop
while True:
    # Get user input
    prompt = get_input()
    # Generate response
    if prompt:
        if "goodbye" in prompt.lower():
                print("Alright then, goodbye!")
                speak("Alright then, goodbye!")
                exit()
        response = generate_response(prompt)
        print("Alfred: " + response)
        speak(response)
        
     # Exit program

