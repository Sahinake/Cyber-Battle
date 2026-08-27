def ler_resposta_sim_nao(mensagem, mensagem_invalida=None):
	while True:
		resposta = input(mensagem).strip().lower()

		if resposta in {"s", "n"}:
			return resposta == "s"

		if mensagem_invalida:
			print(mensagem_invalida)


def ler_numero(mensagem):
	while True:
		try:
			numero = int(input(mensagem))
		except ValueError:
			print("CyberPC: Isso não é um número, humano!")
			continue

		if 1 <= numero <= 20:
			return numero

		print("CyberPC: Escolha um número entre 1 e 20!")
