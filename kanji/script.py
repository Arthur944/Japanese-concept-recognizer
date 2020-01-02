final = [x.split(";") for x in open("final.csv", "r").read().splitlines()]

out = []
for line in final:
    symbol, keyword, heisig, comment, koohii1, koohii2, *rest = line
    out.append([symbol, keyword, heisig, koohii1, koohii2])

to_write =""
for line in out:
    to_write += ";".join([x.strip() for x in line]) + "\n"

open("kanji_notes.txt", "w+").write(to_write.strip())