from mfrc522 import SimpleMFRC522
import boxie
import RPi.GPIO as GPIO
reader = SimpleMFRC522()

character = "cat"
rfidText = "בית קפה"

lastID = None

try:
  while True:
    print("Place your RFID tag near the reader...")
    id, text = reader.read()
    if id != lastID:
      lastID = id
      print(f"RFID tag detected with ID: {id} and text: {text}")
      user_message = text.strip()
      boxie_reply = boxie.talk(character, user_message)
    print(f"ID: {id}")
    print(f"Text: {text}")
finally:
  GPIO.cleanup()