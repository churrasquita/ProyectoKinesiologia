"""
utils/oms_imc.py
Clasificación del IMC infantil con la referencia OMS 2007 (5 a 19 años):
puntaje z de IMC-para-la-edad, según sexo y edad.
"""
import math

from utils.oms_imc_tablas import LMS_NINAS, LMS_NINOS

SEXOS = ("Femenino", "Masculino")
MES_MIN, MES_MAX = 61, 228


def edad_en_meses(edad_anios: int) -> int:
    # El formulario solo captura años enteros: se usa la mitad del año (+6 meses)
    # y se limita al rango que cubre la referencia OMS.
    return max(MES_MIN, min(MES_MAX, int(edad_anios) * 12 + 6))


def puntaje_z_imc(imc: float, edad_anios: int, sexo: str) -> float:
    if sexo not in SEXOS:
        raise ValueError(f"Sexo no válido: {sexo!r}. Use uno de {SEXOS}.")
    if imc <= 0:
        raise ValueError("El IMC debe ser mayor que 0.")

    tabla = LMS_NINAS if sexo == "Femenino" else LMS_NINOS
    l, m, s = tabla[edad_en_meses(edad_anios)]
    if l == 0:
        return math.log(imc / m) / s
    return ((imc / m) ** l - 1) / (l * s)


def clasificar_imc_oms(imc: float, edad_anios: int, sexo: str) -> tuple[str, str, float]:
    """Devuelve (estado, clase_css, z). Cortes OMS: -3, -2, +1 y +2 desviaciones estándar."""
    z = puntaje_z_imc(imc, edad_anios, sexo)

    if z < -3:
        return "Bajo peso severo", "status-derivar", z
    if z < -2:
        return "Bajo peso", "status-alerta", z
    if z <= 1:
        return "Normal", "status-normal", z
    if z <= 2:
        return "Sobrepeso", "status-alerta", z
    return "Obesidad", "status-derivar", z
