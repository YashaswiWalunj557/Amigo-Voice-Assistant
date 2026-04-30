import pyttsx3
import urllib.parse
import pyautogui
import speech_recognition as sr
import wikipedia
import webbrowser
import tkinter as tk
from tkinter import messagebox
import threading
from tkinter import ttk
from datetime import datetime
import cv2
import numpy as np
import datetime
import requests
import os
import time
from PIL import Image, ImageTk, ImageOps
from PIL import Image, ImageDraw
from ecapture import ecapture as ec
import subprocess
import platform
import psutil


# Initialize pyttsx3
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[0].id)  # 1 for female and 0 for male voice

# Initialize the speech recognizer
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Hello,Good Morning")
        print("Hello,Good Morning")
    elif hour>=12 and hour<18:
        speak("Hello,Good Afternoon")
        print("Hello,Good Afternoon")
    else:
        speak("Hello,Good Evening")
        print("Hello,Good Evening")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        speak("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("User said: " + query + "\n")
    except Exception as e:
        print(e)
        speak("I didn't understand")
        return "None"
    return query

def face_recognition_system():
    print("Face Recognition System Started")

    # Load the Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Define the file path for yashu1's reference image
    file_path = r"c:\Users\YASHASWI\Desktop\voice_assistant-master\voice_assistant-master\yashu1_face.png"


    # Load yashu1's face image
    yashu1_image = cv2.imread(r"C:\Users\YASHASWI\Desktop\voice_assistant-master (3)\voice_assistant-master\yashu1_face.png")

    if yashu1_image is None:
        print("Error: Unable to read yashu1_face.png")
        speak("Error: Unable to load reference image.")
        return False

    # Convert yashu1's image to grayscale
    yashu1_gray = cv2.cvtColor(yashu1_image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the reference image
    yashu1_faces = face_cascade.detectMultiScale(yashu1_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(yashu1_faces) == 0:
        print("No face detected in the reference image.")
        speak("No face detected in the reference image.")
        return False

    # Extract the first detected face from the reference image
    (x, y, w, h) = yashu1_faces[0]
    yashu1_face = yashu1_image[y:y+h, x:x+w]

    # Convert the reference face to grayscale and calculate histogram
    yashu1_face_gray = cv2.cvtColor(yashu1_face, cv2.COLOR_BGR2GRAY)
    yashu1_face_hist = cv2.calcHist([yashu1_face_gray], [0], None, [256], [0, 256])
    yashu1_face_hist = cv2.normalize(yashu1_face_hist, yashu1_face_hist)

    # Start webcam feed
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print("Error: Could not access webcam.")
        speak("Error: Webcam not found.")
        return False
    


    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture frame.")
            break

        # Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the current frame
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]

            # Convert the detected face to grayscale and calculate histogram
            face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            face_hist = cv2.calcHist([face_gray], [0], None, [256], [0, 256])
            face_hist = cv2.normalize(face_hist, face_hist)

            # Compare histograms using correlation
            similarity = cv2.compareHist(yashu1_face_hist, face_hist, cv2.HISTCMP_CORREL)

            if similarity > 0.55:  # Threshold for recognition
                label = "Yashaswi"
                color = (0, 255, 0)  # Green for recognized
            else:
                label = "Unknown Face"
                color = (0, 0, 255)  # Red for unknown

            # Display results
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            if similarity > 0.65:  # Final confirmation threshold
                print("Face Recognized: Yashaswi")
                speak("Face recognized! You can now start speaking.")

                # Release resources and close the window
                video_capture.release()
                cv2.destroyAllWindows()
                return True  # Face recognition successful

        # Show the live video feed
        cv2.imshow("Face Recognition", frame)

        # Press 'q' to exit manually
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Face Recognition Stopped by User.")
            break

    # Release resources
    video_capture.release()
    cv2.destroyAllWindows()
    return False  # Return false if face is not recognized

# Run the function
face_recognition_system()

def get_weather(city):
    api_key = "39b828f459dd61ccc35a2d29c6e75828"  # Replace with your API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    # Complete URL to get the weather data for the given city
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"  # Use metric for temperature in Celsius
    
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] == "404":
        return "City not found."
    else:
        main = data["main"]
        weather_description = data["weather"][0]["description"]
        temperature = main["temp"]
        humidity = main["humidity"]
        pressure = main["pressure"]
        
        weather_report = (
            f"The temperature in {city} is {temperature}°C with {weather_description}. "
            f"Humidity is {humidity}% and the pressure is {pressure} hPa."
        )
        return weather_report

def play_song(query):
    # Extract the song name from the query (remove the "play music" part)
    song_name = query.replace("Tum Prem Ho", "").strip()
    
    if song_name:
        # URL encode the song name for use in the search query
        search_query = urllib.parse.quote(song_name)
        
        # Create the YouTube search URL for the song
        youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
        
        speak(f"Searching and playing {song_name}")
        webbrowser.open(youtube_url)
        update_text(f"Amigo: Playing {song_name}")
        exit(0)
    else:
        speak("Please provide the name of the song to play.")
        update_text("Amigo: Please provide the name of the song.")
        exit(0)

def handle_who_is_query(query):
    # Extract the person or subject name from the query
    person_or_subject = query.replace("who is", "").strip()

    if person_or_subject:
        search_query = person_or_subject.replace(" ", "+")  # Format query for URL
        google_url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(google_url)
        
        # Now, search Wikipedia and speak the summary
        speak("Searching Wikipedia...")
        
        try:
            results = wikipedia.summary(person_or_subject, sentences=2)
            speak("According to Wikipedia")
            speak(results)
            update_text(f"Amigo: {results}")
        except wikipedia.exceptions.DisambiguationError as e:
            speak(f"There are multiple results for {person_or_subject}. Let me show you more details.")
            results = e.options[:3]  # Limit to the first 3 options
            speak("Here are some options: " + ", ".join(results))
            update_text(f"Amigo: {', '.join(results)}")

        exit(0)
    else:
        speak("Please ask about a person or subject.")
        update_text("Amigo: Please ask about a person or subject.")
        exit(0)

wishMe()


# Start the assistant in a separate thread
def start_assistant():
    threading.Thread(target=run_assistant).start()

# Assistant logic function
def run_assistant():
    speak("Amigo assistance activated")
    speak("How can I help you?")
    
    while True:
        query = take_command().lower()

        if 'who is' in query or 'give me' in query:
            handle_who_is_query(query)
            exit(0)

        elif 'what is the weather' in query or 'tell me the weather' in query:
            speak("Please tell me the city")
            city = take_command().lower()  # Let the user specify the city
            weather_info = get_weather(city)
            speak(weather_info)
            update_text(f"Amigo: {weather_info}")
            exit(0)

        elif 'what is the date' in query or 'tell me the date' in query:
            now = datetime.datetime.now()
            current_date = now.strftime("%Y-%m-%d")
            date = f"The current date is {current_date}" 
            speak(date)
            update_text(f"Amigo: {date}")
            exit(0)

        elif 'what is the time' in query or 'tell me the time' in query:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            time = f"The current time is {current_time}" 
            speak(time)
            update_text(f"Amigo: {time}")
            exit(0)

        elif 'what is the day' in query or 'tell me the day' in query:
            now = datetime.datetime.now()
            current_day = now.strftime("%A")
            day = f"The current day is {current_day}" 
            speak(day)
            update_text(f"Amigo: {day}")
            exit(0)

        elif 'what is the weather' in query or 'tell me the weather' in query:
            now = datetime.datetime.now()
            current_weather = now.strftime("%A")
            weather = f"The current day is {current_weather}" 
            speak(weather)
            update_text(f"Amigo: {weather}")
            exit(0)

        elif 'are you' in query:
            speak("I am Amigo, developed by Sakshi,Tanvi,Yashu")
            update_text("Amigo: I am Amigo, developed by Sakshi,Tanvi,Yashu")
            exit(0)

        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open_new_tab("youtube.com")
            update_text("Amigo: Opening YouTube")
            exit(0)

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open_new_tab("google.com")
            update_text("Amigo: Opening Google")
            exit(0)
            
        
          
        elif 'open github' in query:
            speak("Opening GitHub")
            webbrowser.open_new_tab("github.com")
            update_text("Amigo: Opening GitHub")
            exit(0)

        elif 'open stackoverflow' in query:
            speak("Opening StackOverflow")
            webbrowser.open_new_tab("stackoverflow.com")
            update_text("Amigo: Opening StackOverflow")
            exit(0)

        elif 'open spotify' in query:
            speak("Opening Spotify")
            webbrowser.open_new_tab("spotify.com")
            update_text("Amigo: Opening Spotify")
            exit(0)

        elif 'open whatsapp' in query:
            speak("Opening WhatsApp")
            webbrowser.open_new_tab("https://web.whatsapp.com/")
            update_text("Amigo: Opening WhatsApp")
            exit(0)

        elif 'open gemini' in query:
            speak("Opening Gemini")
            webbrowser.open_new_tab("https://gemini.google.com/")
            update_text("Amigo: Opening Gemini")
            exit(0)

        elif 'open gmail' in query:
            speak("Opening Gmail")
            webbrowser.open_new_tab("https://mail.google.com/")
            update_text("Amigo: Opening Gmail")
            exit(0)

        elif 'open meet' in query:
            speak("Opening Google Meet")
            webbrowser.open_new_tab("https://meet.google.com/")
            update_text("Amigo: Opening Google Meet")
            exit(0)

        elif 'open chat' in query:
            speak("Opening Google Chat")
            webbrowser.open_new_tab("https://mail.google.com/chat/")
            update_text("Amigo: Opening Google Chat")
            exit(0)

        elif 'open contacts' in query:
            speak("Opening Contacts")
            webbrowser.open_new_tab("https://contacts.google.com/")
            update_text("Amigo: Opening Contacts")
            exit(0)

        elif 'open drive' in query:
            speak("Opening Google Drive")
            webbrowser.open_new_tab("https://drive.google.com/")
            update_text("Amigo: Opening Google Drive")
            exit(0)

        elif 'open calender' in query:
            speak("Opening Calender")
            webbrowser.open_new_tab("https://calendar.google.com/")
            update_text("Amigo: Opening Calender")
            exit(0)

        elif 'open play store' in query:
            speak("Opening Play Store")
            webbrowser.open_new_tab("https://play.google.com/")
            update_text("Amigo: Opening Play Store")
            exit(0)

        elif 'open translator' in query:
            speak("Opening Translator")
            webbrowser.open_new_tab("https://translate.google.com/")
            update_text("Amigo: Opening Translator")
            exit(0)

        elif 'open photos' in query:
            speak("Opening Photos")
            webbrowser.open_new_tab("https://photos.google.com/")
            update_text("Amigo: Opening Photos")
            exit(0)

        elif 'play music' in query:
            play_song(query)
            exit(0)

        elif 'open netflix' in query:
            speak("Opening Netflix")
            webbrowser.open_new_tab("netflix.com")
            update_text("Amigo: Opening Netflix")
            exit(0)
        
        elif 'open command prompt' in query or 'open cmd' in query:
            speak("Opening Command Prompt")
            os.system('start cmd')  # Command to open the command prompt in Windows
            update_text("Amigo: Opening Command Prompt")
            exit(0)

        elif 'open notepad' in query or 'open Notepad' in query:
            speak("Opening Notepad")
            os.system('start notepad')  # Command to open Notepad in Windows
            update_text("Amigo: Opening Notepad")
            exit(0)

        elif 'open word' in query:
            speak("Opening Word")
            os.system('start winword')  # Command to open Word in Windows
            update_text("Amigo: Opening Word")
            exit(0)

        elif 'open excel' in query:
            speak("Opening Excel")
            os.system('start excel')  # Command to open Excel in Windows
            update_text("Amigo: Opening Excel")
            exit(0)

        elif 'open powerpoint' in query:
            speak("Opening PowerPoint")
            os.system('start powerpnt')  # Command to open PowerPoint in Windows
            update_text("Amigo: Opening PowerPoint")
            exit(0)

        elif 'open calculator' in query:
            speak("Opening Calculator")
            os.system('start calc')  # Command to open Calculator in Windows
            update_text("Amigo: Opening Calculator")
            exit(0)

        elif 'open task manager' in query:
            speak("Opening Task Manager")
            os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\System Tools\Task Manager')  # Command to open Task Manager in Windows
            update_text("Amigo: Opening Task Manager")
            exit(0)


        elif 'open gmail' in query:
            webbrowser.open_new_tab("gmail.com")
            speak("Google Mail open now")
            time.sleep(5)

        elif 'news' in query:
            news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India,Happy reading')
            time.sleep(5)

        elif "camera" in query or "take a photo" in query:
            ec.capture(0,"robo camera","img.jpg")

        elif 'stop' in query:
            speak("Shutting down. Goodbye!")
            update_text("Amigo: Shutting down. Goodbye!")
            break

        elif "log off" in query or "sign out" in query:
            speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])

