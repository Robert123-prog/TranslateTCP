import socket
import os
from googletrans import Translator

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 6666))
s.listen()

languages = {}
with open('languages', 'r', encoding='utf-8') as f:
    for line in f:
        # dai split dupa space => lista
        parts = line.split()
        language_name = ' '.join(parts[:-1])
        abbreviation = parts[-1] #ultimu part din rand = abrevierea
        languages[language_name] = abbreviation

translator = Translator()

while True:
    cs, addr = s.accept()

    if os.fork() == 0:
        # inchizi socketu "parent"
        s.close()

        try:
            # trebe decodat
            phrase = cs.recv(1000).decode('utf-8')

            print('Please use one of the following abbreviations: ')
            print(languages)
            language_to_translate_to = input('Enter the language code to translate to: ')

            detected = translator.detect(phrase)
            translation = translator.translate(phrase, src=detected.lang, dest=language_to_translate_to)

            cs.send(translation.text.encode('utf-8'))  # encodezi la loc
        except Exception as e:
            print('Error during translation')
        finally:
            cs.close()
            os._exit(0)
    else:
        cs.close()

#s.listen()
# cs, addr = s.accept()
#
# phrase = cs.recv(1000).decode('utf-8') #trebe decodat
#
#
# print('Please use one of the following abbreviations: ')
# print(languages)
# language_to_translate_to = input('Enter the language code to translate to: ')
#
#
# detected = translator.detect(phrase)
# translation = translator.translate(phrase, src=detected.lang, dest=language_to_translate_to)
#
# cs.send(translation.text.encode('utf-8'))  # encodezi la loc
#
# cs.close()