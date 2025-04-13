import pygame

class GameState:
    def __init__(self):
        self.psyche = 100
        self.suspicion = 0
        self.skill = 0
        self.current_scene = "apartment_start"
        self.current_text = ""
        self.full_text = ""
        self.char_index = 0
        self.is_typing = False
        self.input_text = ""
        self.show_choices = False
        self.choices = []
        self.selected_choice = -1
        self.static_active = False
        self.static_timer = 0
        self.static_duration = 500  # 0.5s

    def update_stats(self, stat_changes):
        """Update Psyche, Suspicion, and Skill."""
        for stat, value in stat_changes.items():
            if stat == "psyche":
                self.psyche = max(0, min(100, self.psyche + value))
            elif stat == "suspicion":
                self.suspicion = max(0, min(100, self.suspicion + value))
            elif stat == "skill":
                self.skill = max(0, min(100, self.skill + value))
        # Trigger static burst if psyche drops significantly
        if "psyche" in stat_changes and stat_changes["psyche"] < -4:
            self.static_active = True
            self.static_timer = pygame.time.get_ticks()
            print(f"Static burst triggered. Psyche: {self.psyche}")

    def process_command(self, command, story):
        """Process typed command and update scene."""
        command = command.lower().strip()
        print(f"Processing command: '{command}'")
        print(f"Available choices: {[c['command'] for c in self.choices]}")
        for choice in self.choices:
            # Match against command or normalized text
            choice_command = choice["command"].lower().strip()
            choice_text = choice["text"].lower().strip()
            if command == choice_command or command == choice_text:
                print(f"Command '{command}' matched to '{choice_command}' or '{choice_text}'. Updating stats and loading next scene...")
                self.update_stats(choice.get("stats", {}))
                self.current_scene = choice["next_scene"]
                story.load_scene(self, self.current_scene)
                return
        # Command not recognized; show valid options in error
        valid_commands = ", ".join([f"{c['command']} ('{c['text']}')" for c in self.choices])
        error_message = f"Command not recognized. Try: {valid_commands}" if self.choices else "Command not recognized. No choices available."
        print(f"Command '{command}' not recognized. Reloading scene with error: {error_message}")
        story.load_scene(self, self.current_scene, error=error_message)

    def select_choice(self, index, story):
        """Process menu choice and update scene."""
        print(f"Selected choice {index}: {self.choices[index]['text']}")
        self.update_stats(self.choices[index].get("stats", {}))
        self.current_scene = self.choices[index]["next_scene"]
        story.load_scene(self, self.current_scene)
