from utils.input_handler import read_number

# Função para ler um número inteiro do usuário, garantindo que esteja entre 1 e 20. Se a entrada for inválida, exibe uma mensagem de erro e solicita novamente.
class Player:

    def pick_number(self):
        return read_number("CyberPC: Insira o seu número: ")