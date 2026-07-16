
import pyttsx3

engine = pyttsx3.init()

engine.setProperty("rate", 170)


text = 'какая погода в Москве?, Сегодня сьел ананас'
name_fail = 'test_4'
path_name = f'temp/{name_fail}.mp3'


engine.save_to_file(text, path_name)
engine.runAndWait()

print("Готово!")