# Function to update the text box with the assistant's responses
def update_text(response):
    text_box.config(state=tk.NORMAL)
    text_box.insert(tk.END, response + '\n')
    text_box.yview(tk.END)
    text_box.config(state=tk.DISABLED)

# Function to clear the output text
def clear_text():
    text_box.config(state=tk.NORMAL)
    text_box.delete(1.0, tk.END)
    text_box.config(state=tk.DISABLED)

# Create the main GUI window
root = tk.Tk()
root.title("Amigo Voice Assistant")
root.geometry("600x700")
root.config(bg="#212121")  # Dark background color

# Function to add the animated background
def background_animation():
    global bg_image, bg_frame, bg_counter

    # Loop through the frames of the animated GIF
    bg_counter += 1
    if bg_counter >= len(bg_frame_list):
        bg_counter = 0

    bg_image = bg_frame_list[bg_counter]  # Get the next frame in the animation
    bg_label.config(image=bg_image)
    bg_label.image = bg_image

    # Update every 100 ms for a smooth animation
    root.after(100, background_animation)


# Frame for the UI elements
frame = tk.Frame(root, bg="#212121")
frame.pack(pady=30)

# Title Label (Center the title)
title_label = tk.Label(frame, text="Amigo Assistant", font=("Helvetica", 30, "bold"), fg="#ffffff", bg="#212121")
title_label.grid(row=0, column=0, columnspan=2, pady=20)

