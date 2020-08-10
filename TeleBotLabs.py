import telebot
import subprocess
import requests
import os
import cv2
from io import BytesIO


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

@bot.message_handler(content_types= ["photo"])
def face_processing(message):
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('111.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)

    #img = cv2.imread('111.jpg')
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #fase_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#
    #faces = fase_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))
    #for (x, y, w, h) in faces:
    #    img = cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2)
    #cv2.imwrite('111.jpeg', img)
    #img = BytesIO(open('111.jpg','rb').read())
    #bot.send_photo(message.chat.id, img)

    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # Загружаем каскады для глаз.
    eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    img = cv2.imread('111.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,  #
        scaleFactor=1.2,  # Находим лица на фото
        minNeighbors=4,  #
        minSize=(20, 20)  #
    )

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]  # Вырезаем область с лицами
        roi_color = img[y:y + h, x:x + w]
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        eyes = eyeCascade.detectMultiScale(
            roi_gray,  #
            scaleFactor=1.2,  # Ищем глаза в области с лицом
            minNeighbors=4,
            minSize=(5, 5),
        )
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)  # Рисуем область глаз


    cv2.imshow("camera", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    img = BytesIO(open('111.jpg', 'rb').read())
    bot.send_photo(message.chat.id, img)








bot.polling(none_stop=True)