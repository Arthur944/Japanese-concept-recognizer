import re
import html2text

file = open("index.html", "r").read()

entry_matches = re.finditer("<table.*?>((.|\s)*?)</table>", file)


def clear_html(text):
    text = re.sub('<span class="no-style-override12">(.*?)</span>', '**\g<1>**', text)
    text = re.sub('<span class="same-author-red-33745-1-override">(.*?)</span>', '_\g<1>_', text)
    text = html2text.html2text(text).replace("\n", " ")
    return text.strip()


csv = []
for match in entry_matches:
    dic = {}
    kanji = re.search('<p class="k-frame-kanji">((.|\s)*?)</p>', match.group())
    kanji_explanation = re.search('<p class="k-kanji-explanation">((.|\s)*?)</p>', match.group())
    if kanji:
        dic['kanji'] = clear_html(kanji.group(1))
        if kanji_explanation:
            dic['kanji_explanation'] = clear_html(kanji_explanation.group(1))
    primitive_explanation = re.search('<p class="k-primitives-explained">((.|\s)*?)</p>', match.group())
    if primitive_explanation:
        dic['primitive_explanation'] = clear_html(primitive_explanation.group(1))
        primitive_meanings = []
        meaning_matches = re.finditer('<span class="same-author-red-33745-1-override">(.*?)</span>', primitive_explanation.group())
        for match in meaning_matches:
            primitive_meanings.append(re.sub("[^A-Za-z ]", "",match.group(1).lower().strip()))
        dic['primitive_meanings'] = list(set(primitive_meanings))
    csv.append(dic)

text = list(csv)
ordered_meanings = []
prim_only = []
order = ['kanji', 'kanji_explanation', 'primitive_meanings', 'primitive_explanation']
for i in range(len(text)):
    if 'primitive_meanings' in text[i].keys():
        text[i] = [text[i][x] if x in text[i].keys() else "" for x in order]
        if text[i][2] != "":
            text[i][2] = ",".join(text[i][2])
        ordered_meanings.append(text[i][2])
        text[i] = ";".join(text[i])

to_write = ""
for line in ordered_meanings:
    if line.strip() != "":
        to_write += line + "\n"
open("order.txt", "w+").write(to_write.strip())

# with open("kanji_and_primitive_exps.csv", "w+") as file:
#     to_write = ""
#     for line in real_text:
#         to_write += line + "\n"
#     file.write(to_write.strip())
