import requests
import wave

print("Введите полное имя файла с расширением для озвучивания:")
filename = input()
name = filename[:filename.rfind('.')]

file = open(filename, "r")


key = "be5f4c47488e4d349dbb06b527492c7c"
region = "francecentral"
auth_url = "https://francecentral.api.cognitive.microsoft.com/sts/v1.0/issueToken"
voice_url = "https://francecentral.tts.speech.microsoft.com/cognitiveservices/v1"
auth_headers = { "Ocp-Apim-Subscription-Key": key, "Content-Length": "0", "Content-type": "application/x-www-form-urlencoded" }

# get token
auth_response = requests.post(auth_url, headers=auth_headers)
token = auth_response.text

#make ssml
ssml_string = '<speak version="1.0" xml:lang="en-US">  <voice xml:lang="en-US" xml-gender="Female" name="en-US-ZiraRUS">' + str(file.read()) + "</voice></speak>"

# get wav-type content
voice_headers = {"Authorization" : "Bearer " + token, "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm", "Content-Type": "application/ssml+xml", "User-Agent": "USER-AGENT"}
voice_response = requests.post(voice_url, data=ssml_string, headers=voice_headers)

#make audiofile
audiofile_name = str(name) + ".wav"
wav_file = wave.open(audiofile_name, "w")
nchannels = 1
sampwidth = 2
framerate = 24000
nframes = None
comptype = "NONE"
compname = "not compressed"

wav_file.setparams((nchannels, sampwidth, framerate, nframes,
    comptype, compname))

wav_file.writeframes(voice_response.content)

wav_file.close()

w = wave.open(audiofile_name, "r")
f = w.getnframes()
r = w.getframerate()
duration = f / float(r)
file = open(filename, "r").read()
print("Длительность символа в секундах = " + str(duration / len(file)))

