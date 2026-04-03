# Issue #1: Kisisel Dashboard

**Oncelik:** Kritik
**Efor:** Orta
**Milestone:** Kisisel Uygulama Deneyimi
**Labels:** `enhancement`, `ux`, `critical`

## Ozet

Giris yapmis kullaniciyi topluluk feed'i yerine kisisel bir dashboard'a yonlendir. Uygulama acildiginda "benim alanima dustum" hissi yaratilmali.

## Mevcut Durum

- Ana sayfa (`/`) topluluk feed'ini gosteriyor (LinkListView)
- Tek kullanici oldugunda bu sayfa bos ve anlamsiz hissettiriyor
- Kullanicinin kendi kayitlarina erisimi sadece `/user/<username>/` uzerinden

## Yapilacaklar

### `/me/` veya `/dashboard/` sayfasi olustur

- [ ] Yeni `DashboardView` olustur
- [ ] Giris yapmis kullaniciyi ana sayfadan dashboard'a yonlendir
- [ ] Giris yapmamis kullaniciya mevcut landing/feed sayfasini goster

### Dashboard icerigi

- [ ] **Son kayitlarim** — Son 10 bookmark kartla gosterilir
- [ ] **Koleksiyonlarim** — Hizli erisim kartlari (koleksiyonlar ozelligi yapildiktan sonra)
- [ ] **En cok kullandigim tag'ler** — Tag bulutu veya liste
- [ ] **Bu gun gecmiste** — 1 yil once kaydedilen linkler (varsa)
- [ ] **Istatistikler** — Toplam kayit, bu hafta eklenen, en aktif gun

### Teknik detaylar

- Dashboard verileri tek bir view'da `get_context_data` ile toplanabilir
- Performans icin basit queryset'ler yeterli, cache'e gerek yok (baslangicta)
- HTMX ile bolumler lazy-load edilebilir

## Kabul Kriterleri

- Giris yapmis kullanici `/` adresine gittiginde dashboard'u gorur
- Dashboard'da son kayitlar, tag'ler ve basit istatistikler bulunur
- Topluluk feed'ine ayri bir link/sekme ile erisilebilir (`/explore/` veya `/feed/`)
- Sayfa mobilde duzgun gorunur
