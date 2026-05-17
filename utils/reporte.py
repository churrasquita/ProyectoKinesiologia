"""
utils/reporte.py
Genera el informe PDF del tamizaje kinésico.
"""
import io
import datetime
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import PIL.Image


# ── Colores institucionales ───────────────────────────────────────────────────
AZUL_UNC   = colors.HexColor("#1B4F72")
AZUL_CLARO = colors.HexColor("#2E86AB")
VERDE_OK   = colors.HexColor("#1A7A4A")
NARANJA    = colors.HexColor("#B85C00")
ROJO       = colors.HexColor("#C0392B")
GRIS_CLARO = colors.HexColor("#F7F8FA")
GRIS_BORDE = colors.HexColor("#E8ECF0")


def _color_estado(estado: str):
    """Devuelve el color según el estado del resultado."""
    if "Normal" in estado:
        return VERDE_OK
    elif "Leve" in estado or "Bajo peso" in estado or "Sobrepeso" in estado:
        return NARANJA
    else:
        return ROJO


def generar_pdf(datos: dict, imagen_anotada: np.ndarray) -> bytes:
    """
    Genera el PDF de informe y lo devuelve como bytes.

    datos debe contener:
        nombre, edad, curso, colegio, peso, talla, imc, estado_imc,
        dif_hombros, estado_hombros, dif_piernas, estado_piernas
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    elementos = []

    # ── Estilo personalizado ──────────────────────────────────────────────
    estilo_titulo = ParagraphStyle(
        "titulo",
        parent=styles["Heading1"],
        fontSize=18,
        textColor=colors.white,
        alignment=TA_CENTER,
        spaceAfter=4
    )
    estilo_subtitulo = ParagraphStyle(
        "subtitulo",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#BCC8D4"),
        alignment=TA_CENTER
    )
    estilo_seccion = ParagraphStyle(
        "seccion",
        parent=styles["Heading2"],
        fontSize=11,
        textColor=AZUL_UNC,
        spaceBefore=14,
        spaceAfter=6
    )
    estilo_normal = ParagraphStyle(
        "normal",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#1B2B3A")
    )
    estilo_pie = ParagraphStyle(
        "pie",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.HexColor("#7A8899"),
        alignment=TA_CENTER
    )

    # ── Encabezado ────────────────────────────────────────────────────────
    encabezado = Table(
        [[
            Paragraph("🦴 Tamizaje Kinésico Escolar", estilo_titulo),
            Paragraph("Universidad Nacional de Coquimbo · 2025", estilo_subtitulo)
        ]],
        colWidths=["100%"]
    )
    encabezado.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AZUL_UNC),
        ("ROUNDEDCORNERS", [8]),
        ("TOPPADDING", (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
    ]))
    elementos.append(encabezado)
    elementos.append(Spacer(1, 16))

    # ── Fecha y folio ─────────────────────────────────────────────────────
    fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    elementos.append(Paragraph(f"Fecha de evaluación: {fecha}", estilo_pie))
    elementos.append(Spacer(1, 12))

    # ── Datos del paciente ────────────────────────────────────────────────
    elementos.append(Paragraph("Datos del paciente", estilo_seccion))

    tabla_datos = Table(
        [
            ["Nombre",  datos.get("nombre", "—"),  "Edad",   f"{datos.get('edad', '—')} años"],
            ["Curso",   datos.get("curso", "—"),   "Colegio", datos.get("colegio", "—")],
            ["Peso",    f"{datos.get('peso', '—')} kg", "Talla", f"{datos.get('talla', '—')} cm"],
        ],
        colWidths=[3*cm, 7*cm, 3*cm, 4.5*cm]
    )
    tabla_datos.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), GRIS_CLARO),
        ("BACKGROUND", (2, 0), (2, -1), GRIS_CLARO),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#7A8899")),
        ("TEXTCOLOR", (2, 0), (2, -1), colors.HexColor("#7A8899")),
        ("GRID", (0, 0), (-1, -1), 0.5, GRIS_BORDE),
        ("ROWBACKGROUND", (0, 0), (-1, -1), [colors.white, GRIS_CLARO]),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    elementos.append(tabla_datos)
    elementos.append(Spacer(1, 16))

    # ── Resultados ────────────────────────────────────────────────────────
    elementos.append(Paragraph("Resultados de la evaluación", estilo_seccion))

    resultados = [
        ["Evaluación", "Valor medido", "Estado"],
        [
            "Asimetría de hombros",
            f"{datos.get('dif_hombros', 0):.1f} cm",
            datos.get("estado_hombros", "—")
        ],
        [
            "Dismetría de miembros inferiores",
            f"{datos.get('dif_piernas', 0):.1f} cm",
            datos.get("estado_piernas", "—")
        ],
        [
            "IMC",
            f"{datos.get('imc', 0):.1f}",
            datos.get("estado_imc", "—")
        ],
    ]

    tabla_res = Table(resultados, colWidths=[8*cm, 4*cm, 5.5*cm])
    estilos_tabla = [
        ("BACKGROUND", (0, 0), (-1, 0), AZUL_CLARO),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, GRIS_BORDE),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("ALIGN", (1, 1), (1, -1), "CENTER"),
    ]

    # Colorear estados
    for i, fila in enumerate(resultados[1:], start=1):
        color = _color_estado(fila[2])
        estilos_tabla.append(("TEXTCOLOR", (2, i), (2, i), color))

    tabla_res.setStyle(TableStyle(estilos_tabla))
    elementos.append(tabla_res)
    elementos.append(Spacer(1, 16))

    # ── Imagen anotada ────────────────────────────────────────────────────
    elementos.append(Paragraph("Fotografía evaluada", estilo_seccion))

    pil_img = PIL.Image.fromarray(imagen_anotada)
    img_buffer = io.BytesIO()
    pil_img.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    img_rl = Image(img_buffer, width=8*cm, height=12*cm)
    img_rl.hAlign = "CENTER"
    elementos.append(img_rl)
    elementos.append(Spacer(1, 16))

    # ── Observaciones ─────────────────────────────────────────────────────
    elementos.append(Paragraph("Observaciones del evaluador", estilo_seccion))
    lineas_obs = Table(
        [[""], [""], [""]],
        colWidths=["100%"],
        rowHeights=[1.2*cm, 1.2*cm, 1.2*cm]
    )
    lineas_obs.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, GRIS_BORDE),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, GRIS_BORDE),
    ]))
    elementos.append(lineas_obs)
    elementos.append(Spacer(1, 20))

    # ── Firma ─────────────────────────────────────────────────────────────
    firma = Table(
        [["_________________________", "_________________________"],
         ["Firma evaluador", "Firma supervisor"]],
        colWidths=["50%", "50%"]
    )
    firma.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 1), (-1, 1), colors.HexColor("#7A8899")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
    ]))
    elementos.append(firma)
    elementos.append(Spacer(1, 20))

    # ── Pie de página ─────────────────────────────────────────────────────
    elementos.append(Paragraph(
        "Este informe es una herramienta de tamizaje y no reemplaza el diagnóstico clínico profesional. "
        "Cualquier resultado fuera del rango normal debe ser evaluado por un kinesiólogo titulado.",
        estilo_pie
    ))

    doc.build(elementos)
    return buffer.getvalue()
