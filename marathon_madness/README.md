# Marathon Madness

An officer on the UESC Marathon in the year 2794, you have traveled to the Tau
Ceti system with the objective to establish a new colony for human kind.
However, disaster has struck: an alien race known as the Pfhor has attacked
your ship, and turned one of it's AI systems, Durandal against you. To save the
Marathon, you must find the malicious AI Core File causing Durandal to fight
for the Pfhor. Normally, this would be easy, but Durandal has self-modified
it's code to scramble all of the file indices! To find the Core File, you must
reverse-engineer Durandal's encryption scheme.

Every file index in Durandal's primary storage cluster has been converted into
a pair of enciphered fragments. A pair of files may be compared by computing
it's *Durandal Coefficient*. The file with the smallest Durandal Coefficient
contains the malicious code. Each fragment is a string of Latin symbols, $A, B,
C\hdots X, Y, Z$.

A single symbol may be converted to an integer value via the following encoding
table:

| symbol | value |
|--------|-------|
| A | 19 |
| B | 18 |
| C | 8 |
| D | 15 |
| E | 20 |
| F | 0 |
| G | 6 |
| H | 22 |
| I | 1 |
| J | 21 |
| K | 13 |
| L | 11 |
| M | 12 |
| N | 4 |
| O | 24 |
| P | 9 |
| Q | 10 |
| R | 16 |
| S | 17 |
| T | 3 |
| U | 14 |
| V | 23 |
| W | 2 |
| X | 25 |
| Y | 5 |
| Z | 7 |

A fragment $f$ may be converted to an integer value by the following equation,
assuming that $f_n$ is the integer-converted version of the $n$-th symbol of
$f$.

$$\sum_{j=0}^{4} 26^j \cdot f_j$$

For example, the fragment "ABCDE" would be converted as:

$$19\cdot 26^0 + 18 \cdot 26^1 + 8 \cdot 26^2 + 15\cdot 26^3 + 20\cdot 26^4 = 9409055$$

The fragment "XY" would be converted as:

$$25 \cdot 26^0 + 5 \cdot 26^1 = 155$$

The fragment "G" would be converted as: 

$$6\cdot 26^0 = 6$$

The Durandal Coefficent of a pair of file indices can be computed as follows,
assuming that the indices being compared are $i_a$ and $i_b$, being comprised
of respectively fragments $f_1, f_2$ and $f_3, f_4$, as their numeric
representations:

$$\left((f_1 - f_3) \cdot (- f_3 + f_1) + (f_2 - f_4) \cdot (-f_4 + f_2)\right)^\frac{1}{2}$$

For example, let's consider the values indices $FM, Z$ and $QK, G$:

$$f_1 = 312 \, f_2 = 7 \, f_3 = 348\, f_4 = 6$$

This would give us a Durndal Coefficent of:

$$\left((312 - 348) \cdot (-348 + 312) + (7 - 6) \cdot (-6 + 7)\right)^\frac{1}{2} \approx 36.0138$$

You must find the file index pair with the lowest Durandal Coefficent before
time runs out for the UESC marathon!

# Input

Input will be provided in the following format:

```
k
x1 y1
x2 y2
x3 y3
...
xk yk
```

$k$ will be an integer in $2\hdots1\cdot10^7$

Each $x_n$ and $y_n$ will be strings containing between one and five uppercase
latin letters. They will always match the regular expression `[A-Z]{1,5}`.

# Output

Output will be in the form

```
x1 y1
x2 y2
```

Where ($x_1, y_1$) and ($x_2, y_2$) are the two index-pairs which have the
lowest Durandal Coefficient.

**NOTE**: for consistency, output must be sorted by the sum of the numeric
values of both fragments of each index. For example, if the output indices were
$A,B$ and $C,D$, then $A,B$ would always be output first, and $C,D$ would
always be output second.

# Samples

## Input 1

```
4
FM Z
QK G
J EN
XH NE
```

## Output 1

```
FM Z
QK G
```

## Explanation 1

The Durindal Coefficient of each index is as follows:

```
Durindal Coeff.		idx a		idx b
36.013886210738214	[FM, Z]		[QK, G]
36.013886210738214	[QK, G]		[FM, Z]
313.639920928443	[FM, Z]		[J, EN]
313.639920928443	[J, EN]		[FM, Z]
347.6391807607422	[J, EN]		[QK, G]
347.6391807607422	[QK, G]		[J, EN]
574.7390712314589	[QK, G]		[XH, NE]
574.7390712314589	[XH, NE]	[QK, G]
590.3507432027168	[FM, Z]		[XH, NE]
590.3507432027168	[XH, NE]	[FM, Z]
701.2674240259561	[J, EN]		[XH, NE]
701.2674240259561	[XH, NE]	[J, EN]
```

## Input 2

```
10
QBY LET
WQOT IEAAY
S VFQGS
T SK
KBUG FQLQU
VG N
G XX
OA LKVYH
SLJ Q
ZHR HJN
```

## Output 2

```
T SK
G XX
```
