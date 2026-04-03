# Issue #8: Tarayici Eklentisi / Bookmarklet

**Oncelik:** Orta
**Efor:** Dusuk
**Milestone:** Kisisel Uygulama Deneyimi
**Labels:** `enhancement`, `feature`

## Ozet

Sayfadayken tek tikla kaydet. Kaydetme surtunmesini minimuma indir. Kisisel araclarda "kaydetme hizi" her seydir.

## Mevcut Durum

- Link kaydetmek icin siteye gidip URL yapistirmak gerekiyor
- Bu, yuksek surtunme yaratiyor ve kaydetme frekansini dusuruyor

## Yapilacaklar

### Bookmarklet (v1 — hizli cozum)

- [ ] JavaScript bookmarklet olustur:
  - Mevcut sayfanin URL'ini alir
  - kaydet.link'in bookmark olusturma sayfasina URL parametresiyle yonlendirir
  - Ornek: `kaydet.link/bookmarks/new/?url=<current_url>`
- [ ] `/bookmarks/new/` view'ini URL parametresini kabul edecek sekilde guncelle
- [ ] URL parametresi varsa otomatik metadata cek
- [ ] Kullanici ayarlarinda/dashboard'da bookmarklet kurulum talimati goster

### Browser Extension (v2 — tam cozum)

- [ ] Chrome/Firefox icin basit extension
- [ ] Sag tik menusunde "kaydet.link'e kaydet"
- [ ] Popup: tag sec, not ekle, koleksiyon sec
- [ ] API endpoint'i gerekli: `POST /api/bookmarks/` (auth token ile)

### API endpoint (extension icin)

- [ ] Token-based authentication (DRF veya basit token)
- [ ] `POST /api/bookmarks/` — bookmark olustur
- [ ] `GET /api/tags/` — mevcut tag'leri listele (autocomplete icin)
- [ ] `GET /api/collections/` — mevcut koleksiyonlari listele

## Kabul Kriterleri

- v1: Bookmarklet tek tikla kaydetme sayfasini aciyor, URL onceden dolu
- v2: Browser extension popup ile hizli kaydetme calisiyor
- Kaydetme sureci 3 tiktan fazla surmemeli
