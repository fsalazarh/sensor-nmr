from recordering.audio_retriever import AudioRetriever

a = AudioRetriever(True)
a.is_recorder_device_ready()

for i in range(0,200):
    a.retrieve_audio()
