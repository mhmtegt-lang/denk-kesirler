import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Sayfa ayarları
st.set_page_config(page_title="Kesirlerde Alan Korunumu", layout="wide")

st.title("🍫 Kesir Fabrikası: Alan Korunumu Modeli")
st.write("Bu model, kesirlerin sayısal değerleri değişse de kapladıkları alanın neden sabit kaldığını (Somuttan Soyuta) gösterir.")

# --- Sidebar (Kontrol Paneli) ---
st.sidebar.header("⚙️ Model Ayarları")
st.sidebar.info("7/8 kesrini 3 ile genişletip/sadeleştiriyoruz.")

# İşlem Seçimi
mod = st.sidebar.radio(
    "Yapılacak İşlem:",
    ["1. Başlangıç (7/8)", "2. Genişletme (7/8 -> 21/24)", "3. Sadeleştirme (21/24 -> 7/8)"]
)

# --- Görselleştirme Fonksiyonu ---
def draw_fraction_model(base_den=8, base_num=7, factor=3, mode="start"):
    fig, ax = plt.subplots(figsize=(12, 4))
    
    # Arka plan (Bütün)
    rect = patches.Rectangle((0, 0), 1, 1, linewidth=3, edgecolor='black', facecolor='white')
    ax.add_patch(rect)
    
    # Boyalı Alan (Pay)
    fill_color = "#3498db" # Güzel bir mavi
    shaded_area = patches.Rectangle((0, 0), base_num/base_den, 1, facecolor=fill_color, alpha=0.7)
    ax.add_patch(shaded_area)

    # Dikey Çizgiler (Ana Kesir - 8 parça)
    for i in range(1, base_den):
        ax.axvline(x=i/base_den, color='black', linestyle='-', linewidth=2)

    # Yatay Çizgiler (Genişletme Faktörü - 3 kat)
    if mode != "start":
        for i in range(1, factor):
            # Sadeleştirme modunda çizgiler kesik ve soluk olur (birleşmeyi temsil eder)
            ls = '--' if mode == "simplify" else '-'
            alpha = 0.3 if mode == "simplify" else 1.0
            ax.axhline(y=i/factor, color='red', linestyle=ls, linewidth=2, alpha=alpha)

    # Eksenleri kapat
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.05, 1.05)
    ax.axis('off')
    return fig

# --- Ana Ekran Akışı ---
col1, col2 = st.columns([2, 1])

with col1:
    if mod == "1. Başlangıç (7/8)":
        st.subheader("📍 Temel Kesir: 7/8")
        st.pyplot(draw_fraction_model(mode="start"))
        st.latex(r"\frac{7}{8}")
        
    elif mod == "2. Genişletme (7/8 -> 21/24)":
        st.subheader("🔪 Genişletme: Dilimlere Ayırma")
        st.pyplot(draw_fraction_model(mode="expand"))
        st.latex(r"\frac{7 \times 3}{8 \times 3} = \frac{21}{24}")
        st.success("Her bir 8 dikey sütunu, 3 yatay parçaya böldük. Toplam 24 parça oldu!")

    elif mod == "3. Sadeleştirme (21/24 -> 7/8)":
        st.subheader("🧪 Sadeleştirme: Dilimleri Birleştirme")
        st.pyplot(draw_fraction_model(mode="simplify"))
        st.latex(r"\frac{21 \div 3}{24 \div 3} = \frac{7}{8}")
        st.warning("Yataydaki kırmızı çizgileri 'hayali olarak siliyoruz'. Parçalar birleşiyor!")

with col2:
    st.markdown("### 🧠 Öğrenme Notu")
    if mod == "1. Başlangıç (7/8)":
        st.write("Ekranda gördüğünüz mavi alan, bütünün 8'de 7'sidir.")
    elif mod == "2. Genişletme (7/8 -> 21/24)":
        st.write("**Odaktan Uzaklaşma:** Sayılar 21 ve 24'e çıktı ama mavi bölgenin kapladığı toplam alan değişmedi. Sadece parçalar küçüldü!")
    elif mod == "3. Sadeleştirme (21/24 -> 7/8)":
        st.write("**Alan Korunumu:** Parçaları birleştirdiğimizde (sadeleştirdiğimizde) aslında en baştaki 7/8 modeline geri döndüğümüzü görüyoruz.")

st.divider()
st.info("Eğitsel İlke: Somuttan Soyuta. Önce görsel alanın sabitliğini gör, sonra rakamlarla işlem yap.")
