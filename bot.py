import os
import random
import numpy as np

import telebot

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

def save_data(array):
    np.save("chat_settings", array)


def load_data():
    return np.load("chat_settings.npy")

msg_counter = 0
reply_after = 50
random_variation = 0
max_random_variation = 0

try:
    chatID_matrix = load_data()
    print("Loaded Saved Matrix")
except OSError:
    print("Generated New Matrix")
    chatID_matrix = np.zeros((1,5), dtype=int)


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
#test
def select_text():
    action, first_name, middle_name, last_name = "", "", "", ""
    if(random.randint(0, 1)):
        first_name = game_names[random.randint(0, len(game_names)-1)]
        action = "jogar"
    else:
        first_name = movie_names[random.randint(0, len(movie_names) - 1)]
        action = "assistir"

    middle_name = opinions[random.randint(0, len(opinions)-1)]
    last_name = motives[random.randint(0, len(motives)-1)]

    return "Acabei de " + action + " " + first_name + " e " + middle_name + " pois " + last_name


def check_for_start(message):
    if (not np.isin(message.chat.id, chatID_matrix[:, 0])):
        bot.reply_to(message, "Acho que não falei contigo antes, que tal dar um /start primeiro?")
        return False
    else: return True

def start_conversation(chatID):
    global chatID_matrix
    properties = [[chatID, msg_counter, reply_after, random_variation, max_random_variation]]
    #itemindex = np.where(chatID_matrix == chatID)
    #print("Check:", np.isin(chatID, chatID_matrix[:, 0]), "chatID:", chatID, "Matrix:", chatID_matrix[:, 0])
    if(not np.isin(chatID, chatID_matrix[:, 0])):
        chatID_matrix = np.append(chatID_matrix, np.array(properties), axis=0)
        save_data(chatID_matrix)
        print(chatID_matrix)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")
    start_conversation(message.chat.id)


@bot.message_handler(commands=['restart'])
def restart_handler(message):
    global chatID_matrix
    ID_index = np.nonzero(chatID_matrix[:, 0] == message.chat.id)[0][0]
    chatID_matrix = np.delete(chatID_matrix, (ID_index), axis=0)
    bot.reply_to(message, "Howdy, how are you doing? All your settings were reset")
    start_conversation(message.chat.id)


@bot.message_handler(commands=['speak'])
def speak_handler(message):
    global chatID_matrix
    ID_index = np.nonzero(chatID_matrix[:, 0] == message.chat.id)[0][0]
    chatID_matrix[ID_index][1] = chatID_matrix[ID_index][2] #msg_counter = reply_after
    count_all(message)


@bot.message_handler(commands=['setInterval'])
def interval_handler(message):
    global chatID_matrix
    ID_index = np.nonzero(chatID_matrix[:, 0] == message.chat.id)[0][0]
    reply_after = chatID_matrix[ID_index][2]
    received_msg = message.text.replace("/setInterval","")
    try:
        reply_after_new = int(received_msg)
        if(reply_after_new < reply_after):
            bot.reply_to(message, "Okay, vou te incomodar mais agora")#print("Okay, I'll bother you less now")
        else:
            bot.reply_to(message, "Okay, vou te incomodar menos agora")#print("Okay, I'll bother you more now")
        reply_after = reply_after_new
        chatID_matrix[ID_index][2] = reply_after
        print("Reply interval updated to", reply_after,"in chat",ID_index)
        save_data(chatID_matrix)
    except: bot.reply_to(message, "Ei, isso não é um número inteiro!")#print("Hey, that's not an int!")


@bot.message_handler(commands=['setRandomVar'])
def randomVar_handler(message):
    global chatID_matrix
    ID_index = np.nonzero(chatID_matrix[:, 0] == message.chat.id)[0][0]
    max_random_variation = chatID_matrix[ID_index][4]
    received_msg = message.text.replace("/setRandomVar", "")
    try:
        max_random_variation_new = int(received_msg)
        if(max_random_variation_new == 0):
            bot.reply_to(message, "Variação entre o tempo de resposta desativada. Sempre responderei após o mesmo número de mensagens agora")
        elif(max_random_variation_new < max_random_variation):
            bot.reply_to(message, "Okay, haverá menos variação entre o tempo de resposta agora")
        else:
            bot.reply_to(message, "Okay, haverá mais variação entre o tempo de resposta agora")
        max_random_variation = max_random_variation_new
        chatID_matrix[ID_index][4] = max_random_variation
        print("Max variation updated to", max_random_variation,"in chat",ID_index)
        save_data(chatID_matrix)
    except: bot.reply_to(message, "Ei, isso não é um número inteiro!")#print("Hey, that's not an int!")



@bot.message_handler(commands=['consult'])
def consult_handler(message):
    global chatID_matrix
    ID_index = np.nonzero(chatID_matrix[:, 0] == message.chat.id)[0][0]
    reply_after = chatID_matrix[ID_index][2]
    random_variation = chatID_matrix[ID_index][3]
    max_random_variation = int(chatID_matrix[ID_index][4])

    reply_text = ("Responder depois de " + str(int(reply_after)) + " mensagens\nVariação máxima: " +
                  str(max_random_variation) + "\nVariação atual: " + str(int(random_variation)))
    bot.reply_to(message, reply_text)


@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.reply_to(message, "/start - Inicia o bot\n/setInterval n - Muda quantas mensagens devem passar até que o bot fale para n. Default: 50\n/setRandomVar n - Muda a variação aleatória +/- n entre o número de mensagens que o bot espera antes de falar. Default: 0\n/speak - Força o bot a falar\n/consult - Consulta as configurações do bot para este chat\n/restart - Reseta as suas configurações e reinicia o bot")

# @bot.message_handler(commands=['setP2'])
# def sign_handler(message):
#     text = "P2, responda a esta mensagem"
#     sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
#     bot.register_next_step_handler(sent_msg, p2_set_reply_handler)
#
#
# def p2_set_reply_handler(message):
#     sign = message.text
#     text = "As definições de P2 foram atualizadas"
#     bot.reply_to(message, text)
#     global p2_id
#     p2_id = message.chat.id


# @bot.message_handler(func=lambda msg: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)

@bot.message_handler(func=lambda msg: True)
def count_all(message):
    global chatID_matrix
    if(check_for_start(message)):
        ID_index = np.nonzero(chatID_matrix[:, 0] == message.chat.id)[0][0]
        #print("chatID_matrix[",ID_index,"][",1,"]")
        msg_counter = chatID_matrix[ID_index][1]
        reply_after = chatID_matrix[ID_index][2]
        random_variation = chatID_matrix[ID_index][3]
        max_random_variation = int(chatID_matrix[ID_index][4])

        if(msg_counter > reply_after - 1):
            text = select_text()
            bot.send_message(message.chat.id, text, parse_mode="Markdown")
            msg_counter = 0 + random_variation
            random_variation = random.randint(-max_random_variation, max_random_variation)
            print("random_variation for chat",ID_index,":", random_variation)
            chatID_matrix[ID_index][3] = random_variation
        else:
            msg_counter = msg_counter + 1
        chatID_matrix[ID_index][1] = msg_counter
        save_data(chatID_matrix)
        print("Messages until next reply for chat", ID_index, ":", reply_after - msg_counter)


bot.infinity_polling()