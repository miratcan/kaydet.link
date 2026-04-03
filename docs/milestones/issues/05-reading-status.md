# Issue #5: Okuma Durumu (Reading Status)

**Oncelik:** Orta
**Efor:** Dusuk
**Milestone:** Kisisel Uygulama Deneyimi
**Labels:** `enhancement`, `feature`

## Ozet

Bookmark'lara basit bir durum ekle: "Okunacak", "Okundu", "Arsiv". Bu, aktif bir todo listesi hissi yaratir ve uygulamaya geri donmek icin somut bir sebep verir.

## Mevcut Durum

- Bookmark'larin hicbir durumu yok
- Kaydettikten sonra uygulamaya geri donmek icin motivasyon yok
- "Sonra oku" ihtiyaci karsilanmiyor

## Yapilacaklar

### Model

- [ ] `Bookmark` modeline `status` alani ekle:
  ```python
  class ReadingStatus(models.TextChoices):
      UNREAD = 'unread', _('Okunacak')
      READ = 'read', _('Okundu')
      ARCHIVED = 'archived', _('Arsiv')
  
  status = CharField(max_length=10, choices=ReadingStatus.choices, default=ReadingStatus.UNREAD)
  ```
- [ ] Migration olustur

### UI

- [ ] Bookmark kartinda durum gostergesi (kucuk ikon veya badge)
- [ ] Tek tikla durum degistirme (HTMX ile sayfa yenilemeden)
- [ ] Dashboard'da "Okunacaklar" bolumu — okunmamis bookmark sayisi ve listesi
- [ ] Filtreleme: sadece okunmamislari / okunmuslari / arsivlenenleri goster

### Toplu islem

- [ ] Birden fazla bookmark'u secip toplu durum degistirme (opsiyonel, v2)

## Kabul Kriterleri

- Yeni bookmark'lar varsayilan "Okunacak" durumuyla olusturulur
- Kullanici tek tikla durumu degistirebilir
- Dashboard'da okunmamis bookmark sayisi gorunur
- Durum bazli filtreleme calisiyor
