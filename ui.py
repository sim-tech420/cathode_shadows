import pygame
import random

class UI:
    def __init__(self):
        # Window settings
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Cathode Shadows")
        # Colors
        self.bg_color = (20, 40, 20)
        self.text_color = (0, 255, 0)
        self.input_color = (0, 200, 0)
        self.choice_color = (0, 255, 0)
        self.choice_hover = (100, 255, 100)
        # Font
        try:
            self.font = pygame.font.Font("fonts/vcr_osd_mono.ttf", 24)
        except FileNotFoundError:
            self.font = pygame.font.SysFont("courier", 24)
        # Sound
        try:
            self.type_sound = pygame.mixer.Sound("sounds/type.wav")
        except FileNotFoundError:
            print("Warning: type.wav not found. Typing sound disabled.")
            self.type_sound = None
        # CRT effect
        self.crt_surface = self.create_crt_surface()
        # Static burst
        self.static_surface = self.create_static_surface()
        # Timing
        self.typing_delay = 80
        self.last_type_time = 0

    def create_crt_surface(self):
        """Create scanline overlay for CRT effect."""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for y in range(0, self.height, 2):
            pygame.draw.line(surface, (0, 0, 0, 50), (0, y), (self.width, y))
        return surface

    def create_static_surface(self):
        """Create white noise for static burst."""
        surface = pygame.Surface((self.width, self.height))
        for x in range(self.width):
            for y in range(self.height):
                gray = random.randint(0, 255)
                surface.set_at((x, y), (gray, gray, gray))
        surface.set_alpha(100)
        return surface

    def wrap_text(self, text, max_width):
        """Wrap text to fit within max_width pixels."""
        lines = []
        current_line = ""
        i = 0
        while i < len(text):
            current_line += text[i]
            test_surface = self.font.render(current_line.rstrip(), True, self.text_color)
            if text[i] == "\n":
                lines.append(current_line.rstrip())
                current_line = ""
            elif test_surface.get_width() > max_width:
                last_space = current_line.rfind(" ")
                if last_space != -1:
                    lines.append(current_line[:last_space].rstrip())
                    current_line = current_line[last_space+1:]
                else:
                    lines.append(current_line.rstrip())
                    current_line = ""
            i += 1
        if current_line:
            lines.append(current_line.rstrip())
        return lines

    def handle_input(self, state, story):
        """Process mouse and keyboard events."""
        mouse_pos = pygame.mouse.get_pos()
        state.selected_choice = -1
        choice_rects = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and not state.is_typing:
                if event.key == pygame.K_RETURN:
                    if state.input_text:
                        # Normalize input for matching
                        typed_command = state.input_text.lower().strip()
                        state.input_text = ""
                        state.process_command(typed_command, story)
                    elif state.show_choices and state.selected_choice >= 0:
                        state.select_choice(state.selected_choice, story)
                elif event.key == pygame.K_BACKSPACE:
                    state.input_text = state.input_text[:-1]
                elif event.unicode.isprintable():
                    state.input_text += event.unicode
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3] and state.show_choices:
                    index = [pygame.K_1, pygame.K_2, pygame.K_3].index(event.key)
                    if index < len(state.choices):
                        state.select_choice(index, story)
            elif event.type == pygame.MOUSEBUTTONDOWN and not state.is_typing and state.show_choices:
                for i, rect in enumerate(choice_rects):
                    if rect.collidepoint(event.pos):
                        state.select_choice(i, story)
        return choice_rects, mouse_pos

    def update_typewriter(self, state, current_time):
        """Handle typewriter effect and sound."""
        if state.is_typing and current_time - self.last_type_time >= self.typing_delay:
            if state.char_index < len(state.full_text):
                state.current_text += state.full_text[state.char_index]
                state.char_index += 1
                self.last_type_time = current_time
                if self.type_sound and state.full_text[state.char_index-1] not in [" ", "\n"]:
                    self.type_sound.play()
            else:
                state.is_typing = False
                state.show_choices = True

    def render(self, state, choice_rects, mouse_pos):
        """Render all UI elements."""
        self.screen.fill(self.bg_color)
        # Text with wrapping and curvature
        lines = self.wrap_text(state.current_text, 700)
        glitch_offset = (0, 0)
        if random.random() < 0.02 or state.psyche < 30 and random.random() < 0.05:
            glitch_offset = (random.randint(-3, 3), random.randint(-1, 1))
        for i, line in enumerate(lines):
            scale = 1.0 - (abs(i - len(lines) / 2) * 0.015)
            text_surface = self.font.render(line, True, self.text_color)
            text_surface = pygame.transform.rotozoom(text_surface, 0, scale)
            x = 50 + glitch_offset[0]
            y = 50 + i * 30 + glitch_offset[1]
            self.screen.blit(text_surface, (x, y))
        # Choice menu (moved up to avoid overlap)
        choice_rects.clear()
        if state.show_choices and not state.is_typing:
            for i, choice in enumerate(state.choices):
                color = self.choice_hover if i == state.selected_choice else self.choice_color
                choice_surface = self.font.render(f"{i+1}. {choice['text']}", True, color)
                rect = choice_surface.get_rect(topleft=(50, 350 + i * 30))  # Moved up from 400 to 350
                self.screen.blit(choice_surface, rect)
                choice_rects.append(rect)
                if rect.collidepoint(mouse_pos):
                    state.selected_choice = i
        # Stats (moved up to avoid overlap)
        stats_text = f"Psyche: {state.psyche}% | Suspicion: {state.suspicion}% | Skill: {state.skill}%"
        stats_surface = self.font.render(stats_text, True, self.input_color)
        self.screen.blit(stats_surface, (50, 450))  # Moved up from 470 to 420
        # Input field
        input_surface = self.font.render(
            "> " + state.input_text + "_" if not state.is_typing else "> Type command...",
            True, self.input_color
        )
        self.screen.blit(input_surface, (50, 500))
        # Static burst
        if state.static_active and pygame.time.get_ticks() - state.static_timer <= state.static_duration:
            self.screen.blit(self.static_surface, (0, 0))
        else:
            state.static_active = False
        # CRT effect
        flicker = random.uniform(0.95, 1.05)
        crt_copy = self.crt_surface.copy()
        crt_copy.set_alpha(int(255 * flicker))
        self.screen.blit(crt_copy, (0, 0))
        pygame.display.flip()
