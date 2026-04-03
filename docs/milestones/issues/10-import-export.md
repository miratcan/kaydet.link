# Issue #10: Ice/Disa Aktarma (Import/Export)

**Oncelik:** Dusuk
**Efor:** Orta
**Milestone:** Kisisel Uygulama Deneyimi
**Labels:** `enhancement`, `feature`, `low-priority`

## Ozet

"Verim bende, istedigim zaman cikarim" hissi yarat. Baska platformlardan import ve kaydet.link'ten export imkani sun.

## Mevcut Durum

- Icerik aktarma yok
- Kullanici sifirdan baslamak zorunda — bu yuksek bariyer
- Cikis yolu yok — "buraya kilitlenme" korkusu

## Yapilacaklar

### Export (Disa Aktarma)

- [ ] JSON export: tum bookmark'lar, notlar, tag'ler, koleksiyonlar
- [ ] HTML export: tarayici bookmark formatinda (Netscape Bookmark File Format)
- [ ] CSV export: basit tablo formati
- [ ] Export sayfasi: `/me/export/`
- [ ] Tek tikla indir

### Import (Ice Aktarma)

- [ ] HTML import: Chrome/Firefox/Safari bookmark export dosyasi
- [ ] JSON import: kaydet.link formatinda (kendi export'u)
- [ ] Import sayfasi: `/me/import/`
- [ ] Import sirasinda:
  - Dublike URL kontrolu (zaten varsa atla)
  - Tag eslestirme
  - Ilerleme gostergesi (buyuk dosyalar icin)

### Ucuncu parti import (v2)

- [ ] Pinboard JSON import
- [ ] Raindrop.io CSV import
- [ ] Pocket HTML export import

## Kabul Kriterleri

- Kullanici tum verilerini JSON/HTML/CSV olarak indirebilir
- Chrome/Firefox bookmark dosyasi import edilebilir
- Import sirasinda dublike kontrol yapilir
- Export dosyasi baska bir kaydet.link hesabina import edilebilir
