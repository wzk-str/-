def filter_efficient_chips():
    chips = [
        {"name": "费曼芯片", "perf": 500, "power": 100},
        {"name": "旧款A100", "perf": 100, "power": 400},
        {"name": "Rubin 2026", "perf": 800, "power": 200},
        {"name": "Hopper 2026", "perf": 900, "power": 300},
        {"name": "普通芯片", "perf": 300, "power": 200}
    ]
    return [c["name"] for c in chips if c["perf"] / c["power"] > 2.0 and any(k in c["name"] for k in ["2026", "费曼", "Rubin"])]

if __name__ == "__main__":
    print(filter_efficient_chips())