# Create Text Box for showing responses
text_box = tk.Text(root, height=8, width=50, font=("Arial", 14), wrap="word", bg="#2e3b47", fg="white", bd=3, padx=10, pady=10)
text_box.pack(pady=20)
text_box.config(state=tk.DISABLED)

# Function for microphone animation during listening   
def mic_animation():
    mic_icon = Image.open("mic_animation.gif")  # Load the animated GIF
    mic_icon = ImageTk.PhotoImage(mic_icon)
    mic_label.config(image=mic_icon)
    mic_label.image = mic_icon
    root.after(200, mic_animation)

# Frame for the animated mic display (if needed)
mic_label = tk.Label(root, bg="#212121")
mic_label.pack(pady=10) 

# Function to create a circular image
def create_circular_image(image_path, size=(120, 120)):
    # Open the image
    img = Image.open(r"C:/Users/YASHASWI/Desktop/voice_assistant-master (3)/voice_assistant-master/mic_img.jpg")
    
    # Resize the image to fit into a square
    img = img.resize(size)

    # Create a circular mask
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)

    # Apply the mask to the image
    img.putalpha(mask)

    return ImageTk.PhotoImage(img)

# Create Circular Microphone Button with a circular image
mic_icon = create_circular_image(r"C:/Users/YASHASWI/Desktop/voice_assistant-master (3)/voice_assistant-master/mic_img.gif")  
mic_button = tk.Button(root, image=mic_icon, relief="flat", command=start_assistant, bg="#4CAF50", bd=0, width=120, height=120)
mic_button.pack(pady=30) 

