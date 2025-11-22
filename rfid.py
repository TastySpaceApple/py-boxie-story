from mfrc522 import SimpleMFRC522
import boxie
import time
import RPi.GPIO as GPIO
reader = SimpleMFRC522()

character = "cat"
rfidText = "בית קפה"

texts = {
  584189665081: "בית קפה"
  584189665080: "גן"
  584189665079: "בריכה"
  584189665078: "יער"
}

lastID = None

try:
  while True:
    print("Place your RFID tag near the reader...")
    id, _ = reader.read()
    if id != lastID:
      lastID = id
      if(id == None):
        continue
      user_message = texts.get(id, "לא ידוע")
      print(f"RFID Tag Detected. ID: {id}, Text: {user_message}")
      boxie_reply = boxie.talk(character, user_message)
    print(f"ID: {id}")
    print(f"Text: {text}")
    time.sleep(1)
finally:
  GPIO.cleanup()