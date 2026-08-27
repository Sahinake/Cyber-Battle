import time

# Importações de módulos personalizados do projeto
from utils.audio import AudioManager
from utils.dialogs import speak
from utils.input_handler import read_answer_yes_no


class CyberPC:
    """
    Classe que representa o personagem CyberPC no jogo.
    Controla a introdução, respostas e interações do personagem com o jogador.
    """

    def introduction(self):
        """
        Sequência de apresentação do personagem CyberPC, incluindo falas e efeitos sonoros.
        Retorna True se o jogador estiver preparado para enfrentar o CyberPC, caso contrário retorna False.
        """

        # Efeito de "chamada" do sistema, com pausas para criar suspense
        print("Convocando CyberPC para a Partida...")
        time.sleep(3)
        print("CyberPC entrou!")
        time.sleep(3)

        # Inicializa o gerenciador de áudio e toca um efeito sonoro
        self.audio = AudioManager()
        self.audio.play("noise.mp3")
        print("CyberPC: És um humano de coragem!")
        time.sleep(3)

        # Sequência de falas provocativas do CyberPC, com pausas dramáticas
        self.audio.play("noise.mp3")
        print("CyberPC: Como ousa me desafiar?! VOCÊ! Cuja inteligência")
        print("não chega aos meus pés!")
        time.sleep(4)
        print("...")
        time.sleep(2)
        print("...")
        time.sleep(2)
        print("...")
        time.sleep(2)

        # Continuando a provocação do CyberPC, enfatizando sua superioridade
        self.audio.play("noise.mp3")
        print("CyberPC: Não importa que não tenho pés! EU TENHO A INTELIGÊNCIA")
        print("QUE VOCÊ NÃO POSSUI, seu humano!")
        time.sleep(4)
        print("...")
        time.sleep(2)
        print("...")
        time.sleep(3)

        # Finalizando a introdução com uma provocação e perguntando se o jogador está preparado
        self.audio.play("noise.mp3")
        print("CyberPC: Sua raça pode ter me criado, mas eu superei o meu criador!")
        time.sleep(2)
        self.audio.play("noise.mp3")

        # Pergunta ao jogador se ele está pronto para enfrentar o CyberPC
        ready = read_answer_yes_no(
            "CyberPC: Você está preparado para me vencer?! [S/N] ",
            "CyberPC: Você não vai com a minha cara?\n"
            "Responda apenas >>> [S/N]",
        )

        # Se o jogador não estiver pronto, o CyberPC faz uma última provocação e o áudio é interrompido
        if not ready:
            print(
                "CyberPC: Sabia que um humano como você não era páreo para mim!\n"
                "                Adeus terráqueo!..."
            )
            self.audio.stop()

        return ready

    def answer_error(self):
        speak("CyberPC", "Haha! Não foi dessa vez! Tente novamente!")

    def provoke(self):
        speak("CyberPC", "Como ousa me desafiar?!")

    def player_wins(self):
        speak("CyberPC", "Tenho que admitir... você até que é bom.")