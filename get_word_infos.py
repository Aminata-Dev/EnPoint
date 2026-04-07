import time
import requests
from bs4 import BeautifulSoup

# Header to bypass Cambridge Dictionary limitations
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

class WordInfoFetcher:
    """
    Class to retrieve word or phrasal verb information from Cambridge Dictionary,
    respecting rate limits for unauthenticated requests.
    """
    
    def __init__(self, word):
        self.word = word.lower()  # Normalize the word to lowercase
        self.last_request_time = 0  # Timestamp of the last request
        url_word = self.word.replace(' ', '-')  # Replace spaces with hyphens for phrasal verbs
        self.cambridge_url = f"https://dictionary.cambridge.org/dictionary/english/{url_word}"
        self.word_soup = self.get_word_soup()  # To store the retrieved soup for later use
        self.pronunciation = self.get_english_transcription()  # English IPA transcription
        self.definitions = self.get_definitions()  # List of definitions
        self.examples = self.get_examples()  # List of examples
    
    def _wait_for_rate_limit(self):
        """Wait if necessary to respect the rate of 5 req/sec"""
        now = time.time()
        time_since_last = now - self.last_request_time
        if time_since_last < 0.2:  # 1/5 = 0.2 seconds minimum between requests
            time.sleep(0.2 - time_since_last)
        self.last_request_time = time.time()
    
    def get_word_soup(self):
        """
        Retrieve the HTML soup from Cambridge Dictionary.
        Returns BeautifulSoup object or None on error.
        """
        self._wait_for_rate_limit()
        
        r = requests.get(self.cambridge_url, headers=headers)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, "html.parser")
        return soup
    
    def get_english_transcription(self):
        """
        Cambridge Dictionary: IPA transcription retrieval for UK English
        """
        if self.word_soup is None:
            return "Transcription not found"
        
        ipa_elem = self.word_soup.find('span', class_='ipa dipa lpr-2 lpl-1')
        if ipa_elem is None:
            return "Transcription not found"
        
        return f"/{ipa_elem.get_text()}/"
    
    def get_definitions(self):
        """
        Retrieve definitions from Cambridge Dictionary.
        Returns a list of definitions.
        """
        if self.word_soup is None:
            return []
        
        definitions = []
        for block in self.word_soup.find_all('div', class_='def-block'):
            definition_tag = block.find('div', class_='def')
            if definition_tag:
                clean_def = definition_tag.get_text()#.strip().rstrip(':')
                definitions.append(clean_def)
        return definitions
    
    def get_examples(self):
        """
        Retrieve examples associated with definitions from Cambridge Dictionary.
        Returns a list of examples.
        """
        if self.word_soup is None:
            return []
        
        examples = []
        for block in self.word_soup.find_all('div', class_='def-block'):
            block_examples = block.find_all('span', class_='eg')
            for ex in block_examples:
                examples.append(ex.get_text().strip())
        return examples
    
    def get_youglish_uk_pronunciation_video(self):
        """Youglish : pronunciation video retrieval"""
        url_word = self.word.replace(' ', '-')  # Replace spaces with hyphens for phrasal verbs
        return f"https://youglish.com/pronounce/{url_word}/english/uk/"
    
    def show_word_infos(self):
        """Utility method to print the retrieved word information in a readable format.
        Those infos will be displayed in the UI
        """
        print()
        print(f"Word or phrasal verb: {self.word}")
        print(f"Cambridge Dictionary URL: {self.cambridge_url}")  # Show the Cambridge Dictionary URL for reference

        print("\n" + "-" * 30 + "\n")

        print("PRONUNCIATION PART:")

        print(f" > English Transcription: {self.pronunciation}")
        print(f" > Youglish UK Pronunciation Youtube videos: {self.get_youglish_uk_pronunciation_video()}")

        print("-" * 30)

        print("DEFINITIONS:")
        for i, defn in enumerate(self.definitions, 1):
            print(f"  {i}. {defn}")

        print("-" * 30)

        print("EXAMPLES:")
        for i, ex in enumerate(self.examples, 1):
            print(f"  {i}. {ex}")
        return


if __name__ == "__main__":
    word = "fan out"  # Test with phrasal verb
    fetcher = WordInfoFetcher(word)

    # print(fetcher.get_examples())
    fetcher.show_word_infos()
    # print(fetcher.word_soup.prettify())
    # print(fetcher.get_english_transcription())
    # print(fetcher.get_definitions())
    # print(fetcher.get_examples())
    # print(fetcher.get_youglish_uk_pronunciation_video())
