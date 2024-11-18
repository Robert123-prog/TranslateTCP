import socket
import os
from googletrans import Translator
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 6667))
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
    # Accept a client connection
    cs, addr = s.accept()

    # Send the languages dictionary to the client
    try:
        cs.send(json.dumps(languages).encode('utf-8'))  # Convert dict to JSON and send as bytes
    except Exception as e:
        print(f"Error sending languages dictionary: {e}")
        cs.close()
        continue

    # Receive the language abbreviation from the client
    try:
        abbrev = cs.recv(100).decode('utf-8')  # Read the language abbreviation
    except Exception as e:
        print(f"Error receiving abbreviation: {e}")
        cs.close()
        continue

    # Fork the process to handle the client
    pid = os.fork()
    if pid == 0:  # Child process
        # Close the parent socket in the child process
        s.close()

        try:
            # Receive the phrase to translate
            phrase = cs.recv(1000).decode('utf-8')

            # Translate the phrase
            detected = translator.detect(phrase)
            translation = translator.translate(phrase, src=detected.lang, dest=abbrev)

            # Send the translated text back to the client
            cs.send(translation.text.encode('utf-8'))
        except Exception as e:
            print(f"Error during translation: {e}")
        finally:
            # Close the client socket and exit the child process
            cs.close()
            os._exit(0)
    else:
        # Close the client socket in the parent process
        cs.close()


