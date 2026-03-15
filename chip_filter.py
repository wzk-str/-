def filter_efficient_chips():
    chips = [
        {"name": "费曼芯片2026", "perf": 500, "power": 100},
        {"name": "旧款A100", "perf": 100, "power": 400},
        {"name": "Rubin Ultra 2026", "perf": 800, "power": 200},
        {"name": "Hopper H100", "perf": 300, "power": 150},
        {"name": "费曼Lite", "perf": 250, "power": 80},
        {"name": "Rubin AI 2026", "perf": 600, "power": 250},
    ]
    return [c["name"] for c in chips if c["perf"]/c["power"] > 2.0 and ("2026" in c["name"] or "费曼" in c["name"] or "Rubin" in c["name"])]


if __name__ == "__main__":
    result = filter_efficient_chips()
    print("高能效新芯片列表:", result)
