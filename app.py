import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Sayfa ayarları
st.set_page_config(page_title="Kesir Fabrikası v4", layout="wide")

st.title("🍫 Kesir Fabrikası: Alan Korunumu")
st.write("Sadeleştirme ve genişletmede sonucun gizlendiği geliştirilmiş eğitim modeli.")

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
selected_key = st.sidebar.selectbox("Bir örnek seçin:", list(problems.keys()))
prob = problems[selected_key]

mod = st.sidebar.radio(
    "Aşama:",
    ["1. Başlangıç Hali", "2. İşlem Sonucu", "3. Alan Korunumu Analizi"]
)

# --- Görselleştirme Fonksiyonu ---
def draw_fraction_model(base_num, base_den, factor, step_mode, op_type):
    fig, ax = plt.subplots(figsize=(10, 3.5))
    rect = patches.Rectangle((0, 0), 1, 1, linewidth=2, edgecolor='black', facecolor='white')
    ax.add_patch(rect)
    
    # Alan her zaman sabittir
    shaded_area = patches.Rectangle((0, 0), base_num/base_den, 1, facecolor="#3498db", alpha=0.6)
    ax.add_patch(shaded_area)

    # Dikey sütunlar
    for i in range(1, base_den):
        ax.axvline(x=i/base_den, color='black', linewidth=1.5)

    # Yatay çizgiler (Sadeleştirmede başlangıçta var, genişletmede sonda var)
    show_horizontal = False
    ls = '-'
    alpha = 1.0
    
    if op_type == "expand":
        if step_mode != "1. Başlangıç Hali": show_horizontal = True
        if step_mode == "3. Alan Korunumu Analizi": ls = '--'; alpha = 0.4
    else: # simplify
        if step_mode == "1. Başlangıç Hali": show_horizontal = True
        if step_mode == "3. Alan Korunumu Analizi": show_horizontal = True; ls = '--'; alpha = 0.4

    if show_horizontal:
        for i in range(1, factor):
            ax.axhline(y=i/factor, color='green' if op_type=="simplify" else 'red', linestyle=ls, alpha=alpha)

    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    return fig

# --- İçerik ve Mantık ---
col1, col2 = st.columns([2, 1])

# Kesir değerlerini hesapla
start_num = prob['base_num'] * prob['factor'] if prob['type'] == "simplify" else prob['base_num']
start_den = prob['base_den'] * prob['factor'] if prob['type'] == "simplify" else prob['base_den']
res_num = prob['base_num'] if prob['type'] == "simplify" else prob['base_num'] * prob['factor']
res_den = prob['base_den'] if prob['type'] == "simplify" else prob['base_den'] * prob['factor']

with col1:
    if mod == "1. Başlangıç Hali":
        st.subheader(f"📍 Başlangıç Kesri: {start_num}/{start_den}")
    elif mod == "2. İşlem Sonucu":
        st.subheader(f"✅ Sonuç: {res_num}/{res_den}")
    else:
        st.subheader("🕵️ Alan Korunumu: Neler Değişti?")
        
    st.pyplot(draw_fraction_model(prob['base_num'], prob['base_den'], prob['factor'], mod, prob['type']))

with col2:
    st.markdown("### 📝 Matematiksel İşlem")
    
    if mod == "1. Başlangıç Hali":
        # Başlangıçta sadece kesrin kendisini göster, işlemi gizle
        st.latex(rf"\text{{Kesir: }} \frac{{{start_num}}}{{{start_den}}}")
        st.info("Bu kesri sadeleştirdiğimizde veya genişlettiğimizde alanın nasıl değişeceğini tahmin edin.")
    
    else:
        # 2. ve 3. adımda tam işlemi göster
        if prob["type"] == "expand":
            st.latex(rf"\frac{{{prob['base_num']}}}{{{prob['base_den']}}} \xrightarrow{{\times {prob['factor']}}} \frac{{{res_num}}}{{{res_den}}}")
            st.write(f"**Genişletme:** Parçalar {prob['factor']} katına çıktı.")
        else:
            st.latex(rf"\frac{{{start_num}}}{{{start_den}}} \xrightarrow{{\div {prob['factor']}}} \frac{{{res_num}}}{{{res_den}}}")
            st.write(f"**Sadeleştirme:** Parçalar {prob['factor']}'erli gruplanıp birleşti.")
            
        st.success("Gördüğünüz gibi, sayısal değerler değişse de kapladığı alan aynı kaldı!")
