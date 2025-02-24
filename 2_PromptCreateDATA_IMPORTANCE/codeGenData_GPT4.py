import pandas as pd

# Tạo danh sách 5000 câu song ngữ kết hợp tiếng Anh và tiếng Việt
sentences = []
topics = [
    "daily life", "study", "hobbies", "work", "travel", 
    "family", "friends", "food", "sports", "music",
    "movies", "technology", "health", "education", "IELTS speaking",
    "shopping", "weather", "future plans", "memories", "relationships"
]

# Mẫu câu để đa dạng hóa nội dung
english_starters = [
    "I think", "Do you know", "Let's", "We should", "Sometimes", 
    "Don't worry", "Have you ever", "I really like", "I don't understand", "It seems that"
]
vietnamese_parts = [
    "mình nên", "bạn có muốn", "học tiếng Anh", "rất thú vị", 
    "khá khó", "cùng nhau", "sẽ tốt hơn", "nếu có thời gian", 
    "thật tuyệt", "rất hữu ích"
]
endings = [
    "together, right?", "in the future.", "because it's fun!", 
    "but it's okay.", "and I enjoy it.", "what do you think?", 
    "to improve ourselves.", "let's try it!", "if you like.", "when you're free."
]

# Sinh 5000 câu
for i in range(5000):
    topic = topics[i % len(topics)]
    start = english_starters[i % len(english_starters)]
    vn_part = vietnamese_parts[i % len(vietnamese_parts)]
    end = endings[i % len(endings)]
    sentence = f"{start}, {vn_part} {end}"
    sentences.append({"Index": i + 1, "Topic": topic, "Sentence": sentence})

# Tạo DataFrame
df_sentences = pd.DataFrame(sentences)

# Lưu file CSV
file_path = '/mnt/data/5000_sentences_english_vietnamese_mix.csv'
df_sentences.to_csv(file_path, index=False)

# Hiển thị cho người dùng
import ace_tools as tools; tools.display_dataframe_to_user(name="5000 Mixed Sentences", dataframe=df_sentences)

file_path
