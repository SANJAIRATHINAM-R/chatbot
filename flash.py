import tkinter as tk
import requests
import random
from bs4 import BeautifulSoup

# Use a constant for Bing API key
BING_API_KEY = "YOUR_BING_API_KEY"

class ChatbotAppWithWikiSearch(tk.Tk):
    def _init_(self):
        super()._init_()

        self.conversation = {
            "hi|hello": ["Hello!", "Hi there!", "How can I assist you today?"],
            "what is your name": ["My name is Flash."],
            "how are you": ["I'm just a computer program, so I don't have feelings, but thanks for asking!"],
            "tell me a joke|joke": [
                "Why did the programmer go broke? Because he used up all his cache!",
                "Here's one: Why don't scientists trust atoms? Because they make up everything!"
            ],
            "search": ["I can search the web for you. Just type 'search' followed by your query."],
            "wiki": ["I can also provide information from Wikipedia. Just type 'wiki' followed by your query."],
            "what is the weather like": ["I'm unable to check the weather right now, but you can use a weather service."],
            "what can you do": ["I can chat with you, tell jokes, and provide information from the web and Wikipedia."],
            "thank you|thanks": ["You're welcome!", "No problem!", "Anytime!"],
            "goodbye|bye": ["Goodbye!", "See you later!", "Take care!"],
            "who created you|who made you": ["I was created by a developer using Python and some libraries like Tkinter."],
            "how old are you": ["I don't have an age, but I've been around as long as I've been running on this machine."],
            "tell me a fact|fact": [
                "Did you know? Honey never spoils.",
                "Here’s a fact: The Eiffel Tower can be 15 cm taller during the summer."
            ],
            "what is your favorite color": ["I don't have preferences, but I think blue is a calming color."],
            "do you like music|what music do you like": ["I don't listen to music, but I can help you find some information about it!"]
        }

        self.context = {}
        self.random = random

        self.title("Flash ")

        self.chat_area = tk.Text(self, wrap=tk.WORD, width=60, height=20)
        self.chat_area.configure(state=tk.DISABLED)

        self.user_input_field = tk.Entry(self, width=60)
        self.send_button = tk.Button(self, text="Send", command=self.on_send_button_click)

        self.chat_area.pack(pady=10)
        self.user_input_field.pack(pady=5)
        self.send_button.pack(pady=5)

    def on_send_button_click(self):
        user_input = self.user_input_field.get()
        response = self.respond(user_input)

        self.chat_area.configure(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"You: {user_input}\nChatbot: {response}\n\n")
        self.chat_area.configure(state=tk.DISABLED)

        self.user_input_field.delete(0, tk.END)

    def fetch_web_data(self, query, source):
        try:
            if source == "bing":
                headers = {
                    'Ocp-Apim-Subscription-Key': BING_API_KEY,
                }
                params = {
                    'q': query,
                    'count': 1,
                    'safeSearch': 'Moderate',
                }
                response = requests.get("https://api.cognitive.microsoft.com/bing/v7.0/search", headers=headers, params=params)
                data = response.json()
                if 'webPages' in data and 'value' in data['webPages']:
                    return data['webPages']['value'][0]['snippet']
                else:
                    return "No relevant information found."
            elif source == "wiki":
                wikipedia_url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
                response = requests.get(wikipedia_url)
                soup = BeautifulSoup(response.text, 'html.parser')
                paragraphs = soup.find_all('p')
                summary = ' '.join([paragraph.text for paragraph in paragraphs[:3]])  # Take first 3 paragraphs
                return summary if summary else "No relevant information found on Wikipedia."
        except requests.RequestException as e:
            print(f"Failed to fetch information. Request Exception: {e}")
            return f"Failed to fetch information. Request Exception: {e}"
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return "An unexpected error occurred."

    def respond(self, user_input):
        for pattern, responses in self.conversation.items():
            if any(keyword in user_input.lower() for keyword in pattern.split('|')):
                response = self.random.choice(responses)
                return response

        if user_input.lower().startswith("search "):
            query = user_input[len("search "):]
            return self.fetch_web_data(query, source="bing")

        elif user_input.lower().startswith("wiki "):
            query = user_input[len("wiki "):]
            return self.fetch_web_data(query, source="wiki")

        return "I'm not sure how to respond to that."

if _name_ == "_main_":
    app = ChatbotAppWithWikiSearch()
    app.mainloop()
