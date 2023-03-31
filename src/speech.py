# from transformers import WhisperProcessor, WhisperForConditionalGeneration
# import librosa


# class SpeechEngine:

#     def __init__(self):

#         self.processor = WhisperProcessor.from_pretrained('openai/whisper-medium.en')
#         self.model = WhisperForConditionalGeneration.from_pretrained('openai/whisper-medium.en')

#     def process(self, filepath: str) -> str:

#         data, sample_rate = librosa.load(filepath, sr=16000)
#         input_features = self.processor(data, sampling_rate=sample_rate, return_tensors='pt').input_features
#         predicted_ids = self.model.generate(input_features)

#         return self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

import openai
from pydub import AudioSegment


class SpeechEngine:

    def __init__(self):

        pass

    def process(self, filepath: str) -> str:

        new_filepath = filepath.split('.')[0] + '.mp3'
        audio_file = AudioSegment.from_file(filepath).export(new_filepath, format="mp3")
        response = openai.Audio.transcribe("whisper-1", audio_file)

        return response['text']
