from pathlib import Path

from pygame import mixer


class AudioManager:
    # Classe responsável por gerenciar a reprodução de efeitos sonoros no jogo.
    def __init__(self):
        mixer.init()

    # Método para reproduzir um arquivo de áudio específico, com a opção de repetir o som várias vezes.
    def play(self, arquivo, loops=0):
        path = Path(__file__).parent.parent / "assets" / "sounds" / arquivo
        mixer.music.load(path)

        mixer.music.play(loops)

    # Método para interromper a reprodução do áudio atual.
    def stop(self):

        mixer.music.stop()