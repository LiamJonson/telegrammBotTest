import telebot
import subprocess
import requests
import os
import cv2



TOKEN = '1362451724:AAEVhhYh_FY2ZaLxWMinb7Kz474kfQmAVD4'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}')
    p = file.content
    with open('test.ogg', 'wb') as output:
        output.write(p)
    subprocess.call(['ffmpeg', '-i', 'test.ogg', '-f','wav' ,'-ar', '16000','ffff.wav'])
    os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.ogg'))


bot.polling(none_stop=True)