import random, string, sys

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

if __name__ == "__main__":
    length = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    print(generate_password(length))
