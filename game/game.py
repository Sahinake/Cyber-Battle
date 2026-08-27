import random

from game.player import Player
from game.cyberpc import CyberPC
from utils.dialogs import falar
from utils.input_handler import ler_resposta_sim_nao


class MentalBattle:

    def __init__(self):
        self.player = Player()
        self.cyberpc = CyberPC()
        self.audio = None
        self.numero_secreto = None
        self.tentativas = 0

    def iniciar(self):
        self.mostrar_titulo()
        self.mostrar_instrucoes()

        if not self.cyberpc.introducao():
            return

        self.audio = self.cyberpc.audio
        self.audio.tocar("mus.mp3", loops=3)
        self.iniciar_batalha()
        self.audio.parar()
        print("CyberPC deixou a sala!")

    def mostrar_titulo(self):
        print("{:=^25}".format(" Mental Battle "))

    def mostrar_instrucoes(self):
        quer_instrucoes = ler_resposta_sim_nao(
            "Antes do jogo começar, gostaria de ver as instruções? [S/N] ",
            "Responda apenas com [S/N]",
        )
        if not quer_instrucoes:
            return

        print("{:=^35}".format(" Instruções Sobre o Jogo "))
        print(
            """
            Você está duelando com CyberPC! Um computador convencido e 
            arrogante que não aceita perder. Ele pensará em um número 
            de 1 à 20 aleatoriamente, e você deve acertar esse número. 

            A tabela de classificação é a seguinte:
            De 1 à 6 tentativas = Vitória!
            De 6 á 10 tentativas = Empate.
            De 10 tentativas para cima: Derrota!
            """
        )
        input("Aperte Enter para prosseguir... ")

    def gerar_numero(self):
        self.numero_secreto = random.randint(1, 20)

    def iniciar_batalha(self):
        self.gerar_numero()

        while True:
            palpite = self.player.escolher_numero()

            self.tentativas += 1

            if palpite == self.numero_secreto:
                break

            self.cyberpc.responder_erro()

        self.mostrar_resultado()

    def mostrar_resultado(self):

        if self.tentativas == 1:
            print("CyberPC: Sensei? Como você me achou?")
            print("Você acertou com 1 tentativa!")

        elif self.tentativas <= 6:
            self.cyberpc.vitoria_jogador()

            print(
                f"Suas tentativas foram {self.tentativas}."
            )

        elif self.tentativas <= 10:
            print(
                "CyberPC: Vamos considerar isso como um empate..."
            )

            print(
                f"Suas tentativas foram {self.tentativas}."
            )

        else:
            print(
                "CyberPC: Sabia que você não era sábio "
                "o suficiente para me deter!"
            )

            print(
                f"Você falhou com {self.tentativas} tentativas!"
            )