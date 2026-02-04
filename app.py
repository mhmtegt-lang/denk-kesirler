import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Sayfa ayarları
st.set_page_config(page_title="Kesir Fabrikası v3 - Fixed", layout="wide")

st.title("🍫 Kesir Fabrikası: Alan Korunumu (Hatasız Model)")
st.write("Sadeleştirme ve genişletme modelleri görsellere uygun şekilde düzeltilmiştir.")

# --- Veri Seti ---
problems = {
    "b) 20/36 (4 ile sadeleştir)": {"type": "simplify", "base_num": 5, "base_den": 9, "factor": 4},
    "c) 11/15 (5 ile genişlet)": {"type": "expand", "base_num": 11, "base_den": 15, "factor": 5},
    "ç) 6/29 (2 ile genişlet)": {"type": "expand", "base_num": 6, "base_den": 29, "factor": 2},
    "d) 48/84 (6 ile sadeleştir)": {"type": "simplify", "base_num": 8, "base_den": 14, "factor": 6},
    "e) 24/32 (8 ile sadeleştir)": {"type": "simplify", "base_num": 3, "base_den": 4, "factor": 8},
    "f) 3/5 (7 ile genişlet)": {"type": "expand", "base_num": 3, "base_den": 5, "factor": 7},
    "g) 18/45 (9 ile sadeleştir)": {"type": "simplify", "base_num": 2, "base_den": 5, "factor": 9},
    "ğ) 1/6 (11 ile genişlet)": {"type": "expand", "base_num": 1, "base_den": 6, "factor": 11},
}

# --- Sidebar ---
st.sidebar.header("🔍 Örnek Seçimi")
selected_key = st.sidebar.selectbox("Lütfen bir örnek seçin:", list(problems.keys()))
prob = problems[selected_key]

mod = st.sidebar.radio(
    "Aşama:",
    ["1. Başlangıç Hali", "2. İşlem Sonucu", "3. Alan Korunumu Analizi"]
)

# --- Görselleştirme Fonksiyonu ---
def draw_fraction_model(base_num, base_den, factor, step_mode, op_type):
    fig, ax = plt.subplots(figsize=(10, 3))
    rect = patches.Rectangle((0, 0), 1, 1, linewidth=2, edgecolor='black', facecolor='white')
    ax.add_patch(rect)
    
    # Boyalı alan oranı her zaman aynıdır
    shaded_area = patches.Rectangle((0, 0), base_num/base_den, 1, facecolor="#3498db", alpha=0.6)
    ax.add_patch(shaded_area)

    # Dikey sütunlar (Ana payda)
    for i in range(1, base_den):
        ax.axvline(x=i/base_den, color='black', linewidth=1.5)

    # Yatay çizgiler (Genişletme/Sadeleştirme katmanı)
    show_horizontal = False
    ls = '-'
    alpha = 1.0
    
    if op_type == "expand":
        if step_mode == "2. İşlem Sonucu": show_horizontal = True
        if step_mode == "3. Alan Korunumu Analizi": show_horizontal = True; ls = '--'; alpha = 0.4
    else: # simplify
        if step_mode == "1. Başlangıç Hali": show_horizontal = True
        if step_mode == "3. Alan Korunumu Analizi": show_horizontal = True; ls = '--'; alpha = 0.4

    if show_horizontal:
        for i in range(1, factor):
            ax.axhline(y=i/factor, color='green' if op_type=="simplify" else 'red', linestyle=ls, alpha=alpha)

    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    return fig

# --- İçerik ---
col1, col2 = st.columns([2, 1])

with col1:
    # Başlıkları ve kesirleri belirle
    if prob["type"] == "expand":
        val1 = f"{prob['base_num']}/{prob['base_den']}"
        val2 = f"{prob['base_num']*prob['factor']}/{prob['base_den']*prob['factor']}"
    else:
        val1 = f"{prob['base_num']*prob['factor']}/{prob['base_den']*prob['factor']}"
        val2 = f"{prob['base_num']}/{prob['base_den']}"

    if mod == "1. Başlangıç Hali":
        st.subheader(f"📍 İlk Hali: {val1}")
        st.pyplot(draw_fraction_model(prob['base_num'], prob['base_den'], prob['factor'], mod, prob['type']))
    elif mod == "2. İşlem Sonucu":
        st.subheader(f"✅ İşlem Sonucu: {val2}")
        st.pyplot(draw_fraction_model(prob['base_num'], prob['base_den'], prob['factor'], mod, prob['type']))
    else:
        st.subheader("🕵️ Alan Korunumu Analizi")
        st.pyplot(draw_fraction_model(prob['base_num'], prob['base_den'], prob['factor'], mod, prob['type']))

with col2:
    st.markdown("### 📝 Matematiksel İşlem")
    if prob["type"] == "expand":
        st.latex(rf"\frac{{{prob['base_num']}}}{{{prob['base_den']}}} \times {prob['factor']} = \frac{{{prob['base_num']*prob['factor']}}}{{{prob['base_den']*prob['factor']}}}")
        st.write("**Genişletme:** Parçalar bölündü, sayı arttı.")
    else:
        st.latex(rf"\frac{{{prob['base_num']*prob['factor']}}}{{{prob['base_den']*prob['factor']}}} \div {prob['factor']} = \frac{{{prob['base_num']}}}{{{prob['base_den']}}}")
        st.write("**Sadeleştirme:** Parçalar birleşti, sayı küçüldü.")
    st.info("Fark ettiyseniz mavi boyalı alanın büyüklüğü iki durumda da aynı kaldı!")
