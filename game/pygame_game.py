import random
from datetime import datetime
from pathlib import Path

import pygame

from utils.audio import AudioManager


class PygameBattle:
    SCREEN_SIZE = (1000, 700)

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Cyber Battle")
        self.screen = pygame.display.set_mode((1200, 850), pygame.NOFRAME | pygame.RESIZABLE)
        self.virtual = pygame.Surface(self.SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.font_path = pygame.font.match_font("dejavusansmono")
        self.fonts = self.criar_fontes()
        self.sprites = self.carregar_sprites()
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
        self.type_started = pygame.time.get_ticks()
        self.type_speed = 18
        self.audio = None
        try:
            self.audio = AudioManager()
        except pygame.error:
            pass

    def criar_fontes(self):
        return {
            "logo": pygame.font.Font(self.font_path, 72),
            "title": pygame.font.Font(self.font_path, 31),
            "large": pygame.font.Font(self.font_path, 27),
            "body": pygame.font.Font(self.font_path, 22),
            "small": pygame.font.Font(self.font_path, 17),
        }

    def carregar_sprites(self):
        caminho = Path(__file__).parent.parent / "assets" / "images" / "spritesheet.png"
        try:
            folha = pygame.image.load(caminho).convert_alpha()
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
        return {nome: folha.subsurface(area).copy() for nome, area in recortes.items()}

    def executar(self):
        while self.running:
            for event in pygame.event.get():
                self.processar_evento(event)
            self.desenhar()
            pygame.display.flip()
            self.clock.tick(60)
        self.parar_audio()
        pygame.quit()

    def tocar(self, arquivo):
        if not self.audio:
            return
        try:
            self.audio.tocar(arquivo)
        except pygame.error:
            pass

    def processar_evento(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.VIDEORESIZE:
            self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
        elif event.type == pygame.KEYDOWN:
            if self.state == "menu":
                self.processar_menu(event)
            elif self.state == "instructions":
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    self.state = "menu"
            elif self.state == "game":
                self.processar_jogo(event)
            elif self.state == "finished" and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                self.running = False

    def processar_menu(self, event):
        if event.key in (pygame.K_UP, pygame.K_DOWN):
            self.menu_index = 1 - self.menu_index
        elif event.key == pygame.K_RETURN:
            if self.menu_index == 0:
                self.iniciar_jogo()
            else:
                self.state = "instructions"
        elif event.key == pygame.K_ESCAPE:
            self.running = False

    def iniciar_jogo(self):
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
        self.definir_mensagem("CyberPC", self.entrance[0][1], digitar=False)
        return

    def iniciar_partida(self):
        self.phase = "guess"
        self.definir_mensagem("CyberPC", "Insira um número entre 1 e 20.")
        try:
            self.audio.tocar("mus.mp3")
        except (AttributeError, pygame.error):
            pass

    def processar_jogo(self, event):
        if self.phase in ("entrance", "intro"):
            return
        if self.phase == "ready":
            if event.key == pygame.K_s:
                self.iniciar_partida()
            elif event.key == pygame.K_n:
                self.definir_mensagem(
                    "CyberPC",
                    "Sabia que um humano como você não era páreo para mim!\n"
                    "Adeus terráqueo!...",
                )
                self.phase = "finished"
                self.state = "finished"
                self.parar_audio()
            return
        if event.key == pygame.K_ESCAPE:
            self.parar_audio()
            self.state = "menu"
        elif event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        elif event.key == pygame.K_RETURN:
            self.enviar_palpite()
        elif event.unicode.isdigit() and len(self.input_text) < 2:
            self.input_text += event.unicode

    def enviar_palpite(self):
        if not self.input_text:
            self.feedback = "Digite um número entre 1 e 20."
            self.definir_mensagem("CyberPC", self.feedback)
            return
        palpite = int(self.input_text)
        self.input_text = ""
        if not 1 <= palpite <= 20:
            self.feedback = "Escolha um número entre 1 e 20."
            self.definir_mensagem("CyberPC", self.feedback)
            return
        self.attempts += 1
        self.concluir_mensagem_ativa()
        self.messages.append(("Você", str(palpite)))
        if palpite == self.secret:
            self.feedback = self.mensagem_resultado()
            self.definir_mensagem("CyberPC", self.feedback)
            self.state = "finished"
            self.parar_audio()
        else:
            self.feedback = "Haha! Não foi dessa vez. Tente novamente!"
            self.definir_mensagem("CyberPC", self.feedback)

    def concluir_mensagem_ativa(self):
        if self.active_message and self.active_message not in self.messages:
            self.messages.append(self.active_message)

    def definir_mensagem(self, personagem, texto, digitar=True):
        self.concluir_mensagem_ativa()
        self.active_message = (personagem, texto)
        if digitar:
            self.iniciar_texto_digitado(texto)
        else:
            self.type_text = texto
            self.type_index = len(texto)

    def atualizar_introducao(self):
        if self.phase == "entrance":
            _, _, duracao, _ = self.entrance[self.entrance_index]
            if pygame.time.get_ticks() - self.entrance_started < duracao:
                return
            self.concluir_mensagem_ativa()
            self.entrance_index += 1
            if self.entrance_index < len(self.entrance):
                self.entrance_started = pygame.time.get_ticks()
                self.definir_mensagem(
                    "CyberPC",
                    self.entrance[self.entrance_index][1],
                    digitar=False,
                )
            else:
                self.phase = "intro"
                self.intro_index = 0
                self.intro_started = pygame.time.get_ticks()
                self.definir_mensagem("CyberPC", self.intro_pages[0][1])
                self.tocar("noise.mp3")
            return

        if self.phase != "intro":
            return
        _, _, duracao, _ = self.intro_pages[self.intro_index]
        if pygame.time.get_ticks() - self.intro_started < duracao:
            return
        self.concluir_mensagem_ativa()
        self.intro_index += 1
        if self.intro_index >= len(self.intro_pages):
            self.phase = "ready"
            self.definir_mensagem("CyberPC", "Você está preparado para me vencer?!")
            return
        personagem, texto, _, tem_som = self.intro_pages[self.intro_index]
        self.active_message = (personagem, texto)
        self.intro_started = pygame.time.get_ticks()
        self.iniciar_texto_digitado(texto)
        if tem_som:
            self.tocar("noise.mp3")

    def mensagem_resultado(self):
        if self.attempts == 1:
            return "Sensei? Como você me achou?"
        if self.attempts <= 6:
            return f"Você venceu. Tentativas: {self.attempts}."
        if self.attempts <= 10:
            return f"Vamos considerar isso como um empate... Tentativas: {self.attempts}."
        return f"Sabia que você não era sábio o suficiente para me deter! Você falhou com {self.attempts} tentativas."

    def iniciar_texto_digitado(self, texto):
        self.type_text = texto
        self.type_index = 0
        self.type_started = pygame.time.get_ticks()

    def texto_digitado(self):
        decorrido = pygame.time.get_ticks() - self.type_started
        self.type_index = min(len(self.type_text), decorrido // self.type_speed)
        return self.type_text[:self.type_index]

    def parar_audio(self):
        if self.audio:
            self.audio.parar()

    def desenhar_texto(self, texto, fonte, cor, x, y, largura=940, linha=8):
        for paragrafo in texto.split("\n"):
            atual = ""
            for palavra in paragrafo.split():
                tentativa = f"{atual} {palavra}".strip()
                if atual and fonte.size(tentativa)[0] > largura:
                    self.virtual.blit(fonte.render(atual, False, cor), (x, y))
                    y += fonte.get_height() + linha
                    atual = palavra
                else:
                    atual = tentativa
            if atual:
                self.virtual.blit(fonte.render(atual, False, cor), (x, y))
                y += fonte.get_height() + linha
        return y

    def desenhar(self):
        self.virtual.fill((7, 10, 16))
        if self.state == "menu":
            self.desenhar_menu()
        elif self.state == "instructions":
            self.desenhar_instrucoes()
        else:
            self.desenhar_jogo()
        self.desenhar_scanlines()
        self.desenhar_monitor()

    def desenhar_menu(self):
        verde = (0, 196, 151)
        titulo = self.fonts["logo"].render("CYBER BATTLE", False, verde)
        self.virtual.blit(titulo, titulo.get_rect(center=(500, 190)))
        byline = self.fonts["body"].render("BY SAHINAKE", False, verde)
        self.virtual.blit(byline, byline.get_rect(center=(500, 270)))
        for indice, opcao in enumerate(self.menu_options):
            prefixo = ">  " if indice == self.menu_index else "   "
            texto = self.fonts["large"].render(prefixo + opcao, False, verde)
            self.virtual.blit(texto, texto.get_rect(center=(500, 405 + indice * 54)))
        copyright_text = self.fonts["small"].render("@ Copyright PIT Corp. 2022", False, verde)
        self.virtual.blit(copyright_text, copyright_text.get_rect(center=(500, 640)))

    def desenhar_instrucoes(self):
        verde = (0, 196, 151)
        self.desenhar_texto("INSTRUCTIONS", self.fonts["title"], verde, 82, 72)
        texto = "Use as setas para navegar no menu e Enter para selecionar.\n\n"
        texto += "Acerte o número secreto entre 1 e 20.\n"
        texto += "De 1 a 6 tentativas: vitória.\nDe 7 a 10: empate.\nAcima de 10: derrota."
        self.desenhar_texto(texto, self.fonts["body"], verde, 82, 160, 820)
        self.desenhar_texto("ESC ou ENTER para voltar", self.fonts["small"], (38, 103, 104), 82, 600)

    def desenhar_jogo(self):
        verde = (0, 196, 151)
        fraco = (0, 108, 102)
        if self.phase in ("entrance", "intro"):
            self.atualizar_introducao()
        self.desenhar_texto("CYBER BATTLE", self.fonts["title"], fraco, 48, 35)
        data = self.fonts["small"].render(datetime.now().strftime("%H:%M de %d/%m/%Y"), False, fraco)
        self.virtual.blit(data, (760, 44))
        self.desenhar_texto("SALA 1#", self.fonts["title"], verde, 48, 88)
        y = 220
        for personagem, texto in self.messages[-5:]:
            cor = verde if personagem == "CyberPC" else (20, 163, 147)
            y = self.desenhar_texto(f"{personagem}: {texto}", self.fonts["body"], cor, 48, y, 900) + 13
        if self.active_message:
            personagem, texto = self.active_message
            cor = verde if personagem == "CyberPC" else (20, 163, 147)
            texto_atual = self.texto_digitado()
            y = self.desenhar_texto(
                f"{personagem}: {texto_atual}",
                self.fonts["body"],
                cor,
                48,
                y,
                900,
            ) + 13
        if self.phase == "entrance":
            self.desenhar_texto(
                "Conectando ao sistema...",
                self.fonts["small"],
                fraco,
                48,
                585,
                900,
            )
        elif self.phase == "intro":
            self.desenhar_texto(
                "S  iniciar batalha    N  sair",
                self.fonts["small"],
                fraco,
                48,
                585,
                900,
            )
        elif self.phase == "ready":
            self.desenhar_texto(
                "S  iniciar batalha    N  sair",
                self.fonts["small"],
                fraco,
                48,
                585,
                900,
            )
        else:
            self.desenhar_texto(
                "Digite um número de 1 a 20 e pressione ENTER para enviar",
                self.fonts["body"],
                (0, 222, 172),
                48,
                595,
                900,
            )
            pygame.draw.rect(self.virtual, (10, 17, 23), (48, 640, 904, 42))
            cor_input = verde if self.input_text else (85, 92, 96)
            self.desenhar_texto(
                self.input_text or "Input do usuário",
                self.fonts["body"],
                cor_input,
                68,
                648,
                860,
            )

    def desenhar_scanlines(self):
        for y in range(0, 700, 4):
            pygame.draw.line(self.virtual, (5, 34, 31), (0, y), (1000, y))

    def desenhar_monitor(self):
        largura, altura = self.screen.get_size()
        escala = min(largura / 1160, altura / 820)
        monitor_w, monitor_h = int(1160 * escala), int(820 * escala)
        origem = ((largura - monitor_w) // 2, (altura - monitor_h) // 2)
        self.screen.fill((22, 42, 43))
        moldura = pygame.Rect(*origem, monitor_w, monitor_h)
        pygame.draw.rect(self.screen, (15, 28, 30), moldura)
        pygame.draw.rect(self.screen, (0, 104, 83), moldura, width=max(2, int(3 * escala)))
        margem = int(32 * escala)
        destino = pygame.Rect(moldura.x + margem, moldura.y + margem, monitor_w - margem * 2, monitor_h - margem * 2)
        imagem = pygame.transform.smoothscale(self.virtual, destino.size)
        self.screen.blit(imagem, destino)