from flask import Flask,abort,jsonify,request
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from transformers import pipeline
from pytube import YouTube
from google.cloud import speech





# define a variable to hold you app
app = Flask(__name__)

# define your resource endpoints
destination="audio"


@app.route('/summarize/',methods=['GET'])
def summarize():
    url = request.args.get('url', '')
    #video_id = url.split('=')[1]    
    #summary=get_video_transcript(video_id)
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio = True).first()
    client=speech.SpeechClient.from_service_account_file('key.json')
    audio_file=speech.RecognitionAudio(content=audio_stream)

    config=speech.RecognitionConfig(
    sample_rate_hertz=44100,
    enable_automatic_punctuation=True,
    language_code='en-US')

    response=client.recognise(
    config=config,
    audio=audio_file

)
    summary=''
    for result in response.results:
        #print(result.alternatives[0].transcript)
        summary+=abstract_summarization(result.alternatives[0].transcript)
    #yt.download(output_path=destination)
    return summary,200
#https://www.youtube.com/watch?v=FaC3fOD9gYs
  
# def get_video_transcript(video_id):
#     #transcript = YouTubeTranscriptApi.get_transcript(video_id)
#     formatter = TextFormatter()
#     transcript = YouTubeTranscriptApi.get_transcript(video_id)
#     formatted_text = formatter.format_transcript(transcript).replace("\n", " ")
#     return abstract_summarization(formatted_text)

def abstract_summarization(text):
    summarization = pipeline("summarization")
    summarized_text = summarization(text)[0]['summary_text']
    return summarized_text


# server the app when this file is run
if __name__ == '__main__':
    #get_video_transcript('Rnwwo9Zol6w')
    app.run(debug=True)