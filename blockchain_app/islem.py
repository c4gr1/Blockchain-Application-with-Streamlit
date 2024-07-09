import json  # JSON (JavaScript Object Notation) modülünü içe aktarır. Bu modül, JSON verilerini Python veri yapılarına dönüştürmek veya Python veri yapılarını JSON formatında serileştirmek için kullanılır.

# İşlem sınıfı tanımı
class Islem:
    def __init__(self, hesapTan, hesaBa, miktar):
        """
        Islem sınıfının başlatıcı (constructor) metodu.
        Bir işlem nesnesi oluşturur ve özelliklerini ayarlar.
        
        :param hesapTan: İşlemi başlatan hesap
        :param hesaBa: İşlem alıcısı hesap
        :param miktar: İşlem miktarı
        """
        self.hesapTan = hesapTan  # İşlemi başlatan hesap
        self.hesaBa = hesaBa  # İşlem alıcısı hesap
        self.miktar = miktar  # İşlem miktarı

# JSON Encoder (Kodlayıcı) sınıfı, işlemleri JSON formatında kodlamak için kullanılır
class Islem_Kodlayici(json.JSONEncoder):
    def default(self, onun):
        """
        JSON Encoder'ın default metodu.
        Bir nesnenin JSON formatında nasıl serileştirileceğini belirler.
        
        :param onun: Serileştirilecek nesne
        :return: Serileştirilmiş nesne
        """
        if isinstance(onun, Islem):  # Eğer verilen nesne Islem sınıfından bir örnekse
            return onun.__dict__  # Nesnenin __dict__ özniteliğini (yani nesnenin özelliklerini içeren sözlüğü) döndür
        return json.JSONEncoder.default(self, onun)  # Eğer verilen nesne Islem sınıfından bir örnek değilse, varsayılan JSON Encoder işlemiyle devam et

# Eğer bu dosya doğrudan çalıştırılıyorsa, aşağıdaki kod bloğu çalıştırılır
if __name__ == '__main__':
    # Yeni bir Islem örneği oluştur, "Cagri" gönderici, "Zeki" alıcı ve 100 işlem miktarı
    isl = Islem("Cagri", "Zeki", 100)
    # Islem nesnesini yazdır (bu, nesnenin __repr__ veya __str__ metodunu kullanır, yoksa varsayılan nesne gösterimini kullanır)
    print(isl)
    # Islem nesnesini JSON formatında serileştir ve sonucu yazdır
    # ensure_ascii=False parametresi, JSON çıktı dosyasının UTF-8 formatında olmasını sağlar (Türkçe karakterlerin doğru görüntülenmesi için)
    # cls=Islem_Kodlayici parametresi, özel JSON Encoder kullanarak Islem nesnesini nasıl serileştireceğini belirler
    print(json.dumps(isl, ensure_ascii=False, cls= Islem_Kodlayici))
