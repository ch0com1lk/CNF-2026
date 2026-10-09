import sys, pathlib
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from fbasym import (M_Z, coeficientes, terminos_A, afb_teorica, rejection_sampling,
                    asimetria_fb, particulas_por_grado, esperado_por_grado)


def test_afb_en_el_polo():
    # valor conocido: A_FB(mu) en el polo de la Z ~ 0.017
    assert abs(afb_teorica(M_Z) - 0.0166) < 0.001


def test_solo_fotón_a_baja_energía():
    A, B = coeficientes(1.0)          # chi -> 0
    assert abs(A - 1) < 1e-3 and abs(B) < 1e-3


def test_terminos_suman_A():
    for E in (50, 80, M_Z, 100, 150):
        assert abs(sum(terminos_A(E)) - coeficientes(E)[0]) < 1e-9


def test_signo_de_afb_alrededor_del_polo():
    assert afb_teorica(80) < 0 < afb_teorica(105)


def test_muestreo_reproduce_afb():
    np.random.seed(0)
    ev, ef = rejection_sampling(1.0, 0.5, 200000)
    assert abs(asimetria_fb(ev) - 3 * 0.5 / 8) < 0.01
    assert 45 < ef < 55


def test_muestreo_rechaza_distribucion_negativa():
    try:
        rejection_sampling(1.0, 5.0, 10)
    except ValueError:
        return
    raise AssertionError("debía lanzar ValueError")


def test_conteo_por_grado_suma_N():
    np.random.seed(1)
    ev, _ = rejection_sampling(1.0, 0.0, 5000)
    cuentas, _ = particulas_por_grado(ev)
    assert len(cuentas) == 180 and cuentas.sum() == 5000
    assert abs(esperado_por_grado(1.0, 0.0, 5000).sum() - 5000) < 1e-6
