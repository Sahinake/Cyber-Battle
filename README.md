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
`assets/sounds/`. A interface possui um menu inspirado no prototipo: use as
setas para alternar entre `START` e `INSTRUCTIONS`, e `Enter` para selecionar.
Na partida, digite o palpite e confirme com `Enter`; use `Backspace` para
corrigir e `Esc` para voltar ao menu.

A area interna do monitor usa uma tela virtual de `1000x700` e e escalada para
acompanhar o tamanho da janela.

## Regras

- O numero secreto fica entre 1 e 20.
- De 1 a 6 tentativas: vitoria.
- De 7 a 10 tentativas: empate.
- Acima de 10 tentativas: derrota.

## Estrutura

```text
.
├── assets/sounds/       # Efeitos sonoros
├── assets/images/prints/ # Prototipos das telas
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

`game/old_versions/cyberBattle.py` é a primeira versão do jogo e foi mantido como
referencia. `game/old_versions/terminal_game.py`é a segunda versão do jogo, ainda no terminal. A versão atual e organizada deve ser executada por `main.py`.
