from blok import Blok  # Blok sınıfını blok.py dosyasından içe aktarır.
import time  # Zaman işlemleri için kullanılan kütüphane.
from islem import Islem  # Islem sınıfını islem.py dosyasından içe aktarır.

class Blokzincir:
    def __init__(self):
        """
        Blokzincir sınıfının başlatıcı (constructor) metodu.
        Yeni bir blok zinciri oluşturur.
        """
        self.zincir = [self.baslangic_blogu_olustur()]  # Zincirin başlangıç bloğunu (genesis block) oluşturur.
        self.zorluk = 3  # Blok kazım zorluk seviyesini belirler.
        self.bekleyen_islemler = []  # Bekleyen işlemleri tutar.
        self.kazim_odulu = 50  # Blok kazımı yapan madenciye verilecek ödülü belirler.

    @staticmethod
    def baslangic_blogu_olustur():
        """
        Genesis bloğunu (başlangıç bloğu) oluşturur.
        :return: Genesis bloğu
        """
        timestamp = time.mktime(time.strptime('2018-06-11 00:00:00', '%Y-%m-%d %H:%M:%S'))  # Genesis bloğu için zaman damgası oluşturur.
        blok = Blok(timestamp, [], '')  # Genesis bloğunu oluşturur.
        return blok

    def son_blogu_al(self):
        """
        Zincirdeki son bloğu alır.
        :return: Son blok
        """
        return self.zincir[-1]  # Zincirdeki son bloğu döndürür.

    def blok_ekle(self, blok):
        """
        Zincire yeni bir blok ekler.
        :param blok: Eklenecek blok
        """
        blok.bir_onceki_hash_degeri = self.son_blogu_al().hash  # Yeni bloğun önceki hash değerini zincirdeki son bloğun hash değeri yapar.
        blok.blogu_kaz(self.zorluk)  # Blok kazımını yapar.
        self.zincir.append(blok)  # Bloğu zincire ekler.

    def islem_ekle(self, islem):
        """
        Zincire yeni bir işlem ekler.
        :param islem: Eklenecek işlem
        """
        self.bekleyen_islemler.append(islem)  # İşlemi bekleyen işlemler listesine ekler.

    def bekleyen_islemi_kaz(self, kazanin_odul_hesabi):
        """
        Bekleyen işlemleri kazım yapar ve zincire ekler.
        :param kazanin_odul_hesabi: Kazım ödül hesabı
        """
        blok = Blok(time.time(), self.bekleyen_islemler, self.zincir[-1].hash)  # Yeni bir blok oluşturur ve bekleyen işlemleri ekler.
        blok.blogu_kaz(self.zorluk)  # Blok kazımını yapar.
        self.zincir.append(blok)  # Bloğu zincire ekler.
        self.bekleyen_islemler = [Islem(None, kazanin_odul_hesabi, self.kazim_odulu)]  # Bekleyen işlemleri sıfırlar ve kazım ödülünü ekler.

    def hesap_bakiyesini_al(self, hesap):
        """
        Belirtilen hesabın bakiyesini alır.
        :param hesap: Hesap adresi
        :return: Bakiye
        """
        bakiye = 0  # Başlangıç bakiyesi
        for blok in self.zincir:  # Zincirdeki her bir blok için
            for isls in blok.islemler:  # Bloktaki her bir işlem için
                if isls.hesapTan == hesap:  # Eğer işlem başlatıcısı belirtilen hesap ise
                    bakiye -= isls.miktar  # Hesaptan çıkan miktarı bakiyeden düşer.
                if isls.hesaBa == hesap:  # Eğer işlem alıcısı belirtilen hesap ise
                    bakiye += isls.miktar  # Hesaba gelen miktarı bakiyeye ekler.
        return bakiye  # Hesabın bakiyesini döndürür.

    def blokzinciri_dogrula(self):
        """
        Blockchain verilerinin eksiksiz olduğunu ve tahrif edilmediğini doğrular.
        :return: Sonucu kontrol et (True veya False)
        """
        for i in range(1, len(self.zincir)):  # Zincirdeki her bir blok için
            suAnki_blok = self.zincir[i]  # Şu anda üzerinde gidilen blok
            onceki_blok = self.zincir[i - 1]  # Geçerli bloğun önceki bloğu
            if suAnki_blok.hash != suAnki_blok.hash_hesapla():  # Geçerli bloğun hash değeri, hesaplanan hash değerine eşit değilse
                return False  # Veri değişmiş demektir, False döndür
            if suAnki_blok.bir_onceki_hash_degeri != onceki_blok.hash_hesapla():  # Mevcut bloğa kaydedilen önceki bloğa ait hash değeri, hesaplanan hash değerine eşit değilse
                return False  # Veri değişmiş demektir, False döndür
        return True  # Zincir doğruysa True döndür

if __name__ == '__main__':
    # Blokzincir sınıfının bir örneğini oluşturur.
    blokzincir = Blokzincir()
    
    # Belirli adreslerin bakiyesini kontrol eder ve yazdırır.
    print('address1  ', blokzincir.hesap_bakiyesini_al('address1'))
    print('address2  ', blokzincir.hesap_bakiyesini_al('address2'))
    print('address3  ', blokzincir.hesap_bakiyesini_al('address3'))
    
    print("---------------------------------")
    
    # Yeni işlemler ekler.
    blokzincir.islem_ekle(Islem('address1', 'address2', 80))
    blokzincir.islem_ekle(Islem('address2', 'address3', 13))
    
    # Bekleyen işlemleri kazım yapar ve zincire ekler.
    blokzincir.bekleyen_islemi_kaz('address3')
    
    print("---------------------------------")
    
    # Belirli adreslerin bakiyesini tekrar kontrol eder ve yazdırır.
    print('address1  ', blokzincir.hesap_bakiyesini_al('address1'))
    print('address2  ', blokzincir.hesap_bakiyesini_al('address2'))
    print('address3 ', blokzincir.hesap_bakiyesini_al('address3'))
    
    # Bekleyen işlemleri tekrar kazım yapar ve zincire ekler.
    blokzincir.bekleyen_islemi_kaz('address2')
    
    # Belirli adreslerin bakiyesini tekrar kontrol eder ve yazdırır.
    print('address1  ', blokzincir.hesap_bakiyesini_al('address1'))
    print('address2  ', blokzincir.hesap_bakiyesini_al('address2'))
    print('address3  ', blokzincir.hesap_bakiyesini_al('address3'))
    
    # Zincirdeki son bloğun detaylarını yazdırır.
    print(blokzincir.son_blogu_al)
    
    # Kazım ödülünü yazdırır.
    print(blokzincir.kazim_odulu)
    
    # Başlangıç bloğunu oluşturur.
    blokzincir.baslangic_blogu_olustur
