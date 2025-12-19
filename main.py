import streamlit as st
import pandas as pd
from datetime import datetime
from uuid import uuid4
import os

# -----------------------------
# Config
# -----------------------------
st.set_page_config(
    page_title="Encuesta — Curso Sabatino (hace 1 año)",
    page_icon="📝",
    layout="centered"
)

LIKERT_OPTIONS = [
    "1 — Totalmente en desacuerdo",
    "2 — En desacuerdo",
    "3 — Ni de acuerdo ni en desacuerdo",
    "4 — De acuerdo",
    "5 — Totalmente de acuerdo",
]

def likert_to_int(option: str) -> int:
    # "3 — ..." -> 3
    return int(option.split("—")[0].strip())

# -----------------------------
# UI
# -----------------------------
st.title("📝 Encuesta — Curso Sabatino de Cálculo Diferencial (hace un año)")
st.caption(
    "Propósito: evaluar el curso con la distancia de un año. "
    "La encuesta es anónima y no afecta calificaciones ni situación académica."
)

with st.expander("Instrucciones", expanded=True):
    st.markdown(
        """
- Responde según tu experiencia **general**.
- Escala Likert: **1** (Totalmente en desacuerdo) a **5** (Totalmente de acuerdo).
- Si **no recuerdas suficiente** para responder un reactivo, elige **3**.
        """
    )

st.divider()

# -----------------------------
# Form
# -----------------------------
if "last_submission" not in st.session_state:
    st.session_state.last_submission = None

with st.form("encuesta_1_anio", clear_on_submit=False):
    st.subheader("Escala Likert (8 afirmaciones)")

    q1 = st.radio(
        "1) En retrospectiva, el curso sabatino aportó a mi comprensión de Cálculo Diferencial.",
        LIKERT_OPTIONS, index=2
    )
    q2 = st.radio(
        "2) El curso sabatino me ayudó a mejorar mi desempeño (tareas, exámenes o participación) durante ese semestre.",
        LIKERT_OPTIONS, index=2
    )
    q3 = st.radio(
        "3) El curso sabatino me ayudó a identificar errores frecuentes que yo cometía al resolver ejercicios.",
        LIKERT_OPTIONS, index=2
    )
    q4 = st.radio(
        "4) Lo trabajado en el sábado estuvo alineado con lo que se evaluaba en el curso regular (lunes a viernes).",
        LIKERT_OPTIONS, index=2
    )
    q5 = st.radio(
        "5) Después de ese semestre, conservé herramientas o formas de estudiar aprendidas en el curso sabatino.",
        LIKERT_OPTIONS, index=2
    )
    q6 = st.radio(
        "6) El nivel del curso sabatino fue adecuado para mi preparación en ese momento.",
        LIKERT_OPTIONS, index=2
    )
    q7 = st.radio(
        "7) La forma de trabajo del sábado (explicación + práctica + retroalimentación) fue efectiva para aprender.",
        LIKERT_OPTIONS, index=2
    )
    q8 = st.radio(
        "8) Si existiera un curso sabatino similar hoy, lo recomendaría a estudiantes con necesidades parecidas.",
        LIKERT_OPTIONS, index=2
    )

    st.subheader("Ítem opcional de perfil")
    perf = st.slider(
        "En ese momento (primer semestre), mi desempeño en matemáticas/cálculo era:",
        min_value=1, max_value=5, value=3,
        help="1 = muy bajo, 5 = muy alto"
    )

    st.subheader("Preguntas abiertas")
    a1 = st.text_area(
        "1) ¿Qué fue lo más valioso del curso sabatino, visto con la distancia de un año?",
        height=110, placeholder="Escribe tu respuesta..."
    )
    a2 = st.text_area(
        "2) ¿Qué fue lo que menos aportó o pudo haberse hecho mejor?",
        height=110, placeholder="Escribe tu respuesta..."
    )
    a3 = st.text_area(
        "3) ¿Para qué tipo de estudiante crees que sí es útil un curso sabatino?",
        height=110, placeholder="Escribe tu respuesta..."
    )
    a4 = st.text_area(
        "4) Si pudieras rediseñar el curso sabatino con una sola mejora clave, ¿cuál sería y por qué?",
        height=110, placeholder="Escribe tu respuesta..."
    )

    submitted = st.form_submit_button("Enviar respuestas ✅")

# -----------------------------
# Submission handling
# -----------------------------
if submitted:
    # Construir registro
    record = {
        "respondent_id": str(uuid4()),
        "timestamp_iso": datetime.now().isoformat(timespec="seconds"),
        "grupo": "tomo_curso_hace_1_anio",

        "q1": likert_to_int(q1),
        "q2": likert_to_int(q2),
        "q3": likert_to_int(q3),
        "q4": likert_to_int(q4),
        "q5": likert_to_int(q5),
        "q6": likert_to_int(q6),
        "q7": likert_to_int(q7),
        "q8": likert_to_int(q8),

        "perfil_desempeno_1a5_opcional": int(perf),

        "a1_mas_valioso": a1.strip(),
        "a2_menos_util": a2.strip(),
        "a3_para_quien_es_util": a3.strip(),
        "a4_mejora_clave": a4.strip(),
    }

    df_new = pd.DataFrame([record])

    # Guardado local (append)
    out_file = "respuestas_encuesta_calculo_1anio.csv"
    if os.path.exists(out_file):
        df_existing = pd.read_csv(out_file)
        df_all = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_all = df_new

    df_all.to_csv(out_file, index=False, encoding="utf-8")

    st.success("¡Gracias! Tu respuesta fue registrada.")
    st.session_state.last_submission = record

    st.divider()
    st.subheader("Descarga de tu registro / archivo acumulado")

    # Descargar el registro individual
    st.download_button(
        label="Descargar mi respuesta (CSV)",
        data=df_new.to_csv(index=False, encoding="utf-8"),
        file_name="mi_respuesta_encuesta_1anio.csv",
        mime="text/csv"
    )

    # Descargar el acumulado
    st.download_button(
        label="Descargar todas las respuestas acumuladas (CSV)",
        data=df_all.to_csv(index=False, encoding="utf-8"),
        file_name=out_file,
        mime="text/csv"
    )

st.caption("Nota: si despliegas esto en Streamlit Cloud, el guardado local puede no ser permanente. El botón de descarga siempre funciona.")
