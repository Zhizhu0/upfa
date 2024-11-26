import json

from pypinyin import pinyin, Style
from pypinyin.contrib.tone_convert import to_initials, to_finals_tone3

with open('双拼规则.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('20902字拼音.json', 'r', encoding='utf-8') as f:
    p20902 = json.load(f)

output = ''

with open('导出方案处理简码-一字一码.txt', 'r', encoding='utf-8') as f:
    j_yy = f.read().split('\n')
for line in j_yy:
    if line != '':
        p = pinyin(line, style=Style.NORMAL)
        ol = ''
        for x in p:
            i = to_initials(x[0]) if to_initials(x[0]) != '' else x[0][0]
            if i in data['initial']:
                i = data['initial'][i]
            ol += i
        output += f'{ol} {line}\n'

with open('导出方案处理简码-单字双码.txt', 'r', encoding='utf-8') as f:
    j_du = f.read().split('\n')

usd = []

for line in j_du:
    if line != '':
        usd.append(line)
        for p in p20902[line]:
            initial = p['initial']
            final = p['final']
            tone = p['tone']
            if initial in data['initial']:
                initial = data['initial'][initial]
            if final in data['final']:
                final = data['final'][final]
            if final == '':
                final = initial
            output += f'{initial}{final} {line}\n'
            if tone != '':
                output += f'{initial}{final}{tone} {line}\n'

with open('导出方案处理全码.txt', 'r', encoding='utf-8') as f:
    qm = f.read().split('\n')
for line in qm:
    if line != '':
        p = pinyin(line, style=Style.NORMAL)
        if len(line) == 2:
            ol = ''
            for x in p:
                initial = to_initials(x[0]) if to_initials(x[0]) != '' else x[0][0]
                final = x[0][len(initial):]
                if initial in data['initial']:
                    initial = data['initial'][initial]
                if final in data['final']:
                    final = data['final'][final]
                if final == '':
                    final = initial
                ol += f'{initial}{final}'
            output += f'{ol} {line}\n'
        elif len(line) == 3:
            ol = ''
            for x in p[:-1]:
                initial = to_initials(x[0]) if to_initials(x[0]) != '' else x[0][0]
                if initial in data['initial']:
                    initial = data['initial'][initial]
                ol += initial
            initial = to_initials(p[-1][0]) if to_initials(p[-1][0]) != '' else p[-1][0][0]
            final = p[-1][0][len(initial):]
            if initial in data['initial']:
                initial = data['initial'][initial]
            if final in data['final']:
                final = data['final'][final]
            if final == '':
                final = initial
            ol += f'{initial}{final}'
            output += f'{ol} {line}\n'
        else:
            ol = ''
            for x in p[:4]:
                initial = to_initials(x[0]) if to_initials(x[0]) != '' else x[0][0]
                if initial in data['initial']:
                    initial = data['initial'][initial]
                ol += initial
            output += f'{ol} {line}\n'

for char in p20902:
    if char in usd:
        continue
    c_list = p20902[char]
    for c in c_list:
        initial = c['initial']
        final = c['final']
        tone = c['tone']
        if initial in data['initial']:
            initial = data['initial'][initial]
        if final in data['final']:
            final = data['final'][final]
        if tone in data['tone']:
            tone = data['tone'][tone]
        output += f'{initial}{final}{tone} {char}\n'

with open('方案.txt', 'w', encoding='utf-8') as f:
    f.write(output)
