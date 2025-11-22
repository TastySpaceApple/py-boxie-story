import time
import sys
import mfrc522

def write_to_rfid(data):
  reader = mfrc522.SimpleMFRC522()
  print("Place your RFID tag near the reader...")
  try:
    reader.write(data)
    print(f"Written '{data}' to RFID tag.")
  except Exception as e:
    print(f"Error writing to RFID tag: {e}")

if __name__ == "__main__":
  write_to_rfid("בית קפה")