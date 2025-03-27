# Simulacija Monty-Hallove Igre

Pythonova skripta famozne Monty-Hallove igre, ki bazira na verjetnosti. Skripta vključuje interaktivno igro in statistično analizo izidov N-iterakcij igre.

## Opis Problema (Igre)

Monty-Hallova igra je povezana z verjetnostjo in izvira iz Ameriške TV oddaje "Let's Make a Deal":
- Imamo 3 vrata.
- Za enimi vrati je nagrada, za ostalimi pa koze (v našem primeru vrsta živali).
- Igralec izbere poljubna vrata.
- Voditelj (ki ve kaj je za vsakimi od vrat) odpre druga (različna od igralčeve izbire) vrata, za katerimi je sigurno koza.
- Igralec dobi možnost, da si premisli in odpre poljubna druga vrata ali vztraja pri prvotni izbiri.
- Vprašanje je: Ali se nam bolj izplača izbrati druga vrata ali vztrajati pri prvi izbiri? - Bolje je izbrati druga vrata.

## Skripta omogoča:

- Interaktivno igranje opisane igre (`monty_python()`).
- Statistična simulacija izidov več iteracij igre (`sim_mh()`).
- Vizualizacija rezultatov, s katerimi primerjamo:
  - Delež zmag, če si ne premislimo.
  - Delež zmag, če si premislimo.
  - Teoretično napoved verjetnosti (1/3, če si ne premislimo in 2/3, če si premislimo).

## Knjižnice

```python
import random
import numpy as np
import matplotlib.pyplot as plt
```

## Uporaba skirpte

### Korak 1 (Interaktivna Igra)
```python
monty_python()
```

### Korak 2 (Simulacija)
```python
# Run 1000 simulations and plot results
ostr, premr = sim_mh(1000)
Grafi(ostr, premr)
```

## Funkcije

- `monty_python()`: Interaktivna igra, ki zahteva uporabnikov vnos odločitev.
- `sim_mh(št_ig)`: Simulacija več iger, ki poda statistiko zmag in porazov.
- `Grafi(ostr, premr)`: Izris grafov.

## Rezultati

S simulacijo demonstriramo sledeče:
- Če si ne premislimo, zmagamo v ~ 33 % (1/3).
- Če si premislimo, zmagamo v ~ 67 % (2/3).

S tem potrdimo sprva neintuitivno teoretično napoved razmerij zmag, ki narekuje, da s tem, da si premislimo, podvojimo možnost za pridobitev nagrade namesto koze.