# CNF-2026
# Estudio Fenomenológico de la Asimetría Forward-Backward mediante Técnicas de Simulación Numérica

**Trabajo LXIX-012672**  
Presentado para el Congreso Nacional de Física (CNF 2026), Área: Partículas y Campos,  
Fecha: 16/10/2026,  
Lugar: Ensenada, Baja California,  
Organizado por la Sociedad Mexicana de Física.

**Autores:** M. Salinas Ibáñez (CINVESTAV), V. López Agustín y H. Novales Sánchez (FCFM-BUAP).

## Simulación Monte Carlo de la Forward-Backward Asymmetry en $e^+e^-\to\mu^+\mu^-$

Este proyecto implementa una simulación Monte Carlo (método de aceptación-rechazo) que genera la distribución angular de los muones producidos en $e^+e^-\to\mu^+\mu^-$ a partir de la interferencia entre el fotón virtual y el bosón $Z$, y permite estudiar cómo aparece la asimetría Forward-Backward ($A_{FB}$) al variar la energía de centro de masa $\sqrt{s}$.

## Requisitos

- Python 3.8 o superior  
- NumPy  
- Matplotlib  
- Jupyter (para ejecutar los notebooks)  
- pytest (opcional, para las pruebas)

## Instalación

```bash
git clone <url-del-repositorio>
cd fb-asymmetry-montecarlo
python -m venv .venv
source .venv/bin/activate          # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Estructura de Directorios

```
fb-asymmetry-montecarlo/
├── README.md
├── requirements.txt
├── docs/
│   └── teoria.md                      # Derivación completa de la sección eficaz
├── src/fbasym/
│   ├── physics.py                     # Coeficientes A(s), B(s), propagador, A_FB
│   ├── sampling.py                    # Algoritmo de aceptación-rechazo
│   ├── analysis.py                    # chi2, conteo por grado, extracción de sin²θ_W
│   └── plots.py                       # Figuras
├── notebooks/
│   ├── 01_fenomenologia_y_coeficientes.ipynb
│   ├── 02_simulacion_tres_casos.ipynb
│   ├── 03_transicion_con_la_energia.ipynb
│   ├── 04_sensibilidad_sin2thetaW.ipynb
│   └── 05_conteo_por_grado.ipynb
├── tests/
│   └── test_fbasym.py                 # Pruebas del código
├── data/
│   └── conteo_angular.csv             # Partículas por grado (180 filas)
└── figures/                           # Figuras generadas por los notebooks
```

## Plan de Trabajo

1. Análisis fenomenológico del proceso $e^+e^-\to\mu^+\mu^-$.  
2. Derivación de la sección eficaz diferencial a partir de la amplitud de dispersión.  
3. Inclusión de los términos de interferencia $\gamma$–$Z$.  
4. Implementación del algoritmo Monte Carlo (aceptación-rechazo) en Python:  
   - Generación de eventos que modelan la distribución angular de los muones.  
   - Análisis de distintas energías de centro de masa $\sqrt{s}$, en particular $\sqrt{s}=m_Z=91.1876$ GeV.  
   - Incorporación del propagador de Breit-Wigner.  
5. Observación de la distribución simétrica (solo fotón).  
6. Observación de la transición de la distribución simétrica a la asimétrica.  
7. Validación de la sensibilidad del método Monte Carlo para extraer parámetros físicos.  
8. Conteo de partículas en cada grado, de 0° a 180°.

## Uso

1. Ejecutar los notebooks en orden desde la carpeta `notebooks/`:

```bash
cd notebooks
jupyter notebook
```

| Notebook | Contenido |
|---|---|
| `01` | Fenomenología, amplitud, interferencia $\gamma$–$Z$ y coeficientes $A(\sqrt{s})$, $B(\sqrt{s})$ |
| `02` | Algoritmo de aceptación-rechazo y los tres casos: simétrico, asimetría propuesta y corrientes neutras |
| `03` | Transición simétrica → asimétrica y barrido en energía |
| `04` | Sensibilidad del método y extracción de $\sin^2\theta_W$ |
| `05` | Partículas por grado, de 0° a 180° |

2. Ejecutar las pruebas:

```bash
pytest
```

### El sistema

- Genera 10 000 eventos por caso con distribución $f(x)=A(1+x^2)+Bx$, con $x=\cos\theta$.  
- Calcula $A$ y $B$ para cualquier energía a partir de las amplitudes de helicidad (*helicity amplitudes*).  
- Incluye el propagador de Breit-Wigner de la $Z$ ($m_Z=91.1876$ GeV, $\Gamma_Z=2.4952$ GeV, $\sin^2\theta_W=0.23126$).  
- Implementa como métricas el $\chi^2/\text{ndof}$, los residuos normalizados y el error estadístico de $A_{FB}$.  
- Reproduce la distribución teórica con $\chi^2/\text{ndof}\approx1$ y una eficiencia de aceptación de aproximadamente 50 %.  
- Recupera $\sin^2\theta_W=0.2313\pm0.0020$ con $N=10^5$ eventos.

## Uso con Parámetros Propios

1. Elegir la energía de centro de masa $\sqrt{s}$ (en GeV) o, directamente, los coeficientes $A$ y $B$.  
2. Generar los eventos y medir la asimetría:

```python
import sys
sys.path.append("src")

