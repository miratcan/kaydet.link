# Issue #4: Tam Metin Arama

**Oncelik:** Yuksek
**Efor:** Dusuk-Orta
**Milestone:** Kisisel Uygulama Deneyimi
**Labels:** `enhancement`, `feature`, `high-priority`

## Ozet

Kisisel bir arac olarak kaydet.link'in en temel ihtiyaci: "o linki bulabilmek". Header'a kalici bir arama kutusu ekle, bookmark basligi, notu, URL'i ve tag'leri uzerinden arama yap.

## Mevcut Durum

- Hicbir arama fonksiyonu yok
- 50+ kayittan sonra platform kullanilmaz hale geliyor
- Kullanici kaydettigini bulamayinca platforma guvenini kaybediyor

## Yapilacaklar

### Arama altyapisi

- [ ] `SearchView` olustur (`/search/`)
- [ ] Arama sorgusu: Link.metadata title + description, Bookmark.note, Tag.name, Link.url uzerinden
- [ ] Django ORM `Q` objeleri ile basit arama (baslangic icin yeterli)
- [ ] PostgreSQL kullaniliyorsa `SearchVector` / `SearchRank` ile full-text search

### UI

- [ ] Header'a (`base.html`) kalici arama kutusu ekle
- [ ] Arama sonuclari sayfasi — mevcut link kart tasarimiyla
- [ ] Arama sonuclarinda eslesen kelimeleri vurgula (highlight)
- [ ] Bos sonuc durumu: "Hicbir sonuc bulunamadi" mesaji

### Kapsam filtreleri

- [ ] "Sadece benim kayitlarimda ara" (varsayilan, giris yapmis kullanici icin)
- [ ] "Tum platformda ara" (ikincil secenek)
- [ ] Tag'e gore filtrele (arama + tag kombinasyonu)

### Performans

- [ ] Arama sorgularina `select_related` / `prefetch_related` ekle
- [ ] Sonuclari sayfalandir (paginate)
- [ ] Opsiyonel: HTMX ile anlik arama (debounce ile)

## Kabul Kriterleri

- Header'da her sayfada gorunen bir arama kutusu var
- Baslik, not, URL ve tag uzerinden arama yapiyor
- Giris yapmis kullanici varsayilan olarak kendi kayitlarinda ariyor
- Sonuclar sayfalanmis ve performansli
- Bos sonuc durumu duzgun isleniyor
