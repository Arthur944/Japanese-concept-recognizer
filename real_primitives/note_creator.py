book = [x.split(";") for x in open("book.csv", "r").readlines()]

prims = {}
i = 0
for line in book:
    i += 1
    meanings = line[2].split(",")
    for meaning in meanings:
        prims[meaning] = {'symbol': line[0], 'kanji_story': line[1], 'prim_story': line[2], 'ordering': i}

notes = [x.split(";") for x in open("notes.txt", "r").readlines()]
missing_meanings = []
for line in notes:
    meanings = [x.strip().lower() for x in line[0].split(",")]
    missing = []
    for meaning in meanings:
        if meaning in prims.keys():
            prims[meaning]['symbol'] = line[1]
        else:
            missing.append(meaning)
    if missing:
        missing_meanings.append(missing)
for line in missing_meanings:
    print(line)

real_dic = {}
for key in prims.keys():
    symbol = prims[key]['symbol']
    if symbol not in real_dic.keys():
        real_dic[symbol] = [prims[key]['ordering'], [key]]
    else:
        real_dic[symbol][1].append(key)

lines = []
for key in real_dic.keys():
    lines.append([
        real_dic[key][0],
        ",".join(list(set(real_dic[key][1]))),
        key
    ])
lines = list(sorted(lines, key=lambda x: x[0]))

to_write = ""
for line in lines:
    to_write += line[1].strip() + ";" + line[2].strip() + "\n"
open("out.txt","w+").write(to_write.strip())
