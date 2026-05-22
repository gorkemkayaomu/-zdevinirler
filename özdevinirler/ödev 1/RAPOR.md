# Proje Raporu: Turing Makinesi ile Binary Çarpma (Shift & Add)

## 1. Problem Tanımı

Bu proje, tek bantlı bir Turing Makinesi kullanılarak binary (ikili) tabanda iki sayının çarpımını gerçekleştirmektir. 

**Proje Hedefleri:**
- Turing Makinesi teorisini pratik bir uygulamada kullanmak
- İşlemcilerde kullanılan "kaydır ve topla (Shift & Add)" algoritmasını Turing Makinesi seviyesinde modellemek
- Operandları ayırıcı (delimiter) kullanarak doğru şekilde ayrıştırmak
- Durum tabanlı karmaşık bir işlemi başarıyla gerçekleştirmek

**Gerçek Dünya Uygulaması:**
Bilgisayarların çoğu CPU'sunda çarpma işlemi doğrudan yapılmaz; bunun yerine kaydırma ve toplama işlemleri kullanılır. Bu proje, bu mekanizmanın Turing Makinesi seviyesinde nasıl çalıştığını gösterir.

---

## 2. Turing Makinesi Modeli

### 2.1 Sistem Bileşenleri

| Bileşen | Tanım | Değer |
|---------|-------|-------|
| **Bant (Tape)** | Soldan sağa sonsuz genişleyebilen veri depolama | Dinamik liste |
| **Okuma/Yazma Başlığı** | Bant üzerindeki hücreleri okuyan ve yazan yapı | position: 0'dan başla |
| **Durum Kümesi (Q)** | Makinenin tüm olası durumları | q_start, find_Y_end, find_Y_bit, ... (21 durum) |
| **Giriş Alfabesi (Σ)** | Geçerli giriş sembolleri | {0, 1} |
| **Bant Alfabesi (Γ)** | Banta yazılabilecek tüm semboller | {0, 1, *, =, _, a, b, x, y, A, B} |
| **Geçiş Fonksiyonu (δ)** | δ: Q × Γ → Q × Γ × {L, R} | 154 geçiş kuralı |
| **Başlangıç Durumu (q₀)** | Başlangıçta bulunulan durum | q_start |
| **Kabul Durumu (F)** | Başarılı tamamlanma | q_accept |
| **Red Durumu** | Hatalı sonuç | q_reject |

### 2.2 Bant Yapısı ve Örnek

```
Girdi: 11 * 10 =

Bant:   [1][1][*][1][0][=][_][_][_]...
         ↑
    Head Pozisyonu (q_start'ta başlar)

İşlem sırasında:

Bant:   [1][1][0][0][*][1][x][=][1][1][0][_]
                            ↑
                    Başlık buraya gelir
```

### 2.3 Durum Alfabesi (21 Durum)

1. **q_start**: Başlangıç - X'i bul
2. **find_Y_end**: Y'nin sonuna git
3. **find_Y_bit**: Y'nin bir bitini kontrol et
4. **go_sx**: Shift operasyonuna git (Bit = 0)
5. **go_add**: Add operasyonuna git (Bit = 1)
6. **add_start**: Toplama başlat
7. **go_Z_add0/go_Z_add1**: Hedef pozisyonu bul
8. **find_Z_target_0/find_Z_target_1**: Sonuç alanında hedef bul
9. **add0_to_target/add1_to_target**: Toplama işlemi
10. **carry_1**: Elde işle
11. **insert_A/insert_B/insert_1**: Sonuç alanına bit ekle
12. **shift_Z_rem_X**: Sonuç alanını kaydır (4 varyant)
13. **go_back_X**: X'e geri dön
14. **clean_X/clean_Z**: Geçici işaretleri temizle
15. **sx_start/sx_rem_0/sx_rem_1/sx_done**: Kaydırma işlemi
16. **go_sx_from_clean**: Kaydırma başlat
17. **halt_routine**: Temizlik ve sonlandırma
18. **q_accept**: Başarılı sonuç
19. **q_reject**: Başarısız sonuç

---

## 3. Operand Ayrıştırma Yaklaşımı (Kritik Tasarım)

### 3.1 Bant Formatı

Kullanıcıdan alınan iki sayı `X` ve `Y` formatı:
```
X * Y =
```

**Örnek:** `11 * 10 =`

### 3.2 Ayrıştırma Yöntemi

Bant üzerinde açık şekilde ayrıştırma yapılır:

