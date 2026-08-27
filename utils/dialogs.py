import time

# Função para exibir falas de personagens com uma pausa entre elas, simulando uma conversa.
def speak(personagem, texto, tempo=2):

    print(f"{personagem}: {texto}")

    time.sleep(tempo)