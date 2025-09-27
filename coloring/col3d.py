import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def complex_map_surface(
    f,
    xlim=(-2, 2),
    ylim=(-2, 2),
    n=200,
    cmap="hsv",
    clip_r=None,
    elev=30,
    azim=45,
    title=None,
    show=True,
    save=None,
):
    """
    Visualize a complex function f: C -> C.

    Domain:  z = x + i y over [xlim] x [ylim] (grid size n x n)
    Range:   w = f(z)
    Plot:    z-axis = |w|, face color = arg(w)
    """
    # Build domain grid
    x = np.linspace(xlim[0], xlim[1], n)
    y = np.linspace(ylim[0], ylim[1], n)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    # Evaluate function
    W = f(Z)

    # Magnitude and angle
    R = np.abs(W)                     # height
    Theta = np.angle(W)               # in (-pi, pi]
    Theta_wrapped = (Theta + np.pi) % (2 * np.pi)  # [0, 2pi)

    # Optional clipping of magnitude to reduce extreme spikes
    if clip_r is not None:
        R = np.minimum(R, clip_r)

    # Handle invalids: make them transparent & drop surface height to NaN
    invalid = ~np.isfinite(R) | ~np.isfinite(Theta_wrapped)
    R = R.astype(float)
    R[invalid] = np.nan

    # Set up colormap based on theta
    cmap_obj = plt.get_cmap(cmap)
    norm = mcolors.Normalize(vmin=0.0, vmax=2 * np.pi)
    facecolors = cmap_obj(norm(Theta_wrapped))
    # Make invalid areas transparent
    facecolors = facecolors.copy()
    facecolors[..., 3][invalid] = 0.0

    # Plot
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(
        X, Y, R,
        facecolors=facecolors,
        rstride=1,
        cstride=1,
        antialiased=False,
        linewidth=0
    )

    ax.set_xlabel("x = Re(z)")
    ax.set_ylabel("y = Im(z)")
    ax.set_zlabel(r"|f(z)|")
    ax.view_init(elev=elev, azim=azim)
    ax.set_title(title or "Complex map: height = |f(z)|, color = arg(f(z))")

    # Angle colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap_obj, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, pad=0.1, shrink=0.75)
    cbar.set_label(r"arg(f(z)) (radians)")
    ticks = [0, 0.5*np.pi, np.pi, 1.5*np.pi, 2*np.pi]
    cbar.set_ticks(ticks)
    cbar.set_ticklabels([r"$-\pi$", r"$-\pi/2$", r"$0$", r"$\pi/2$", r"$\pi$"])

    plt.tight_layout()

    if save is not None:
        fig.savefig(save, dpi=150, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig, ax


# -----------------------
# EXAMPLES & TESTS
# -----------------------

def test_z_squared():
    complex_map_surface(
        lambda z: z**2,
        xlim=(-2, 2), ylim=(-2, 2), n=100, clip_r=10,
        cmap="hsv", show=False, save="test_z2.png",
        title="f(z)=z^2 (test)"
    )
    print("PASS: test_z_squared (saved to test_z2.png)")

def test_mobius():
    def f(z): return (z - 1) / (z + 1)
    complex_map_surface(
        f,
        xlim=(-2, 2), ylim=(-2, 2), n=120, clip_r=5,
        cmap="twilight_shifted", show=False, save="test_mobius.png",
        title="f(z)=(z-1)/(z+1) (test)"
    )
    print("PASS: test_mobius (saved to test_mobius.png)")

def test_exp():
    complex_map_surface(
        np.exp,
        xlim=(-2, 2), ylim=(-2, 2), n=120, clip_r=20,
        cmap="twilight", show=False, save="test_exp.png",
        title="f(z)=exp(z) (test)"
    )
    print("PASS: test_exp (saved to test_exp.png)")

# ---- New richer examples ----

def test_reciprocal():
    # Avoid division by exact zero by adding a tiny epsilon where needed
    def f(z):
        z_safe = np.where(z == 0, 1e-12 + 0j, z)
        return 1.0 / z_safe
    complex_map_surface(
        f,
        xlim=(-2, 2), ylim=(-2, 2), n=140, clip_r=25,
        cmap="hsv", show=False, save="test_reciprocal.png",
        title="f(z)=1/z (test)"
    )
    print("PASS: test_reciprocal (saved to test_reciprocal.png)")

def test_logarithm():
    # Principal branch of log – clear branch cut along negative real axis
    def f(z):
        # avoid log(0)
        z_safe = np.where(z == 0, 1e-12 + 0j, z)
        return np.log(z_safe)
    complex_map_surface(
        f,
        xlim=(-3, 3), ylim=(-3, 3), n=160, clip_r=4,
        cmap="twilight_shifted", show=False, save="test_log.png",
        title="f(z)=log(z) (principal branch, test)"
    )
    print("PASS: test_logarithm (saved to test_log.png)")

def test_sqrt():
    # Square root shows a classic branch cut
    def f(z):
        return np.sqrt(z)
    complex_map_surface(
        f,
        xlim=(-3, 3), ylim=(-3, 3), n=160, clip_r=3,
        cmap="twilight", show=False, save="test_sqrt.png",
        title="f(z)=sqrt(z) (principal branch, test)"
    )
    print("PASS: test_sqrt (saved to test_sqrt.png)")

def test_tan():
    # Dense poles; clip_r keeps the surface readable
    def f(z):
        return np.tan(z)
    complex_map_surface(
        f,
        xlim=(-2.5, 2.5), ylim=(-2.5, 2.5), n=160, clip_r=8,
        cmap="hsv", show=False, save="test_tan.png",
        title="f(z)=tan(z) (test)"
    )
    print("PASS: test_tan (saved to test_tan.png)")

def test_blaschke():
    # Blaschke product B_a(z) = (z-a) / (1 - conj(a) z), |a|<1
    a = 0.5 * np.exp(1j * np.pi/4)  # off-center in unit disk
    def f(z):
        return (z - a) / (1 - np.conj(a) * z)
    complex_map_surface(
        f,
        xlim=(-1.5, 1.5), ylim=(-1.5, 1.5), n=160, clip_r=4,
        cmap="twilight_shifted", show=False, save="test_blaschke.png",
        title="Blaschke product B_a(z) (|a|<1) (test)"
    )
    print("PASS: test_blaschke (saved to test_blaschke.png)")

def test_rational_cubic():
    # (z^3 - 1) / (z^3 + 1): three zeros and three poles → vivid phase pattern
    def f(z):
        return (z**3 - 1) / (z**3 + 1)
    complex_map_surface(
        f,
        xlim=(-2, 2), ylim=(-2, 2), n=160, clip_r=8,
        cmap="hsv", show=False, save="test_rat_cubic.png",
        title="f(z)=(z^3-1)/(z^3+1) (test)"
    )
    print("PASS: test_rational_cubic (saved to test_rat_cubic.png)")

def test_sin():
    def f(z):
        return np.sin(z)
    complex_map_surface(
        f,
        xlim=(-3, 3), ylim=(-3, 3), n=160, clip_r=8,
        cmap="twilight", show=False, save="test_sin.png",
        title="f(z)=sin(z) (test)"
    )
    print("PASS: test_sin (saved to test_sin.png)")


if __name__ == "__main__":
    # Headless-friendly backend
    matplotlib.use("Agg", force=True)

    # Original trio
    test_z_squared()
    test_mobius()
    test_exp()

    # New richer set
    test_reciprocal()
    test_logarithm()
    test_sqrt()
    test_tan()
    test_blaschke()
    test_rational_cubic()
    test_sin()

    # To view interactively, comment out the Agg line above and call any test with show=True
