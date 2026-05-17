# Tamizaje Kinésico Escolar 🦴
Sistema de evaluación postural con visión artificial para jornadas de tamizaje en colegios.

**Desarrollado por:** 2 Estudiantes de Ingeniería Civil Informática — UCN Coquimbo · 2026

---

## Qué hace el sistema

- Detecta automáticamente los puntos clave del cuerpo usando MediaPipe
- Mide la **asimetría de hombros** (indicador de escoliosis)
- Mide la **dismetría de miembros inferiores** (diferencia entre piernas)
- Calcula el **IMC** con clasificación pediátrica (OMS)
- Evalúa la **proyección cervical anterior** (postura del cuello)
- Genera un **informe PDF** descargable por paciente

---

## Instalación

### Requisitos previos
- Python 3.10 o superior
- pip actualizado

### Pasos

```bash
# 1. Clonar o descargar el proyecto
cd tamizaje_kinesico

# 2. (Recomendado) Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la app
streamlit run app.py
```

El navegador se abre automáticamente en `http://localhost:8501`

---

## Estructura del proyecto

```
tamizaje_kinesico/
├── app.py                  # Aplicación principal Streamlit
├── requirements.txt        # Dependencias
├── README.md
└── utils/
    ├── __init__.py
    ├── mediciones.py       # Detección de landmarks y cálculos posturales
    └── reporte.py          # Generación de PDF con ReportLab
```

---

## Cómo tomar la fotografía

1. El alumno se para de frente a la cámara, brazos a los costados
2. Sostiene una **hoja carta** (21.59 cm) pegada al cuerpo
3. La foto debe incluir figura completa: cabeza hasta pies
4. Buena iluminación frontal, sin contraluz
5. Distancia recomendada: 2 a 3 metros

---

## Calibración

El sistema usa la hoja carta como regla:
- En la app, ajusta el slider "Ancho de la hoja en la foto (píxeles)"
- Eso calcula automáticamente cuántos centímetros mide cada píxel
- Si no hay hoja carta, puedes ingresar el factor manualmente

---

## Deploy en Streamlit Cloud 

1. Subir el proyecto a GitHub
2. Ir a [share.streamlit.io](https://share.streamlit.io)
3. Conectar el repositorio
4. Seleccionar `app.py` como archivo principal
5. URL pública para compartir

---

## Limitaciones conocidas

- MediaPipe puede perder precisión con ropa oscura o mala iluminación
- La calibración manual es aproximada; en versión futura se detectará la hoja automáticamente
- Los umbrales clínicos son referenciales; deben validarse con kinesiólogos de la UNC
- No reemplaza el diagnóstico clínico profesional

---

## Tecnologías utilizadas

| Librería | Uso |
|---|---|
| Streamlit | Interfaz web |
| MediaPipe | Detección de landmarks corporales |
| OpenCV | Procesamiento de imágenes |
| ReportLab | Generación de PDF |
| NumPy | Operaciones matemáticas |

---

## Próximas mejoras (post-junio)

- [ ] Detección automática de la hoja carta con OpenCV
- [ ] Historial de pacientes con base de datos SQLite
- [ ] Comparación entre evaluaciones del mismo alumno
- [ ] Exportar resultados en Excel por curso completo
- [ ] Modo cámara en tiempo real
