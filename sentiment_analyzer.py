def analyze_sentiment(text):
    positive = {'好', '棒', '优秀', '开心', '爱', 'happy', 'good', 'love', 'great', 'nice'}
    negative = {'坏', '差', '糟糕', '难过', '恨', 'sad', 'bad', 'hate', 'terrible', 'awful'}
    pos_count = sum(1 for w in positive if w in text.lower())
    neg_count = sum(1 for w in negative if w in text.lower())
    return '正面' if pos_count > neg_count else '负面' if neg_count > pos_count else '中性'

if __name__ == '__main__':
    text = input('请输入句子：')
    print(f'情感分析结果：{analyze_sentiment(text)}')
