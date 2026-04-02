import time
import requests

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
        self.word = word
        self.last_request_time = 0  # Timestamp of the last request
        self.word_infos = self.get_word_info()  # To store the retrieved data for later use
    
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
        url = f"https://en.wiktionary.org/api/rest_v1/page/definition/{self.word}"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"HTTP error {response.status_code} for word '{self.word}'")
                return None
        except Exception as e:
            print(f"Error retrieving '{self.word}': {e}")
            return None


# Synchronous function for compatibility
def get_wiktionary_data(word):
    fetcher_audio = WordInfoFetcher(word)
    return fetcher_audio.get_word_info()

if __name__ == "__main__":
    word = "audio"
    fetcher_audio = WordInfoFetcher(word)
    data = fetcher_audio.get_word_info()["en"]

    if isinstance(data, list):
        print(data)
    elif isinstance(data, dict):
        print(data.keys())
