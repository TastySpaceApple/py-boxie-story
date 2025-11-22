from mfrc522 import SimpleMFRC522
import boxie
import RPi.GPIO as GPIO
reader = SimpleMFRC522()

character = "cat"
rfidText = "בית קפה"

try:
  while True:
    print("Place your RFID tag near the reader...")
    id, text = reader.read()
    boxie_reply = boxie.talk(character, rfidText)
    print("Boxie:", boxie_reply)
    print(f"ID: {id}")
    print(f"Text: {text}")
finally:
  GPIO.cleanup()