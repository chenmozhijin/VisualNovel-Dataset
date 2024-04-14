import json
subject_types = []  # 1:书籍 2: 动画 4: 游戏

with open('../data/bangumi-character.jsonl', 'r', encoding='utf-8') as file:
    contents = [json.loads(line) for line in file]

result = []

for content in contents:
    subjects = content['subjects']
    for subject in subjects:
        if subject['subject_type'] in subject_types:
            result.append(subject)

with open('bangumi-character-filtered.jsonl', 'w', encoding='utf-8') as file:
    for character in result:
        file.write(json.dumps(subject, ensure_ascii=False) + '\n')