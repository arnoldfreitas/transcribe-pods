import os
from pprint import pprint
# Specifically MP3 file
from mutagen.mp3 import MP3
from transformers import AutoProcessor, AutoModelForPreTraining
import torch
import numpy as np
import torchaudio
from transformers import pipeline

# import matplotlib.pyplot as plt
from torchaudio.io import StreamReader

token  = os.getenv("HFTOKEN", default = None)
file_path = os.path.abspath(os.path.join(__file__, ".."))

def load_model(model_name = "facebook/wav2vec2-large-xlsr-53-portuguese"):
    processor = AutoProcessor.from_pretrained(model_name, token=token)
    model = AutoModelForPreTraining.from_pretrained(model_name, token=token)

    return processor, model

def run_model(processor, model, audio):
    inputs = processor(audio, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)
        pprint(outputs)

def stream_audio(audio_path):
    waveform_generator = miniaudio.stream_file(
        filename = audio_path)
    tmp = []
    for waveform in waveform_generator:
        #do something with the waveform....
        tmp.extend(waveform.tolist())
    return np.array(tmp, dtype=float)

def play_audio_example(audio_path):
    target_sampling_rate = 44100  #the input audio will be resampled a this sampling rate
    n_channels = 1  #either 1 or 2
    waveform_duration = 30 #in seconds
    offset = 15 #this means that we read only in the interval [15s, duration of file]

    waveform_generator = miniaudio.stream_file(
        filename = audio_path)

        # sample_rate = target_sampling_rate,
        # seek_frame = int(offset * target_sampling_rate),
        # frames_to_read = int(waveform_duration * target_sampling_rate),
        # output_format = miniaudio.SampleFormat.FLOAT32,
        # nchannels = n_channels)
    
    # with miniaudio.PlaybackDevice() as device:
    #     device.start(waveform_generator)

if __name__=="__main__":
    audio_path = f'{file_path}/../data/fronteiras_20_africa_do_sul.mp3'
    # play_audio_example(audio_path)
    print(audio_path)

    # info = MP3(audio_path).info# Load model directly
    # sample_rate = info.sample_rate
    # bitrate = info.bitrate
    # length = info.length
    # channels = info.channels

    pipe = pipeline(model="facebook/wav2vec2-large-xlsr-53-portuguese")
    output = pipe(audio_path, chunk_length_s=10)
    pprint(output)
    # audio = stream_audio(audio_path)
    # pprint(audio.dtype)
    # pprint(audio.shape)
    # processor, model =  load_model()
    # run_model(processor, model, audio)