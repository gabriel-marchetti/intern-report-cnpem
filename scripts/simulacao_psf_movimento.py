"""Quina estática observada por probe ideal com jitter gaussiano isotrópico."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

out = Path(__file__).resolve().parents[1] / 'imagens'
n = 160
obj = np.zeros((n, n))
obj[48:, 48:] = 1
sigmas = [0, 2, 6, 10, 12]
fig, axes = plt.subplots(1, 5, figsize=(13, 3.2))
for ax, sigma in zip(axes, sigmas):
    measured = obj if sigma == 0 else gaussian_filter(obj, sigma=sigma, mode='nearest')
    ax.imshow(measured, cmap='gray', vmin=0, vmax=1, interpolation='nearest')
    ax.set_title(rf'$\sigma_{{\rm mov}} = {sigma}$ px', fontsize=12)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.plot([99, 139], [140, 140], color='black', linewidth=2)
    ax.text(119, 134, '40 px', ha='center', va='bottom', fontsize=9)
fig.subplots_adjust(left=.015, right=.985, top=.88, bottom=.04, wspace=.10)
fig.savefig(out / 'quina_psf_oscilacao.pdf', bbox_inches='tight')
fig.savefig(out / 'quina_psf_oscilacao.png', dpi=220, bbox_inches='tight')
plt.close(fig)
