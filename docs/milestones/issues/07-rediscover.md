# Issue #7: Yeniden Kesfet / Bu Gun Gecmiste

**Oncelik:** Orta
**Efor:** Dusuk
**Milestone:** Kisisel Uygulama Deneyimi
**Labels:** `enhancement`, `engagement`

## Ozet

Kullaniciya eski kayitlarini hatirlatarak arsivle duygusal bag kur. "Arsivim yasiyor" hissi yarat.

## Mevcut Durum

- `/links/random/` endpoint'i var ama tum platformdan rastgele link gosteriyor
- Kullanicinin kendi gecmisiyle etkilesim yok
- Eski kayitlar unutuluyor

## Yapilacaklar

### "Bu gun gecmiste" ozelligi

- [ ] Kullanicinin 1 yil / 6 ay / 3 ay once bugun kaydettigi linkleri sorgula
- [ ] Dashboard'da "Bu gun gecmiste" karti goster (varsa)
- [ ] Yoksa bu bolumu gizle (bos durum yok)

### "Rastgele bir kaydim" ozelligi

- [ ] Mevcut `/links/random/` endpoint'ini kullanicinin kendi kayitlarindan rastgele secmeye cevir (giris yapmissa)
- [ ] Dashboard'da "Unuttugun bir kayit" bolumu
- [ ] Her sayfa yenilemede farkli bir kayit

### E-posta hatirlatma (opsiyonel, v2)

- [ ] Haftalik digest'e "Bu hafta gecmiste" bolumu ekle
- [ ] DigestService'e gecmis kayitlari sorgulama ekle

## Kabul Kriterleri

- Dashboard'da gecmis kayitlardan en az biri gosteriliyor
- Rastgele link ozelligi kullanicinin kendi kayitlarindan seciyor
- Gecmiste kayit yoksa bolum gizleniyor (bos durumda rahatsiz etmiyor)
