import json
import sys

class Story:
    def __init__(self):
        try:
            with open("story.json", "r") as f:
                self.scenes = json.load(f)["scenes"]
        except FileNotFoundError:
            print("Error: story.json not found. Exiting.")
            sys.exit()

    def load_scene(self, state, scene_id, error=None):
        """Load a scene and update game state."""
        state.is_typing = True
        state.current_text = ""
        state.char_index = 0
        state.show_choices = False
        if scene_id not in self.scenes:
            state.full_text = "Error: Scene not found."
            state.choices = []
        else:
            scene = self.scenes[scene_id]
            base_text = scene["text"]
            # Stat-based text variations
            if state.psyche < 30:
                base_text += " Your hands tremble slightly."
            if state.suspicion > 50:
                base_text += " You feel eyes watching."
            state.full_text = base_text if not error else error
            state.choices = scene.get("choices", [])
        state.current_scene = scene_id
