import os
import random
import time
import datetime
import requests
from telebot.apihelper import ApiTelegramException

import numpy as np

from markov import MarkovManager

import telebot

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

def save_data(array):
    np.save("chat_settings", array)


def load_data():
    return np.load("chat_settings.npy")

def load_suggestions():
    saved_suggestions = np.load("suggestions.npz")
    return saved_suggestions


msg_counter = 0
reply_after = 50
random_variation = 0
max_random_variation = 0
anti_spam = False

last_reply = 0

try:
    chatID_matrix = load_data()
    print("Loaded Saved Matrix")
    #print(chatID_matrix)
except OSError:
    print("Generated New Matrix")
    chatID_matrix = np.zeros((1,6), dtype=int)


game_names = ["The Last of Us", "Among Us", "Xenoblade Chronicles", "Sonic '06", "Sonic R", "Zelda 2", "Mario Is Missing",
              "Spore", "Pong", "Meet and Fuck 3", "GTA San Andreas", "Cyberpunk 2077", "Minecraft", "Terraria",
              "Lethal Company", "Fall Guys", "Mafia II", "Alan Wake", "Stellaris", "Day of Defeat", "Danganronpa",
              "Spider-Man", "Forza", "Little Witch Nobeta", "Dark Souls 2", "SimCity (2013)", "The Sims 3", "Minesweeper",
              "Tetris", "UNO", "Jogo da Vida", "Tamagochi", "uma pedra avulsa", "Roleta Russa", "999", "GTA IV", "Star Citizen",
              "No Man's Sky", "Starfield", "Daggerfall", "encarar o sol", "Half-Life", "Melty Blood", "Umineko",
              "Dr.Jekyll and Mr.Hyde", "Contra", "Castlevania", "Bloodstained", "Dwarf Fortress", "Super 3D Noah's Ark"]

movie_names = ["Among Us - The Movie", "The Emoji Movie", "Cats", "AVGN Movie", "Godzilla Minus One", "Dune",
               "O Dia em Que a Terra Parou", "Os Incríveis", "ET", "o filme do Pelé", "O Auto da Compadecida", "Cuties",
               "Tropa de Elite", "Spy x Family", "Full House", "Friends", "One Punch Man", "Madoka", "Polly Pocket",
               "Barbie", "Oppenheimer", "Attack on Titan", "Yuru Yuri", "o filme do Sonic", "Frieren", "Euphoria",
               "School Days", "Steins;Gate", "Death Note", "K-ON", "Blue Archive"]

opinions = ["goes hard as fuck", "brabissimo demais", "sony simplesmente assassinou um jogo",
            "é muito pica", "devia morrer de novo", "- ESSE MAL TEM NOME", "é extremamente bom", "esse lugar mudou minha vida",
            "I love this game", "infelizmente ele é constantemente washed", "é muito bonito", "eu amo esse livro",
            "eu acho essa estatua muito massa", "esse eu achei muito legal tbm", "a gente devia assistir esse",
            "jumpscared por musica br muito pika", "Todd", "os dois foram fantasticos", "filmasso da porra ta doido",
            "eu admiro muito", "impressionante", "caralho, vou ficar calvo", "só esperando a existencia do resto",
            "historiadores vão ler isso e dizer: ele parece valorizar sua amizade com homens"]

motives = ["that happens in the game", "bro liked his own comment", "I gotta hop on the classics sometimes",
            "eu conheci antes da original", "this quote goes hard as fuck", "meu cerebro é só catarro",
            "eu estou em estado vegetativo", "eu gosto do Kendrick então posso ser biased mas meu deus",
            "i am the motherfucking card master", "idk but i like making the joke", "a voz da megan é meio estranha",
           "french", "o segredo foi a lot of blocking", "juscelino kubitschek", "estou sofrendo como a livia",
           "I do like him because of that", "a cena final é muito fodastica", "nossa 3 hrs de filme", "é na vdd looney toones",
           "aparece um cara sendo cuzão", "the fentanyl got me moving like a claymation figure", "o estado afundou bixo",
           "pau no cu da sony", "o q eu tenho foi mais baratim", "apagonis", "caralho q porra é essa isso é real",
           "pensei em padrinhos magicos tbm", "I have no idea", "Urobuchi you cooked again",
           "all you have to do is not let him near women", "I am smart", "(Tava afim de comer lamen)",
           "when the spire is slain\nBottom text"]
