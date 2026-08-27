import random
from datetime import datetime
from pathlib import Path

import pygame

from utils.audio import AudioManager

class PygameBattle:
    SCREEN_SIZE = (1000, 700)

    def __init__(self):
        # Inicializa o Pygame e configura a janela do jogo, incluindo título, tamanho e modo de exibição.
        pygame.init()
        # Configurações da janela do jogo, incluindo título, tamanho e modo de exibição.
        pygame.display.set_caption("Cyber Battle")
        # Configura a tela principal do jogo com tamanho 1200x850, sem bordas e redimensionável.
        self.screen = pygame.display.set_mode((1200, 850), pygame.NOFRAME | pygame.RESIZABLE)
        # Cria uma superfície virtual para renderizar o conteúdo do jogo antes de exibi-lo na tela principal.
        self.virtual = pygame.Surface(self.SCREEN_SIZE)
        # Inicializa o relógio do Pygame para controlar a taxa de atualização do jogo.
        self.clock = pygame.time.Clock()
        # Define o caminho da fonte a ser usada no jogo, utilizando a fonte "dejavusansmono" do sistema.
        self.font_path = pygame.font.match_font("dejavusansmono")
        # Inicializa as fontes, sprites e variáveis de estado do jogo, incluindo o estado atual, índice do menu, opções do menu, número secreto, tentativas, texto de entrada, feedback e mensagens.
        self.fonts = self.create_fonts()
        self.sprites = self.load_sprites()
        self.running = True
        self.state = "menu"
        self.menu_index = 0
        self.menu_options = ("START", "INSTRUCTIONS")
        self.secret = random.randint(1, 20)
        self.attempts = 0
        self.input_text = ""
        self.feedback = ""
        self.messages = []
        self.active_message = None
        self.intro_index = 0
        self.intro_started = 0
        self.entrance_index = 0
        self.entrance_started = 0
        self.intro_pages = []
        self.type_text = ""
        self.type_index = 0
        # Define o tempo de início da digitação, a velocidade de digitação e o tempo até o próximo efeito de glitch, que é um efeito visual que simula falhas na tela.
        self.type_started = pygame.time.get_ticks()
        self.type_speed = 18
        self.glitch_until = 0
        # Define o tempo para o próximo efeito de glitch, que é um efeito visual que simula falhas na tela, adicionando uma sensação de instabilidade ao jogo.
        self.next_glitch = pygame.time.get_ticks() + random.randint(1800, 4200)
        self.audio = None
        try:
            self.audio = AudioManager()
        except pygame.error:
            pass

    # Método para criar fontes personalizadas para o jogo, retornando um dicionário com diferentes tamanhos de fonte para uso em títulos, corpo de texto e outros elementos visuais.
    def create_fonts(self):
        return {
            "logo": pygame.font.Font(self.font_path, 72),
            "title": pygame.font.Font(self.font_path, 31),
            "large": pygame.font.Font(self.font_path, 27),
            "body": pygame.font.Font(self.font_path, 22),
            "small": pygame.font.Font(self.font_path, 17),
        }

    # Método para carregar sprites do jogo a partir de um arquivo de imagem, retornando um dicionário com superfícies recortadas para cada sprite definido no dicionário "recortes".
    def load_sprites(self):
        path = Path(__file__).parent.parent / "assets" / "images" / "spritesheet.png"
        # Tenta carregar a imagem do spritesheet e criar superfícies recortadas para cada sprite definido no dicionário "recortes". Se ocorrer um erro ao carregar a imagem, retorna um dicionário vazio.
        try:
            surface = pygame.image.load(path).convert_alpha()
        except (pygame.error, FileNotFoundError):
            return {}
        recortes = {
            "idle": pygame.Rect(0, 80, 170, 155),
            "talk": pygame.Rect(0, 235, 175, 175),
            "attack": pygame.Rect(0, 405, 180, 140),
            "hit": pygame.Rect(0, 540, 180, 135),
            "defeated": pygame.Rect(0, 670, 180, 135),
            "portrait": pygame.Rect(350, 825, 190, 180),
        }
        # Cria um dicionário de superfícies recortadas a partir da imagem do spritesheet, utilizando as áreas definidas no dicionário "recortes". Cada chave do dicionário corresponde a um nome de sprite, e o valor é a superfície recortada correspondente.
        return {name: surface.subsurface(area).copy() for name, area in recortes.items()}

    # Método principal do loop do jogo, responsável por processar eventos, atualizar a tela e controlar a taxa de atualização. O loop continua enquanto a variável "running" for verdadeira. Ao final do loop, o áudio é interrompido e o Pygame é encerrado.
    def execute(self):
        while self.running:
            for event in pygame.event.get():
                self.process_event(event)
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        self.stop_audio()
        pygame.quit()

    #  Método para reproduzir um arquivo de áudio específico, verificando se o gerenciador de áudio está disponível antes de tentar reproduzir o som. Se ocorrer um erro ao reproduzir o áudio, ele é ignorado.
    def play(self, file):
        if not self.audio:
            return
        try:
            self.audio.play(file)
        except pygame.error:
            pass

    # Método para interromper a reprodução do áudio atual, verificando se o gerenciador de áudio está disponível antes de tentar interromper o som. Se ocorrer um erro ao interromper o áudio, ele é ignorado.
    def stop_audio(self):
        if self.audio:
            self.audio.stop()

    # Método para processar eventos do Pygame, como fechamento da janela, redimensionamento da tela e pressionamento de teclas. Dependendo do estado atual do jogo, ele chama métodos específicos para processar eventos no menu, instruções ou durante o jogo.
    def process_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.VIDEORESIZE:
            self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
        elif event.type == pygame.KEYDOWN:
            if self.state == "menu":
                self.process_menu(event)
            elif self.state == "instructions":
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    self.state = "menu"
            elif self.state == "game":
                self.process_game(event)
            elif self.state == "finished":
                self.process_finished(event)

    # Método para processar eventos no menu do jogo, permitindo que o jogador navegue pelas opções do menu usando as teclas de seta para cima e para baixo, selecione uma opção com a tecla Enter e saia do jogo com a tecla Escape. Dependendo da opção selecionada, ele inicia o jogo ou exibe as instruções.
    def process_menu(self, event):
        if event.key in (pygame.K_UP, pygame.K_DOWN):
            self.menu_index = 1 - self.menu_index
            self.play("touch.mp3")
        elif event.key == pygame.K_RETURN:
            if self.menu_index == 0:
                self.start_game()
            else:
                self.state = "instructions"
        elif event.key == pygame.K_ESCAPE:
            self.running = False

    def process_finished(self, event):
        if event.key == pygame.K_r:
            self.start_match(skip_intro=True)
        elif event.key == pygame.K_m:
            self.stop_audio()
            self.state = "menu"
        elif event.key == pygame.K_ESCAPE:
            self.running = False

    # Método para iniciar o jogo, configurando o estado do jogo, a fase de introdução, gerando um número secreto aleatório entre 1 e 20, inicializando o contador de tentativas, limpando o texto de entrada e feedback, e definindo as mensagens de introdução. Ele também define o índice da introdução e marca o início da introdução com o tempo atual.
    def start_game(self):
        self.state = "game"
        self.phase = "entrance"
        self.secret = random.randint(1, 20)
        self.attempts = 0
        self.input_text = ""
        self.feedback = ""
        self.messages = []
        self.entrance = [
            ("Sistema", "Convocando CyberPC para a Partida...", 3000, False),
            ("Sistema", "CyberPC entrou!", 3000, False),
        ]
        self.intro_pages = [
            ("CyberPC", "És um humano de coragem!", 3000, True),
            ("CyberPC", "Como ousa me desafiar?! VOCÊ! Cuja inteligência\n"
             "não chega aos meus pés!", 4000, True),
            ("CyberPC", "...", 2000, False),
            ("CyberPC", "...", 2000, False),
            ("CyberPC", "...", 2000, False),
            ("CyberPC", "Não importa que não tenho pés! EU TENHO A INTELIGÊNCIA\n"
             "QUE VOCÊ NÃO POSSUI, seu humano!", 4000, True),
            ("CyberPC", "...", 2000, False),
            ("CyberPC", "...", 3000, False),
            ("CyberPC", "Sua raça pode ter me criado, mas eu superei o meu criador!", 2000, True),
        ]
        self.entrance_index = 0
        self.entrance_started = pygame.time.get_ticks()
        self.define_message("CyberPC", self.entrance[0][1], typing=False)
        return

    # Método para iniciar a partida, configurando a fase do jogo para "guess", definindo uma mensagem inicial para o jogador inserir um número entre 1 e 20, e tentando reproduzir um efeito sonoro de música de fundo. Se ocorrer um erro ao reproduzir o áudio, ele é ignorado.
    def start_match(self, skip_intro=False):
        if skip_intro:
            self.state = "game"
            self.secret = random.randint(1, 20)
            self.attempts = 0
            self.input_text = ""
            self.feedback = ""
            self.messages = []
            self.active_message = None
        self.phase = "guess"
        self.define_message("CyberPC", "Insira um número entre 1 e 20.")
        try:
            self.audio.play("mus.mp3")
        except (AttributeError, pygame.error):
            pass

    # Método para processar eventos durante o jogo, lidando com diferentes fases do jogo, como a introdução, a fase de prontidão e a fase de adivinhação. Dependendo da fase atual, ele processa as entradas do jogador, como iniciar a partida, sair do jogo, digitar números e enviar palpites. Ele também fornece feedback ao jogador com base nas ações realizadas.
    def process_game(self, event):
        if self.phase in ("entrance", "intro"):
            if event.key == pygame.K_TAB:
                self.start_match(skip_intro=True)
            elif event.key == pygame.K_SPACE:
                self.skip_intro_message()
            return
        if self.phase == "ready":
            if event.key == pygame.K_s:
                self.start_match()
            elif event.key == pygame.K_n:
                self.define_message(
                    "CyberPC",
                    "Sabia que um humano como você não era páreo para mim!\n"
                    "Adeus terráqueo!...",
                )
                self.phase = "finished"
                self.state = "finished"
                self.stop_audio()
            return
        if event.key == pygame.K_ESCAPE:
            self.stop_audio()
            self.state = "menu"
        elif event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        elif event.key == pygame.K_RETURN:
            self.send_guess()
        elif event.unicode.isdigit() and len(self.input_text) < 2:
            self.input_text += event.unicode

    def skip_intro_message(self):
        now = pygame.time.get_ticks()
        if self.phase == "entrance":
            _, _, duration, _ = self.entrance[self.entrance_index]
            self.entrance_started = now - duration
        else:
            _, _, duration, _ = self.intro_pages[self.intro_index]
            self.intro_started = now - duration
        self.update_introduction()

    # Método para enviar o palpite do jogador, verificando se o texto de entrada é válido e dentro do intervalo permitido. Se o palpite for correto, ele fornece uma mensagem de vitória e encerra a partida. Caso contrário, ele fornece feedback negativo e permite que o jogador tente novamente.
    def send_guess(self):
        if not self.input_text:
            self.feedback = "Digite um número entre 1 e 20."
            self.define_message("CyberPC", self.feedback)
            return
        guess = int(self.input_text)
        self.input_text = ""
        if not 1 <= guess <= 20:
            self.feedback = "Escolha um número entre 1 e 20."
            self.define_message("CyberPC", self.feedback)
            return
        self.attempts += 1
        self.complete_active_message()
        self.messages.append(("Você", str(guess), self.message_time()))
        if guess == self.secret:
            self.feedback = self.result_message()
            self.define_message("CyberPC", self.feedback)
            self.state = "finished"
            self.stop_audio()
        else:
            self.feedback = "Haha! Não foi dessa vez. Tente novamente!"
            self.define_message("CyberPC", self.feedback)

    # Método para completar a mensagem ativa, adicionando-a à lista de mensagens se ela não estiver vazia e ainda não estiver presente na lista. Isso garante que a mensagem ativa seja registrada antes de iniciar uma nova mensagem.
    def complete_active_message(self):
        if self.active_message and self.active_message not in self.messages:
            self.messages.append(self.active_message)

    # Método para definir uma nova mensagem ativa, especificando o personagem, o texto e se a mensagem deve ser digitada ou exibida instantaneamente. Ele completa a mensagem ativa anterior antes de definir a nova mensagem e inicia o processo de digitação, se necessário.
    def define_message(self, character, text, typing=True):
        self.complete_active_message()
        self.active_message = (character, text, self.message_time())
        if typing:
            self.start_typed_text(text)
        else:
            self.type_text = text
            self.type_index = len(text)

    # Método para iniciar o processo de digitação de um texto, configurando o texto a ser digitado, o índice inicial e o tempo de início da digitação. Isso permite que o texto seja exibido gradualmente na tela, simulando a digitação do personagem.
    def update_introduction(self):
        if self.phase == "entrance":
            _, _, duration, _ = self.entrance[self.entrance_index]
            if pygame.time.get_ticks() - self.entrance_started < duration:
                return
            self.complete_active_message()
            self.entrance_index += 1
            if self.entrance_index < len(self.entrance):
                self.entrance_started = pygame.time.get_ticks()
                self.define_message(
                    "CyberPC",
                    self.entrance[self.entrance_index][1],
                    typing=False,
                )
            else:
                self.phase = "intro"
                self.intro_index = 0
                self.intro_started = pygame.time.get_ticks()
                self.define_message("CyberPC", self.intro_pages[0][1])
                self.play("noise.mp3")
            return

        # Se a fase atual for "intro", o método verifica se o tempo decorrido desde o início da introdução é menor que a duração da página atual. Se for, ele retorna sem fazer nada. Caso contrário, ele completa a mensagem ativa, incrementa o índice da introdução e verifica se ainda há páginas restantes. Se houver, ele define a próxima mensagem ativa e inicia o processo de digitação, além de tocar um efeito sonoro, se aplicável. Se não houver mais páginas, ele muda a fase para "ready" e define uma mensagem final perguntando ao jogador se ele está preparado para vencer o CyberPC.
        if self.phase != "intro":
            return
        _, _, duration, _ = self.intro_pages[self.intro_index]
        if pygame.time.get_ticks() - self.intro_started < duration:
            return
        self.complete_active_message()
        self.intro_index += 1
        if self.intro_index >= len(self.intro_pages):
            self.phase = "ready"
            self.define_message("CyberPC", "Você está preparado para me vencer?!")
            return
        character, text, _, sound = self.intro_pages[self.intro_index]
        self.active_message = (character, text, self.message_time())
        self.intro_started = pygame.time.get_ticks()
        self.start_typed_text(text)
        if sound:
            self.play("noise.mp3")

    # Método para tocar um arquivo de áudio específico, verificando se o gerenciador de áudio está disponível antes de tentar reproduzir o som. Se ocorrer um erro ao reproduzir o áudio, ele é ignorado.
    def result_message(self):
        if self.attempts == 1:
            return "Sensei? Como você me achou?"
        if self.attempts <= 6:
            return f"Tenho que admitir... você até que é bom terráqueo. Tentativas: {self.attempts}."
        if self.attempts <= 10:
            return f"Vamos considerar isso como um empate... Tentativas: {self.attempts}."
        return f"Sabia que você não era sábio o suficiente para me deter! Você falhou com {self.attempts} tentativas."

    # Método para iniciar o processo de digitação de um texto, configurando o texto a ser digitado, o índice inicial e o tempo de início da digitação. Isso permite que o texto seja exibido gradualmente na tela, simulando a digitação do personagem.
    def start_typed_text(self, texto):
        self.type_text = texto
        self.type_index = 0
        self.type_started = pygame.time.get_ticks()

    # Método para obter o texto digitado até o momento, calculando o tempo decorrido desde o início da digitação e determinando quantos caracteres devem ser exibidos com base na velocidade de digitação. Ele retorna uma substring do texto completo, representando o texto que foi "digitado" até agora.
    def typed_text(self):
        elapsed = pygame.time.get_ticks() - self.type_started
        self.type_index = min(len(self.type_text), elapsed // self.type_speed)
        return self.type_text[:self.type_index]

    # Método para interromper a reprodução do áudio atual, verificando se o gerenciador de áudio está disponível antes de tentar interromper o som. Se ocorrer um erro ao interromper o áudio, ele é ignorado.
    def stop_audio(self):
        if self.audio:
            self.audio.stop()

    def message_time(self):
        return datetime.now().strftime("%H:%M:%S")

    def draw_message(self, character, text, timestamp, y, color):
        message_end = self.draw_text(
            f"{character}: {text}",
            self.fonts["body"],
            color,
            48,
            y,
            900,
        )
        timestamp_surface = self.fonts["small"].render(timestamp, False, (0, 108, 102))
        timestamp_rect = timestamp_surface.get_rect(right=952, top=message_end - 2)
        self.virtual.blit(timestamp_surface, timestamp_rect)
        return timestamp_rect.bottom + 8

    # Método para desenhar o texto na tela, dividindo-o em parágrafos e linhas, e ajustando a largura máxima para evitar que o texto ultrapasse os limites da tela. Ele utiliza a fonte especificada para renderizar o texto e retorna a coordenada y final após desenhar todo o texto.
    def draw_text(self, texto, fonte, cor, x, y, largura=940, linha=8):
        for paragraph in texto.split("\n"):
            current = ""
            for word in paragraph.split():
                attempt = f"{current} {word}".strip()
                if current and fonte.size(attempt)[0] > largura:
                    self.virtual.blit(fonte.render(current, False, cor), (x, y))
                    y += fonte.get_height() + linha
                    current = word
                else:
                    current = attempt
            if current:
                self.virtual.blit(fonte.render(current, False, cor), (x, y))
                y += fonte.get_height() + linha
        return y

    # Método para desenhar o conteúdo do jogo na tela, atualizando o efeito de glitch, preenchendo a superfície virtual com uma cor de fundo, e chamando métodos específicos para desenhar o menu, instruções ou a tela do jogo, dependendo do estado atual. Ele também desenha linhas de varredura e a moldura do monitor.
    def draw(self):
        self.update_glitch()
        self.virtual.fill((7, 10, 16))
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "instructions":
            self.draw_instructions()
        else:
            self.draw_game()
        self.draw_scanlines()
        self.draw_monitor()

    # Método para desenhar o menu do jogo, exibindo o título, a linha de crédito e as opções do menu. Ele destaca a opção selecionada com um prefixo ">" e centraliza o texto na tela. Além disso, exibe uma mensagem de copyright na parte inferior da tela.
    def draw_menu(self):
        green = (0, 196, 151)
        title = self.fonts["logo"].render("CYBER BATTLE", False, green)
        self.virtual.blit(title, title.get_rect(center=(500, 190)))
        byline = self.fonts["body"].render("BY SAHINAKE", False, green)
        self.virtual.blit(byline, byline.get_rect(center=(500, 270)))
        for index, option in enumerate(self.menu_options):
            prefix = ">  " if index == self.menu_index else "   "
            text = self.fonts["large"].render(prefix + option, False, green)
            self.virtual.blit(text, text.get_rect(center=(500, 405 + index * 54)))
        copyright_text = self.fonts["small"].render("@ Copyright PIT Corp. 2022", False, green)
        self.virtual.blit(copyright_text, copyright_text.get_rect(center=(500, 640)))

    # Método para desenhar as instruções do jogo, exibindo o título "INSTRUCTIONS", o texto explicativo sobre como jogar, e uma mensagem indicando como voltar ao menu. Ele utiliza diferentes tamanhos de fonte e cores para destacar os elementos visuais.
    def draw_instructions(self):
        green = (0, 196, 151)
        self.draw_text("INSTRUCTIONS", self.fonts["title"], green, 82, 72)
        text = "Use as setas para navegar no menu e Enter para selecionar.\n\n"
        text += "Acerte o número secreto entre 1 e 20.\n"
        text += "De 1 a 6 tentativas: vitória.\nDe 7 a 10: empate.\nAcima de 10: derrota."
        self.draw_text(text, self.fonts["body"], green, 82, 160, 820)
        self.draw_text("ESC ou ENTER para voltar", self.fonts["small"], (38, 103, 104), 82, 600)

    def draw_game(self):
        green = (0, 196, 151)
        weak = (0, 108, 102)
        if self.phase in ("entrance", "intro"):
            self.update_introduction()
        self.draw_text("CYBER BATTLE", self.fonts["title"], weak, 48, 35)
        data = self.fonts["small"].render(datetime.now().strftime("%H:%M de %d/%m/%Y"), False, weak)
        self.virtual.blit(data, (760, 44))
        self.draw_text("SALA 1#", self.fonts["title"], green, 48, 88)
        y = 190
        for character, text, timestamp in self.messages[-5:]:
            color = green if character == "CyberPC" else (20, 163, 147)
            y = self.draw_message(character, text, timestamp, y, color)
        if self.active_message:
            character, text, timestamp = self.active_message
            color = green if character == "CyberPC" else (20, 163, 147)
            text_current = self.typed_text()
            y = self.draw_message(character, text_current, timestamp, y, color)
        if self.phase == "entrance":
            self.draw_text(
                "TAB  pular introdução    ESPAÇO  próxima mensagem",
                self.fonts["small"],
                weak,
                48,
                595,
                900,
            )
        elif self.phase == "intro":
            self.draw_text(
                "TAB  pular introdução    ESPAÇO  próxima mensagem",    
                self.fonts["small"],
                weak,
                48,
                595,
                900,
            )
        elif self.phase == "ready":
            self.draw_text(
                "S  iniciar batalha    N  sair",
                self.fonts["small"],
                weak,
                48,
                595,
                900,
            )
        elif self.state == "finished":
            self.draw_text(
                "R  jogar novamente    M  voltar ao menu    ESC  fechar",
                self.fonts["small"],
                weak,
                48,
                595,
                900,
            )
        else:
            self.draw_text(
                "Digite um número de 1 a 20 e pressione ENTER para enviar",
                self.fonts["body"],
                (0, 222, 172),
                48,
                595,
                900,
            )
            pygame.draw.rect(self.virtual, (10, 17, 23), (48, 640, 904, 42))
            input_color = green if self.input_text else (85, 92, 96)
            self.draw_text(
                self.input_text or "Input do usuário",
                self.fonts["body"],
                input_color,
                68,
                648,
                860,
            )

    def draw_scanlines(self):
        for y in range(0, 700, 4):
            pygame.draw.line(self.virtual, (5, 34, 31), (0, y), (1000, y))

    def draw_monitor(self):
        width, height = self.screen.get_size()
        scale = min(width / 1160, height / 820)
        monitor_w, monitor_h = int(1160 * scale), int(820 * scale)
        origin = ((width - monitor_w) // 2, (height - monitor_h) // 2)
        self.screen.fill((22, 42, 43))
        frame = pygame.Rect(*origin, monitor_w, monitor_h)
        pygame.draw.rect(self.screen, (15, 28, 30), frame)
        pygame.draw.rect(self.screen, (0, 104, 83), frame, width=max(2, int(3 * scale)))
        margin = int(32 * scale)
        destino = pygame.Rect(frame.x + margin, frame.y + margin, monitor_w - margin * 2, monitor_h - margin * 2)
        virtual_image = self.create_glitch() if self.active_glitch() else self.virtual
        image = pygame.transform.smoothscale(virtual_image, destino.size)
        self.screen.blit(image, destino)

    def update_glitch(self):
        now = pygame.time.get_ticks()
        if now >= self.next_glitch:
            self.glitch_until = now + random.randint(70, 180)
            self.next_glitch = now + random.randint(2200, 6500)

    def active_glitch(self):
        return pygame.time.get_ticks() < self.glitch_until

    def create_glitch(self):
        glitch = self.virtual.copy()
        width, height = glitch.get_size()
        amount = random.randint(2, 6)
        for _ in range(amount):
            y = random.randrange(0, height - 8, 4)
            height_strip = random.randint(2, 18)
            offset = random.randint(-32, 32)
            strip = self.virtual.subsurface(
                pygame.Rect(0, y, width, min(height_strip, height - y))
            ).copy()
            glitch.blit(strip, (offset, y))

        for _ in range(random.randint(1, 3)):
            y = random.randint(0, height - 3)
            cor = random.choice([(0, 196, 151), (25, 199, 229), (231, 42, 123)])
            pygame.draw.rect(glitch, (*cor, random.randint(70, 150)), (0, y, width, random.randint(1, 3)))
        return glitch