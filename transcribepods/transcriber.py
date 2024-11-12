import os
from pprint import pprint

from mutagen.mp3 import MP3
import torch
import numpy as np
import torchaudio
from transformers import pipeline

# from transformers import AutoProcessor, AutoModelForPreTraining
# import matplotlib.pyplot as plt
# from torchaudio.io import StreamReader

from utils import load_from_json, save_to_json


hf_token  = os.getenv("HFTOKEN", default = None)
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

    def load_pipeline(self):
        self.pipe = pipeline(model=self.model_name)

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
            data[self.podcast] = {ep_name : output}
        
        save_to_json(data, info="phase1")


if __name__=="__main__":
    transcriber = AudioTranscriber()
    transcriber.load_pipeline()
    transcriber()

