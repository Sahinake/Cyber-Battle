from pathlib import Path

from pygame import mixer


class AudioManager:

    def __init__(self):
        mixer.init()

    def tocar(self, arquivo, loops=0):
        caminho = Path(__file__).parent.parent / "assets" / "sounds" / arquivo
        mixer.music.load(caminho)

        mixer.music.play(loops)

    def parar(self):

        mixer.music.stop()