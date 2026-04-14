import pyfiglet, sys

text = pyfiglet.figlet_format("WORDLE")
lines = text.splitlines()

out = "\033[1G"               # explizit zu Spalte 1 — NEU

for i in lines:
    out += i+"\033[B"+f"\033[{len(i)}D"

sys.stdout.write(out)
sys.stdout.flush()

print(repr(out))