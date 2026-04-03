# Issue #6: Gelismis Notlar

**Oncelik:** Orta
**Efor:** Dusuk
**Milestone:** Kisisel Uygulama Deneyimi
**Labels:** `enhancement`, `ux`

## Ozet

Not alanini daha belirgin ve yonlendirici yap. Notlar, kaydet.link'i "link listesi"nden "kisisel bilgi tabani"na donusturur.

## Mevcut Durum

- Not alani Markdown destekliyor ama formda ikincil hissediyor
- Placeholder/yonlendirme yok — kullanici ne yazacagini bilmiyor
- Notlar uzerinden arama yapilamiyor (Issue #4 ile birlikte cozulecek)

## Yapilacaklar

### Not alani iyilestirmeleri

- [ ] Not alanini formda daha belirgin yap (boyut, konum)
- [ ] Yonlendirici placeholder ekle:
  - "Bu linki neden kaydediyorsun? Ne ogrenmistin?"
  - "Kendine bir not birak..."
- [ ] Markdown onizleme (HTMX ile canli veya toggle)

### Not goruntuleme

- [ ] Link detay sayfasinda notu daha belirgin goster
- [ ] Link kartinda not varsa kucuk bir gosterge/preview

### Sablonlar (opsiyonel, v2)

- [ ] "Kitap Notu", "Makale Ozeti", "Tarif" gibi not sablonlari
- [ ] Sablon sectikten sonra markdown iskelet doldurulur

## Kabul Kriterleri

- Not alani formda belirgin ve davetkar
- Placeholder kullaniciyi not yazmaya yonlendiriyor
- Markdown onizleme calisiyor
- Not iceren bookmark'lar listede ayirt edilebilir
