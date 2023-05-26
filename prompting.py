import openai 
import requests

with open("./KEYFILE", "r") as f:
    openai.api_key = f.read().strip()

class OpenAi():
    MODEL: str

    def __init__(self):
        self.model = self.MODEL

    def get_translation(self, query):        
        if (self.MODEL == "gpt-3.5-turbo" or 
            self.MODEL == "gpt-4"):
            message_log = [
                {"role": "user", "content": query}
            ]            
            response = openai.ChatCompletion.create(
                model = self.MODEL,
                messages = message_log,
                max_tokens = 1000,
                temperature = 0.4,
                top_p = 0.9,
                stream = True
            )
            return response
        
        else:
            response = openai.Completion.create(
                engine = self.MODEL,
                prompt = query,
                max_tokens = 1000,
                temperature = 0.4,
                top_p = 0.9,
                stream = True
            )
            return response
        
class OpenAiChatGPT3(OpenAi):
    MODEL = "gpt-3.5-turbo"

class OpenAiChatGPT4(OpenAi):
    MODEL = "gpt-4"

class OpenAiDavinci(OpenAi):
    MODEL = "text-davinci-003"



