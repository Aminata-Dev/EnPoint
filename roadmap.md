# Next step

- fuctional wikitionary scraper (get IPA transcription) based on bs4 (cf Obervatoire du mot project)
- UI (JavaScript/TypeScript ? Streamlit ?)
  - Link to YouGlish page of the words (the video will be embedded to the UI if possible)

# Speech-to-text improvement

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