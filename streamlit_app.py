import streamlit as st
from streamlit_ace import st_ace
import sys
from io import StringIO

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="DeepDive Academy",
    page_icon="🌊",
    layout="wide"
)

# --- 2. STYLING ---
st.markdown("""
    <style>
    /* Стиль для черного терминала */
    .terminal-output {
        background-color: #1e1e1e;
        color: #00ff00;
        padding: 15px;
        border-radius: 5px;
        font-family: 'Courier New', Courier, monospace;
        border: 1px solid #333;
        margin-top: 10px;
        white-space: pre-wrap;
    }
    /* Дополнительный отступ для редактора, чтобы первая строка была видна на 100% */
    .stAceEditor {
        margin-top: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🌊 DeepDive")
    st.markdown("---")
    st.write("📊 **Progress**")
    st.progress(10)
    st.info("Current Module: **Variables**")

# --- 4. MAIN INTERFACE ---
st.header("Mission 1: The Variable Anchor")

col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    st.subheader("📝 Mission Briefing")
    st.info("Goal: Create a variable named `depth` and set it to `50`.")
    
    # Validation targets
    target_var = "depth"
    target_val = 50

    with st.expander("💡 Hint"):
        st.write("To create a variable, type: `variable_name = value`")

with col2:
    # Adding extra space to ensure the first line of code is 100% visible
    st.write("") 
    
    # ACE EDITOR
    user_code = st_ace(
        language="python",
        theme="monokai",
        font_size=16,
        height=250,
        key="deepdive_editor",
        auto_update=True,
        show_gutter=True,
        show_print_margin=False,
    )

    # BUTTONS IN ONE LINE
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        # Standard gray button
        run_btn = st.button("▶ RUN CODE", use_container_width=True)

    with btn_col2:
        # Primary colored button (Red/Orange depending on theme)
        execute_btn = st.button("🚀 EXECUTE MISSION", use_container_width=True, type="primary")

    st.write("🔎 **Terminal Output:**")
    
    # --- 5. LOGIC HANDLING ---

    # Logic for RUN button (Pure execution)
    if run_btn:
        output_buffer = StringIO()
        sys.stdout = output_buffer
        try:
            # We use a simple exec for the Run button
            exec(user_code)
            result = output_buffer.getvalue()
            st.markdown(f'<div class="terminal-output">{result if result else "Code executed... No output."}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Console Error: {e}")
        finally:
            sys.stdout = sys.__stdout__

    # Logic for EXECUTE button (Validation)
    if execute_btn:
        local_env = {}
        try:
            # Execute in isolated env to check variables
            exec(user_code, {}, local_env)
            
            if target_var in local_env and local_env[target_var] == target_val:
                st.success("✅ MISSION COMPLETE! The system is calibrated.")
                st.balloons()
            else:
                st.error(f"❌ Target not reached. Make sure you set `{target_var}` to `{target_val}`.")
        except Exception as e:
            st.error(f"Execution Error: {e}")