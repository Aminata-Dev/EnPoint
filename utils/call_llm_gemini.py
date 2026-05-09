import argparse

SYSTEM_PROMPT = "You are an british English pronunciation teacher. You will help me improve my English pronunciation. I will give you words or phrases in English, and you will provide me with the phonetic transcription of those words or phrases using the International Phonetic Alphabet (IPA). Additionally, you will give me advice on how to pronounce those words or phrases, focusing on sounds that are difficult for French speakers. For example, if I give you the word 'thought', you might tell me that the phonetic transcription is /θɔːt/ and that the /θ/ sound is often difficult for French speakers because it does not exist in French. You could advise me to place my tongue between my teeth to produce this sound correctly. Feel free to give me examples of similar words to help me understand the sounds."

# USER_PROMPT = "week and weak ?"

from google import genai
from google.genai import types

def call_gemini_llm(system_prompt = SYSTEM_PROMPT, user_prompt = None):

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.1
        ),
        contents=[user_prompt]
    )

    print("--- PUPIL QUESTION ---")
    print(user_prompt)
    print("--- COACH PRONUNCIATION ANSWER ---")
    print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CLI tool to call Gemini LLM for British English pronunciation practice."
    )

    parser.add_argument(
        "-up", "--user_prompt", 
        type=str, 
        required=True,
        help="The user prompt for the LLM."
    )

    parser.add_argument(
        "-sp", "--system_prompt", 
        type=str, 
        default=SYSTEM_PROMPT, 
        help="The system prompt for the LLM."
    )

    args = parser.parse_args() #Parse the arguments

    call_gemini_llm(system_prompt=args.system_prompt, user_prompt=args.user_prompt)