import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Sayfa Yapılandırması
st.set_page_config(page_title="Matematik İllüzyonisti", page_icon="🪄")

# Başlık ve Giriş
st.title("🪄 Matematik İllüzyonisti: Kesirlerin Gizemi")
st.write("""
*Hoş geldiniz! Bugün sayıların aslında göründüğü gibi olmadığını kanıtlayacağız. 
Bakalım gözleriniz mi yanılıyor yoksa matematik mi yalan söylüyor?*
""")

st.divider()

# Yan Menü Kontrolleri
st.sidebar.header("İllüzyon Kontrolleri")
step = st.sidebar.radio(
    "Görselleştirme Adımları:",
    ["1. Başlangıç (Bütün)", "2. İlk Katlama (1/2)", "3. Genişletme (2/4)", "4. İllüzyonun Sırrı (Decentering)"]
)

# Çizim Fonksiyonu
def draw_paper(parts, shaded_parts, show_folds=True):
    fig, ax = plt.subplots(figsize=(10, 2))
    
    # Ana kağıt (Beyaz)
    rect = patches.Rectangle((0, 0), 1, 1, linewidth=2, edgecolor='black', facecolor='white')
    ax.add_patch(rect)
    
    # Boyalı Alan
    width_per_part = 1 / parts
    shaded_width = width_per_part * shaded_parts
    shaded_rect = patches.Rectangle((0, 0), shaded_width, 1, facecolor='#FF4B4B', alpha=0.6)
    ax.add_patch(shaded_rect)
    
    # Kat İzleri
    if show_folds:
        for i in range(1, parts):
            ax.axvline(x=i * width_per_part, color='black', linestyle='--', linewidth=1)
            
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.1, 1.1)
    ax.axis('off')
    return fig

# Senaryo Akışı
if step == "1. Başlangıç (Bütün)":
    st.subheader("Elimizde bir bütün kağıt şerit var.")
    st.pyplot(draw_paper(1, 1))
    st.info("Bu bizim başlangıç noktamız. Henüz hiçbir numara yok!")

elif step == "2. İlk Katlama (1/2)":
    st.subheader("Hokus Pokus! Kağıdı ikiye katladık.")
    st.pyplot(draw_paper(2, 1))
    st.latex(r"\frac{1}{2}")
    st.write("Şu an elimizde koca bir dilim var. Yarısı boyalı, yarısı değil.")

elif step == "3. Genişletme (2/4)":
    st.subheader("Dikkatli Bakın: Parçaları çoğaltıyorum!")
    st.pyplot(draw_paper(4, 2))
    st.latex(r"\frac{2}{4}")
    st.warning("Gördünüz mü? Sayılar büyüdü (2 ve 4). Peki boyalı alan gerçekten büyüdü mü?")
    
    if st.button("Sayılar büyüdüğü için alan da büyüdü mü?"):
        st.error("Hayır! İşte bu bir matematik illüzyonudur.")

elif step == "4. İllüzyonun Sırrı (Decentering)":
    st.subheader("🕵️‍♂️ İllüzyonun Sırrı: Odaktan Uzaklaşma")
    st.pyplot(draw_paper(4, 2))
    st.write("""
    **İşin sırrı şu:** Sayılar büyüdüğünde aslında daha fazla yemeğe sahip olmuyoruz. 
    Sadece dilimleri küçültüyoruz! 
    
    - Dilim sayısı arttı ($2 \rightarrow 4$) 
    - Ama her bir dilim küçüldü.
    - **Sonuç:** Toplam miktar (alan) sabit kaldı!
    """)
    
    if st.checkbox("Kat izlerini sil (Sadeleştirme)"):
        st.write("Bakın, kat izlerini hayalimizde sildiğimizde yine aynı $1/2$ karşımızda!")
        st.pyplot(draw_paper(4, 2, show_folds=False))

st.divider()
st.caption("Matematik Dedektifleri için geliştirilmiştir. 2026")