try:
    game_names_suggested = (load_suggestions()["a"]).tolist()
    movie_names_suggested = (load_suggestions()["b"]).tolist()
    opinions_suggested = (load_suggestions()["c"]).tolist()
    motives_suggested = (load_suggestions()["d"]).tolist()
    print("Suggestions loaded successfully")
except:
    game_names_suggested = []
    movie_names_suggested = []
    opinions_suggested = []
    motives_suggested = []
    print("Suggestions file not found")

#print(motives_suggested)

def save_suggestions():
    #saved_suggestions = [game_names_suggested, movie_names_suggested, opinions_suggested, motives_suggested]
    np.savez("suggestions", a=game_names_suggested, b=movie_names_suggested, c=opinions_suggested, d=motives_suggested)


def select_text():
    action, first_name, middle_name, last_name = "", "", "", ""
    game_names_all = game_names + game_names_suggested
    movie_names_all = movie_names + movie_names_suggested
    opinions_all = opinions + opinions_suggested
    motives_all = motives + motives_suggested

    if(random.randint(0, 1)):
        first_name = game_names_all[random.randint(0, len(game_names_all)-1)]
        action = "jogar"
    else:
        first_name = movie_names_all[random.randint(0, len(movie_names_all) - 1)]
        action = "assistir"

    middle_name = opinions_all[random.randint(0, len(opinions_all)-1)]
    last_name = motives_all[random.randint(0, len(motives_all)-1)]

    return "Acabei de " + action + " " + first_name + " e " + middle_name + " pois " + last_name


def safe_send_message(chat_id, text, retries=3, delay=2, parse_mode=None):
    for attempt in range(retries):
        try:
            return bot.send_message(chat_id, text, parse_mode=parse_mode)
        except (requests.exceptions.RequestException, ApiTelegramException) as e:
            print(f"[safe_send_message] Attempt {attempt+1} failed: {e}")
            time.sleep(delay)
    print("[safe_send_message] All retries failed.")
    return None

def safe_reply(chat_id, text, retries=3, delay=2, parse_mode=None):
    for attempt in range(retries):
        try:
            return bot.reply_to(chat_id, text, parse_mode=parse_mode)
        except (requests.exceptions.RequestException, ApiTelegramException) as e:
            print(f"[safe_send_message] Attempt {attempt+1} failed: {e}")
            time.sleep(delay)
    print("[safe_send_message] All retries failed.")
    return None

def check_for_start(message):
    if (not np.isin(message.chat.id, chatID_matrix[:, 0])):
        safe_reply(message, "Acho que não falei contigo antes, que tal dar um /start primeiro?")
        return False
    else: return True

def start_conversation(chatID):
    global chatID_matrix
    properties = [[chatID, msg_counter, reply_after, random_variation, max_random_variation, anti_spam]]
    #itemindex = np.where(chatID_matrix == chatID)
    #print("Check:", np.isin(chatID, chatID_matrix[:, 0]), "chatID:", chatID, "Matrix:", chatID_matrix[:, 0])
    if(not np.isin(chatID, chatID_matrix[:, 0])):
        chatID_matrix = np.append(chatID_matrix, np.array(properties), axis=0)
        save_data(chatID_matrix)
        print(chatID_matrix)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    safe_reply(message, "Howdy, how are you doing?")
    start_conversation(message.chat.id)


@bot.message_handler(commands=['restart'])
def restart_handler(message):
    global chatID_matrix
    if (check_for_start(message)):
        ID_index = np.nonzero(chatID_matrix[:, 0] == message.chat.id)[0][0]
        chatID_matrix = np.delete(chatID_matrix, (ID_index), axis=0)
        safe_reply(message, "Howdy, how are you doing? All your settings were reset")
        start_conversation(message.chat.id)


@bot.message_handler(commands=['talk'])
def speak_handler(message):
    global chatID_matrix, last_reply
    if (check_for_start(message)):
        ID_index = np.nonzero(chatID_matrix[:, 0] == message.chat.id)[0][0]
        chatID_matrix[ID_index][1] = chatID_matrix[ID_index][2] #msg_counter = reply_after
        last_reply = 0
        count_all(message)

@bot.message_handler(commands=['antiSpam'])
def spam_handler(message):
    global chatID_matrix
    if check_for_start(message):
        ID_index = np.nonzero(chatID_matrix[:, 0] == message.chat.id)[0][0]
        anti_spam = chatID_matrix[ID_index][5]
        anti_spam = not anti_spam
        if(anti_spam): state = "ativada"
        else: state = "desativada"
        text = "Função anti-spam " + state
        chatID_matrix[ID_index][5] = anti_spam
        save_data(chatID_matrix)
        safe_reply(message, text)


