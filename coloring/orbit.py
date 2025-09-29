# orbit_complex_fourier.py
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Literal, Optional, Sequence, Tuple

Metric = Literal["cosine", "euclidean"]


# ----------------- (reuse your distance functions if needed) -----------------
def _as_2d(a: np.ndarray) -> np.ndarray:
    a = np.asarray(a)
    if a.ndim == 1:
        a = a[None, :]
    return a


def cosine_distance_matrix(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    A = _as_2d(A).astype(np.float64)
    b = np.asarray(b, dtype=np.float64).ravel()
    A_norm = np.linalg.norm(A, axis=1, keepdims=True)
    b_norm = np.linalg.norm(b)
    A_safe = np.divide(A, np.maximum(A_norm, 1e-12), where=A_norm != 0)
    b_safe = b / max(b_norm, 1e-12)
    sim = A_safe @ b_safe
    return 1.0 - sim


def euclidean_distance_matrix(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    A = _as_2d(A).astype(np.float64)
    b = np.asarray(b, dtype=np.float64).ravel()
    return np.linalg.norm(A - b, axis=1)


# ----------------- complex orbit helpers -----------------
def make_complex_orbit(
    distances: Sequence[float], overlaps: Sequence[float]
) -> np.ndarray:
    """
    Build complex series z = distance + 1j*overlap (overlap expected in [0,1]).
    """
    d = np.asarray(distances, dtype=np.float64).ravel()
    o = np.asarray(overlaps, dtype=np.float64).ravel()
    if d.shape != o.shape:
        raise ValueError("distances and overlaps must have same length.")
    # clip to [0,1] for safety
    o = np.clip(o, 0.0, 1.0)
    return d + 1j * o


def detrend_pairwise(
    z: np.ndarray, mode: Literal["none", "mean", "linear"] = "mean"
) -> np.ndarray:
    """
    Detrend real and imaginary parts separately and recombine.
    """
    z = np.asarray(z, dtype=np.complex128).ravel()
    x = z.real
    y = z.imag

    def _detrend(a: np.ndarray) -> np.ndarray:
        if mode == "none":
            return a
        if mode == "mean":
            return a - a.mean()
        if mode == "linear":
            n = len(a)
            t = np.arange(n)
            A = np.vstack([t, np.ones(n)]).T
            m, c = np.linalg.lstsq(A, a, rcond=None)[0]
            return a - (m * t + c)
        raise ValueError("mode must be 'none', 'mean', or 'linear'.")

    xr = _detrend(x)
    yr = _detrend(y)
    return xr + 1j * yr


def apply_window(
    z: np.ndarray, window: Optional[Literal["hann"]] = "hann"
) -> np.ndarray:
    z = np.asarray(z, dtype=np.complex128).ravel()
    if window == "hann":
        w = np.hanning(len(z))
        # amplitude-correct roughly so scales stay readable
        z = (z * w) / (w.mean() if w.mean() != 0 else 1.0)
    return z


# ----------------- FFT / iFFT for complex series -----------------
def compute_fft_complex(
    z: Sequence[complex],
    sampling: float = 1.0,
    window: Optional[Literal["hann"]] = "hann",
    detrend_mode: Literal["none", "mean", "linear"] = "mean",
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Complex FFT. Returns (freqs, magnitude, complex_spectrum).
    """
    z = detrend_pairwise(z, detrend_mode)
    z = apply_window(z, window)
    Z = np.fft.fft(z)  # complex spectrum (two-sided)
    freqs = np.fft.fftfreq(len(z), d=sampling)
    mag = np.abs(Z)
    return freqs, mag, Z


def ifft_reconstruct_complex(
    spectrum: np.ndarray,
    keep: Literal["lowpass", "topk"] = "lowpass",
    lowpass_frac: float = 0.1,
    topk: int = 10,
) -> np.ndarray:
    """
    Filter complex spectrum and iFFT. Works on two-sided FFT output.
    """
    Z = spectrum.copy()
    N = len(Z)

    if keep == "lowpass":
        # keep symmetric lowest |f| bins
        half = N // 2
        cutoff = max(1, int(np.floor(lowpass_frac * half)))
        mask = np.zeros(N, dtype=bool)
        mask[:cutoff] = True
        mask[-cutoff:] = True
        Z = np.where(mask, Z, 0)
    elif keep == "topk":
        mag = np.abs(Z)
        # ensure DC kept if present
        keep_bins = np.argpartition(mag, -topk)[-topk:]
        mask = np.zeros_like(mag, dtype=bool)
        mask[keep_bins] = True
        mask[0] = True
        Z = np.where(mask, Z, 0)
    else:
        raise ValueError("keep must be 'lowpass' or 'topk'.")

    z_rec = np.fft.ifft(Z)
    return z_rec


# ----------------- Plotting -----------------
def plot_orbit_components(
    z: Sequence[complex],
    title: str = "Orbit components",
    figsize: Tuple[int, int] = (10, 4),
    save_path: Optional[str] = None,
    show: bool = True,
) -> None:
    z = np.asarray(z, dtype=np.complex128).ravel()
    idxs = np.arange(len(z))
    plt.figure(figsize=figsize)
    plt.plot(idxs, z.real, marker="o", linewidth=1.25, label="Distance (real)")
    plt.plot(idxs, z.imag, linewidth=1.25, label="Overlap (imag)")
    plt.xlabel("Sentence index")
    plt.ylabel("Value")
    plt.title(title)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    if save_path:
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
    if show:
        plt.tight_layout()
        plt.show()
    else:
        plt.close()


def plot_complex_plane(
    z: Sequence[complex],
    title: str = "Complex-plane view: overlap (imag) vs distance (real)",
    figsize: Tuple[int, int] = (5, 5),
    save_path: Optional[str] = None,
    show: bool = True,
) -> None:
    z = np.asarray(z, dtype=np.complex128).ravel()
    plt.figure(figsize=figsize)
    plt.scatter(z.real, z.imag, s=40)  # default color
    plt.xlabel("Distance (real)")
    plt.ylabel("Overlap (imag, 0..1)")
    plt.title(title)
    plt.grid(True, linestyle="--", alpha=0.4)
    if save_path:
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
    if show:
        plt.tight_layout()
        plt.show()
    else:
        plt.close()


def plot_fft_magnitude_complex(
    freqs: np.ndarray,
    magnitude: np.ndarray,
    title: str = "Complex FFT magnitude spectrum",
    figsize: Tuple[int, int] = (10, 4),
    xlim: Optional[Tuple[float, float]] = None,
    save_path: Optional[str] = None,
    show: bool = True,
) -> None:
    plt.figure(figsize=figsize)
    # shift for symmetric display (optional but neat)
    f = np.fft.fftshift(freqs)
    m = np.fft.fftshift(magnitude)
    plt.plot(f, m, linewidth=1.25)
    plt.xlabel("Frequency (cycles per index)")
    plt.ylabel("|Z(f)|")
    plt.title(title)
    plt.grid(True, linestyle="--", alpha=0.4)
    if xlim:
        plt.xlim(*xlim)
    if save_path:
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
    if show:
        plt.tight_layout()
        plt.show()
    else:
        plt.close()


def plot_reconstruction_components(
    z: Sequence[complex],
    z_rec: Sequence[complex],
    title: str = "Reconstruction (components)",
    figsize: Tuple[int, int] = (10, 4),
    save_path: Optional[str] = None,
    show: bool = True,
) -> None:
    z = np.asarray(z, dtype=np.complex128).ravel()
    zr = np.asarray(z_rec, dtype=np.complex128).ravel()
    idxs = np.arange(len(z))
    plt.figure(figsize=figsize)
    # real (distance)
    plt.plot(
        idxs,
        z.real,
        marker="o",
        linewidth=1.0,
        alpha=0.85,
        label="Real orig (distance)",
    )
    plt.plot(idxs, zr.real, linewidth=2.0, alpha=0.95, label="Real recon")
    # imag (overlap)
    plt.plot(idxs, z.imag, linewidth=1.0, alpha=0.85, label="Imag orig (overlap)")
    plt.plot(idxs, zr.imag, linewidth=2.0, alpha=0.95, label="Imag recon")
    plt.xlabel("Sentence index")
    plt.ylabel("Value")
    plt.title(title)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    if save_path:
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
    if show:
        plt.tight_layout()
        plt.show()
    else:
        plt.close()


# ----------------- Example wiring -----------------
if __name__ == "__main__":
    rng = np.random.default_rng(0)

    # Fake distances/overlaps for demo (replace with your real ones)
    n = 120
    distances = (
        np.abs(np.sin(np.linspace(0, 8 * np.pi, n)) + 0.1 * rng.normal(size=n)) + 0.3
    )
    overlaps = np.clip(
        0.5
        + 0.4 * np.sin(np.linspace(0, 3 * np.pi, n) + 1.2)
        + 0.1 * rng.normal(size=n),
        0,
        1,
    )

    z = make_complex_orbit(distances, overlaps)

    # 1) Time-domain components and complex-plane view
    plot_orbit_components(z, title="Orbit components: distance (real) & overlap (imag)")
    plot_complex_plane(z, title="Complex-plane view (distance vs overlap)")

    # 2) Complex FFT magnitude
    freqs, mag, Z = compute_fft_complex(
        z, sampling=1.0, window="hann", detrend_mode="mean"
    )
    plot_fft_magnitude_complex(
        freqs, mag, title="Complex FFT magnitude (detrended + Hann)"
    )

    # 3) iFFT reconstructions (lowpass and topK)
    z_low = ifft_reconstruct_complex(Z, keep="lowpass", lowpass_frac=0.08)
    plot_reconstruction_components(
        z, z_low, title="Low-pass iFFT reconstruction (8% of |f|)"
    )

    z_topk = ifft_reconstruct_complex(Z, keep="topk", topk=12)
    plot_reconstruction_components(z, z_topk, title="Top-12 peaks iFFT reconstruction")
