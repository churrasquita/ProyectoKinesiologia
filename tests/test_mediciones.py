"""
Pruebas de los cálculos posturales y de la clasificación OMS del IMC.
Usan landmarks sintéticos: no necesitan el modelo .task ni cámara.

Ejecutar desde la raíz del proyecto:
    python -m unittest discover -s tests -v
"""
import os
import sys
import unittest
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.mediciones import (
    calcular_angulo_cervical,
    calcular_asimetria_hombros,
    calcular_dismetria_piernas,
    calibrar_con_hoja,
)
from utils.oms_imc import (
    MES_MAX,
    MES_MIN,
    clasificar_imc_oms,
    edad_en_meses,
    puntaje_z_imc,
)

# Imagen de 1024 x 1024: con coordenadas normalizadas múltiplos de 1/1024
# la conversión a píxeles es exacta.
W = H = 1024


def landmarks(**puntos):
    """33 landmarks visibles en (0.5, 0.5); `puntos` sobreescribe por índice: l11=(x, y[, vis])."""
    lista = [SimpleNamespace(x=0.5, y=0.5, visibility=1.0) for _ in range(33)]
    for nombre, valores in puntos.items():
        idx = int(nombre[1:])
        x, y, *vis = valores
        lista[idx] = SimpleNamespace(x=x, y=y, visibility=vis[0] if vis else 1.0)
    return lista


def px(n):
    return n / 1024


class TestCalibracion(unittest.TestCase):
    def test_factor_de_escala(self):
        self.assertAlmostEqual(calibrar_con_hoja(280), 0.1)

    def test_ancho_invalido(self):
        with self.assertRaises(ValueError):
            calibrar_con_hoja(0)


class TestPosturales(unittest.TestCase):
    def test_asimetria_hombros(self):
        lm = landmarks(l11=(0.25, px(512)), l12=(0.75, px(520)))
        self.assertAlmostEqual(calcular_asimetria_hombros(lm, W, H, 0.1), 0.8)

    def test_asimetria_hombros_nivelados(self):
        lm = landmarks(l11=(0.25, px(512)), l12=(0.75, px(512)))
        self.assertEqual(calcular_asimetria_hombros(lm, W, H, 0.1), 0.0)

    def test_dismetria_piernas(self):
        lm = landmarks(
            l23=(0.25, px(256)), l27=(0.25, px(768)),   # pierna izquierda: 512 px
            l24=(0.75, px(256)), l28=(0.75, px(778)),   # pierna derecha: 522 px
        )
        self.assertAlmostEqual(calcular_dismetria_piernas(lm, W, H, 0.1), 1.0)

    def test_angulo_cervical_vertical(self):
        lm = landmarks(l7=(px(512), px(256)), l11=(px(512), px(512)))
        self.assertAlmostEqual(calcular_angulo_cervical(lm, W, H), 90.0)

    def test_angulo_cervical_45_grados(self):
        lm = landmarks(l7=(px(256), px(256)), l11=(px(512), px(512)))
        self.assertAlmostEqual(calcular_angulo_cervical(lm, W, H), 45.0)

    def test_angulo_cervical_poca_visibilidad(self):
        lm = landmarks(l7=(0.25, 0.25, 0.2), l11=(0.5, 0.5))
        self.assertIsNone(calcular_angulo_cervical(lm, W, H))


class TestIMCOMS(unittest.TestCase):
    # Valores de BMI para -3, -2, 0, +1, +2 DE tomados de las columnas SD de las
    # tablas expandidas oficiales de la OMS (mes 126 = 10 años, mes 174 = 14 años).
    REF = {
        ("Masculino", 10): dict(sd3n=12.905, sd2n=13.886, sd0=16.679, sd1=18.808, sd2=21.914),
        ("Masculino", 14): dict(sd3n=14.489, sd2n=15.747, sd0=19.394, sd1=22.235, sd2=26.462),
        ("Femenino", 10): dict(sd3n=12.542, sd2n=13.666, sd0=16.914, sd1=19.429, sd2=23.134),
        ("Femenino", 14): dict(sd3n=14.207, sd2n=15.674, sd0=19.907, sd1=23.145, sd2=27.804),
    }

    def test_z_en_los_cortes_oficiales(self):
        esperado = dict(sd3n=-3, sd2n=-2, sd0=0, sd1=1, sd2=2)
        for (sexo, edad), cortes in self.REF.items():
            for clave, z_ok in esperado.items():
                with self.subTest(sexo=sexo, edad=edad, corte=clave):
                    self.assertAlmostEqual(puntaje_z_imc(cortes[clave], edad, sexo), z_ok, delta=0.03)

    def test_clasificacion_por_tramos(self):
        for (sexo, edad), c in self.REF.items():
            casos = [
                (c["sd3n"] - 0.3, "Bajo peso severo", "status-derivar"),
                (c["sd2n"] - 0.1, "Bajo peso", "status-alerta"),
                (c["sd0"], "Normal", "status-normal"),
                (c["sd1"] + 0.3, "Sobrepeso", "status-alerta"),
                (c["sd2"] + 0.5, "Obesidad", "status-derivar"),
            ]
            for imc, estado, clase in casos:
                with self.subTest(sexo=sexo, edad=edad, imc=imc):
                    est, cls, _ = clasificar_imc_oms(imc, edad, sexo)
                    self.assertEqual((est, cls), (estado, clase))

    def test_el_sexo_importa(self):
        z_m = puntaje_z_imc(21.0, 10, "Masculino")
        z_f = puntaje_z_imc(21.0, 10, "Femenino")
        self.assertNotAlmostEqual(z_m, z_f, places=2)

    def test_edad_en_meses_limites(self):
        self.assertEqual(edad_en_meses(5), 66)
        self.assertEqual(edad_en_meses(19), MES_MAX)
        self.assertEqual(edad_en_meses(4), MES_MIN)

    def test_entradas_invalidas(self):
        with self.assertRaises(ValueError):
            puntaje_z_imc(18.0, 12, "Otro")
        with self.assertRaises(ValueError):
            puntaje_z_imc(0, 12, "Femenino")


if __name__ == "__main__":
    unittest.main()
