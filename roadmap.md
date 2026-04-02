# Next step

- Rename STT to live STT
- Here is the DOM for audio pronunciation on Wikitionary
<audio id="mwe_player_0_html5_api" preload="metadata" data-mw-tmh="" class="vjs-tech" style="width:175px;" data-durationhint="2" data-mwtitle="en-us-audio.ogg" data-mwprovider="wikimediacommons" playsinline="playsinline" tabindex="-1" src="//upload.wikimedia.org/wikipedia/commons/0/0c/En-us-audio.ogg"><source src="//upload.wikimedia.org/wikipedia/commons/0/0c/En-us-audio.ogg" type="audio/ogg; codecs=&quot;vorbis&quot;" data-width="0" data-height="0"><source src="//upload.wikimedia.org/wikipedia/commons/transcoded/0/0c/En-us-audio.ogg/En-us-audio.ogg.mp3" type="audio/mpeg" data-transcodekey="mp3" data-width="0" data-height="0"></audio>
- WordReference has more sounds. Check if WordReference have an API or if it is scrapable
- Live STT needs to return the result so I can  compare it to the test word and send a congrats if it corresponds
- improve wikitionary scraper
  - handle case where the word doesn't exist
  - in then end, every function will be called in the init() method so that we can retreive info by fetcher_for_audio.pronunciation or .definition
- UI (JavaScript/TypeScript ? Streamlit ?)
  - Link to YouGlish page of the words (the video will be embedded to the UI if possible)

## Speech-to-text improvement

- I should wait for silence to stop, not seconds
- Enhance responsiveness of the speech-to-text system :
    - Overlapping windows: Record continuously and transcribe overlapping 2-second segments
    - Real-time streaming: Use a different library like speech_recognition with Google API (faster but less accurate)
    - Parallel processing: Record in one thread, transcribe in another
- Listen to : either my microphone, either my laptop

# Word test

- "Audio"

# History

- try multiple model on faster-api
- class creation -fetcher- because the scraping needed the same user-agent and type of verification about requests (see politcy) -> a class was better adapted to get multiple infos around a same word 
- test : use API according to policy but the endpoints doesn't provide all informations needed (International Phonetic Transcription). Therefore I'll use bs4 to scrape infos I need. On my "Observatoire du mot" model (previous project)
- Feat : Fetcher class : IPA works
- Add main_application_ipynb which simulates the application to test different modules together
- Add a youglish link fetcher on the fetcher class
- Add a show method to the fetcher. Will be all the infos on the UI