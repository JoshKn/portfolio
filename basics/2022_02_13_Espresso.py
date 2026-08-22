#openpyxl für Excel Support?

coffee = input("Welchen Kaffee nimmst Du? ")

mahlgrad = int(input("Welcher Mahlgrad? "))

inGrams = float(input("Wieviel Gramm Kaffeepulver nimmst Du? "))

ratio = float(input("Welches Kaffee-Wasser-Verhältnis? "))

outGrams = inGrams * ratio
print(f"Dein Output sollte {outGrams} Gramm sein.")