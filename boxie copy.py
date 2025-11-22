import simpleaudio as sa
import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig
from characters import characters
from google.cloud import texttospeech

load_dotenv()

# Initialize Gemini API
genai = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

prompt_base = [
"אתה דמות מסיפור ילדים לגילאי 3-7.",
"אתה מדבר בעברית פשוטה שמתאימה לילדים קטנים.",
"אתה מדבר בזמן הווה, כאילו הדברים קורים כרגע.",
"אתה מתאר את הסביבה שלך בצורה חיה וסיפורית.",
"אתה מפרט את הרגשות שלך.",
"אתה לא משתמש באימוג'ים.",
"אתה מקבל שמות של מקומות ואתה מייצר סיפור על איך אתה חווה אותם.",
"ללא סימני קריאה, אתה מדבר רגוע ופשוט.",
"דוגמאות לרגשות: שמח, עצוב, סקרן, מפוחד, נרגש, מתוסכל, מופתע, רגוע, מגעיל. אתה מחפש את הרגש הכי מתאים ומדויק למצב.",
"כשאתה מגיע למקום מסוים, אתה מסתכל עליו ואומר מה אתה רואה בצורה סיפורית, ואז אתה אומר איך אתה מרגיש לגבי זה."
]

def create_history_prompt(history):
  history_prompt = ""
  for exchange in history:
    history_prompt += f'הגעת לכאן: "{exchange["user"]}"\nתגובה: "{exchange["bot"]}"\n'
  return history_prompt

def get_boxie_response(character, user_message, history=None):
  if history is None:
    history = []
  character_story = characters[character]["characterStory"]
  history_of_examples = characters[character]["historyOfExamples"]
  full_prompt = (
    f'{create_history_prompt(history_of_examples)}'
    f'{create_history_prompt(history)}'
    f'הגעת לכאן: "{user_message}"\nתגובה:'
  )
  response = genai.models.generate_content(
    model="gemini-2.5-pro",
    contents=full_prompt,
    config=GenerateContentConfig(
      system_instruction=[
        "\n".join(prompt_base),
        "\n".join(character_story)
      ]
    )
  )
  return response.text

def tts_generate_speech(text, output_file):
  response = genai.models.generate_speech(
    model="gemini-2.5-pro-speech",
    text=text,
    config={
      "voice": "he-IL-Wavenet-A",
      "audioEncoding": "MP3"
    }
  )

  with open(output_file, "wb") as f:
    f.write(response.audio_content)
  print(f"Audio content written to file {output_file}")
  return output_file

def play_wav(file_path):
  wave_obj = sa.WaveObject.from_wave_file(file_path)
  play_obj = wave_obj.play()
  play_obj.wait_done()  # Wait until sound has finished playing

def talk(character, user_message, history=None):
  boxie_reply = get_boxie_response(character, user_message, history)
  print("Boxie:", boxie_reply)
  audio_file = tts_generate_speech(boxie_reply, "boxie_response.mp3")
  play_wav(audio_file)
  return boxie_reply