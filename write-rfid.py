import time
import sys
import mfrc522

try:
except ImportError:
  print("MFRC522 library not found. Please install it for RFID support.")
  sys.exit(1)

def write_to_rfid(data):
  reader = mfrc522.SimpleMFRC522()
  print("Place your RFID tag near the reader...")
  try:
    reader.write(data)
    print(f"Written '{data}' to RFID tag.")
  except Exception as e:
    print(f"Error writing to RFID tag: {e}")
  finally:
    reader.cleanup()

if __name__ == "__main__":
  write_to_rfid("בית קפה")