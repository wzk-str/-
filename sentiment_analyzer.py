def analyze_sentiment(text):
    positive = ['good', 'great', 'excellent', 'happy', 'love', '好', '棒', '喜欢', '开心', '优秀']
    negative = ['bad', 'terrible', 'awful', 'sad', 'hate', '坏', '差', '讨厌', '难过', '糟糕']
    negators = ['不', '没', '无', '非', 'not ', ' no ', 'never', 'hardly']
    t = ' ' + text.lower() + ' '
    p = sum(t.count(w) for w in positive)
    n = sum(t.count(w) for w in negative)
    neg = sum(t.count(w) for w in negators)
    score = (p - n) * (-1 if neg % 2 == 1 else 1)
    return '正面' if score > 0 else '负面' if score < 0 else '中性'

if __name__ == "__main__":
    import sys
    text = sys.argv[1] if len(sys.argv) > 1 else input("请输入句子: ")
    print(f"情感: {analyze_sentiment(text)}")
