"""Eliminasi Gauss langkah demi langkah, dengan aritmetika Fraction (eksak)."""
from fractions import Fraction
from typing import NamedTuple

UNIK, TAK_ADA, TAK_HINGGA = "unik", "tak_ada_solusi", "tak_hingga"


class Langkah(NamedTuple):
    deskripsi: str
    matriks: list


class Hasil(NamedTuple):
    status: str
    solusi: list | None
    log: list


def _pecahan(x):
    # Fraction(0.1) membawa galat biner; lewat str hasilnya 1/10.
    return x if isinstance(x, Fraction) else Fraction(str(x))


def _teks(x):
    return str(x).replace("-", "−")


def _catat(log, deskripsi, M):
    log.append(Langkah(deskripsi, [baris[:] for baris in M]))


def _augmented(A, B):
    n = len(A)
    if n == 0 or len(B) != n or any(len(baris) != n for baris in A):
        raise ValueError(
            f"A harus persegi n×n dengan n ≥ 1 dan len(B) = n; "
            f"diterima A: {[len(b) for b in A]}, B: {len(B)}"
        )
    return [[_pecahan(v) for v in baris] + [_pecahan(b)] for baris, b in zip(A, B)]


def _eliminasi_maju(M, log):
    """Ubah M menjadi bentuk eselon baris. Mengembalikan rank.

    Invarian: baris 0..r-1 sudah punya pivot dan entri di bawahnya nol.
    Baris hanya ditukar bila pivot di posisi (r, c) nol.
    """
    n = len(M)
    r = 0
    for c in range(n):
        asal = next((i for i in range(r, n) if M[i][c] != 0), None)
        if asal is None:
            _catat(log, f"Kolom {c + 1} tanpa pivot", M)
            continue
        if asal != r:
            M[r], M[asal] = M[asal], M[r]
            _catat(log, f"R{r + 1} ↔ R{asal + 1}", M)
        for i in range(r + 1, n):
            if M[i][c]:
                faktor = M[i][c] / M[r][c]
                M[i] = [a - faktor * b for a, b in zip(M[i], M[r])]
                _catat(log, f"R{i + 1} ← R{i + 1} − ({_teks(faktor)})·R{r + 1}", M)
        r += 1
    return r


def _klasifikasi(M, rank):
    n = len(M)
    if any(not any(baris[:n]) and baris[n] for baris in M):  # ada baris 0 = c, c ≠ 0
        return TAK_ADA
    return UNIK if rank == n else TAK_HINGGA


def _substitusi_mundur(M, log):
    n = len(M)
    x = [Fraction(0)] * n
    for i in reversed(range(n)):
        sisa = M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))
        x[i] = sisa / M[i][i]
        _catat(log, f"{nama(i, n)} = {_teks(x[i])}", M)
    return x


def solve(A, B):
    """Selesaikan A·X = B. Mengembalikan Hasil(status, solusi, log)."""
    M = _augmented(A, B)
    log = []
    _catat(log, "Matriks augmented [A | B]", M)
    status = _klasifikasi(M, _eliminasi_maju(M, log))
    if status != UNIK:
        _catat(log, f"Status: {status}", M)
        return Hasil(status, None, log)
    return Hasil(UNIK, _substitusi_mundur(M, log), log)


def nama(i, n):
    return "xyz"[i] if n <= 3 else f"x{i + 1}"


def format_matriks(M):
    sel = [[_teks(v) for v in baris] for baris in M]
    lebar = [max(map(len, kolom)) for kolom in zip(*sel)]
    pas = [[s.rjust(w) for s, w in zip(baris, lebar)] for baris in sel]
    return "\n".join(f"[ {'  '.join(b[:-1])} | {b[-1]} ]" for b in pas)


def format_log(log):
    return "\n\n".join(
        f"{i}. {langkah.deskripsi}\n{format_matriks(langkah.matriks)}"
        for i, langkah in enumerate(log)
    )


def format_solusi(solusi):
    """Dibulatkan 2 desimal. Hanya untuk status unik."""
    n = len(solusi)
    return "\n".join(f"{nama(i, n)} = {float(v):.2f}" for i, v in enumerate(solusi))


if __name__ == "__main__":
    hasil = solve([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], [8, -11, -3])
    print(format_log(hasil.log))
    print(f"\nStatus: {hasil.status}")
    if hasil.status == UNIK:
        print(format_solusi(hasil.solusi))
