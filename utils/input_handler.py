# Função para ler uma resposta do usuário, esperando "s" (sim) ou "n" (não). Se a resposta for inválida, exibe uma mensagem de erro opcional e solicita novamente.
def read_answer_yes_no(message, invalid_message=None):
	while True:
		# Solicita a entrada do usuário e remove espaços em branco e converte para minúsculas.
		answer = input(message).strip().lower()

		if answer in {"s", "n"}:
			return answer == "s"

		if invalid_message:
			print(invalid_message)

# Função para ler um número inteiro do usuário, garantindo que esteja entre 1 e 20. Se a entrada for inválida, exibe uma mensagem de erro e solicita novamente.
def read_number(message):
	while True:
		try:
			read_number = int(input(message))
		except ValueError:
			print("CyberPC: Isso não é um número, humano!")
			continue

		if 1 <= read_number <= 20:
			return read_number

		print("CyberPC: Escolha um número entre 1 e 20!")
