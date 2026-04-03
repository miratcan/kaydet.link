# kaydet.link — Design Brief

## 1. Bu araç nedir

kaydet.link bir yer imi paylaşım platformudur. Kullanıcılar internette buldukları linkleri kaydeder, not ekler, etiketler ve diğer kullanıcıların kaydettiği linkleri keşfeder. Sosyal bir yer imi defteri.

Temel döngü şudur: Birisi bir link kaydeder. Başka birisi o linki görür, beğenir, kendi notunu ve etiketlerini ekleyerek kendisi de kaydeder. Linkler yorumlanır. Etiketlerle gezinilir. Topluluk bilgisi wiki sayfalarında birikir.

Platform, 2012'den kalma LinkFloyd projesinin ruhani devamıdır.

## 2. Bu araç ne değildir

- Bir read-it-later servisi değildir. Amaç "sonra okurum" değil, "bunu paylaşıyorum"dur.
- Bir haber agregratörü değildir. İçerik editoryal olarak küratlenmiyor, upvote/downvote yok.
- Bir sosyal ağ değildir. Takip, arkadaşlık, mesajlaşma yok.
- Bir arama motoru değildir. Linklerin içeriği indekslenmez, sadece metadata tutulur.
- Bir kişisel not defteri değildir. Kaydedilen her şey herkese açıktır.

## 3. Sayfalar ve içerikleri

### 3.1. Genel yapı (tüm sayfalar)

Her sayfada tekrar eden iskelet:

- **Üst çubuk**
  - Marka linki (anasayfaya götürür)
  - Giriş yapmış kullanıcı için:
    - Kaydet butonu
    - Bildirimler linki
      - Okunmamış bildirim sayısı rozeti
    - Kullanıcı adı linki (kendi profil sayfasına)
    - Çıkış linki
  - Giriş yapmamış kullanıcı için:
    - Giriş linki

- **Alt çubuk**
  - Marka adı
  - Etiketler sayfası linki
  - Wiki sayfası linki
  - Issue bildir linki

- **Mesaj alanı** (koşullu)
  - Sistem mesajları (başarı, hata)

### 3.2. Link akışı (anasayfa)

Ana sayfa. Kaydedilmiş linklerin listesi.

- **Sayfa başlığı**
  - Etiket filtresi aktifse: etiket adı
  - Kullanıcı filtresi aktifse: kullanıcı adı
  - Varsayılan: genel başlık

- **Sıralama sekmeleri**
  - Popüler, En çok kaydedilen, En yeni, En çok yorumlanan
  - Aktif sekme belirginleştirilmiş

