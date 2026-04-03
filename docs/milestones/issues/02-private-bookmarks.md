# Issue #2: Ozel (Private) Kayitlar

**Oncelik:** Kritik
**Efor:** Dusuk
**Milestone:** Kisisel Uygulama Deneyimi
**Labels:** `enhancement`, `privacy`, `critical`

## Ozet

Kullanicilara bookmark'larini ozel (sadece kendileri gorebilir) olarak kaydetme imkani ver. Kisisel not defterine her seyi yazmak gibi — cesaret etmeden kaydetme bariyerini kaldir.

## Mevcut Durum

- Tum bookmark'lar herkese acik
- Kullanici sadece "gostermeye deger" buldugu linkleri kaydetmeye meyilli
- Bu, kaydetme frekansini dramatik sekilde dusuruyor

## Yapilacaklar

### Model degisiklikleri

- [ ] `Bookmark` modeline `is_private = BooleanField(default=True)` alani ekle
- [ ] Migration olustur
- [ ] Varsayilan deger: `True` (kisisel kullanimi tesvik etmek icin)

### Form degisiklikleri

- [ ] `BookmarkForm` ve `BookmarkEditForm`'a `is_private` checkbox'u ekle
- [ ] UI'da anlasilir sekilde goster: "Sadece ben gorebilirim" toggle/checkbox

### Feed ve profil filtreleme

- [ ] `LinkListView` queryset'inde ozel bookmark'lari filtrele (sadece sahibi gorebilir)
- [ ] `/user/<username>/` profilinde baskalarinin ozel bookmark'larini gizle
- [ ] Tag sayfalarinda ozel bookmark'lari sayma
- [ ] `Link.save_count` hesaplamasinda ozel kayitlari haric tut (veya ayri say)

### Gorsel gosterge

- [ ] Link kartinda ozel kayitlar icin kilit ikonu goster
- [ ] Dashboard'da ozel/acik filtresi

## Kabul Kriterleri

- Kullanici bookmark olustururken "ozel" secebilir
- Ozel bookmark'lar feed'de, tag sayfalarinda ve baska kullanicilarin profilinde gorunmez
- Ozel bookmark'lar sadece sahibinin dashboard/profilinde gorunur
- Ozel bookmark'larda gorsel bir kilit/gizlilik gostergesi vardir
- Varsayilan: ozel (yeni kayitlar icin)
