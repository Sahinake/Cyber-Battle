import time

def falar(personagem, texto, tempo=2):

    print(f"{personagem}: {texto}")

    time.sleep(tempo)