# Synthetic MinerU-style excerpt (test fixture)

This file is NOT the lecture slides. It is a hand-written stand-in for a MinerU
`full.md` that contains only the three estimation equations used by the L03
example note, written the way MinerU emits formulas (digits split by spaces).
It exists so `tests/test_check_note.py` can exercise check_note.py's
`--source` constants check without redistributing copyrighted slide text.

## Hirschfelder equation

$$
D _ {A B} = \frac {0 . 0 0 1 8 5 8 T ^ {3 / 2} \left(\frac {1} {M _ {A}} + \frac {1} {M _ {B}} \right) ^ {1 / 2}} {P \sigma _ {A B} ^ {2} \Omega _ {D}}
$$

## Fuller correlation

$$
D _ {A B} = \frac {1 0 ^ {- 3} T ^ {1 . 7 5} \left(\frac {1} {M _ {A}} + \frac {1} {M _ {B}} \right) ^ {1 / 2}} {P \left[ (\Sigma v) _ {A} ^ {1 / 3} + (\Sigma v) _ {B} ^ {1 / 3} \right] ^ {2}}
$$

## Brokaw equation

$$
\Omega _ {D} = \Omega _ {D 0} + \frac {0 . 1 9 6 \delta _ {A B} ^ {2}} {T ^ {*}}
$$

$$
\delta = \frac {1 . 9 4 \times 1 0 ^ {3} \mu _ {p} ^ {2}} {V _ {b} T _ {b}}
$$

$$
\frac {\varepsilon} {\kappa} = 1. 1 8 (1 + 1 . 3 \delta ^ {2}) T _ {b}
$$

$$
\sigma = \left(\frac {1 . 5 8 5 V _ {b}} {1 + 1 . 3 \delta ^ {2}} \right) ^ {1 / 3}
$$