@bot.message_handler(commands=['setInterval'])
def interval_handler(message):
    global chatID_matrix
    if(check_for_start(message)):
        ID_index = np.nonzero(chatID_matrix[:, 0] == message.chat.id)[0][0]
        reply_after = chatID_matrix[ID_index][2]
        received_msg = message.text.replace("/setInterval","")
        try:
            reply_after_new = int(received_msg)
            if(reply_after_new < reply_after):
                safe_reply(message, "Okay, vou te incomodar mais agora")#print("Okay, I'll bother you less now")
            else:
                safe_reply(message, "Okay, vou te incomodar menos agora")#print("Okay, I'll bother you more now")
            reply_after = reply_after_new
            chatID_matrix[ID_index][2] = reply_after
            print("Reply interval updated to", reply_after,"in chat",ID_index)
            save_data(chatID_matrix)
        except: safe_reply(message, "Ei, isso não é um número inteiro!")#print("Hey, that's not an int!")


@bot.message_handler(commands=['setRandomVar'])
def randomVar_handler(message):
    global chatID_matrix
    if(check_for_start(message)):
        ID_index = np.nonzero(chatID_matrix[:, 0] == message.chat.id)[0][0]
        max_random_variation = chatID_matrix[ID_index][4]
        received_msg = message.text.replace("/setRandomVar", "")
        try:
            max_random_variation_new = int(received_msg)
            if(max_random_variation_new == 0):
                safe_reply(message, "Variação entre o tempo de resposta desativada. Sempre responderei após o mesmo número de mensagens agora")
            elif(max_random_variation_new < max_random_variation):
                safe_reply(message, "Okay, haverá menos variação entre o tempo de resposta agora")
            else:
                safe_reply(message, "Okay, haverá mais variação entre o tempo de resposta agora")
            max_random_variation = max_random_variation_new
            chatID_matrix[ID_index][4] = max_random_variation
            print("Max variation updated to", max_random_variation,"in chat",ID_index)
            save_data(chatID_matrix)
        except: safe_reply(message, "Ei, isso não é um número inteiro!")#print("Hey, that's not an int!")



@bot.message_handler(commands=['consult'])
def consult_handler(message):
    global chatID_matrix
    if(check_for_start(message)):
        ID_index = np.nonzero(chatID_matrix[:, 0] == message.chat.id)[0][0]
        reply_after = chatID_matrix[ID_index][2]
        random_variation = chatID_matrix[ID_index][3]
        max_random_variation = int(chatID_matrix[ID_index][4])
        anti_spam = chatID_matrix[ID_index][5]

        if (anti_spam):
            state = "ativado"
        else:
            state = "desativado"

        reply_text = ("Responder depois de " + str(int(reply_after)) + " mensagens\nVariação máxima: " +
                    str(max_random_variation) + "\nVariação atual: " + str(int(random_variation)) + "\nAnti-Spam: " + state)
        safe_reply(message, reply_text)


@bot.message_handler(commands=['help'])
def help_handler(message):
    safe_reply(message, "/start - Inicia o bot\n/setInterval _n_ - Muda quantas mensagens devem passar até que o bot fale para _n_. Default: 50\n/setRandomVar _n_ - Muda a variação aleatória +/- _n_ entre o número de mensagens que o bot espera antes de falar. Default: 0\n/talk - Força o bot a falar\n/antiSpam - Quando ativado, o bot esperará no mínimo 10 minutos antes de falar a menos que forçado a falar com o _speak_. Default: off\n/consult - Consulta as configurações do bot para este chat\n/restart - Reseta as suas configurações e reinicia o bot\n*Contexto para as opções abaixo:* Uma fala do bot consiste de: *\"Acabei de jogar/assistir* _jogo/filme_ *e* _opinião_ *pois* _motivo_*\"*\n/suggestGame _gameName_ - Sugere um nome de jogo para a database\n/suggestMovie _movieName_ - Sugere um nome de filme para a database\n/suggestOpinion _opinion_ - Sugere uma opinião para a database\n/suggestMotive _motive_ - Sugere um motivo para a database", parse_mode = "Markdown")

