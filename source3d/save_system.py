import json
import os


class SaveManager:
    def __init__(self, save_path):
        self.save_path = save_path
        self.state = {
            "player": [0.0, 18.0, 0.0],
            "blocks": {},
            "inventory": {},
            "hotbar_slots": [None] * 9,
            "health": 20,
            "tool_durability": {},
        }
        self._load()

    @staticmethod
    def _block_key(position):
        x, y, z = position
        return f"{int(x)},{int(y)},{int(z)}"

    def _load(self):
        if not os.path.exists(self.save_path):
            return

        try:
            with open(self.save_path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, json.JSONDecodeError):
            return

        if isinstance(data, dict):
            self.state["player"] = data.get("player", self.state["player"])
            self.state["blocks"] = data.get("blocks", self.state["blocks"])
            self.state["inventory"] = data.get("inventory", self.state.get("inventory", {}))
            hotbar_slots = data.get("hotbar_slots", self.state.get("hotbar_slots", [None] * 9))
            if not isinstance(hotbar_slots, list):
                hotbar_slots = [None] * 9
            hotbar_slots = hotbar_slots[:9] + [None] * max(0, 9 - len(hotbar_slots))
            self.state["hotbar_slots"] = hotbar_slots
            self.state["health"] = data.get("health", self.state.get("health", 20))
            tool_durability = data.get("tool_durability", self.state.get("tool_durability", {}))
            if not isinstance(tool_durability, dict):
                tool_durability = {}
            self.state["tool_durability"] = tool_durability

    def save(self):
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        with open(self.save_path, "w", encoding="utf-8") as handle:
            json.dump(self.state, handle, ensure_ascii=True, indent=2)

    def get_player_position(self):
        data = self.state.get("player", [0.0, 18.0, 0.0])
        if not isinstance(data, list) or len(data) != 3:
            return 0.0, 18.0, 0.0
        return float(data[0]), float(data[1]), float(data[2])

    def set_player_position(self, position):
        self.state["player"] = [float(position[0]), float(position[1]), float(position[2])]

    def get_health(self):
        return self.state.get("health", 20)

    def set_health(self, health):
        self.state["health"] = max(0, min(20, health))

    def get_block_override(self, position):
        return self.state["blocks"].get(self._block_key(position), "__missing__")

    def set_block_override(self, position, block_type):
        key = self._block_key(position)
        self.state["blocks"][key] = block_type

    def get_inventory(self):
        return self.state.setdefault("inventory", {})

    def get_hotbar_slots(self):
        hotbar_slots = self.state.setdefault("hotbar_slots", [None] * 9)
        if not isinstance(hotbar_slots, list):
            hotbar_slots = [None] * 9
        hotbar_slots = hotbar_slots[:9] + [None] * max(0, 9 - len(hotbar_slots))
        self.state["hotbar_slots"] = hotbar_slots
        return hotbar_slots

    def set_hotbar_slots(self, hotbar_slots):
        normalized = list(hotbar_slots[:9]) + [None] * max(0, 9 - len(hotbar_slots))
        self.state["hotbar_slots"] = normalized

    def get_tool_durability(self):
        tool_durability = self.state.setdefault("tool_durability", {})
        if not isinstance(tool_durability, dict):
            tool_durability = {}
        self.state["tool_durability"] = tool_durability
        return tool_durability

    def set_tool_durability(self, tool_durability):
        self.state["tool_durability"] = dict(tool_durability)

    def iter_block_overrides(self):
        for key, block_type in self.state["blocks"].items():
            parts = key.split(",")
            if len(parts) != 3:
                continue
            try:
                x, y, z = (int(parts[0]), int(parts[1]), int(parts[2]))
            except ValueError:
                continue
            yield (x, y, z), block_type
