from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
import csv
import os

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
    
        self.word = word.lower()
        url_word = self.word.replace(' ', '-')  # Replace spaces with hyphens for phrasal verbs
        self.cambridge_url = f"https://dictionary.cambridge.org/dictionary/english/{url_word}"

        
        self.last_request_time = 0  # Timestamp of the last request in order to not be detected as a bot by Cambridge Dictionary #doesn't seem to work well
        
        self.word_soup = self.get_word_soup()  # store the retrieved soup for later use
        self.pronunciation = self.get_english_transcription() 
        self.definitions = self.get_definitions()
        self.examples = self.get_examples()

    
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
        
        definitions = set()  # Use a set to avoid duplicates
        for block in self.word_soup.find_all('div', class_='def-block'):
            definition_tag = block.find('div', class_='def')
            if definition_tag:
                clean_def = definition_tag.get_text().strip().rstrip(':')
                definitions.add(clean_def)
        return list(definitions) # Convert back to list for consistent return type
    
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


    def save_word_info_to_csv(self, filename="vocabulary_history", source = None, example = None, display_message=True): #add the reason for which we need to fetch the word : definition or pronunciation purpose
        """
        Create a CSV for my Notion
        """
        # visual separator : "|" for multiple definitions/examples in the same cell
        definition_text = " | ".join(self.definitions)
        exemple_text = " | ".join(self.examples)
        
        # my Notion columns #to-do : translate headers to english
        headers = ["Mot / Expression", "Pronunciation", "Sens", "Exemple (phrase)", "Date", "Source"] 
        row = [self.word, f"{self.pronunciation}\n{self.get_youglish_uk_pronunciation_video()}", definition_text, (f"{example}\n{exemple_text}" if example is not None else exemple_text), datetime.now().strftime("%Y-%m-%d"), (source if source is not None else "")]
        
        file = f"{filename}.csv"
        file_exists = os.path.isfile(file)
        
        # Use utf-8-sig to ensure special characters like IPA symbols are correctly read by Excel/Notion
        with open(file, mode='a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            if not file_exists:
                writer.writerow(headers)
                
            writer.writerow(row)
        
        if display_message:
            print(f"✅ '{self.word}' added to {file}")

    def show_word_infos(self):
        """Utility method to print the retrieved word information in a readable format.
        Those infos will be displayed in the UI
        """
        print()
        print(f"Word or phrasal verb: {self.word}")
        print(f"Cambridge Dictionary URL: {self.cambridge_url}")  # Show the Cambridge Dictionary URL for reference

        print("\n" + "-" * 30 + "\n")

        print("BRITISH ENGLISH PRONUNCIATION PART:")

        print(f" > Phonetic Transcription: {self.pronunciation}")
        print(f" > Pronunciation Youtube videos (Youglish): {self.get_youglish_uk_pronunciation_video()}")

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
    word = "reaper"
    
    fetcher = WordInfoFetcher(word)

    fetcher.save_word_info_to_csv(
        # source = "Wake Up! song",
#         example = """With my lightning bolts a glowing
# I can see where I am going to be
# When the reaper reaches and touches my hand
#         """
    )
    # print(fetcher.get_examples())
    fetcher.show_word_infos()
    

    # print(fetcher.word_soup.prettify())
    # print(fetcher.get_english_transcription())
    # print(fetcher.get_definitions())
    # print(fetcher.get_examples())
    # print(fetcher.get_youglish_uk_pronunciation_video())

    