@bot.message_handler(commands=['suggestGame'])
def suggest_game_handler(message):
    global game_names_suggested
    parsed = [message.text.replace("/suggestGame ", "")]
    if not ((parsed == ["/suggestGame"]) or (parsed == [""])):
        game_names_suggested = game_names_suggested + parsed
        save_suggestions()
        safe_reply(message, "Sugestão adicionada à database")
    else:
        safe_reply(message, "Por favor digite alguma coisa")

@bot.message_handler(commands=['suggestMovie'])
def suggest_movie_handler(message):
    global movie_names_suggested
    parsed = [message.text.replace("/suggestMovie ", "")]
    if not ((parsed == ["/suggestMovie"]) or (parsed == [""])):
        movie_names_suggested = movie_names_suggested + parsed
        save_suggestions()
        safe_reply(message, "Sugestão adicionada à database")
    else:
        safe_reply(message, "Por favor digite alguma coisa")

@bot.message_handler(commands=['suggestOpinion'])
def suggest_opinion_handler(message):
    global opinions_suggested
    parsed = [message.text.replace("/suggestOpinion ", "")]
    if not ((parsed == ["/suggestOpinion"]) or (parsed == [""])):
        opinions_suggested = opinions_suggested + parsed
        save_suggestions()
        safe_reply(message, "Sugestão adicionada à database")
    else:
        safe_reply(message, "Por favor digite alguma coisa")


@bot.message_handler(commands=['suggestMotive'])
def suggest_motive_handler(message):
    global motives_suggested
    parsed = [message.text.replace("/suggestMotive ", "")]
    if not ((parsed == ["/suggestMotive"]) or (parsed == [""])):
        motives_suggested = motives_suggested + parsed
        save_suggestions()
        safe_reply(message, "Sugestão adicionada à database")
    else:
        safe_reply(message, "Por favor digite alguma coisa")


# @bot.message_handler(commands=['setP2'])
# def sign_handler(message):
#     text = "P2, responda a esta mensagem"
#     sent_msg = safe_send_message(message.chat.id, text, parse_mode="Markdown")
#     bot.register_next_step_handler(sent_msg, p2_set_reply_handler)
#
#
# def p2_set_reply_handler(message):
#     sign = message.text
#     text = "As definições de P2 foram atualizadas"
#     safe_reply(message, text)
#     global p2_id
#     p2_id = message.chat.id


# @bot.message_handler(func=lambda msg: True)
# def echo_all(message):
#     safe_reply(message, message.text)

manager = MarkovManager()

@bot.message_handler(content_types=['text', 'photo', 'sticker', 'video', 'animation', 'document'])
def count_all(message):
    global chatID_matrix, last_reply
    if(check_for_start(message)):
        ID_index = np.nonzero(chatID_matrix[:, 0] == message.chat.id)[0][0]
        #print("chatID_matrix[",ID_index,"][",1,"]")
        msg_counter = chatID_matrix[ID_index][1]
        reply_after = chatID_matrix[ID_index][2]
        random_variation = chatID_matrix[ID_index][3]
        max_random_variation = int(chatID_matrix[ID_index][4])

        anti_spam = chatID_matrix[ID_index][5]

        if anti_spam:
            condition = (time.time() - last_reply) > 600
        else:
            condition = (time.time() - last_reply) > 0.0001 #True

        if (message.from_user.username == "WAFFLEDUDE"):
            if (message.text is not None):
                manager.learn_text(message.chat.id, message.text)
            elif (message.caption is not None):
                manager.learn_text(message.chat.id, message.caption)

        '''if ((message.text is not None) and (message.from_user.username == "WAFFLEDUDE")):
            manager.learn_text(message.chat.id, message.text)'''

        if (msg_counter > reply_after - 1) and condition:
            msg_counter = 0 + random_variation
            text = select_text()

            if(random.randint(0,99) < 10):
                safe_send_message(message.chat.id, manager.generate_text(message.chat.id))
            else:
                safe_send_message(message.chat.id, text, parse_mode="Markdown")

            last_reply = time.time()
            random_variation = random.randint(-max_random_variation, max_random_variation)
            print("random_variation for chat",ID_index,":", random_variation)
            chatID_matrix[ID_index][3] = random_variation
        else:
            msg_counter = msg_counter + 1
        chatID_matrix[ID_index][1] = msg_counter
        save_data(chatID_matrix)
        ct = datetime.datetime.now()
        print(ct.time(),"- Messages until next reply for chat", ID_index, ":", reply_after - msg_counter,f"- {message.content_type}",)




while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)  # Wait a bit before retrying