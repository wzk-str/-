def generate_auth_code(chip_id):
    shifted = ''.join(chr(ord(c) + 3) if c.isalnum() else c for c in chip_id[::-1])
    return shifted + "_0315"

if __name__ == "__main__":
    print(generate_auth_code("FM-2026-X"))
