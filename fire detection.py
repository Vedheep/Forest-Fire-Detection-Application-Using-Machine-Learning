
   import cv2  # Library for OpenCV
import threading  # Library for threading
import pygame  # Library for playing sound
import smtplib  # Library for email sending

# Initialize Pygame mixer for sound playback
pygame.mixer.init()

# Load the fire detection cascade model
fire_cascade = cv2.CascadeClassifier('fire_detection_cascade_model.xml')

# Start the camera (0 for built-in, 1 for external)
vid = cv2.VideoCapture(0)
runOnce = False  # Boolean to track if the alarm has already been triggered

def play_alarm_sound_function(): 
    """Play the fire alarm sound."""
    pygame.mixer.music.load('fire_alarm.mp3')  # Load the alarm sound file
    pygame.mixer.music.play()  # Play the sound
    print("Fire alarm ended")  # Log to console

def send_mail_function(): 
    """Send an email alert about fire detection."""
    recipient_mail = "vtu20994@veltech.edu.in"  # Recipient's email
    recipient_mail = recipient_mail.lower()  # Convert to lowercase
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("vtu21020@veltech.edu.in", 'Sain9490757316..')  # Sender's email and password
        server.sendmail('vtu21020@veltech.edu.in', recipient_mail, "Warning: fire accident has been reported")  # Send email
        print("Alert mail sent successfully to {}".format(recipient_mail))  # Log to console
        server.close()  # Close server
        
    except Exception as e:
        print(f"Error sending email: {e}")  # Print error if any

while True:
    ret, frame = vid.read()  # Read video frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert frame to gray scale
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5)  # Detect fire

    # Highlight detected fire with a rectangle
    for (x, y, w, h) in fire:
        cv2.rectangle(frame, (x-20, y-20), (x+w+20, y+h+20), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        print("Fire alarm initiated")
        threading.Thread(target=play_alarm_sound_function).start()  # Start the alarm thread

        if not runOnce:
            print("Email send initiated")
            threading.Thread(target=send_mail_function).start()  # Start the email thread
            runOnce = True  # Set the flag to True

    cv2.imshow('Fire Detection', frame)  # Show the video frame with detection
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit on 'q' key
        break

# Release resources
vid.release()
cv2.destroyAllWindows()
