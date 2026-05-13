import streamlit as st
import google.generativeai as genai

# 1. Configuración visual de la página
st.set_page_config(page_title="Copy B2B - Matchers", page_icon="🚀")
st.title("🚀 Generador de Copy B2B")
st.markdown("**Agencia Matchers** - Herramienta interna para escalar **tu estrategia**.")

# 2. Sidebar para poner la API Key de forma segura
with st.sidebar:
    st.header("⚙️ Configuración")
    api_key = st.text_input("Ingresá tu Gemini API Key:", type="password")
    st.caption("Obtené tu clave gratis en Google AI Studio.")

# 3. Cajas de texto para los Datos Variables
st.subheader("Datos del Talento")
nombre_handle = st.text_input("1. Nombre y Handle:", placeholder="Ej: Maca Castro @macacastrook")
nicho = st.text_input("2. Nicho/Enfoque (Máx. 5 palabras):", placeholder="Ej: Moda y lifestyle")
valor_unico = st.text_input("3. Punto de Valor Único:", placeholder="Ej: carisma, presencia, autoridad")

# 4. El botón que hace la magia
if st.button("Generar Copy Estratégico", type="primary"):
    
    # Validaciones previas
    if not api_key:
        st.warning("⚠️ Primero ingresá tu API Key en el menú de la izquierda.")
    elif not nombre_handle or not nicho or not valor_unico:
        st.warning("⚠️ Por favor completá los 3 datos del influencer.")
    else:
        try:
            # Conectar con Google Gemini
            genai.configure(api_key=api_key)
            # Usamos el modelo Flash que es rapidísimo y súper económico
            # Buscar automáticamente el mejor modelo disponible para tu cuenta
            modelo_elegido = None
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    modelo_elegido = m.name
                    if 'flash' in m.name: # Priorizamos la versión Flash por ser más rápida
                        break
            
            # Conectar con el modelo detectado
            model = genai.GenerativeModel(modelo_elegido)

            # Este es el prompt oculto que le da las reglas a la IA
            prompt = f"""
            Actúa como copywriter experto en marketing de influencers B2B para Agencia Matchers (@agenciamatchers). 
            Genera un texto promocional para este influencer bajo estas restricciones:

            Datos Variables:
            1. Nombre/Handle: {nombre_handle}
            2. Nicho: {nicho}
            3. Valor Único: {valor_unico}

            Restricciones Estrictas:
            1. Límite: No exceder 150 caracteres.
            2. Tono: Español argentino formal/entusiasta. Usar 'TÚ' (tu marca/tu estrategia). Prohibido lenguaje inclusivo ('x', 'e', '@').
            3. Formato de Handle: PROHIBIDO poner signos de puntuación pegados al handle del usuario. Debe haber un espacio en blanco inmediatamente después del nombre de usuario (ej: usar "{nombre_handle} " en lugar de "{nombre_handle}," o "{nombre_handle}.").
            4. Estructura Exacta:
               - Gancho: Frase apertura (máx 8 palabras) con nicho o valor.
               - Talento: Handle del influencer justo después, respetando la regla de formato.
               - CTA: Frase que invite a la acción a la marca.
               - Hashtags OBLIGATORIOS (al final, juntos): #AgenciaDeMarketingDeInfluencers #ResultadosReales #ContenidoDeImpacto #BrandingDigital
            """

            # Mostrar un mensajito mientras la IA piensa
            with st.spinner("Redactando el copy perfecto para tu marca..."):
                respuesta = model.generate_content(prompt)
            
            # Mostrar el resultado final
            st.success("¡Listo!")
            # st.code crea un cuadro fácil de copiar con un botón
            st.code(respuesta.text, language="text")
            
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")