# Create Buttons (Stop, Clear)
stop_button = tk.Button(root, text="Stop Assistant", width=20, font=("Arial", 12, "bold"), bg="#F44336", fg="white", relief="flat", command=root.quit)
stop_button.pack(pady=5)

clear_button = tk.Button(root, text="Clear Output", width=20, font=("Arial", 12, "bold"), bg="#2196F3", fg="white", relief="flat", command=clear_text)
clear_button.pack(pady=5)

# Animation function for the microphone button (pulse effect)
def mic_button_pulse():
    # Scale the mic button larger and then return to normal size
    mic_button.config(width=140, height=140)  # Expand button
    root.after(100, lambda: mic_button.config(width=120, height=120))  # Return to original size
    root.after(200, lambda: mic_button.config(width=140, height=140))  # Expand again
    root.after(300, lambda: mic_button.config(width=120, height=120))  # Return to original size
    root.after(400, lambda: mic_button.config(width=120, height=120))  # Ensure button is normal after animation

# Call the pulse effect when the microphone button is clicked
def start_assistant_with_pulse():
    mic_button_pulse()  # Trigger the pulse animation
    start_assistant()  # Start the assistant

# Set the command for the microphone button with animation
mic_button.config(command=start_assistant_with_pulse)

# Create a Floating Animation for Buttons
def button_animation():
    stop_button.config(bg="#F44336", relief="raised")
    stop_button.after(100, lambda: stop_button.config(bg="#D32F2F", relief="flat"))
    clear_button.config(bg="#2196F3", relief="raised")
    clear_button.after(100, lambda: clear_button.config(bg="#1976D2", relief="flat"))

# Periodic animation updates
def update_animations():
    button_animation()
    root.after(1000, update_animations)

update_animations()  # Start animations

# Run the GUI
root.mainloop()
