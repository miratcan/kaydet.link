# Issue #9: Pin / Sabitle

**Oncelik:** Dusuk
**Efor:** Cok Dusuk
**Milestone:** Kisisel Uygulama Deneyimi
**Labels:** `enhancement`, `feature`, `low-priority`

## Ozet

En onemli 5-10 bookmark'u sabitleyerek dashboard'da her zaman ustte goster. Hizli referans araci.

## Mevcut Durum

- Tum bookmark'lar kronolojik sirali
- Sik kullanilan linklere hizli erisim yok

## Yapilacaklar

### Model

- [ ] `Bookmark` modeline `is_pinned = BooleanField(default=False)` ekle
- [ ] `pinned_at = DateTimeField(null=True, blank=True)` ekle (siralama icin)
- [ ] Migration olustur
- [ ] Pin limiti: maksimum 10 sabitleme (model seviyesinde validation)

### UI

- [ ] Bookmark kartinda "sabitle/kaldir" butonu (HTMX ile)
- [ ] Dashboard'da "Sabitlenenler" bolumu — en ustte
- [ ] Sabitlenmis bookmark'larda gorsel gosterge (pin ikonu)

### View

- [ ] `toggle_pin` endpoint'i (HTMX POST)
- [ ] Pin limiti asildiysa kullaniciya uyari

## Kabul Kriterleri

- Kullanici tek tikla bookmark sabitleyebilir/kaldirir
- Sabitlenen bookmark'lar dashboard'da en ustte gorunur
- Maksimum 10 sabitleme limiti var
