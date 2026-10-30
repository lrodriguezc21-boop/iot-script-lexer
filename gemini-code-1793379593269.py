import streamlit as st
import re
import pandas as pd

# Configuración de página
st.set_page_config(
    page_title="IoT-Script Lexer",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Analizador Léxico — Lenguaje IoT-Script")
st.caption("Proyecto Final Grupal | Lenguajes Formales y Autómatas — Entrega 2")

# Especificación de Tokens mediante Expresiones Regulares (ER)
TOKEN_SPEC = [
    ('KW_SI',        r'\bsi\b'),
    ('KW_ENTONCES',   r'\bentonces\b'),
    ('KW_SENSOR',    r'\bsensor\b'),
    ('KW_ACTUADOR',  r'\bactuador\b'),
    ('KW_LEER',      r'\bleer\b'),
    ('KW_IMPRIMIR',  r'\bimprimir\b'),
    ('MAYOR_IGUAL',  r'>='),
    ('MENOR_IGUAL',  r'<='),
    ('ASIGNACION',   r'='),
    ('PUNTO_COMA',   r';'),
    ('CADENA',       r'"([^"\\]|\\.)*"'),
    ('NUMERO_DEC',   r'\b\d+\.\d+\b'),
    ('NUMERO_ENT',   r'\b\d+\b'),
    ('IDENTIFICADOR',r'\b[a-zA-R_][a-zA-R0-9_]*\b'),
    ('PAREN_IZQ',    r'\('),
    ('PAREN_DER',    r'\)'),
    ('SKIP',         r'[ \t\n]+'),
    ('COMENTARIO',   r'//.*'),
    ('MISMATCH',     r'.'),
]

def analizar_lexico(codigo_fuente):
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPEC)
    linea = 1
    tokens = []
    errores = []
    
    for mo in re.finditer(tok_regex, codigo_fuente):
        tipo = mo.lastgroup
        valor = mo.group()
        
        if tipo in ('SKIP', 'COMENTARIO'):
            linea += valor.count('\n')
            continue
        elif tipo == 'MISMATCH':
            errores.append({
                "Línea": linea,
                "Carácter Inválido": valor,
                "Detalle": "Símbolo fuera del alfabeto reconocido"
            })
        else:
            tokens.append({
                "Línea": linea,
                "Token": tipo,
                "Lexema / Valor": valor
            })
            
    return tokens, errores

# Interfaz Principal en Streamlit
col_izq, col_der = st.columns([1, 1])

with col_izq:
    st.subheader("📝 Código Fuente IoT-Script")
    
    codigo_ejemplo = """// Configuración y Control IoT
sensor temp_interior;
actuador bomba_agua;

si temp_interior >= 30 entonces
  sensor temp@1;
  bomba_agua = 1;"""
    
    codigo_usuario = st.text_area(
        "Ingresa o modifica el código para analizar en vivo:",
        value=codigo_ejemplo,
        height=300
    )
    
    btn_analizar = st.button("🚀 Analizar Código", use_container_width=True)

with col_der:
    st.subheader("🔍 Resultado del Análisis Léxico")
    
    if btn_analizar or codigo_usuario:
        lista_tokens, lista_errores = analizar_lexico(codigo_usuario)
        
        if lista_errores:
            st.error(f"❌ Se detectaron {len(lista_errores)} error(es) léxico(s):")
            st.table(pd.DataFrame(lista_errores))
        else:
            st.success("✅ ¡Código analizado sin errores léxicos!")
            
        if lista_tokens:
            st.write(f"**Total de Tokens Reconocidos:** {len(lista_tokens)}")
            st.dataframe(pd.DataFrame(lista_tokens), use_container_width=True, height=250)