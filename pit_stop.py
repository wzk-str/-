import random

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
    strategy = PitStopStrategy(40, 85)
    print(strategy.decide())
