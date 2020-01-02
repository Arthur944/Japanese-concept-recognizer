explanations = [x.split(";") for x in open("primitive_explanations.txt", "r").read().splitlines()]
symbols = [x.split(";") for x in open("primitive_symbols.txt", "r").read().splitlines()]
symbols = {x[0]: x[1] for x in symbols}
explanations = {x[1]: x[0] for x in explanations}

out = []
for key in explanations.keys():
    meanings = [x.strip() for x in key.split(",")]
    symbol = ""
    for meaning in meanings:
        if meaning in symbols.keys():
            symbol = symbols[meaning]
            break
    out.append([key, symbol, explanations[key]])

to_write = ""
for line in out:
    to_write += ";".join([x.strip() for x in line]) + "\n"
open("primitive_notes.txt", "w+").write(to_write.strip())