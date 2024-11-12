import os
from pprint import pprint

from mutagen.mp3 import MP3
import torch
import numpy as np
import torchaudio
from transformers import pipeline
from openai import OpenAI
from dotenv import load_dotenv


from nltk import tokenize
import tiktoken

# from transformers import AutoProcessor, AutoModelForPreTraining
# import matplotlib.pyplot as plt
# from torchaudio.io import StreamReader

from utils import load_from_json, save_to_json

load_dotenv(os.path.abspath(os.path.join(__file__, "../../.env")))

HFTOKEN  = os.getenv("HFTOKEN", default = None)
OPENAI_ORG  = os.getenv("OPENAI_ORG", default = None)
OPENAI_PROJ  = os.getenv("OPENAI_PROJ", default = None)
file_path = os.path.abspath(os.path.join(__file__, ".."))
data_folder_path = os.path.abspath(os.path.join(__file__, "./../../data"))


class AudioTranscriber():
    def __init__(self,
                 model_name = "facebook/wav2vec2-large-xlsr-53-portuguese",
                 podcast = "fronteiras_invisiveis",
                 ) -> None:
        # processor = AutoProcessor.from_pretrained(model_name, token=token)
        # model = AutoModelForPreTraining.from_pretrained(model_name, token=token)
        self.podcast = podcast
        self.podcast_folder = f"{data_folder_path}/{self.podcast}"
        self.model_name = model_name

        self.pipe = None
        self.sample_rate = None
        self.bitrate = None
        self.length = None
        self.channels = None
        self.openai_client = None
        self.openai_model = None

    def load_pipeline(self):
        self.pipe = pipeline(model=self.model_name)

    def init_openai_client(self,
                           model="gpt-4o-mini"):
        self.openai_client = OpenAI(
            organization=OPENAI_ORG,
            project=OPENAI_PROJ,)
        self.openai_model = model


    def get_audio_metadata(self, audio_path):
        info = MP3(audio_path).info # Load model directly
        self.sample_rate = info.sample_rate
        self.bitrate = info.bitrate
        self.length = info.length
        self.channels = info.channels

    def load_audio_from_folder(self):
        for item in os.listdir(f"{data_folder_path}/{self.podcast}"):
            pprint(item)
    
    def __call__(self, *args, **kwds):
        # tmp =  kwds["tmp"]
        data = {self.podcast : {}}
        for ep_name in os.listdir(self.podcast_folder):
            audio = os.path.abspath(os.path.join(self.podcast_folder, ep_name))
            pprint(f"Transcribing Audio: {audio}")
            self.get_audio_metadata(audio)
            output = self.pipe(audio, chunk_length_s=20, stride_length_s=3)
            ep_name = ep_name.replace(".mp3", "")
            data[self.podcast] = {ep_name : output}
        
        save_to_json(data, info="phase1")


    def prep_text_tolkenizer(self,
                             corpus,
                             max_tokens = 8172):

        # Split text into sentences or paragraphs
        sentences = tokenize.sent_tokenize(corpus, language="portuguese")  # For sentences
        encoding = tiktoken.encoding_for_model(self.openai_model)
        # Ensure each chunk is within token limits
        chunks = []
        current_chunk = ""
        for sentence in sentences:
            # Check if adding the sentence would exceed the token limit
            if len(encoding.encode(current_chunk + sentence)) > max_tokens:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += " " + sentence

        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks, len(encoding.encode(current_chunk))

    def clear_text_with_gpt(self, chunks, ep_name="episode"):
        corrected_chunks = []
        for chunk in chunks:
            response = self.openai_client.chat.completions.create(
                model=self.openai_model,  # Replace with your model
                messages=[
                    {"role": "system", "content": "Você é um assistente altamente capacitado, especializado na língua portuguesa (pt-BR). Sua tarefa é revisar a transcrição de um podcast de notícias, corrigindo erros de gramática, ortografia e pontuação. Além disso, você deve melhorar a estrutura do texto, garantindo que ele esteja claro, coeso e adequado ao português do Brasil. Preserve o significado e o tom original do podcast enquanto realiza as correções."},
                    {"role": "user", "content": chunk}
                ],
                # max_tokens=8172  # Adjust based on your output size and model limits
            )
            corrected_chunks.append(response['choices'][0]['message']['content'])
        
        
        data = {self.podcast : {}}
        data[self.podcast] = {ep_name : corrected_chunks}
        
        save_to_json(data, info="phase2")
        return corrected_chunks

def transcribe_phase1():
    transcriber = AudioTranscriber()
    transcriber.load_pipeline()
    transcriber()

def transcribe_phase2():
    data = load_from_json("phase1")
    pprint(data["fronteiras_invisiveis"]["fronteiras_20_africa_do_sul"]["text"][:200])

    transcriber = AudioTranscriber()
    transcriber.init_openai_client()
    chunks, n_tokens = transcriber.prep_text_tolkenizer(
        data["fronteiras_invisiveis"]["fronteiras_20_africa_do_sul"]["text"])

    completion = transcriber.clear_text_with_gpt(
        chunks,
        ep_name="fronteiras_20_africa_do_sul")
    pprint(completion)

if __name__=="__main__":
    transcribe_phase2()


