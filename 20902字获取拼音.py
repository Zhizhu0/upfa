import json

from pypinyin import pinyin, Style
from pypinyin.contrib.tone_convert import to_initials, to_finals_tone3

with open('20902字.txt', 'r', encoding='utf-8') as f:
    text = f.read()

res = {}

for char in text:
    p = pinyin(char, heteronym=True, style=Style.TONE3)[0]
    sub_res = []
    for s in p:
        initial = to_initials(s) if to_initials(s) != '' else s[0]
        tone = s[-1] if s[-1].isdigit() else ''
        final = s[len(initial):-len(tone)]
        item = {
            'initial': initial,
            'final': final,
            'tone': tone,
        }
        sub_res.append(item)

    res[char] = sub_res

with open('20902字拼音.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False)
