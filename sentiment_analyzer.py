def analyze_sentiment(text):
    positive = ['喜欢', '开心', '高兴', '好', '棒', '优秀', 'great', 'happy', 'good', 'excellent']
    negative = ['讨厌', '难过', '伤心', '差', '坏', '糟糕', 'hate', 'sad', 'bad', 'terrible']
    text_lower = text.lower()
    pos_count = sum(1 for w in positive if w in text_lower)
    neg_count = sum(1 for w in negative if w in text_lower)
    if pos_count > neg_count:
        return "正面"
    elif neg_count > pos_count:
        return "负面"
    else:
        return "中性"
