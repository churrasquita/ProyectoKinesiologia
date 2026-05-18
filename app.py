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
    edad      = st.number_input("Edad", min_value=5, max_value=20, value=13)
    curso     = st.selectbox("Curso", ["7° Básico", "8° Básico", "1° Medio", "2° Medio"])
    colegio   = st.text_input("Colegio")
    peso_kg   = st.number_input("Peso (kg)", min_value=20.0, max_value=150.0, value=50.0, step=0.5)
    talla_cm  = st.number_input("Talla (cm)", min_value=100.0, max_value=220.0, value=155.0, step=0.5)

    st.markdown("---")
    st.markdown("### Tipo de evaluación")
    eval_frontal = st.checkbox("Vista frontal (hombros + piernas)", value=True)
    eval_perfil  = st.checkbox("Vista de perfil (cuello)", value=False)

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
        <div class="step-box"><div class="step-num">1</div><div>El alumno debe pararse de frente a la cámara, con los brazos a los lados.</div></div>
        <div class="step-box"><div class="step-num">2</div><div>Sostener una <b>hoja carta</b> (21.59 cm) pegada al cuerpo, con ambas manos.</div></div>
        <div class="step-box"><div class="step-num">3</div><div>La foto debe incluir la figura completa: cabeza hasta pies.</div></div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="step-box"><div class="step-num">4</div><div>Buena iluminación frontal, sin contraluz ni sombras fuertes.</div></div>
        <div class="step-box"><div class="step-num">5</div><div>Distancia recomendada: 2 a 3 metros entre el alumno y la cámara.</div></div>
        <div class="step-box"><div class="step-num">6</div><div>Para perfil: repetir el mismo proceso con el alumno de lado.</div></div>
        """, unsafe_allow_html=True)

# ── Subida de imagen ─────────────────────────────────────────────────────────
st.markdown("### Subir fotografía")
foto = st.file_uploader(
    "Arrastra la foto aquí o haz clic para seleccionar",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

# ── Procesamiento ─────────────────────────────────────────────────────────────
if foto is not None:
    import numpy as np
    import cv2
    import mediapipe as mp
    from utils.mediciones import (
        detectar_landmarks,
        calibrar_con_hoja,
        calcular_asimetria_hombros,
        calcular_dismetria_piernas,
        calcular_angulo_cervical,
        clasificar_imc_pediatrico
    )
    from utils.reporte import generar_pdf

    # Leer imagen
    file_bytes = np.asarray(bytearray(foto.read()), dtype=np.uint8)
    imagen_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    imagen_rgb = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2RGB)

    col_img, col_res = st.columns([1.2, 1])

    with col_img:
        st.markdown("#### Vista con puntos detectados")

        # Detectar landmarks
        landmarks, imagen_anotada = detectar_landmarks(imagen_rgb.copy())

        if landmarks is None:
            st.error("No se detectó ninguna persona en la imagen. Intenta con otra foto.")
        else:
            st.image(imagen_anotada, use_container_width=True)

            # Calibración con hoja carta
            st.markdown("**Calibración con hoja carta**")
            st.info("Haz clic en las dos esquinas superiores de la hoja carta para calibrar.")

            usar_escala_manual = st.checkbox("Ingresar escala manualmente (si no hay hoja carta)")
            if usar_escala_manual:
                factor_escala = st.slider(
                    "Factor de escala (cm/píxel) — ajusta hasta que las medidas sean lógicas",
                    min_value=0.01, max_value=0.5, value=0.08, step=0.001,
                    format="%.3f"
                )
            else:
                h, w = imagen_rgb.shape[:2]
                ancho_hoja_px = st.slider(
                    "Ancho de la hoja carta en la foto (píxeles)",
                    min_value=50, max_value=w, value=int(w * 0.2), step=1
                )
                factor_escala = 21.59 / ancho_hoja_px
                st.caption(f"Factor calculado: {factor_escala:.4f} cm/píxel")

    with col_res:
        st.markdown("#### Resultados de evaluación")

        if landmarks is not None:
            h, w = imagen_rgb.shape[:2]

            # ── Hombros ──────────────────────────────────────────────────
            dif_hombros = calcular_asimetria_hombros(landmarks, w, h, factor_escala)
            if dif_hombros < 0.5:
                estado_h, clase_h = "Normal", "status-normal"
            elif dif_hombros < 1.5:
                estado_h, clase_h = "Leve asimetría", "status-alerta"
            else:
                estado_h, clase_h = "Derivar a especialista", "status-derivar"

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Asimetría de hombros</div>
                <div class="metric-value">{dif_hombros:.1f} cm</div>
                <span class="{clase_h}">{estado_h}</span>
            </div>
            """, unsafe_allow_html=True)

            # ── Piernas ──────────────────────────────────────────────────
            dif_piernas = calcular_dismetria_piernas(landmarks, w, h, factor_escala)
            if dif_piernas < 0.5:
                estado_p, clase_p = "Normal", "status-normal"
            elif dif_piernas < 1.5:
                estado_p, clase_p = "Leve dismetría", "status-alerta"
            else:
                estado_p, clase_p = "Derivar a especialista", "status-derivar"

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Dismetría de miembros inferiores</div>
                <div class="metric-value">{dif_piernas:.1f} cm</div>
                <span class="{clase_p}">{estado_p}</span>
            </div>
            """, unsafe_allow_html=True)

            # ── IMC ───────────────────────────────────────────────────────
            imc = peso_kg / ((talla_cm / 100) ** 2)
            estado_imc, clase_imc = clasificar_imc_pediatrico(imc, edad)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">IMC</div>
                <div class="metric-value">{imc:.1f}</div>
                <div class="metric-sub">{peso_kg} kg · {talla_cm} cm</div>
                <span class="{clase_imc}">{estado_imc}</span>
            </div>
            """, unsafe_allow_html=True)

            # ── Ángulo cervical (si se marcó perfil) ─────────────────────
            if eval_perfil:
                angulo = calcular_angulo_cervical(landmarks, w, h)
                if angulo is not None:
                    if angulo > 50:
                        estado_c, clase_c = "Normal", "status-normal"
                    elif angulo > 40:
                        estado_c, clase_c = "Proyección leve", "status-alerta"
                    else:
                        estado_c, clase_c = "Proyección cervical anterior", "status-derivar"
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Proyección cervical anterior</div>
                        <div class="metric-value">{angulo:.1f}°</div>
                        <span class="{clase_c}">{estado_c}</span>
                    </div>
                    """, unsafe_allow_html=True)

            # ── Generar PDF ───────────────────────────────────────────────
            st.markdown("---")
            if st.button("📄 Descargar informe PDF"):
                datos = {
                    "nombre": nombre or "Sin nombre",
                    "edad": edad,
                    "curso": curso,
                    "colegio": colegio or "Sin especificar",
                    "peso": peso_kg,
                    "talla": talla_cm,
                    "imc": imc,
                    "estado_imc": estado_imc,
                    "dif_hombros": dif_hombros,
                    "estado_hombros": estado_h,
                    "dif_piernas": dif_piernas,
                    "estado_piernas": estado_p,
                }
                pdf_bytes = generar_pdf(datos, imagen_anotada)
                st.download_button(
                    label="⬇️ Guardar PDF",
                    data=pdf_bytes,
                    file_name=f"tamizaje_{nombre or 'paciente'}.pdf",
                    mime="application/pdf"
                )

else:
    st.markdown("""
    <div style="text-align:center; padding: 3rem; color: #7A8899;">
        <div style="font-size: 3rem;">📸</div>
        <p style="font-size: 1rem; margin-top: 0.5rem;">Sube una fotografía para comenzar la evaluación</p>
    </div>
    """, unsafe_allow_html=True)
