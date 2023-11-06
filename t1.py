from google.cloud import speech_v1p1beta1
from google.protobuf.json_format import MessageToJson
from google.cloud.speech_v1p1beta1 import enums
import io
import os
import json
from SpeakerIdentification import test_model


globalduration = list()
def checkvoice(start_time,end_time,filepath):
    from pydub import AudioSegment
    t1 = start_time #Works in milliseconds
    t2 = end_time
    newAudio = AudioSegment.from_wav(filepath)
    newAudio = newAudio[t1:t2]
    
    newAudio.export('C:/Users/nitin/Documents/Radio_EY/testing_set/newSong.wav', format="wav")
    return test_model()
def sample_long_running_recognize(local_file_path):
    """
    Print confidence level for individual words in a transcription of a short audio
    file
    Separating different speakers in an audio file recording

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'nitinapi.json'
    client = speech_v1p1beta1.SpeechClient()

    # local_file_path = 'resources/commercial_mono.wav'
     #It was giving me this error before: Must use single channel (mono) audio, but WAV header indicates 2 channels.
    audio_channel_count = 1
    '''
    # The use case of the audio, e.g. PHONE_CALL, DISCUSSION, PRESENTATION, et al.
    interaction_type = enums.RecognitionMetadata.InteractionType.VOICE_SEARCH

    # The kind of device used to capture the audio
    recording_device_type = enums.RecognitionMetadata.RecordingDeviceType.SMARTPHONE
    
    metadata = {
        "interaction_type": interaction_type,
        "recording_device_type": recording_device_type,
        
    }
    '''
    # If enabled, each word in the first alternative of each result will be
    # tagged with a speaker tag to identify the speaker.
    enable_speaker_diarization = True

    # Optional. Specifies the estimated number of speakers in the conversation.
    diarization_speaker_count = 3

    # When enabled, the first result returned by the API will include a list
    # of words and the start and end time offsets (timestamps) for those words.
    enable_word_time_offsets = True

    # The language of the supplied audio
    language_code = "en-IN"

    # The use case of the audio, e.g. PHONE_CALL, DISCUSSION, PRESENTATION, et al.
    interaction_type = enums.RecognitionMetadata.InteractionType.VOICE_SEARCH

    # The kind of device used to capture the audio
    recording_device_type = enums.RecognitionMetadata.RecordingDeviceType.SMARTPHONE
    microphone_distance =  enums.RecognitionMetadata.MicrophoneDistance.NEARFIELD

    # The device used to make the recording.
    # Arbitrary string, e.g. 'Pixel XL', 'VoIP', 'Cardioid Microphone', or other
    # value.
    
    metadata = {
        "interaction_type": interaction_type,
        "recording_device_type": recording_device_type,
        "microphone_distance" : microphone_distance,
        
    }

    config = {
        "enable_speaker_diarization": enable_speaker_diarization,
        "diarization_speaker_count": diarization_speaker_count,
        "language_code": language_code,
        "audio_channel_count": audio_channel_count,
        "model": "default",
        "enable_word_time_offsets": enable_word_time_offsets,
        
        

        
    }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()
    change = True
    duration =[]
    transcripts=[]
    preend = 0
    for result in response.results:
        # First alternative has words tagged with speakers
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))
        transcripts.append(alternative.transcript)
        # Print the speaker_tag of each word
        for word in alternative.words:
            #print(u"Word: {}".format(word.word))
            #print(u"Speaker tag: {}".format(word.speaker_tag))
            
            #print(u"start time: {} seconds {} nanos".format(word.start_time.seconds, word.start_time.nanos) )

            #print(u"End time: {} seconds {} nanos".format(word.end_time.seconds, word.end_time.nanos) )
            
            if change:
                pre_endsec = word.end_time.seconds
                pre_endnano = word.end_time.nanos
                pre_strtsec = word.start_time.seconds
                pre_strtnano = word.start_time.nanos
                pre_endnano = pre_strtsec
                pre_tag = word.speaker_tag
                change = False
                
            if word.start_time.nanos ==  pre_endnano:            
                pre_endnano = word.end_time.nanos
                pre_endsec = word.end_time.seconds
                pre_tag = word.speaker_tag
                
            else:
                
                duration.append([pre_tag,pre_strtsec,pre_strtnano,pre_endsec,pre_endnano])
                pre_endsec=0
                pre_endnano=0
                pre_tag = 0
                pre_strtsec = word.start_time.seconds
                pre_strtnano = word.start_time.nanos
                pre_endsec = word.end_time.seconds
                pre_endnano = word.end_time.nanos
                pre_tag = word.speaker_tag
    if pre_strtsec > preend:
        duration.append([pre_tag,pre_strtsec,pre_strtnano,pre_endsec,pre_endnano])
        preend = pre_endsec
    print(duration)
    
    global globalduration
    globalduration = duration

    '''
    print(duration)

    voices=[]
    for arr in duration:
        st= arr[1]*1000 + arr[2]/1000000
        et= arr[3]*1000 + arr[4]/1000000
        voices.append(checkvoice(st,et,local_file_path))
    print(voices)
    '''
    print(transcripts)
    return transcripts
def get_duration():
    return globalduration

"""
if __name__ == "__main__":
"""
def get_transcript():

    return sample_long_running_recognize("tv1.wav")
get_transcript()