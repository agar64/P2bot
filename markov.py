import os
import pickle
import random
import re
from collections import defaultdict

class MarkovChain:
    def __init__(self):
        self.model = defaultdict(list)

    def tokenize(self, text):
        return re.findall(r'\b\w+\b', text.lower())

    def learn(self, text):
        words = self.tokenize(text)
        if len(words) < 3:
            return
        for i in range(len(words) - 2):
            key = (words[i], words[i + 1])
            self.model[key].append(words[i + 2])

    def generate(self, max_words=20):
        if not self.model:
            return "I don't know anything yet!"
        key = random.choice(list(self.model.keys()))
        output = [key[0], key[1]]
        for _ in range(max_words - 2):
            next_words = self.model.get(key)
            if not next_words:
                break
            next_word = random.choice(next_words)
            output.append(next_word)
            key = (key[1], next_word)
        return ' '.join(output)

class ChatMemory:
    def __init__(self):
        self.text_model = MarkovChain()
        self.stickers = []
        self.gifs = []
        self.message_count = 0
        self.trigger_rate = 50

class MarkovManager:
    def __init__(self, model_dir="models"):
        self.model_dir = model_dir
        os.makedirs(self.model_dir, exist_ok=True)
        self.models = {}

    def _get_model_path(self, chat_id):
        return os.path.join(self.model_dir, f"markov_model_{chat_id}.pkl")

    def get_memory(self, chat_id):
        if chat_id not in self.models:
            self.models[chat_id] = self._load_model(chat_id)
        return self.models[chat_id]

    def _load_model(self, chat_id):
        path = self._get_model_path(chat_id)
        if os.path.exists(path):
            with open(path, 'rb') as f:
                raw = pickle.load(f)
                mem = ChatMemory()
                mem.text_model.model = defaultdict(list, raw.get("text_model", {}))
                mem.stickers = raw.get("stickers", [])
                mem.gifs = raw.get("gifs", [])
                mem.message_count = raw.get("message_count", 0)
                mem.trigger_rate = raw.get("trigger_rate", 50)
                return mem
        return ChatMemory()

    def save_model(self, chat_id):
        mem = self.get_memory(chat_id)
        path = self._get_model_path(chat_id)
        with open(path, 'wb') as f:
            pickle.dump({
                "text_model": dict(mem.text_model.model),
                "stickers": mem.stickers,
                "gifs": mem.gifs,
                "message_count": mem.message_count,
                "trigger_rate": mem.trigger_rate,
            }, f)

    def learn_text(self, chat_id, text):
        mem = self.get_memory(chat_id)
        mem.text_model.learn(text)
        mem.message_count += 1
        self.save_model(chat_id)

    def learn_sticker(self, chat_id, file_id):
        mem = self.get_memory(chat_id)
        mem.stickers.append(file_id)
        self.save_model(chat_id)

    def learn_gif(self, chat_id, file_id):
        mem = self.get_memory(chat_id)
        mem.gifs.append(file_id)
        self.save_model(chat_id)

    def generate_text(self, chat_id, max_words=20):
        mem = self.get_memory(chat_id)
        return mem.text_model.generate(max_words)

    def get_random_sticker(self, chat_id):
        mem = self.get_memory(chat_id)
        return random.choice(mem.stickers) if mem.stickers else None

    def get_random_gif(self, chat_id):
        mem = self.get_memory(chat_id)
        return random.choice(mem.gifs) if mem.gifs else None

    def should_speak(self, chat_id):
        mem = self.get_memory(chat_id)
        if mem.message_count >= mem.trigger_rate:
            mem.message_count = 0
            self.save_model(chat_id)
            return True
        self.save_model(chat_id)
        return False

    def set_trigger_rate(self, chat_id, rate):
        mem = self.get_memory(chat_id)
        mem.trigger_rate = rate
        self.save_model(chat_id)
