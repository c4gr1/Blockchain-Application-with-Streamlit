import streamlit as st
from blok import Blok
from islem import Islem
from blokzincir import Blokzincir

blockchain = Blokzincir()
tum_islemler = []

st.title("Blok Zinciri Uygulaması")

gonderen = st.text_input("Gönderen : ")
alici = st.text_input("Alıcı : ")
miktar = st.number_input("Miktar : ", min_value=0, step=1)

if st.button("İşlemi Gönder"):
    try:
        if gonderen and alici and (miktar > 0):
            islem = Islem(gonderen, alici, miktar)
            blockchain.islem_ekle(islem)
            tum_islemler.append(islem)
            st.success("İşlem Başarıyla Gönderildi")
        else:
            st.error("Geçersiz İşlem Formatı ör: adres1, adres2, miktar")
    except Exception as e:
        st.error(f"Hata {str(e)}")

for islem in tum_islemler:
    st.write(f"{islem.hesapTan} - {islem.hesaBa}")

st.header("Blok Zinciri")
for blok in blockchain.zincir:
    st.write(f"İşlemler: ")
    st.write(f"{gonderen} -> {alici} : {miktar}")
    st.write("-------------------------------")
