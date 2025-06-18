import tkinter as tk
import requests
import random
from bs4 import BeautifulSoup  # Fixed: import from bs4

# Replace with your actual API keys
BING_API_KEY = "YOUR_BING_API_KEY"

def new_func():
    GROQ_API_KEY = "YOUR_GROQ_API_KEY"
    return GROQ_API_KEY

GROQ_API_KEY = new_func()

class ChatbotAppWithWikiSearch(tk.Tk):
    def __init__(self):
        super().__init__()

        # Conversation patterns and canned responses
        self.conversation = {
            "hi|hello": ["Hello!", "Hi there!", "How can I assist you today?"],
            "what is your name": ["My name is Flash."],
            "how are you": ["I'm just a computer program, but thanks for asking!"],
            "tell me a joke|joke": [
                "Why did the programmer go broke? Because he used up all his cache!",
                "Why don't scientists trust atoms? Because they make up everything!"
            ],
            "search": ["Type 'search' followed by your query."],
            "wiki": ["Type 'wiki' followed by your query."],
            "goodbye|bye": ["Goodbye!", "See you later!"],
            "who created you": ["I was created by a Python developer."],
            "fact|tell me a fact": ["Did you know? Honey never spoils.", "Bananas are berries, but strawberries are not."]
        }

        self.title("Flash - AI Chat Assistant")
        self.chat_area = tk.Text(self, wrap=tk.WORD, width=60, height=20)
        self.chat_area.configure(state=tk.DISABLED)

        self.user_input_field = tk.Entry(self, width=60)
        self.send_button = tk.Button(self, text="Send", command=self.on_send_button_click)

        self.chat_area.pack(pady=10)
        self.user_input_field.pack(pady=5)
        self.send_button.pack(pady=5)

    def on_send_button_click(self):
        user_input = self.user_input_field.get().strip()
        if user_input == "":
            return
        response = self.respond(user_input)

        self.chat_area.configure(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"You: {user_input}\nFlash: {response}\n\n")
        self.chat_area.configure(state=tk.DISABLED)

        self.user_input_field.delete(0, tk.END)

    def fetch_web_data(self, query, source):
        try:
            if source == "bing":
                headers = {'Ocp-Apim-Subscription-Key': BING_API_KEY}
                params = {'q': query, 'count': 1, 'safeSearch': 'Moderate'}
                response = requests.get("https://api.cognitive.microsoft.com/bing/v7.0/search", headers=headers, params=params)
                data = response.json()
                if 'webPages' in data and 'value' in data['webPages']:
                    return data['webPages']['value'][0]['snippet']
                else:
                    return "No info found."
            elif source == "wiki":
                url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                paragraphs = soup.find_all('p')
                summary = ' '.join(p.text for p in paragraphs[:3])
                return summary if summary else "No info found."
        except Exception as e:
            return f"Error fetching data: {e}"

    def call_groq_ai(self, prompt):
        try:
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "messages": [{"role": "user", "content": prompt}],
                "model": "llama3-70b-8192",
                "temperature": 0.7,
                "max_tokens": 300,
                "stop": None
            }
            response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
            response_data = response.json()
            # Check if "choices" exists in the response
            if "choices" in response_data:
                return response_data["choices"][0]["message"]["content"]
            else:
                return f"Error from Groq AI: {response_data}"
        except Exception as e:
            return f"Error from Groq AI: {e}"

    def respond(self, user_input):
        user_input_lower = user_input.lower()

        for pattern, responses in self.conversation.items():
            if any(keyword in user_input_lower for keyword in pattern.split('|')):
                return random.choice(responses)

        if user_input_lower.startswith("search "):
            return self.fetch_web_data(user_input[7:], source="bing")
        elif user_input_lower.startswith("wiki "):
            return self.fetch_web_data(user_input[5:], source="wiki")
        else:
            # Fallback: use Groq LLaMA3 to generate a reply
            return self.call_groq_ai(user_input)

if __name__ == "__main__":
    app = ChatbotAppWithWikiSearch()
    app.mainloop()
