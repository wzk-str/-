import random

def filter_efficient_chips():
    chips = [
        {"name": "费曼芯片", "perf": 500, "power": 100},
        {"name": "旧款A100", "perf": 100, "power": 400},
        {"name": "Rubin 2026", "perf": 800, "power": 200},
        {"name": "Hopper 2026", "perf": 900, "power": 300},
        {"name": "普通芯片", "perf": 300, "power": 200}
    ]
    return [c["name"] for c in chips if c["perf"] / c["power"] > 2.0 and any(k in c["name"] for k in ["2026", "费曼", "Rubin"])]

def generate_auth_code(chip_id):
    reversed_id = chip_id[::-1]
    encoded = ''.join(chr(ord(c) + 3) if c.isalnum() else c for c in reversed_id)
    return encoded + "_0315"

class PitStopStrategy:
    def __init__(self, current_lap, wear):
        self.current_lap = current_lap
        self.wear = wear
    
    def decide(self):
        if random.random() < 0.1:
            return "立即进站"
        if self.wear > 80 or self.current_lap == 45:
            return "进站：换硬胎"
        if self.wear < 30 and self.current_lap < 50:
            return "继续：保持软胎"
        return "观察：下一圈决定"

if __name__ == "__main__":
    print(filter_efficient_chips())
    print(generate_auth_code("FM-2026-X"))
    strategy = PitStopStrategy(40, 50)
    print(strategy.decide())
