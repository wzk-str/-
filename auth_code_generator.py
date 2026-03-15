def generate_auth_code(chip_id):
    return ''.join(chr(ord(c) + 3) if c.isalnum() else c for c in chip_id[::-1]) + "_0315"


if __name__ == "__main__":
    test_ids = ["FM-2026-X", "Rubin-2026-Ultra", "AB-123-XYZ"]
    for chip_id in test_ids:
        print(f"芯片ID: {chip_id} -> 防伪码: {generate_auth_code(chip_id)}")
