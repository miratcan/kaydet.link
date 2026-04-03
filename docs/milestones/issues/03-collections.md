# Issue #3: Koleksiyonlar (Collections)

**Oncelik:** Yuksek
**Efor:** Orta
**Milestone:** Kisisel Uygulama Deneyimi
**Labels:** `enhancement`, `feature`, `high-priority`

## Ozet

Kullanicilara kendi koleksiyonlarini olusturma imkani ver: "Tasarim Ilhamlari", "Django Kaynaklari", "Yemek Tarifleri" gibi. Tag'ler kesfif icin, koleksiyonlar kisisel organizasyon icin.

## Mevcut Durum

- Sadece tag sistemi var (duz, kesfif odakli)
- Tag'ler "herkesin etiketledigi seyler" hissi veriyor
- Kisisel organizasyon araci yok

## Yapilacaklar

### Model

- [ ] `Collection` modeli olustur:
  - `name` (CharField, max 100)
  - `slug` (SlugField, unique per user)
  - `description` (TextField, blank=True)
  - `cover_image` (URLField, blank=True, opsiyonel)
  - `user` (ForeignKey to User)
  - `is_private` (BooleanField, default=True)
  - `position` (IntegerField, siralama icin)
  - `created_at`, `updated_at`
- [ ] `Bookmark` modeline `collections` (ManyToManyField, blank=True) ekle
- [ ] Migration olustur

### View'lar

- [ ] `CollectionListView` — Kullanicinin tum koleksiyonlari (`/me/collections/`)
- [ ] `CollectionDetailView` — Koleksiyon icindeki bookmark'lar (`/collections/<slug>/`)
- [ ] `CollectionCreateView` — Yeni koleksiyon olustur
- [ ] `CollectionEditView` — Koleksiyon duzenle
- [ ] `CollectionDeleteView` — Koleksiyon sil

### Bookmark entegrasyonu

- [ ] Bookmark olusturma/duzenleme formuna koleksiyon secici ekle
- [ ] Link detay sayfasinda "koleksiyona ekle" butonu
- [ ] Koleksiyon icinde bookmark siralama (drag & drop veya manuel pozisyon)

### Paylasim

- [ ] Koleksiyonlar varsayilan ozel, istege bagli paylasim linki
- [ ] Acik koleksiyonlar icin public URL: `/user/<username>/collections/<slug>/`

## Kabul Kriterleri

- Kullanici koleksiyon olusturabilir, duzenleyebilir, silebilir
- Bir bookmark birden fazla koleksiyona eklenebilir
- Koleksiyonlar varsayilan ozel, istege bagli acik
- Dashboard'da koleksiyonlara hizli erisim var
- Koleksiyon sayfasinda bookmark'lar listelenebilir ve siralanabilir