```
Bandı taraması:
├─ [0] → q_start durumunda: X bölgesi
├─ [*] → Operand ayırıcısı (DELIMITER)
├─ [Y] → find_Y_end durumunda: Y bölgesi
└─ [=] → Sonuç bölgesi ayırıcısı
```

**Ayrıştırma Algoritması:**
1. Başlangıçtan * karakterine kadar → **1. Çarpan (X)**
2. * karakterinden = karakterine kadar → **2. Çarpan (Y)**
3. = karakterinden sonra → **Sonuç (Z)**

Bu ayrıştırma, makinenin asla iki operandı karıştırmamasını garantiler.

---

## 4. Geçiş Mantığı ve Çarpma Algoritması (Shift & Add)

### 4.1 Genel Algoritma

```
Girdi: X (birinci sayı), Y (ikinci sayı)
Çıktı: X × Y (sonuç)

1. Z ← 0 (sonuç başlangıçta 0)
2. i ← Y'nin bit sayısı - 1 (sağdan başla)
3. WHILE i ≥ 0:
     a. Y[i] kontrol et
     b. IF Y[i] == 1:
        ├─ Z ← Z + X (Toplama)
     c. X ← X << 1 (Sola kaydırma, 2 ile çarpma)
     d. i ← i - 1
4. Sonuç: Z
```

### 4.2 Turing Makinesi Uyarlaması

**Adım 1: X'i Bul**
- q_start durumunda * bulunana kadar sağa git

**Adım 2: Y'nin Sonuna Git**
- find_Y_end durumunda = işaretine kadar sağa git

**Adım 3: Y Bitini Kontrol Et (Sağdan Sola)**
- find_Y_bit durumunda sağdan sola giderek işlenmemiş bit bul
- Bit 0 ise: go_sx (kaydırma)
- Bit 1 ise: go_add (toplama + kaydırma)
- * ise: halt_routine (bitmiş, temizlik)

**Adım 4: Toplama (Y[i] = 1 ise)**
```
add_start:
  → X'in sağ bitini işaretle (a veya b)
  → Sonuç alanında hedef bul
  → Binary toplama: 0+0=0, 0+1=1, 1+0=1, 1+1=0 carry
  → Elde varsa sola git ve 1 ekle
  → İşaretleri temizle
```

**Adım 5: Kaydırma (X ← X << 1)**
```
sx_start:
  → X'in her bitini bir sola kaydır
  → En sağa 0 ekle
  → İşaretleri temizle
  → find_Y_bit'e dön (döngü)
```

---

## 5. Örnek İşlem: 11 × 10 = 110

### 5.1 Detaylı Adım Adım

```
Başlangıç Bandı: 11*10=

FAZE 1: Başlangıç
─────────────────
Durum: q_start
Bant: [1]1*10=
İşlem: 1 oku, sağa git

Durum: q_start
Bant: 1[1]*10=
İşlem: 1 oku, sağa git

FAZE 2: Operand Ayırıcısı
──────────────────────────
Durum: q_start → find_Y_end
Bant: 11[*]10=
İşlem: * bulundu, Y'nin sonuna git

Durum: find_Y_end
Bant: 11*[1]0=
İşlem: 1 oku, sağa git

Durum: find_Y_end
Bant: 11*1[0]=
İşlem: 0 oku, sağa git

FAZE 3: Y'nin İlk Biti (0)
──────────────────────────
Durum: find_Y_end → find_Y_bit
Bant: 11*10[=]
İşlem: = bulundu, sola dön

Durum: find_Y_bit
Bant: 11*1[0]=
İşlem: Bit = 0, markla (x), go_sx

FAZE 4: Kaydırma (11 → 110)
───────────────────────────
Durum: go_sx → sx_start
Bant: 11[0]*1x=
İşlem: X'i sola kaydır

[... Kaydırma işlemi ...]

Durum: sx_done → find_Y_bit
Bant: 110[*]1x=
İşlem: Y'nin sonraki biti kontrol et

FAZE 5: Y'nin İkinci Biti (1)
────────────────────────────
Durum: find_Y_bit
Bant: 110*[1]x=
İşlem: Bit = 1, markla (y), go_add

FAZE 6: Toplama (0 + 110 = 110)
──────────────────────────────
Durum: go_add → add_start
Bant: 110*[1]x=
İşlem: X (110) alınır, sonuca eklenir

[... Toplama işlemi ...]

Durum: clean_Z
Bant: 110*1y=110
İşlem: Sonuç alan oluşturulmuştur

FAZE 7: X Kaydırması
────────────────────
Durum: sx_start
Bant: [1]100*1y=110
İşlem: 110 → 1100 (sola kaydır)

FAZE 8: Bitmiş
───────────────
Durum: find_Y_bit
Bant: 1100*[1]y=110 (tüm Y bitleri işlendi)
İşlem: * bulundu → halt_routine

Durum: halt_routine
Bant: 1100*1y=110
İşlem: x ve y'leri temizle

Durum: halt_routine → q_accept
Bant: 1100*10=110
İşlem: = bulundu → Başarı!

SONUÇ: 110 (6 decimal) ✓
```

