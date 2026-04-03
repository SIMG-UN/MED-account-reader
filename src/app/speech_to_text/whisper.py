import os
import json
from settings import OUTPUT_PATH, INPUT_PATH

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize the Groq client
client = Groq()

# Specify the path to the audio file
filename = os.path.dirname(__file__) + INPUT_PATH + "/sample_audio.m4a" # Replace with your audio file!

# Open the audio file
with open(filename, "rb") as file:
    # Create a transcription of the audio file
    transcription = client.audio.transcriptions.create(
      file=file, # Required audio file
      model="whisper-large-v3-turbo", # Required model to use for transcription
      response_format="verbose_json",  # Optional
      timestamp_granularities = ["segment"], # Optional (must set response_format to "json" to use and can specify "word", "segment" (default), or both)
      language="es",  # Optional
      temperature=0.0  # Optional
    )
    # To print only the transcription text, you'd use print(transcription.text) (here we're printing the entire transcription object to access timestamps)
    # print(json.dumps(transcription, indent=2, default=str))

output_path = os.path.dirname(__file__) + OUTPUT_PATH + "\\transcription.txt" # Replace with your audio file!

with open(output_path, "w", encoding='utf-8') as file:
    file.write(transcription.text)