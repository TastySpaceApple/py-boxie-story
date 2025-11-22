import os
from dotenv import load_dotenv
from openai import OpenAI
from openai.helpers import LocalAudioPlayer

from characters import characters

load_dotenv()

client = OpenAI()


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
  messages = []
  for exchange in history:
    messages.append({
      "role": "user",
      "content": exchange["user"]
    })
    messages.append({
      "role": "assistant",
      "content": exchange["bot"]
    })
  return messages

def get_boxie_response(character, user_message, history=None):
  if history is None:
    history = []
  character_story = characters[character]["characterStory"]
  history_of_examples = characters[character]["historyOfExamples"]
  completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {
        "role": "developer", 
        "content": "\n".join(prompt_base) + "\n" + "\n".join(character_story)
      },
      *create_history_prompt(history_of_examples),
      *create_history_prompt(history),
      {
        "role": "user",
        "content": user_message
      }
    ],
  )

  return completion.choices[0].message.content


def tts_generate_speech(character, text, output_file):
  with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="coral",
    input=text,
    instructions="Speak in a cheerful and positive tone like a character from a children's storybook. " + characters[character]["characterVoice"],
    response_format="wav"
  ) as response:
    response.stream_to_file(output_file)

  print(f"Audio content written to file {output_file}")
  return output_file

def play_wav(file_path_wav, method="aplay"):
  if method == "aplay":
    os.system(f'aplay {file_path_wav}')
  else:
    LocalAudioPlayer.play(file_path_wav)

def talk(character, user_message, history=None):
  boxie_reply = get_boxie_response(character, user_message, history)
  print("Boxie:", boxie_reply)
  audio_file = tts_generate_speech(character, boxie_reply, "boxie_response.wav")
  play_wav(audio_file)
  return boxie_reply