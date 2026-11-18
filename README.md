Kinesiologia
=======
# Tamizaje Kinésico Escolar 🦴
Sistema de evaluación postural con visión artificial para jornadas de tamizaje en colegios.

**Desarrollado por:** 2 Estudiantes de Ingeniería Civil Informática — UCN Coquimbo · 2026

---

## Qué hace el sistema

- Detecta automáticamente los puntos clave del cuerpo usando MediaPipe
- Mide la **asimetría de hombros** (indicador de escoliosis)
- Mide la **dismetría de miembros inferiores** (diferencia entre piernas)
- Calcula el **IMC** y lo clasifica con el puntaje z de IMC-para-la-edad de la OMS (referencia 2007, 5 a 19 años, según sexo y edad)
- Evalúa la **proyección cervical anterior** (postura del cuello) con la foto de costado
- Calibra las medidas con la **talla del alumno**, sin objeto de referencia
- Genera un **informe PDF** descargable por paciente

---

## Instalación y Ejecución

Tienes dos opciones para ejecutar este proyecto en tu máquina:

### Opción A: Ejecución nativa con Python

#### Requisitos previos
- Python 3.10 o superior.
- El archivo del modelo de MediaPipe `pose_landmarker_full.task` descargado en la raíz del proyecto.

#### Pasos
```bash
# 1. Clonar o descargar el proyecto
cd ProyectoKinesiologia

# 2. Crear entorno virtual (Recomendado)
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la app
streamlit run app.py


El navegador se abre automáticamente en `http://localhost:8501`

---
```
### Opción B: Docker

Esta opción empaqueta automáticamente todas las dependencias del sistema operativo que OpenCV y MediaPipe necesitan, garantizando que el sistema funcione de inmediato.

Requisitos previos:
Tener instalado y ejecutándose Docker Desktop.
``` bash
# 1. Construir la imagen de Docker
docker build -t proyecto-kinesiologia .

# 2. Ejecutar el contenedor mapeando el puerto de Streamlit
docker run -p 8501:8501 proyecto-kinesiologia

```
## Estructura del proyecto

```
tamizaje_kinesico/
├── app.py                  # Aplicación principal Streamlit
├── requirements.txt        # Dependencias de Python
├── packages.txt            # Librerías del sistema (Streamlit Cloud)
├── README.md
├── tests/
│   └── test_mediciones.py  # Pruebas con landmarks sintéticos y tablas OMS
└── utils/
    ├── __init__.py
    ├── mediciones.py       # Detección de landmarks y cálculos posturales
    ├── oms_imc.py          # Clasificación del IMC (puntaje z OMS)
    ├── oms_imc_tablas.py   # Tablas OMS 2007 (generado desde los .xlsx oficiales)
    └── reporte.py          # Generación de PDF con ReportLab
```

---

## Pruebas

```bash
python -m unittest discover -s tests -v
```

Las pruebas no necesitan el modelo `.task` ni cámara: usan landmarks sintéticos.

---

## Cómo tomar las fotografías

Se piden **dos fotos** por alumno (sugerencia del kinesiólogo asesor). **No se usa objeto de calibración**: se mide solo a la persona.

1. **Foto de frente:** de pie, mirando a la cámara, brazos a los costados → asimetría de hombros y dismetría de miembros inferiores
2. **Foto de costado:** de pie, de perfil a la cámara, mirada al frente → ángulo cervical (oreja–hombro)
3. Alumno descalzo, ropa ajustada, cuerpo completo en la foto (cabeza a pies)
4. Cámara quieta a la altura de la cadera, a 2–3 metros; buena iluminación, sin contraluz
5. Registrar la talla real (tallímetro) en la barra lateral

---

## Calibración

La escala píxel → cm se obtiene de la **talla real del alumno**:

- MediaPipe ubica los ojos y la planta del pie; como no marca la coronilla, la altura total en la foto se extrapola sabiendo que los ojos están, en promedio, al 93,5 % de la talla.
- `factor (cm/píxel) = talla (cm) / altura en la foto (píxeles)`
- En la app se dibuja una línea amarilla con la altura usada y se puede corregir a mano en "Ajuste manual de la altura detectada".
- Un error de pocos % en la escala cambia poco las diferencias medidas (p. ej. 3 % de 1,5 cm ≈ 0,05 cm); el error de detección de los puntos pesa más.

---

## Deploy en Streamlit Cloud 

1. Subir el proyecto a GitHub
2. Ir a [share.streamlit.io](https://share.streamlit.io)
3. Conectar el repositorio
4. Seleccionar `app.py` como archivo principal
5. URL pública para compartir

`packages.txt` instala las librerías del sistema que MediaPipe y OpenCV necesitan en Streamlit Cloud. El modelo `pose_landmarker_full.task` se descarga solo la primera vez si no está en el repositorio.

---

## Limitaciones conocidas

- MediaPipe puede perder precisión con ropa oscura o mala iluminación
- La altura en la foto se estima desde los ojos (proporción antropométrica promedio), por lo que la escala es aproximada
- La máscara de segmentación de MediaPipe 0.10.x no se usa: leerla hace caer el proceso
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

## Próximas mejoras 

- [ ] Historial de pacientes con base de datos SQLite
- [ ] Comparación entre evaluaciones del mismo alumno
- [ ] Exportar resultados en Excel por curso completo
- [ ] Modo cámara en tiempo real