import numpy as np
from fbasym import coeficientes, rejection_sampling, asimetria_fb, particulas_por_grado

np.random.seed(42)
A, B = coeficientes(95.0)                          # energía en GeV
eventos, eficiencia = rejection_sampling(A, B, 10000)

print("A_FB medida:", asimetria_fb(eventos))
cuentas, theta = particulas_por_grado(eventos)     # 180 intervalos de 1°
```

3. Para una asimetría arbitraria, usar `rejection_sampling(A, B, N)` con los valores deseados (la distribución debe ser no negativa en $[-1,1]$).  
4. El conteo por grado de los tres casos principales se guarda en `data/conteo_angular.csv`.

---

## Metodología

- Amplitud de dispersión con intercambio de $\gamma$ y $Z$ para fermiones sin masa, descompuesta en amplitudes de helicidad ($LL$, $RR$, $LR$, $RL$).  
- Sección eficaz diferencial de la forma $\dfrac{d\sigma}{dx}\propto A(1+x^2)+Bx$, donde:  
  - $A$ reúne los términos $\gamma\gamma$, de interferencia $\gamma Z$ y $ZZ$.  
  - $B$ controla la asimetría y se anula si solo existe el fotón.  
- Forward-Backward asymmetry: $A_{FB}=\dfrac{N_F-N_B}{N_F+N_B}=\dfrac{3}{8}\dfrac{B}{A}$.  
- Generación de eventos con el método de aceptación-rechazo:  
  - Proponer $x\in[-1,1]$ y una altura $y\in[0,f_{\max}]$.  
  - Aceptar el evento si $y\le f(x)$.  
- Conversión a ángulo con $\theta=\arccos(x)$ y conteo en intervalos de $1^\circ$.

## Validación

La simulación se valida mediante métricas cuantitativas como:  
- $\chi^2/\text{ndof}$ entre el histograma simulado y la distribución teórica  
- Residuos normalizados $(O_i-E_i)/\sqrt{E_i}$  
- Error estadístico de $A_{FB}$, $\sqrt{(1-A_{FB}^2)/N}$, que decrece como $1/\sqrt{N}$  
- Recuperación del valor verdadero de $\sin^2\theta_W$ en experimentos repetidos

## Limitaciones

Cálculo a nivel árbol, sin correcciones radiativas, sin radiación de estado inicial, sin efectos del detector, y solo con la forma angular (no la sección eficaz absoluta).


