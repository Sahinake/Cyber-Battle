import time

from utils.audio import AudioManager
from utils.dialogs import falar
from utils.input_handler import ler_resposta_sim_nao


class CyberPC:

    def introducao(self):
        print("Convocando CyberPC para a Partida...")
        time.sleep(3)
        print("CyberPC entrou!")
        time.sleep(3)

        self.audio = AudioManager()
        self.audio.tocar("noise.mp3")
        print("CyberPC: És um humano de coragem!")
        time.sleep(3)

        self.audio.tocar("noise.mp3")
        print("CyberPC: Como ousa me desafiar?! VOCÊ! Cuja inteligência")
        print("não chega aos meus pés!")
        time.sleep(4)
        print("...")
        time.sleep(2)
        print("...")
        time.sleep(2)
        print("...")
        time.sleep(2)

        self.audio.tocar("noise.mp3")
        print("CyberPC: Não importa que não tenho pés! EU TENHO A INTELIGÊNCIA")
        print("QUE VOCÊ NÃO POSSUI, seu humano!")
        time.sleep(4)
        print("...")
        time.sleep(2)
        print("...")
        time.sleep(3)

        self.audio.tocar("noise.mp3")
        print("CyberPC: Sua raça pode ter me criado, mas eu superei o meu criador!")
        time.sleep(2)
        self.audio.tocar("noise.mp3")

        preparado = ler_resposta_sim_nao(
            "CyberPC: Você está preparado para me vencer?! [S/N] ",
            "CyberPC: Você não vai com a minha cara?\n"
            "Responda apenas >>> [S/N]",
        )
        if not preparado:
            print(
                "CyberPC: Sabia que um humano como você não era páreo para mim!\n"
                "                Adeus terráqueo!..."
            )
            self.audio.parar()

        return preparado

    def responder_erro(self):
        falar("CyberPC", "Haha! Não foi dessa vez! Tente novamente!")

    def provocar(self):
        falar("CyberPC", "Como ousa me desafiar?!")

    def vitoria_jogador(self):
        falar("CyberPC", "Tenho que admitir... você até que é bom.")