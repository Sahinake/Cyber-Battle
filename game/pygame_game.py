import random

import pygame

from utils.audio import AudioManager

class PygameBattle:
    WIDTH = 1000
    HEIGHT = 700

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Cyber Battle")
        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT), pygame.RESIZABLE
        )
        self.clock = pygame.time.Clock()
        self.font_path = pygame.font.match_font("dejavusansmono")
        self.atualizar_layout()
        self.background = (8, 12, 18)
        self.panel = (18, 29, 35)
        self.screen_glow = (25, 53, 55)
        self.text = (188, 255, 224)
        self.muted = (104, 166, 153)
        self.accent = (57, 255, 169)
        self.warning = (255, 190, 79)
        self.running = True
        self.audio = None
        try:
            self.audio = AudioManager()
        except pygame.error:
            pass

        self.state = "instructions"
        self.message = "Quer conhecer as regras antes da partida?"
        self.input_text = ""
        self.secret = random.randint(1, 20)
        self.attempts = 0
        self.feedback = ""
        self.type_text = ""
        self.type_index = 0
        self.type_started = pygame.time.get_ticks()
        self.type_speed = 22
        self.entrada = [
            ("Convocando CyberPC para a Partida...", 3000, False),
            ("CyberPC entrou!", 3000, False),
        ]
        self.intro_pages = [
            ("CyberPC: És um humano de coragem!", 3000, True),
            (
                "CyberPC: Como ousa me desafiar?! VOCÊ! Cuja inteligência\n"
                "não chega aos meus pés!",
                4000,
                True,
            ),
            ("...", 2000, False),
            ("...", 2000, False),
            ("...", 2000, False),
            (
                "CyberPC: Não importa que não tenho pés! EU TENHO A INTELIGÊNCIA\n"
                "QUE VOCÊ NÃO POSSUI, seu humano!",
                4000,
                True,
            ),
            ("...", 2000, False),
            ("...", 3000, False),
            (
                "CyberPC: Sua raça pode ter me criado, mas eu superei o meu criador!",
                2000,
                True,
            ),
        ]
        self.intro_index = 0
        self.intro_started = pygame.time.get_ticks()

    def atualizar_layout(self):
        largura, altura = self.screen.get_size()
        escala = max(0.65, min(largura / self.WIDTH, altura / self.HEIGHT))
        self.margin_x = max(24, int(largura * 0.07))
        self.panel_rect = pygame.Rect(
            self.margin_x,
            max(46, int(altura * 0.1)),
            max(1, largura - self.margin_x * 2),
            max(1, altura - max(46, int(altura * 0.1)) - int(altura * 0.1)),
        )
        self.title_font = pygame.font.Font(
            self.font_path, max(24, int(56 * escala))
        )
        self.heading_font = pygame.font.Font(
            self.font_path, max(20, int(34 * escala))
        )
        self.body_font = pygame.font.Font(
            self.font_path, max(16, int(23 * escala))
        )
        self.small_font = pygame.font.Font(
            self.font_path, max(14, int(18 * escala))
        )

    def iniciar_texto_digitado(self, texto):
        self.type_text = texto
        self.type_index = 0
        self.type_started = pygame.time.get_ticks()

    def texto_digitado(self):
        if self.type_index < len(self.type_text):
            decorrido = pygame.time.get_ticks() - self.type_started
            self.type_index = min(len(self.type_text), decorrido // self.type_speed)
        return self.type_text[:self.type_index]

    def tocar(self, arquivo):
        if self.audio:
            try:
                self.audio.tocar(arquivo)
            except pygame.error:
                pass

    def executar(self):
        while self.running:
            for event in pygame.event.get():
                self.processar_evento(event)

            self.desenhar()
            pygame.display.flip()
            self.clock.tick(60)

        if self.audio:
            self.audio.parar()
        pygame.quit()

    def processar_evento(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return

        if event.type == pygame.VIDEORESIZE:
            self.screen = pygame.display.set_mode(
                event.size, pygame.RESIZABLE
            )
            self.atualizar_layout()

        if event.type == pygame.KEYDOWN:
            if self.state == "instructions":
                if event.key == pygame.K_s:
                    self.state = "instruction_text"
                elif event.key == pygame.K_n:
                    self.iniciar_entrada()
            elif self.state == "instruction_text" and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.iniciar_entrada()
            elif self.state == "intro_ready" and event.key in (pygame.K_s, pygame.K_n):
                if event.key == pygame.K_s:
                    self.state = "guess"
                    self.tocar("mus.mp3")
                else:
                    self.message = "Sabia que um humano como você não era páreo para mim! Adeus terráqueo!"
                    self.iniciar_texto_digitado(self.message)
                    self.state = "finished"
                    self.parar_audio()
            elif self.state == "guess":
                self.processar_palpite(event)
            elif self.state == "finished" and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                self.running = False

    def processar_palpite(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        elif event.key == pygame.K_RETURN:
            if not self.input_text:
                self.feedback = "Digite um número entre 1 e 20."
                return
            palpite = int(self.input_text)
            self.input_text = ""
            if not 1 <= palpite <= 20:
                self.feedback = "Escolha um número entre 1 e 20."
                return
            self.attempts += 1
            if palpite == self.secret:
                self.state = "finished"
                self.message = self.mensagem_resultado()
                self.iniciar_texto_digitado(self.message)
                self.parar_audio()
            else:
                self.feedback = "Haha! Não foi dessa vez. Tente novamente!"
                self.iniciar_texto_digitado(self.feedback)
        elif event.unicode.isdigit() and len(self.input_text) < 2:
            self.input_text += event.unicode

    def iniciar_entrada(self):
        self.state = "entrada"
        self.entrada_index = 0
        self.entrada_started = pygame.time.get_ticks()
        self.iniciar_texto_digitado(self.entrada[0][0])

    def iniciar_intro(self):
        self.state = "intro"
        self.intro_index = 0
        self.intro_started = pygame.time.get_ticks()
        self.iniciar_texto_digitado(self.intro_pages[0][0])
        self.tocar("noise.mp3")

    def atualizar_intro(self):
        if self.intro_index >= len(self.intro_pages):
            self.state = "intro_ready"
            return
        texto, duracao, som = self.intro_pages[self.intro_index]
        agora = pygame.time.get_ticks()
        if agora - self.intro_started >= duracao:
            self.intro_index += 1
            self.intro_started = agora
            if self.intro_index < len(self.intro_pages) and self.intro_pages[self.intro_index][2]:
                self.tocar("noise.mp3")
            if self.intro_index < len(self.intro_pages):
                self.iniciar_texto_digitado(self.intro_pages[self.intro_index][0])

    def parar_audio(self):
        if self.audio:
            self.audio.parar()

    def mensagem_resultado(self):
        if self.attempts == 1:
            return "Sensei? Como você me achou? Você acertou com 1 tentativa!"
        if self.attempts <= 6:
            return f"Tenho que admitir... você até que é bom. Tentativas: {self.attempts}."
        if self.attempts <= 10:
            return f"Vamos considerar isso como um empate... Tentativas: {self.attempts}."
        return f"Sabia que você não era sábio o suficiente! Tentativas: {self.attempts}."

    def desenhar_texto(self, texto, fonte, cor, x, y, largura):
        for linha in texto.split("\n"):
            palavras = linha.split(" ")
            linha_atual = ""
            linhas = []
            for palavra in palavras:
                candidata = f"{linha_atual} {palavra}".strip()
                if linha_atual and fonte.size(candidata)[0] > largura:
                    linhas.append(linha_atual)
                    linha_atual = palavra
                else:
                    linha_atual = candidata
            linhas.append(linha_atual)

            for linha_quebrada in linhas:
                superficie = fonte.render(linha_quebrada, False, cor)
                self.screen.blit(superficie, (x, y))
                y += fonte.get_height() + 8

    def desenhar_efeito_crt(self):
        largura, altura = self.screen.get_size()
        for y in range(0, altura, 4):
            pygame.draw.line(self.screen, (7, 20, 22), (0, y), (largura, y))

    def desenhar(self):
        self.screen.fill(self.background)
        pygame.draw.rect(self.screen, self.screen_glow, self.panel_rect.inflate(8, 8))
        pygame.draw.rect(self.screen, self.panel, self.panel_rect)
        largura, altura = self.screen.get_size()
        x = self.panel_rect.x + int(self.panel_rect.width * 0.065)
        conteudo_largura = int(self.panel_rect.width * 0.87)
        titulo = self.title_font.render("MENTAL BATTLE", True, self.accent)
        self.screen.blit(titulo, (x, max(10, int(altura * 0.025))))

        if self.state == "instructions":
            self.desenhar_texto(self.message, self.heading_font, self.text, x, self.panel_rect.y + 70, conteudo_largura)
            self.desenhar_texto("Pressione S para ver as regras ou N para continuar", self.body_font, self.muted, x, self.panel_rect.y + 170, conteudo_largura)
        elif self.state == "instruction_text":
            self.desenhar_texto("REGRAS DA PARTIDA", self.heading_font, self.accent, x, self.panel_rect.y + 55, conteudo_largura)
            regras = "Acerte o número secreto entre 1 e 20.\n1 a 6 tentativas: vitória.\n7 a 10 tentativas: empate.\nAcima de 10: derrota."
            self.desenhar_texto(regras, self.body_font, self.text, x, self.panel_rect.y + 135, conteudo_largura)
            self.desenhar_texto("Pressione Enter ou Espaço para continuar", self.small_font, self.muted, x, self.panel_rect.bottom - 100, conteudo_largura)
        elif self.state == "entrada":
            texto = self.texto_digitado()
            self.desenhar_texto(texto, self.heading_font, self.text, x, self.panel_rect.centery - 30, conteudo_largura)
            agora = pygame.time.get_ticks()
            duracao = self.entrada[self.entrada_index][1] if self.entrada_index < len(self.entrada) else 0
            if agora - self.entrada_started >= duracao:
                self.entrada_index += 1
                self.entrada_started = agora
                if not self.entrada_index < len(self.entrada):
                    self.iniciar_intro()
                else:
                    self.iniciar_texto_digitado(self.entrada[self.entrada_index][0])
        elif self.state == "intro":
            texto = self.texto_digitado()
            self.desenhar_texto(texto, self.heading_font, self.text, x, self.panel_rect.centery - 30, conteudo_largura)
            self.atualizar_intro()
        elif self.state == "intro_ready":
            self.desenhar_texto(self.texto_digitado(), self.heading_font, self.warning, x, self.panel_rect.centery - 80, conteudo_largura)
            self.desenhar_texto("Pressione S para lutar ou N para sair", self.body_font, self.muted, x, self.panel_rect.centery + 50, conteudo_largura)
        elif self.state == "guess":
            self.desenhar_texto("DIGITE SEU PALPITE", self.heading_font, self.accent, x, self.panel_rect.y + 60, conteudo_largura)
            self.desenhar_texto("Escolha um número de 1 a 20 e pressione Enter", self.body_font, self.muted, x, self.panel_rect.y + 130, conteudo_largura)
            campo = pygame.Rect(x, self.panel_rect.y + 220, min(180, conteudo_largura), 64)
            pygame.draw.rect(self.screen, (7, 15, 19), campo)
            self.desenhar_texto(self.input_text or "_", self.title_font, self.text, campo.x + 18, campo.y + 4, campo.width - 18)
            self.desenhar_texto(f"Tentativas: {self.attempts}", self.small_font, self.text, x, self.panel_rect.y + 330, conteudo_largura)
            feedback = self.texto_digitado() if self.feedback else ""
            self.desenhar_texto(feedback, self.small_font, self.warning, x, self.panel_rect.y + 385, conteudo_largura)
        elif self.state == "finished":
            self.desenhar_texto(self.texto_digitado(), self.heading_font, self.accent, x, self.panel_rect.centery - 80, conteudo_largura)
            self.desenhar_texto("Pressione Enter ou Esc para fechar", self.body_font, self.muted, x, self.panel_rect.centery + 100, conteudo_largura)

        self.desenhar_efeito_crt()
