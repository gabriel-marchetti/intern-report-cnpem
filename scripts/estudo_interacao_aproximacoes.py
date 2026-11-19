"""Reproduz os quatro casos do notebook error_analysis_beam_profile e suas figuras."""
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/relatorio-matplotlib')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
from scipy.optimize import curve_fit

out = Path(__file__).resolve().parents[1] / 'imagens'
x = np.linspace(-10, 10, 3001)
dx = x[1] - x[0]

def area(y):
    return np.trapz(y, x)

def gaussian(x, center, sigma, amplitude):
    return amplitude * np.exp(-((x-center)**2)/(2*sigma**2))

sinc2 = np.sinc(x)**2
sinc2 /= area(sinc2)
popt, _ = curve_fit(gaussian, x, sinc2, p0=[0.,1.,1.])
g = gaussian(x, *popt)
g /= area(g)
f0 = np.where(x < 0, 0., 1.)
f1 = np.clip(x + .5, 0, 1)
conv = lambda f,h: fftconvolve(f,h,mode='same')*dx
cases = [conv(f0,g), conv(f1,g), conv(f0,sinc2), conv(f1,sinc2)]
c = cases[3]-cases[2]-cases[1]+cases[0]
assert np.allclose(c,conv(f1-f0,sinc2-g),atol=1e-12)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12})
fig, axes = plt.subplots(4,3,figsize=(12.8,10.5),layout='constrained')
for i,(f,h,ft,ht) in enumerate([(f0,g,'Degrau ideal','Gaussiana'),(f1,g,'Borda em rampa','Gaussiana'),(f0,sinc2,'Degrau ideal',r'$\mathrm{sinc}^2$'),(f1,sinc2,'Borda em rampa',r'$\mathrm{sinc}^2$')]):
    for j,(y,color,title) in enumerate([(f,'blue',ft),(h,'orange',ht),(cases[i],'#23852c',f'Caso {i+1}: {ft.lower()} * '+ht)]):
        ax=axes[i,j];ax.plot(x,y,color=color,lw=1.6);ax.set_xlim(-5,5);ax.set_title(title,fontsize=12);ax.set_xlabel('Posição');ax.set_ylabel('Valor do perfil');ax.tick_params(labelsize=10)
fig.savefig(out/'interacao_aproximacoes_quatro_casos.pdf');fig.savefig(out/'interacao_aproximacoes_quatro_casos.png',dpi=180);plt.close(fig)
for overlay,name in [(False,'interacao_aproximacoes_residuo'),(True,'interacao_aproximacoes_comparacao_gaussiana')]:
    fig,ax=plt.subplots(figsize=(8,4.5),layout='constrained')
    ax.plot(x,c,color='purple',lw=1.6,label=r'$C=c_4-c_3-c_2+c_1$')
    if overlay:ax.plot(x,g,color='orange',ls='--',lw=1.7,label='Gaussiana normalizada')
    ax.set(xlabel='Posição',ylabel='Valor numérico',title='Resíduo de interação'+(' e perfil gaussiano' if overlay else ' entre as aproximações'))
    ax.grid(alpha=.15);ax.legend(fontsize=10);ax.set_xlim(-10,10)
    fig.savefig(out/f'{name}.pdf');fig.savefig(out/f'{name}.png',dpi=200);plt.close(fig)
print('pico de |C|:',np.max(abs(c)))
print('max|C|/max|c1|:',np.max(abs(c))/np.max(abs(cases[0])))
print('norma L2 C/norma L2 c1:',np.linalg.norm(c)/np.linalg.norm(cases[0]))
print('gaussian fit center sigma amplitude:',popt)
