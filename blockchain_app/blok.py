import hashlib  # Hash işlemleri için kullanılan kütüphane.
import json  # JSON (JavaScript Object Notation) işlemleri için kullanılan kütüphane.
import time  # Zaman işlemleri için kullanılan kütüphane.
from islem import Islem_Kodlayici  # Islem sınıfını JSON formatında kodlamak için kullanılan özel encoder.

class Blok:
    def __init__(self, timestap, islemler, bir_onceki_hash_degeri=""):
        """
        Blok sınıfının başlatıcı (constructor) metodu.
        Bir blok oluşturulduğunda, blokun özelliklerini ayarlar.
        
        :param timestap: Blokun oluşturulduğu zaman damgası
        :param islemler: Blok içinde saklanacak işlemler
        :param bir_onceki_hash_degeri: Zincirdeki bir önceki bloğun hash değeri
        """
        self.bir_onceki_hash_degeri = bir_onceki_hash_degeri  # Bir önceki bloğun hash değeri
        self.timestap = timestap  # Blokun oluşturulma zaman damgası
        self.islemler = islemler  # Blok içinde saklanan işlemler
        self.nonce = 0  # Kazım (mining) işlemi sırasında kullanılan nonce değeri
        self.hash = self.hash_hesapla()  # Blokun hash değeri, hash hesaplama metodu ile belirlenir

    def hash_hesapla(self):
        """
        Blok için hash hesaplama metodu.
        Blok içeriği ve nonce değeri kullanılarak SHA-256 algoritması ile hash değeri hesaplanır.
        
        :return: Blokun hash değeri
        """
        # Blok içeriği (önceki hash, zaman damgası, işlemler ve nonce) bir string olarak birleştirilir
        islenMemis_ifade = self.bir_onceki_hash_degeri + str(self.timestap) + json.dumps(self.islemler, ensure_ascii=False, cls=Islem_Kodlayici) + str(self.nonce)
        sha256 = hashlib.sha256()  # SHA-256 hash algoritması kullanılır
        sha256.update(islenMemis_ifade.encode('utf-8'))  # Blok içeriği UTF-8 formatında kodlanarak hash algoritmasına verilir
        hash = sha256.hexdigest()  # Hash değeri hexadecimal formatta alınır
        return hash

    def blogu_kaz(self, zorluk):
        """
        Blok kazım (mining) metodu.
        Belirli bir zorluk seviyesine ulaşmak için nonce değerini artırarak hash hesaplamaları yapılır.
        
        :param zorluk: Kazım zorluk seviyesi. Hash değerinin ilk 'zorluk' kadar karakteri sıfır olmalıdır
        """
        zamanin_baslangici = time.process_time()  # Kazım işleminin başlangıç zamanı
        # İstenen zorluk seviyesine ulaşılana kadar hash hesaplaması yapılır
        while self.hash[0: zorluk] != ''.join(['0'] * zorluk):
            self.nonce += 1  # Nonce değeri her seferinde bir artırılır
            self.hash = self.hash_hesapla()  # Yeni nonce değeri ile hash tekrar hesaplanır
        # Kazım işlemi tamamlandığında süre hesaplanır ve ekrana yazdırılır
        print("Blogun Kazimi için:%s,  %fSaniye Sürdü" % (self.hash, time.process_time() - zamanin_baslangici))