- **Link kartları listesi**
  - Her kart için bkz. [3.2.1. Link kartı](#321-link-kartı)
  - Boş durum: bilgi mesajı

- **Sayfalama**
  - Önceki/sonraki sayfa linkleri
  - Mevcut sayfa göstergesi

#### 3.2.1. Link kartı

Tekrar eden bileşen. Hem akışta hem detay sayfasında kullanılır.

- **Küçük resim**
  - Linkin og:image'ı varsa: resim
  - Resim yoksa ama başlık varsa: baş harflerden oluşan yer tutucu
  - Hiçbiri yoksa: ikon yer tutucu

- **Gövde** (linkin detay sayfasına götürür)
  - Başlık (veya başlık yoksa URL)
  - Açıklama (varsa)

- **Meta bilgi**
  - Kaydedilme sayısı
  - Yorum sayısı
  - Eylem butonu:
    - Kullanıcı bu linki kaydetmişse: "Kaydedildi" butonu (düzenleme sayfasına götürür)
    - Kaydetmemişse: "Kaydet" butonu

### 3.3. Link detay sayfası

Tek bir linkin tüm bilgileri.

- **Link kartı** (bkz. [3.2.1](#321-link-kartı))

- **Kaydeden kullanıcılar bölümü**
  - Her kayıt için:
    - Kullanıcı adı
    - Zaman damgası (göreli)
    - Düzenle linki (sadece kayıt sahibine görünür)
    - Not (varsa)
    - Etiketler (varsa, her biri tıklanabilir)
  - Boş durum: bilgi mesajı

- **Yorumlar bölümü**
  - Yorum sayısı başlığı
  - Her yorum için:
    - Yazar kullanıcı adı
    - Zaman damgası (göreli)
    - Düzenle linki (sadece yazara görünür)
    - Yorum içeriği (HTML render edilmiş)
  - Giriş yapmış kullanıcı için:
    - Yorum formu
      - Metin alanı
      - Gönder butonu
  - Giriş yapmamış kullanıcı için:
    - Giriş yapma daveti linki

### 3.4. Link kaydetme sayfası

Yeni bir link kaydetme veya mevcut kaydı düzenleme.

- **Sayfa başlığı** (yeni kayıt veya düzenleme durumuna göre değişir)

- **Form**
  - **URL alanı** (yeni kayıtta görünür, düzenlemede gizli)
    - URL girildiğinde otomatik metadata çekme
    - Yükleniyor göstergesi
    - Çekilen metadata'nın ön izlemesi
  - **Not alanı** (opsiyonel)
  - **Etiketler alanı** (opsiyonel, virgülle ayrılmış)
  - Kaydet butonu

- **Mevcut link bilgisi** (düzenleme modunda veya başka bir kayıttan kaydederken)
  - OG kart ön izlemesi
    - Küçük resim
    - Başlık
    - Açıklama

- **Silme bölümü** (sadece düzenleme modunda)
  - Onay sorusu
  - Sil butonu

### 3.5. Etiketler sayfası

Tüm etiketlerin listesi.

- **Sayfa başlığı**
- **Etiket bulutu**
  - Her etiket tıklanabilir, ilgili link akışına götürür
- Boş durum: bilgi mesajı

### 3.6. Bildirimler sayfası

Kullanıcıya gelen bildirimler. Sayfa açıldığında tüm bildirimler okunmuş olarak işaretlenir.

- **Sayfa başlığı**
- **Bildirim listesi**
  - Her bildirim:
    - Aksiyonu yapan kullanıcı adı
    - Bildirim türü açıklaması
    - İlgili linkin başlığı (tıklanabilir)
    - Zaman damgası (göreli)
- Boş durum: bilgi mesajı
- **Sayfalama**

### 3.7. Ayarlar sayfası

Kullanıcı tercihleri.

- **Sayfa başlığı**
- **Form**
  - Biyografi alanı
  - Özet e-posta tercihi (Günlük / Haftalık / Hiçbir zaman)
  - Kaydet butonu

### 3.8. Wiki sayfaları

#### 3.8.1. Wiki dizini

- **Sayfa başlığı**
- **Sayfa listesi**
  - Her wiki sayfasının adı (tıklanabilir)
  - Sadece listelenebilir olarak işaretlenmiş sayfalar
- Boş durum: bilgi mesajı

#### 3.8.2. Wiki sayfa görünümü

- **Sayfa adı başlığı**
- **Düzenle linki** (sadece giriş yapmış kullanıcıya görünür)
- **Sayfa içeriği** (Markdown'dan dönüştürülmüş HTML)

#### 3.8.3. Wiki sayfa düzenleme

- **Sayfa başlığı**
- **Form**
  - Sayfa adı alanı
  - İçerik alanı (Markdown)
  - Listelensin mi onay kutusu
  - Kaydet butonu

### 3.9. Giriş sayfası

- **Sayfa başlığı**
- **Google ile giriş butonu**

### 3.10. Çıkış sayfası

- **Sayfa başlığı**
- Onay sorusu
- **Çıkış formu**
  - Çıkış butonu

### 3.11. Sosyal hesap kayıt sayfası

Google ile ilk kez giriş yapan kullanıcılar için.

- **Sayfa başlığı**
- Açıklama metni
- **Form**
  - Kullanıcı adı seçme alanı
  - Kayıt butonu

### 3.12. Issue bildir (modal)

Footer'daki "Issue Bildir" linkine basıldığında devreye giren etkileşimli akış.

- **Eleman seçme modu**
  - İmleç değişir
  - Sayfa elemanları üzerine gelindiğinde vurgulanır
  - Tıklanan eleman seçilir ve farklı şekilde vurgulanır

- **Bildirim formu** (eleman seçildikten sonra)
  - Başlık alanı (zorunlu)
  - Açıklama alanı (opsiyonel)
  - Seçilen elemanın teknik tanımlayıcısı (otomatik)
  - İptal butonu
  - Gönder butonu (GitHub issue sayfasını açar)
    - Sayfa URL'i, başlık, eleman bilgisi ve açıklama otomatik doldurulur
