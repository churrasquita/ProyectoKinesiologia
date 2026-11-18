import streamlit as st

st.set_page_config(
    page_title="Tamizaje Kinésico Escolar",
    page_icon="🦴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Estilos personalizados ──────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

    .main { background-color: #F7F8FA; }
.header-block {
    background: #00438A;
    padding: 1.2rem 2rem;
    border-radius: 14px;
    margin-bottom: 2rem;
    color: white;
    display: flex;
    align-items: center;
    gap: 20px;
}
    .header-block h1 { font-size: 1.8rem; font-weight: 600; margin: 0; color: white; }
    .header-block p  { font-size: 0.95rem; opacity: 0.85; margin: 0.3rem 0 0; color: white; }

    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        border: 1px solid #E8ECF0;
        margin-bottom: 12px;
    }
    .metric-label { font-size: 0.75rem; color: #7A8899; text-transform: uppercase; letter-spacing: 0.05em; }
    .metric-value { font-size: 1.6rem; font-weight: 600; color: #1B2B3A; margin: 2px 0; }
    .metric-sub   { font-size: 0.8rem; color: #7A8899; }

    .status-normal   { color: #1A7A4A; background: #E8F7EF; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 500; }
    .status-alerta   { color: #B85C00; background: #FFF3E0; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 500; }
    .status-derivar  { color: #C0392B; background: #FDECEA; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 500; }

    .step-box {
        background: white;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        border: 1px solid #E8ECF0;
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 8px;
    }
    .step-num {
        background: #2E86AB;
        color: white;
        width: 26px;
        height: 26px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 600;
        flex-shrink: 0;
    }

    div[data-testid="stFileUploader"] {
        border: 2px dashed #BCC8D4;
        border-radius: 12px;
        padding: 1rem;
        background: white;
    }

    .stButton > button {
        background: #2E86AB;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
        width: 100%;
    }
    .stButton > button:hover { background: #1B4F72; }

    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="background:#00438A; border-radius:10px; padding:10px 14px; margin-bottom:16px; display:flex; align-items:center; gap:10px;">
    <svg width="22" height="22" viewBox="0 0 28 28" fill="none">
        <rect x="11" y="0" width="6" height="28" fill="white"/>
        <rect x="0" y="11" width="28" height="6" fill="white"/>
    </svg>
    <div>
        <div style="font-size:15px; font-weight:700; color:white; letter-spacing:0.08em;">UCN</div>
        <div style="font-size:9px; color:rgba(255,255,255,0.75);">Univ. Católica del Norte</div>
        <div style="font-size:9px; color:#7EC8E3; font-weight:500;">Sede Coquimbo</div>
    </div>
</div>
""", unsafe_allow_html=True)
    st.markdown("### Datos del paciente")
    nombre    = st.text_input("Nombre completo")
    edad      = st.number_input("Edad", min_value=5, max_value=19, value=13)
    sexo      = st.selectbox("Sexo", ["Femenino", "Masculino"])
    curso     = st.selectbox("Curso", ["7° Básico", "8° Básico", "1° Medio", "2° Medio"])
    colegio   = st.text_input("Colegio")
    peso_kg   = st.number_input("Peso (kg)", min_value=20.0, max_value=150.0, value=50.0, step=0.5)
    talla_cm  = st.number_input(
        "Talla (cm)", min_value=100.0, max_value=220.0, value=155.0, step=0.5,
        help="Medida con tallímetro, sin zapatos. Se usa también para calibrar la foto (píxel → cm)."
    )

    st.markdown("---")
    st.caption("Sistema de Tamizaje Kinésico Escolar\nUCN Coquimbo · 2026")

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-block">
    <div class="header-logo">
        <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
            <rect x="11" y="0" width="6" height="28" fill="white"/>
            <rect x="0" y="11" width="28" height="6" fill="white"/>
        </svg>
        <div class="header-sigla">UCN</div>
    </div>
    <div class="header-text">
        <h1>🦴 Tamizaje Kinésico Escolar</h1>
        <p>Sistema de evaluación postural · Universidad Católica del Norte</p>
    </div>
    <div class="header-sede">
        Campus
        <strong>Coquimbo</strong>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Instrucciones ────────────────────────────────────────────────────────────
with st.expander("📋 Instrucciones de captura", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="step-box"><div class="step-num">1</div><div>Se necesitan <b>dos fotos</b> del alumno: una <b>de frente</b> y una <b>de costado</b>. No se usa ningún objeto de calibración.</div></div>
        <div class="step-box"><div class="step-num">2</div><div><b>De frente:</b> de pie, mirando a la cámara, brazos a los lados, pies levemente separados.</div></div>
        <div class="step-box"><div class="step-num">3</div><div><b>De costado:</b> de pie, perfil a la cámara, mirada al frente, brazos relajados.</div></div>
        <div class="step-box"><div class="step-num">4</div><div>Alumno <b>descalzo</b> y con ropa ajustada; la foto debe incluir el cuerpo completo, de cabeza a pies.</div></div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="step-box"><div class="step-num">5</div><div>Registrar la <b>talla real</b> (tallímetro) en la barra lateral: con ella se calibran las medidas en cm.</div></div>
        <div class="step-box"><div class="step-num">6</div><div>Cámara a la altura de la cadera, quieta y recta; distancia de 2 a 3 metros.</div></div>
        <div class="step-box"><div class="step-num">7</div><div>Buena iluminación frontal, fondo despejado, sin contraluz ni sombras fuertes.</div></div>
        <div class="step-box"><div class="step-num">8</div><div>Solo una persona en la foto.</div></div>
        """, unsafe_allow_html=True)

# ── Subida de imágenes ───────────────────────────────────────────────────────
st.markdown("### Subir fotografías")
col_up_f, col_up_p = st.columns(2)
with col_up_f:
    st.markdown("**1 · Foto de frente**")
    foto_frontal = st.file_uploader(
        "Foto de frente", type=["jpg", "jpeg", "png"],
        key="foto_frontal", label_visibility="collapsed"
    )
with col_up_p:
    st.markdown("**2 · Foto de costado**")
    foto_perfil = st.file_uploader(
        "Foto de costado", type=["jpg", "jpeg", "png"],
        key="foto_perfil", label_visibility="collapsed"
    )


def _leer_imagen(archivo):
    import numpy as np
    import cv2
    from PIL import Image, ImageOps

    # exif_transpose: las fotos de celular vienen giradas según la metadata EXIF
    img = ImageOps.exif_transpose(Image.open(archivo)).convert("RGB")
    imagen = np.array(img)
    # Limitar tamaño para que la detección sea rápida (la escala se calcula sobre esta misma imagen)
    h, w = imagen.shape[:2]
    lado_max = 1600
    if max(h, w) > lado_max:
        f = lado_max / max(h, w)
        imagen = cv2.resize(imagen, (int(w * f), int(h * f)), interpolation=cv2.INTER_AREA)
    return imagen


def _tarjeta(titulo, valor, estado, clase, sub=""):
    # HTML en una sola línea: si queda una línea vacía con sangría, Markdown lo muestra como código
    sub_html = f'<div class="metric-sub">{sub}</div>' if sub else ""
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{titulo}</div>'
        f'<div class="metric-value">{valor}</div>{sub_html}'
        f'<span class="{clase}">{estado}</span></div>',
        unsafe_allow_html=True,
    )


# ── Procesamiento ─────────────────────────────────────────────────────────────
if foto_frontal is None and foto_perfil is None:
    st.markdown("""
    <div style="text-align:center; padding: 3rem; color: #7A8899;">
        <div style="font-size: 3rem;">📸</div>
        <p style="font-size: 1rem; margin-top: 0.5rem;">Sube la foto de frente y la foto de costado para comenzar la evaluación</p>
    </div>
    """, unsafe_allow_html=True)
else:
    from utils.mediciones import (
        detectar_landmarks,
        altura_persona_px,
        calibrar_con_talla,
        dibujar_altura,
        calcular_asimetria_hombros,
        calcular_dismetria_piernas,
        calcular_angulo_cervical,
    )
    from utils.oms_imc import clasificar_imc_oms
    from utils.reporte import generar_pdf

    datos = {
        "nombre": nombre or "Sin nombre",
        "edad": edad,
        "sexo": sexo,
        "curso": curso,
        "colegio": colegio or "Sin especificar",
        "peso": peso_kg,
        "talla": talla_cm,
    }
    imagen_frontal_pdf = None
    imagen_perfil_pdf = None

    # ── IMC (no depende de las fotos) ────────────────────────────────────
    imc = peso_kg / ((talla_cm / 100) ** 2)
    estado_imc, clase_imc, z_imc = clasificar_imc_oms(imc, edad, sexo)
    datos.update(imc=imc, estado_imc=estado_imc, z_imc=z_imc)

    # ── Vista frontal ────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Vista de frente")
    if foto_frontal is None:
        st.warning("Falta la foto de frente: sin ella no se evalúan hombros ni miembros inferiores.")
    else:
        imagen_rgb = _leer_imagen(foto_frontal)
        h, w = imagen_rgb.shape[:2]
        landmarks, imagen_anotada = detectar_landmarks(imagen_rgb, vista="frontal")

        col_img, col_res = st.columns([1.2, 1])
        if landmarks is None:
            with col_img:
                st.image(imagen_rgb, use_container_width=True)
            with col_res:
                st.error("No se detectó ninguna persona en la foto de frente. Intenta con otra foto.")
        else:
            rango = altura_persona_px(landmarks, w, h)
            with col_res:
                st.markdown("#### Calibración por talla")
                if rango is None:
                    st.error("No se pudo estimar la altura del alumno en la foto: deben verse los ojos y los pies.")
                    factor_escala = None
                else:
                    y_sup, y_inf = rango
                    altura_px = y_inf - y_sup
                    with st.expander("Ajuste manual de la altura detectada"):
                        st.caption("La altura se estima desde los ojos hasta la planta del pie. Corrige solo si la línea amarilla de la imagen no va de la coronilla a los pies.")
                        y_sup, y_inf = st.slider(
                            "Desde la cabeza hasta los pies (píxeles, desde arriba)",
                            min_value=0, max_value=h - 1, value=(int(y_sup), int(y_inf)), step=1,
                        )
                        altura_px = max(1, y_inf - y_sup)
                    factor_escala = calibrar_con_talla(talla_cm, altura_px)
                    imagen_anotada = dibujar_altura(imagen_anotada, y_sup, y_inf)
                    st.caption(
                        f"Altura en la foto: {altura_px} px · talla {talla_cm:.1f} cm → "
                        f"{factor_escala:.4f} cm/píxel"
                    )
                    if y_sup <= 2 or y_inf >= h - 3:
                        st.warning("La figura toca el borde de la foto: puede faltar parte de la cabeza o los pies.")

            with col_img:
                st.image(imagen_anotada, use_container_width=True,
                         caption="Puntos detectados · línea amarilla: altura usada para calibrar")
            imagen_frontal_pdf = imagen_anotada

            if factor_escala is not None:
                with col_res:
                    st.markdown("#### Resultados")
                    dif_hombros = calcular_asimetria_hombros(landmarks, w, h, factor_escala)
                    if dif_hombros < 0.5:
                        estado_h, clase_h = "Normal", "status-normal"
                    elif dif_hombros < 1.5:
                        estado_h, clase_h = "Leve asimetría", "status-alerta"
                    else:
                        estado_h, clase_h = "Derivar a especialista", "status-derivar"
                    _tarjeta("Asimetría de hombros", f"{dif_hombros:.1f} cm", estado_h, clase_h)

                    dif_piernas = calcular_dismetria_piernas(landmarks, w, h, factor_escala)
                    if dif_piernas < 0.5:
                        estado_p, clase_p = "Normal", "status-normal"
                    elif dif_piernas < 1.5:
                        estado_p, clase_p = "Leve dismetría", "status-alerta"
                    else:
                        estado_p, clase_p = "Derivar a especialista", "status-derivar"
                    _tarjeta("Dismetría de miembros inferiores", f"{dif_piernas:.1f} cm", estado_p, clase_p)

                    datos.update(
                        dif_hombros=dif_hombros, estado_hombros=estado_h,
                        dif_piernas=dif_piernas, estado_piernas=estado_p,
                    )

    # ── Vista de costado ─────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Vista de costado")
    if foto_perfil is None:
        st.warning("Falta la foto de costado: sin ella no se evalúa la postura cervical.")
    else:
        imagen_rgb_p = _leer_imagen(foto_perfil)
        hp, wp = imagen_rgb_p.shape[:2]
        landmarks_p, imagen_anotada_p = detectar_landmarks(imagen_rgb_p, vista="perfil")

        col_img_p, col_res_p = st.columns([1.2, 1])
        with col_img_p:
            st.image(imagen_anotada_p, use_container_width=True,
                     caption="Línea oreja → hombro y horizontal de referencia")
        with col_res_p:
            if landmarks_p is None:
                st.error("No se detectó ninguna persona en la foto de costado. Intenta con otra foto.")
            else:
                imagen_perfil_pdf = imagen_anotada_p
                st.markdown("#### Resultados")
                angulo = calcular_angulo_cervical(landmarks_p, wp, hp)
                if angulo is None:
                    st.warning("No se vieron con claridad la oreja y el hombro. Repite la foto con el alumno bien de perfil.")
                else:
                    if angulo > 50:
                        estado_c, clase_c = "Normal", "status-normal"
                    elif angulo > 40:
                        estado_c, clase_c = "Proyección leve", "status-alerta"
                    else:
                        estado_c, clase_c = "Proyección cervical anterior", "status-derivar"
                    _tarjeta("Ángulo cervical (oreja–hombro)", f"{angulo:.1f}°", estado_c, clase_c,
                             sub="Ángulo con la horizontal; menor ángulo = cabeza más adelantada")
                    datos.update(angulo_cervical=angulo, estado_cervical=estado_c)

    # ── IMC y PDF ────────────────────────────────────────────────────────
    st.markdown("---")
    col_imc, col_pdf = st.columns([1, 1])
    with col_imc:
        _tarjeta("IMC", f"{imc:.1f}", estado_imc, clase_imc,
                 sub=f"{peso_kg} kg · {talla_cm} cm · z = {z_imc:+.2f}")
    with col_pdf:
        if imagen_frontal_pdf is None and imagen_perfil_pdf is None:
            st.info("El informe PDF estará disponible cuando se detecte al alumno en al menos una foto.")
        else:
            pdf_bytes = generar_pdf(datos, imagen_frontal_pdf, imagen_perfil_pdf)
            st.download_button(
                label="📄 Descargar informe PDF",
                data=pdf_bytes,
                file_name=f"tamizaje_{nombre or 'paciente'}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
