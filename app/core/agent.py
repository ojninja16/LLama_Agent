from typing import Any, Dict
import requests
from config import TOGETHER_AI_API_KEY
import langdetect
from core.crypto_service import CryptoService
from config import SUPPORTED_CRYPTO 
import time
class AIAgent:
    def __init__(self):
        self.api_key = TOGETHER_AI_API_KEY
        self.api_url = "https://api.together.xyz/v1/chat/completions"
        self.model_name="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
        self.conversation_history: Dict[str, Any] = {}
        self.crypto_service=CryptoService()
    async def handle_request(self, prompt: str) -> str:
        if not prompt:
            return "Looks like you forgot to ask a question!"
        try:
            lang = langdetect.detect(prompt)
            print("Detected language:",lang)
            if lang != "en":
                translate_prompt=f"Translate the following text from {lang} to English:\n{prompt}"
                translate_payload={
                    "model": self.model_name,
                    "messages":[{"role": "user", "content": translate_prompt}],
                     "max_tokens": 150,
            "temperature": 0.4
                }
                # translate_response=await
                translate_response = await self._make_together_ai_request(translate_payload)
                translated_prompt = translate_response.json()["choices"][0]["message"]["content"]
                self.conversation_history["translated_prompt"] = translated_prompt
            else:
                translated_prompt = prompt  # If language is English, no need to translate
        
        # Determine if the request is for cryptocurrency details
            if "price" in translated_prompt.lower() or "crypto" in translated_prompt.lower():
                return await self.handle_crypto_request(translated_prompt)
            else:
            # Handle general queries using the chat completion API
               return await self.generate_response(translated_prompt)
                
        except langdetect.lang_detect_exception.LangDetectException:
            return "I'm sorry, I couldn't detect the language of your request. Please try again."    
        
        
    async def handle_crypto_request(self, prompt: str) -> str:
        print(prompt)
        crypto_symbol=next( (crypto for crypto in SUPPORTED_CRYPTO if crypto in prompt.lower().replace(" ", "-")),
    None)
        print(crypto_symbol)
        if crypto_symbol:
            price=await self.crypto_service.get_crypto_price(crypto_symbol)
            crypto_prompt=(
    f"The latest price of {crypto_symbol.upper()} is ${price:.2f}. "
    "Provide an overview of recent trends, notable factors influencing this cryptocurrency, "
    "and any important insights related to its current market position.")
            final_payload={
                "model":self.model_name,
                "messages":[
                {"role":"user", "content":crypto_prompt},
                {"role": "assistant", "content": self.get_full_context(crypto_prompt)}
            ],
                 "max_tokens": 150,
            "temperature": 0.4
        }
            final_response=await self._make_together_ai_request(final_payload)
            return final_response.json()["choices"][0]["message"]["content"]
        else:
            return "I'm sorry, I couldn't find the cryptocurrency symbol in your request."
            
    async def generate_response(self, prompt: str) -> str:
        # Prepare the request payload for the chat completion AP
        start_time = time.time()
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": self.get_full_context(prompt)}],
            "max_tokens": 150,
            "temperature": 0.4
        }

        # Send the request to the Together API
        response = await self._make_together_ai_request(payload)
        model_response = response.json()["choices"][0]["message"]["content"]
        print(model_response)
        self.conversation_history["model_response"] = model_response
        end_time = time.time()
        print(f"API request took {end_time - start_time:.2f} seconds")
        return model_response

    async def _make_together_ai_request(self, payload: Dict[str, Any]) -> requests.Response:
        print("Making request to Together AI API",self.api_key,self.api_url,payload)
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.api_key}"
        }

        response = requests.post(self.api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response

    def get_full_context(self, prompt: str) -> str:
        if "model_response" in self.conversation_history:
            return f"{self.conversation_history['model_response']}\n{prompt}"
        else:
            return prompt