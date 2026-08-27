# Cyber-Battle

Jogo de adivinhacao em Python no qual o jogador enfrenta o CyberPC em uma
interface grafica feita com pygame. O computador escolhe um numero entre 1 e
20, e o jogador tenta descobri-lo.

## Requisitos

- Python 3.10 ou superior
- pygame

## Instalacao

Clone o repositorio e crie um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Execucao

Com o ambiente virtual ativado, execute:

```bash
python3 main.py
```

O jogo reproduz sons durante a introducao e usa os arquivos em
`assets/sounds/`. Na interface, use `S` e `N` para responder, `Enter` para
confirmar telas e palpites, e `Backspace` para corrigir o numero digitado.

## Regras

- O numero secreto fica entre 1 e 20.
- De 1 a 6 tentativas: vitoria.
- De 7 a 10 tentativas: empate.
- Acima de 10 tentativas: derrota.

## Estrutura

```text
.
├── assets/sounds/       # Efeitos sonoros
├── game/
│   ├── cyberpc.py       # Dialogos e comportamento do CyberPC
│   ├── game.py          # Fluxo da partida em modo texto
│   ├── pygame_game.py   # Interface grafica e eventos
│   └── player.py        # Entrada e validacao dos palpites
├── utils/
│   ├── audio.py         # Gerenciamento de audio
│   ├── dialogs.py       # Falas com pausas
│   └── input_handler.py # Validacao das entradas
├── main.py              # Ponto de entrada
└── requirements.txt     # Dependencias
```

`game/old_versions/cyberBattle.py` e a primeira versao do jogo e foi mantido como
referencia. A versao organizada deve ser executada por `main.py`.
