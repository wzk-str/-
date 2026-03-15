import random
import string
import sys

def generate_password(length=12):
    all_chars = string.ascii_letters + string.digits + string.punctuation
    password = [random.choice(string.ascii_lowercase),
                random.choice(string.ascii_uppercase),
                random.choice(string.digits),
                random.choice(string.punctuation)]
    password += [random.choice(all_chars) for _ in range(max(0, length - 4))]
    random.shuffle(password)
    return ''.join(password)

if __name__ == "__main__":
    length = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    print(generate_password(length))
