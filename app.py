import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Sayfa ayarları
st.set_page_config(page_title="Kesir Fabrikası v2", layout="wide")

st.title("🍫 Kesir Fabrikası: Alan Korunumu ve Yeni Örnekler")
st.write("Görsellerdeki tüm örnekleri içeren interaktif matematik modelleme aracı.")

# --- Veri Seti (Görsellerdeki Örnekler) ---
problems = {
    "7/8 Örneği (Varsayılan)": {"type": "expand", "num": 7, "den": 8, "factor": 3, "label": "7/8"},
    "b) 20/36 (4 ile sadeleştir)": {"type": "simplify", "num": 5, "den": 9, "factor": 4, "label": "20/36"},
    "c) 11/15 (5 ile genişlet)": {"type": "expand", "num": 11, "den": 15, "factor": 5, "label": "11/15"},
    "ç) 6/29 (2 ile genişlet)": {"type": "expand", "num": 6, "den": 29, "factor": 2, "label": "6/29"},
    "d) 48/84 (6 ile sadeleştir)": {"type": "simplify", "num": 8, "den": 14, "factor": 6, "label": "48/84"},
    "e) 24/32 (8 ile sadeleştir)": {"type": "simplify", "num": 3, "den": 4, "factor": 8, "label": "24/32"},
    "f) 3/5 (7 ile genişlet)": {"type": "expand", "num": 3, "den": 5, "factor": 7, "label": "3/5"},
    "g) 18/45 (9 ile sadeleştir)": {"type": "simplify", "num": 2, "den": 5, "factor": 9, "label": "18/45"},
    "ğ) 1/6 (11 ile genişlet)": {"type": "expand", "num": 1, "den": 6, "factor": 11, "label": "1/6"},
}

# --- Sidebar (Kontrol Paneli) ---
st.sidebar.header("🔍 Problem Seçimi")
selected_key = st.sidebar.selectbox("Lütfen bir örnek seçin:", list(problems.keys()))
prob = problems[selected_key]

# İşlem Seçimi
mod = st.sidebar.radio(
    "Aşama:",
    ["1. Başlangıç Hali", "2. İşlem Sonrası (Genişletme/Sadeleştirme)", "3. Alan Korunumu Analizi"]
)

# --- Görselleştirme Fonksiyonu ---
def draw_fraction_model(base_num, base_den, factor, mode, is_expand=True):
    fig, ax = plt.subplots(figsize=(12, 4))
    
    # Arka plan
    rect = patches.Rectangle((0, 0), 1, 1, linewidth=2, edgecolor='black', facecolor='white')
    ax.add_patch(rect)
    
    # Boyalı Alan
    fill_color = "#3498db"
    shaded_area = patches.Rectangle((0, 0), base_num/base_den, 1, facecolor=fill_color, alpha=0.7)
    ax.add_patch(shaded_area)

    # Dikey Çizgiler (Ana sütunlar)
    for i in range(1, base_den):
        ax.axvline(x=i/base_den, color='black', linestyle='-', linewidth=1.5)

    # Yatay Çizgiler (Katmanlar)
    if mode != "start":
        for i in range(1, factor):
            ls = '--' if mode == "analyze" else '-'
            alpha = 0.4 if mode == "analyze" else 1.0
            color = 'red' if is_expand else 'green'
            ax.axhline(y=i/factor, color=color, linestyle=ls, linewidth=1, alpha=alpha)

    ax.set_xlim(-0.01, 1.01)
    ax.set_ylim(-0.05, 1.05)
    ax.axis('off')
    return fig

# --- İçerik Akışı ---
is_expand = (prob["type"] == "expand")
col1, col2 = st.columns([2, 1])

with col1:
    if mod == "1. Başlangıç Hali":
        display_num = prob["num"] if is_expand else prob["num"] * prob["factor"]
        display_den = prob["den"] if is_expand else prob["den"] * prob["factor"]
        st.subheader(f"📍 Kesrin İlk Hali: {display_num}/{display_den}")
        st.pyplot(draw_fraction_model(prob["num"], prob["den"], prob["factor"], "start", is_expand))
        
    elif mod == "2. İşlem Sonrası (Genişletme/Sadeleştirme)":
        target_num = prob["num"] * prob["factor"] if is_expand else prob["num"]
        target_den = prob["den"] * prob["factor"] if is_expand else prob["den"]
        st.subheader(f"🔪 İşlem Sonucu: {target_num}/{target_den}")
        st.pyplot(draw_fraction_model(prob["num"], prob["den"], prob["factor"], "process", is_expand))
        
        if is_expand:
            st.latex(rf"\frac{{{prob['num']}}}{{{prob['den']}}} \xrightarrow{{\times {prob['factor']}}} \frac{{{target_num}}}{{{target_den}}}")
        else:
            st.latex(rf"\frac{{{prob['num'] * prob['factor']}}}{{{prob['den'] * prob['factor']}}} \xrightarrow{{\div {prob['factor']}}} \frac{{{prob['num']}}}{{{prob['den']}}}")

    elif mod == "3. Alan Korunumu Analizi":
        st.subheader("🕵️ Analiz: Alan Neden Değişmedi?")
        st.pyplot(draw_fraction_model(prob["num"], prob["den"], prob["factor"], "analyze", is_expand))
        st.info("Kırmızı/Yeşil çizgiler hayali olarak kaldırıldığında veya eklendiğinde mavi alanın (miktarın) sabit kaldığını görebilirsiniz.")

with col2:
    st.markdown("### 🧪 Laboratuvar Notları")
    if is_expand:
        st.write(f"**Genişletme:** Parça sayısını **{prob['factor']}** katına çıkardık. Sayılar büyüdü ama her parçanın boyutu aynı oranda küçüldü.")
    else:
        st.write(f"**Sadeleştirme:** Küçük parçaları **{prob['factor']}**'erli gruplar halinde birleştirdik. Sayılar küçüldü ama miktar korundu.")
