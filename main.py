from engine import CNF

a1 = ["\~", ["\Rightarrow", ["\Rightarrow", ["\Vee", "P", ["\~", "Q"]], "R"], ["\Wedge", "P", "R"]]]
cnf = CNF(a1)
print(cnf.convert(a1))