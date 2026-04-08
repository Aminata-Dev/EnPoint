IPA stands for [International Phonetic Transcription](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet)

# Enhancements



  



## Live speech-to-text enhancements

- ~~silence detection : wait for silence to stop, not seconds~~
- ~~Rename STT to live STT~~
- add TTS to compare a phrase I say to a correct pronunciation. Mistral AI V. (march 2026) or EvenLabs. TTS live (comparaison) or variable -> audio (if I can't pronounce the phrase correctly yet)
- Live STT needs to return the result so I can compare it to a test word and send a congrats if it corresponds
- Freestyle mode : I get the IPA of the words I say
- Enhance responsiveness of the speech-to-text system ?
    - Overlapping windows: Record continuously and transcribe overlapping 2-second segments
    - Parallel processing: Record in one thread, transcribe in another
- Think of a dashboard division : pronunciation specific page ?

## Application

- UI : Generate a JavaScript/TypeScript web app. What I need :
  - Aesethics
  - Embedded Youtube videos
    - YouGlish pronunciation videos embedded 
    - If IPA clicked, youtube videos of each phonem. [example video 1](https://www.youtube.com/watch?v=b_XMthn4iUc) or [example video 2](https://www.youtube.com/watch?v=KwDJnXt3ZVQ)
  - Separation of information / page subdivision
    - If IPA is clicked
      - Each phonem is clickable a provide the audio, as in a Cambridge Dictionary Pronunciation page ([example pronunciation page](https://dictionary.cambridge.org/pronunciation/english/uncharted))
  - Save to .png button
  - Considered technologies : React (Python Fast API), Tailwind CSS + Shadcn/ui ...
- Use a second laptop or raspberry pi to run a server for my app (generate dashbord, record word in database, save .png dashboard, log, ...)

## Scraper

# History

- try multiple model on faster-api
- class creation -fetcher- because the scraping needed the same user-agent and type of verification about requests (see politcy) -> a class was better adapted to get multiple infos around a same word 
- Add main_application_ipynb which simulates the application to test different modules in a same place
- Add a youglish link fetcher on the fetcher class
- Add a show method to the fetcher. Will be all the infos on the UI
- Silence detection

- Add a readme and make the repo public


## Reflexions on information source for definitions, examples, british english phonectic transcription

### Wikitionary WebScraper

- wikitionary webscraper : use API according to policy but the endpoints doesn't provide all informations needed (International Phonetic Transcription). Therefore I'll use bs4 to scrape infos I need. On my "Observatoire du mot" model (previous project)
- 
- improve wikitionary scraper
  - handle case where the word doesn't exist
  - in the end, every function will be called in the init() method so that we can retreive info by fetcher_for_audio.pronunciation or .definition. If it's a good pratice.
  - 
- Here is the DOM for audio pronunciation on Wikitionary
<audio id="mwe_player_0_html5_api" preload="metadata" data-mw-tmh="" class="vjs-tech" style="width:175px;" data-durationhint="2" data-mwtitle="en-us-audio.ogg" data-mwprovider="wikimediacommons" playsinline="playsinline" tabindex="-1" src="//upload.wikimedia.org/wikipedia/commons/0/0c/En-us-audio.ogg"><source src="//upload.wikimedia.org/wikipedia/commons/0/0c/En-us-audio.ogg" type="audio/ogg; codecs=&quot;vorbis&quot;" data-width="0" data-height="0"><source src="//upload.wikimedia.org/wikipedia/commons/transcoded/0/0c/En-us-audio.ogg/En-us-audio.ogg.mp3" type="audio/mpeg" data-transcodekey="mp3" data-width="0" data-height="0"></audio>

Could use https://freedictionaryapi.com/ too.

Problem : Wikitionary doesn't provide all the information required for the project -example : IPA for british pronunciation-

## Cambridge Dictionary

- From Wikitionary web scraper to Cambridge Dictionary web scraper.
~~- Include phrasal verbs~~

# Others

- Create a Oxford Dictionary python library bc (1) no repo on Github (2) personal preferences for their definitions
- WordReference has more sounds. Check if WordReference have an API or if it is scrapable ?