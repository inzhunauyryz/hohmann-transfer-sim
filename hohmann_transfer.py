import matplotlib.pyplot as plt
import numpy as np

MU_EARTH = 398600.4418  # км^3 / с^2
R_EARTH = 6378.137  # км


class HohmannTransfer:

  def __init__(self, alt_initial_km: float, alt_target_km: float):
    self.r1 = R_EARTH + alt_initial_km
    self.r2 = R_EARTH + alt_target_km
    self.a_trans = (self.r1 + self.r2) / 2.0

  def calculate_burns(self):
    v1 = np.sqrt(MU_EARTH / self.r1)
    v2 = np.sqrt(MU_EARTH / self.r2)

    v_trans_peri = np.sqrt(MU_EARTH * (2.0 / self.r1 - 1.0 / self.a_trans))
    v_trans_apo = np.sqrt(MU_EARTH * (2.0 / self.r2 - 1.0 / self.a_trans))

    dv1 = v_trans_peri - v1
    dv2 = v2 - v_trans_apo
    dv_total = dv1 + dv2

    tof_seconds = np.pi * np.sqrt((self.a_trans**3) / MU_EARTH)
    tof_hours = tof_seconds / 3600.0

    return {
        'v1': v1,
        'v2': v2,
        'dv1': dv1,
        'dv2': dv2,
        'dv_total': dv_total,
        'tof_hours': tof_hours,
    }

  def plot_orbits(self, save_filename='hohmann_transfer.png'):
    results = self.calculate_burns()

    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
    theta = np.linspace(0, 2 * np.pi, 500)

    x1 = self.r1 * np.cos(theta)
    y1 = self.r1 * np.sin(theta)
    ax.plot(x1, y1, 'b--', label=f'Initial Orbit (r1 = {self.r1:.0f} km)')

    x2 = self.r2 * np.cos(theta)
    y2 = self.r2 * np.sin(theta)
    ax.plot(x2, y2, 'g--', label=f'Target Orbit (r2 = {self.r2:.0f} km)')

    ecc = (self.r2 - self.r1) / (self.r2 + self.r1)
    theta_half = np.linspace(0, np.pi, 300)
    r_trans_half = (self.a_trans * (1 - ecc**2)) / (1 + ecc * np.cos(theta_half))

    ax.plot(
        r_trans_half * np.cos(theta_half),
        r_trans_half * np.sin(theta_half),
        'r-',
        linewidth=2,
        label='Hohmann Transfer Trajectory',
    )

    earth = plt.Circle((0, 0), R_EARTH, color='darkblue', alpha=0.6, label='Earth')
    ax.add_patch(earth)

    ax.scatter(
        [self.r1], [0], color='red', s=70, zorder=5, label=f'Δv1 ({results["dv1"]:.3f} km/s)'
    )
    ax.scatter(
        [-self.r2],
        [0],
        color='orange',
        s=70,
        zorder=5,
        label=f'Δv2 ({results["dv2"]:.3f} km/s)',
    )

    ax.set_aspect('equal')
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.set_title(
        'Hohmann Transfer Orbit Simulation (LEO -> GEO)',
        fontsize=12,
        fontweight='bold',
    )
    ax.set_xlabel('X Position (km)')
    ax.set_ylabel('Y Position (km)')
    ax.legend(loc='upper right', fontsize=8)

    plt.tight_layout()
    plt.savefig(save_filename)
    return results


if __name__ == '__main__':
  sim = HohmannTransfer(alt_initial_km=300, alt_target_km=35786)
  res = sim.plot_orbits()
