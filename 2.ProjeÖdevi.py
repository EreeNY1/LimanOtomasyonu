class Tir:
    def __init__(self, gelis_zamani, tir_plakasi, ulke, ton_20_adet, ton_30_adet, yuk_miktari, maliyet):
        self.gelis_zamani = gelis_zamani
        self.tir_plakasi = tir_plakasi
        self.ulke = ulke
        self.ton_20_adet = int(ton_20_adet)
        self.ton_30_adet = int(ton_30_adet)
        self.yuk_miktari = int(yuk_miktari)
        self.maliyet = int(maliyet)
        self.yuk_bilgisi = {'ulke': self.ulke, 'konteyner_20t': self.ton_20_adet, 'konteyner_30t': self.ton_30_adet,
                            'miktar': self.yuk_miktari, 'maliyet': self.maliyet}

class Gemi:
    def __init__(self, gelis_zamani, gemi_adi, kapasite, gidecek_ulke):
        self.gelis_zamani = gelis_zamani
        self.gemi_adi = gemi_adi
        self.kapasite = int(kapasite)
        self.gidecek_ulke = gidecek_ulke
        self.yuk_bilgisi = {'ulke': None, 'konteyner_20t': 0, 'konteyner_30t': 0, 'miktar': 0, 'maliyet': 0}
def dosyadan_nesneleri_yukle(dosya_yolu, sinif):
    nesneler = []
    with open(dosya_yolu, 'r', encoding='windows-1254') as dosya:
        next(dosya)  # Başlık satırını atla
        satirlar = sorted(dosya, key=lambda satir: int(satir.strip().split(',')[0]))  # Geliş zamanına göre sırala

        gecis = 1  # Geliş zamanı için başlangıç değeri
        for satir in satirlar:
            satir = satir.strip().split(',')
            try:
                nesne = sinif(gecis, *satir[1:])  # Geliş zamanı değişkenini ekleyerek nesneyi oluştur
                nesneler.append(nesne)
                gecis += 1  # Geliş zamanını bir arttır
                if gecis > 3000:  # Belirli bir sınıra ulaşıldığında döngüyü sonlandır
                    break
            except ValueError as e:
                print(f"Hata: {e}. Satır okunamadı: {satir}")
    return nesneler


class Liman:
    def __init__(self, tir_listesi: list, gemi_listesi: list):
        self.tir_listesi = tir_listesi
        self.gemi_listesi = gemi_listesi
        self.istif_alani1 = []
        self.istif_alani2 = []
        self.yuklenen_tir = None  # Bu satır eklenmiştir

    def plaka_sirala(self, tir_listesi: list) -> list:
        return sorted(tir_listesi, key=lambda tir: tir.tir_plakasi)

    def tir_sirala(self) -> None:
        pass

    def tir_indir(self, tir: Tir) -> None:
        print(f"{tir.tir_plakasi} plakalı TIR yükünü indirmeye başladı.")

        print(f"{tir.tir_plakasi} plakalı TIR yükünü indirdi.")
        print(f"İndirilen yük miktarı: {tir.yuk_miktari} ton")

        # 1 numaralı istif alanına yük ekle
        self.istif_alani1.append(tir.yuk_bilgisi)

        print(f"1 numaralı istif alanındaki toplam yük miktarı: {sum(yuk['miktar'] for yuk in self.istif_alani1)} ton")

    def gemi_yukle(self, gemi: Gemi, tir: Tir) -> None:

        print(f"{gemi.gemi_adi} adlı gemiye yük yüklemeye başladı.")


        print(f"{gemi.gemi_adi} adlı gemiye yük yüklemesi tamamlandı.")

        # Yük bilgisi güncellenmeli
        gemi.yuk_bilgisi['miktar'] += tir.yuk_miktari
        gemi.yuk_bilgisi['konteyner_20t'] += tir.ton_20_adet
        gemi.yuk_bilgisi['konteyner_30t'] += tir.ton_30_adet

        print(f"Yüklenen yük miktarı: {gemi.yuk_bilgisi['miktar']} ton")

        # Doluluk oranı güncellenmeli
        doluluk_orani = gemi.yuk_bilgisi['miktar'] / gemi.kapasite * 100
        print(f"Geminin doluluk oranı: {doluluk_orani}%")

        # Gemi kapasitesinin en az %95'i dolduysa limandan ayrılmalı
        if doluluk_orani >= 95:
            print(f"{gemi.gemi_adi} adlı gemi limandan ayrıldı.")
            # Gemi listesinden gemiyi çıkarmalı
            self.gemi_listesi.remove(gemi)
            # İstif alanından yükü silmeli
            self.istif_alani1.remove(tir.yuk_bilgisi)
            # Yükleme sırası bir sonraki gemiye geçmeli
            if self.gemi_listesi:
                yeni_gemi = self.gemi_listesi[0]
                print(f"Yükleme sırası {yeni_gemi.gemi_adi} adlı gemiye geçti.")
            else:
                print("Limanda yük yüklenecek gemi kalmadı.")
    def vinc(self) -> None:
        islem_sayisi = 0
        while islem_sayisi < 20:
            if self.yuklenen_tir is None:  # Eklendi satır
                if self.tir_listesi:
                    tir = self.tir_listesi[0]
                    self.tir_indir(tir)
                    self.tir_listesi.remove(tir)
                    islem_sayisi += 1
                    self.yuklenen_tir = tir
                else:
                    print("TIR listesi boş. Yük indirilecek TIR yok.")
                    break
            else:
                if self.gemi_listesi:
                    gemi = self.gemi_listesi[0]
                    self.gemi_yukle(gemi, self.yuklenen_tir)
                    islem_sayisi += 1
                    self.yuklenen_tir = None
                else:
                    print("Gemi listesi boş. Yük yüklenecek gemi yok.")
                    break

def menu_goster():
    print("1. TIR Listesini Görüntüle")
    print("2. Gemi Listesini Görüntüle")
    print("3. Operasyonları Başlat")
    print("4. Çıkış")
    return input("Bir seçenek seçin (1-4): ")

def main():
    gemi_listesi = dosyadan_nesneleri_yukle("gemiler.csv", Gemi)
    tir_listesi = dosyadan_nesneleri_yukle("olaylar.csv", Tir)
    tir_listesi.sort(key=lambda x: (x.gelis_zamani, int(x.tir_plakasi.split('_')[-1])))
    liman = Liman(tir_listesi, gemi_listesi)

    while True:
        secim = menu_goster()

        if secim == "1":
            print("TIR Listesi:")
            for tir in liman.tir_listesi:
                print(f"Plaka: {tir.tir_plakasi}, Geliş Zamanı: {tir.gelis_zamani}")
        elif secim == "2":
            print("Gemi Listesi:")
            for gemi in liman.gemi_listesi:
                print(f"Gemi Adı: {gemi.gemi_adi}, Kapasite: {gemi.kapasite}")
        elif secim == "3":
            liman.vinc()
        elif secim == "4":
            print("Programdan çıkılıyor.")
            break
        else:
            print("Geçersiz seçenek. Lütfen 1 ile 4 arasında bir sayı girin.")

if __name__ == "__main__":
    main()