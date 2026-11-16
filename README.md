# Solver SPLTV langkah demi langkah / Step-by-step SPLTV solver

Eliminasi Gauss yang ditulis sendiri, tanpa `np.linalg.solve`, dan mencetak setiap operasi baris.
Gauss elimination written from scratch, no `np.linalg.solve`, printing every row operation.

[Bahasa Indonesia](#bahasa-indonesia) · [English](#english)

```
 2x +  y −  z =   8
−3x −  y + 2z = −11
−2x +  y + 2z =  −3
```

```
1. R2 ← R2 − (−3/2)·R1
[  2    1   −1 |  8 ]
[  0  1/2  1/2 |  1 ]
[ −2    1    2 | −3 ]

...

3. R3 ← R3 − (4)·R2
[ 2    1   −1 | 8 ]
[ 0  1/2  1/2 | 1 ]
[ 0    0   −1 | 1 ]

4. z = −1
5. y = 3
6. x = 2

Status: unik
x = 2.00
y = 3.00
z = -1.00
```

Keluaran di atas dipotong dari `python gauss_solver.py`. Setiap langkah aslinya diikuti matriks augmented.
The output above is trimmed from `python gauss_solver.py`. Every step is followed by the augmented matrix in the real output.

## Bahasa Indonesia

### Cara pakai

Python 3.10 ke atas. Solver hanya memakai pustaka standar.

```python
from gauss_solver import solve, format_log, format_solusi

hasil = solve([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], [8, -11, -3])
print(hasil.status)                 # "unik"
print(format_log(hasil.log))        # semua langkah beserta matriksnya
print(format_solusi(hasil.solusi))  # hanya bila status "unik"
```

`solve(A, B)` mengembalikan `Hasil(status, solusi, log)`. `solusi` berisi `Fraction`, dan bernilai `None` bila status bukan `unik`. Bentuk A yang bukan persegi, panjang B yang salah, atau matriks kosong memunculkan `ValueError`.

### Beda dari `linear-solver`

`linear-solver` memanggil `np.linalg.solve`: jawabannya benar, tetapi prosesnya tidak terlihat. Repo ini menulis eliminasi dan substitusi mundurnya sendiri supaya setiap langkah bisa dibaca dan dicek dengan tangan. NumPy hanya dipakai di tes, sebagai pembanding.

### Tiga status

| Status | Arti | Contoh |
|---|---|---|
| `unik` | tepat satu solusi | contoh di atas |
| `tak_ada_solusi` | ada baris `0 = c` dengan c ≠ 0 | x + y = 1 dan x + y = 2 |
| `tak_hingga` | rank < n tanpa kontradiksi | x + y = 1 dan 2x + 2y = 2 |

### Keputusan desain

- Semua hitungan memakai `fractions.Fraction`, jadi hasilnya eksak, log menampilkan `1/2` dan bukan `0.5`, dan pivot nol cukup dicek dengan `== 0`. Tidak ada toleransi float.
- Baris ditukar hanya bila pivot bernilai nol, supaya log mirip hitungan tangan.
- Untuk `tak_hingga`, solver hanya melaporkan status, tanpa bentuk parametrik.

### Tes

```
pip install pytest numpy
pytest
```

Tes mencakup lima jenis sistem (unik, tanpa solusi, tak hingga, pivot nol di baris pertama, dan 30 sistem acak yang dicocokkan dengan `np.linalg.solve`), serta input yang dimensinya salah.

## English

### Usage

Python 3.10 or newer. The solver uses only the standard library.

```python
from gauss_solver import solve, format_log, format_solusi

result = solve([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], [8, -11, -3])
print(result.status)                 # "unik"
print(format_log(result.log))        # every step with its matrix
print(format_solusi(result.solusi))  # only when the status is "unik"
```

`solve(A, B)` returns `Hasil(status, solusi, log)`. `solusi` is a list of `Fraction` and is `None` unless the status is `unik`. A non-square A, a B of the wrong length, or an empty matrix raises `ValueError`.

Identifiers and log text are in Indonesian. `solusi` is the solution, and a log line such as `Kolom 1 tanpa pivot` means "column 1 has no pivot".

### How it differs from `linear-solver`

`linear-solver` calls `np.linalg.solve`: the answer is right, but the process is hidden. This repo writes the elimination and back substitution itself, so every step can be read and checked by hand. NumPy is used only in the tests, as a reference.

### The three statuses

| Status | Meaning | Example |
|---|---|---|
| `unik` | exactly one solution | the example above |
| `tak_ada_solusi` | no solution: a row reads `0 = c` with c ≠ 0 | x + y = 1 and x + y = 2 |
| `tak_hingga` | infinitely many: rank < n with no contradiction | x + y = 1 and 2x + 2y = 2 |

### Design decisions

- All arithmetic uses `fractions.Fraction`: results are exact, the log shows `1/2` instead of `0.5`, and a zero pivot is a plain `== 0` check. There is no float tolerance.
- Rows are swapped only when the pivot is zero, so the log reads like working by hand.
- For `tak_hingga` the solver reports the status only, with no parametric form.

### Tests

```
pip install pytest numpy
pytest
```

The tests cover the five kinds of system (unique, no solution, infinite, zero pivot in the first row, and 30 random systems checked against `np.linalg.solve`), plus malformed dimensions.