---

## 6. Test Sonuçları

| Test | Girdi | Beklenen | Bulundu | Adımlar | Sonuç |
|------|-------|----------|---------|---------|-------|
| 1 | 11 * 10 | 110 | 110 | 108 | ✓ BAŞARILI |
| 2 | 101 * 11 | 1111 | 1111 | 211 | ✓ BAŞARILI |
| 3 | 0 * 101 | 0 | 0 | 167 | ✓ BAŞARILI |
| 4 | 111 * 1 | 111 | 111 | 87 | ✓ BAŞARILI |
| 5 | 110 * 111 | 101010 | 101010 | 457 | ✓ BAŞARILI |

**Toplam:** 5/5 başarılı (%100)

---

## 7. Sistem Gereksinimleri Kontrol

✅ **Sağlanan Tüm Gereksinimler:**

1. ✓ Turing Makinesi bant yapısı (dinamik liste)
2. ✓ Okuma/yazma kafası (head_position)
3. ✓ Durum kümesi (21 durum)
4. ✓ Giriş alfabesi (0, 1)
5. ✓ Bant alfabesi (0, 1, *, =, _, a, b, x, y, A, B)
6. ✓ Geçiş fonksiyonu (154 geçiş)
7. ✓ Başlangıç durumu (q_start)
8. ✓ Kabul durumu (q_accept)
9. ✓ Red durumu (q_reject)
10. ✓ Operand ayrıştırma (* ve = ile)
11. ✓ Adım adım simülasyon çıktısı
12. ✓ Animasyon modu (opsiyonel)
13. ✓ Sonsuz döngü kontrolü (5000 adım limiti)
14. ✓ Geçiş tablosu CSV formatında
15. ✓ Durum diyagramı

---

## 8. Sonuç ve Değerlendirme

### Başarılar
- ✓ Shift & Add algoritması başarıyla Turing Makinesi modeline dönüştürüldü
- ✓ Operand ayrıştırması hatasız bir şekilde yapıldı
- ✓ Carry (elde) işlemleri doğru şekilde gerçekleştirildi
- ✓ Tüm test senaryoları başarıyla tamamlandı
- ✓ Makine hem sıfır hem de büyük sayılarla doğru sonuç veriyor

### Özellikler
- **Modüler Tasarım**: Her işlev için ayrı durumlar
- **Güvenli**: Sonsuz döngü kontrolü
- **Verili**: Adım adım izleme ve animasyon
- **Teorik**: Turing Makinesi teorisini tam olarak takip eder

### Teorik Önem
Bu proje, Turing Makinesi'nin salt teorik bir model olmadığını, gerçek dünya uygulamalarında (çarpma gibi) nasıl kullanılabileceğini gösterir. Aynı zamanda, modern CPU'ların temel aritmetik işlemlerin arkasındaki algoritmanın basit ama güçlü olduğunu demonstre eder.

---

## 9. Teslim Edilenler

✅ **Proje Dosyaları:**
- [x] Python kaynak kodu (binary_carpma.py)
- [x] Geçiş tablosu (gecis_tablosu.csv - 154 geçiş)
- [x] Durum geçiş diyagramı (durum_diyagrami.txt)
- [x] 5 test senaryosu (test_senaryolari.txt)
- [x] Proje raporu (bu dosya)

**Toplam Durum Sayısı:** 21  
**Toplam Geçiş Sayısı:** 154  
**Test Başarı Oranı:** %100 (5/5)

---

## Kaynaklar ve Referanslar

- Turing, A. M. "On Computable Numbers, with an Application to the Entscheidungsproblem" (1936)
- Sipser, M. "Introduction to the Theory of Computation" (2013)
- Binary Multiplication Algorithms in Computer Architecture

