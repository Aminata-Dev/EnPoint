import time
import requests
from bs4 import BeautifulSoup

# Header compliant with Wikimedia User-Agent policy
headers = {
    "User-Agent": "EnPoint/1.0 (Aminata-Dev on Github) [python3.13/requests]"
}

class WordInfoFetcher:
    """
    Class to retrieve word information from Wiktionary,
    respecting rate limits for unauthenticated requests:
    - Below 5 requests per second overall
    """
    
    def __init__(self, word):
        self.word = word.lower()  # Normalize the word to lowercase
        self.last_request_time = 0  # Timestamp of the last request
        self.word_infos = self.get_word_info()  # To store the retrieved data for later use
        self.pronunciation = self.get_pronunciation() # good pratice ?
    
    def _wait_for_rate_limit(self):
        """Wait if necessary to respect the rate of 5 req/sec"""
        now = time.time()
        time_since_last = now - self.last_request_time
        if time_since_last < 0.2:  # 1/5 = 0.2 seconds minimum between requests -> https://wikitech.wikimedia.org/wiki/Robot_policy#REST_API_rules
            time.sleep(0.2 - time_since_last)
        self.last_request_time = time.time()
    
    def get_word_info(self):
        """
        Retrieve information about a word from Wiktionary.
        Returns JSON data or None on error.
        """
        self._wait_for_rate_limit()
        url = f"https://en.wiktionary.org/wiki/{self.word}"
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        
        return soup
        
    def get_pronunciation(self):
        """
        Wikitionary : IPA transcription retrieval
        """

        #model
        #<span class="IPA nowrap">/ˈɔː.di.əʊ/</span>
  
        for span in self.word_infos.find("span", class_="IPA nowrap"): #first = received pronunciation
            pronunciation = span.text
        
        return pronunciation
    
    def get_youglish_uk_pronunciation_video(self):
        """Youglish : pronunciation video retrieval"""
        return f"https://youglish.com/pronounce/{self.word}/english/uk/"
    
    def show_word_infos(self):
        """Utility method to print the retrieved word information in a readable format.
        Those infos will be displayed in the UI
        """
        print(f"Pronunciation: {self.pronunciation}")
        print(f"Youglish UK Pronunciation Youtube videos: {self.get_youglish_uk_pronunciation_video()}")
        return


if __name__ == "__main__":
    word = "audio"
    fetcher_audio = WordInfoFetcher(word)
    # print(fetcher_audio.word_infos.prettify())
    print(fetcher_audio.get_pronunciation())
    print(fetcher_audio.get_youglish_uk_pronunciation_video())
