# pytorch3d kurulumu
pip3 install torch torchvision torchaudio
pip install https://github.com/facebookresearch/pytorch3d/archive/main.zip

# 2D Teknik Çizimden 3D Model Oluşturma Projesi

Bu proje, 2D teknik çizimlerden otomatik olarak 3D modeller oluşturan gelişmiş bir bilgisayarlı görü ve 3D modelleme sistemidir.

## 🎯 Proje Özeti

Sistem, görüntü işleme teknikleri, kontur analizi ve voxel-tabanlı 3D rekonstrüksiyon algoritmalarını kullanarak teknik çizimlerdeki geometrik şekilleri ve delikleri tespit eder, ardından bunları üç boyutlu mesh modellere dönüştürür.

## 🚀 Özellikler

- ✅ **Otomatik Ana Şekil Tespiti**: Hiyerarşi analizi ile doğru kontur seçimi
- ✅ **Delik Tespiti**: İç içe delik yapılarının otomatik tanınması
- ✅ **3D Dönüşüm**: Voxel-tabanlı gerçek 3D model oluşturma
- ✅ **İnteraktif Görselleştirme**: Open3D ile 3D model inceleme
- ✅ **Çoklu Format Desteği**: PNG, JPEG, JPG dosyaları
- ✅ **Debug Modu**: İşlem adımlarının görsel takibi

## 📋 Gereksinimler

```bash
pip install opencv-python
pip install open3d
pip install numpy
pip install scikit-image
pip install reportlab  # Rapor oluşturma için
```

## 🛠️ Kurulum

1. Repoyu klonlayın:
```bash
git clone <repo-url>
cd 2D-to-3D
```

2. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

## 📖 Kullanım

### Temel Kullanım

```python
from technical_drawing_to_3d import TechnicalDrawingTo3D

# 2D teknik çizimi yükle ve 3D'ye dönüştür
converter = TechnicalDrawingTo3D("path/to/your/drawing.png")
mesh = converter.process()
```

### Komut Satırından Çalıştırma

```bash
python technical_drawing_to_3d.py
```

## 🏗️ Sistem Mimarisi

### Ana Bileşenler

| Bileşen | Dosya | Ana Görev |
|---------|-------|-----------|
| `TechnicalDrawingProcessor` | `technical_drawing_processor.py` | Görüntü işleme ve kontur tespiti |
| `TechnicalDrawingTo3D` | `technical_drawing_to_3d.py` | 3D mesh oluşturma ve görselleştirme |

### İş Akışı

```
Görüntü Yükleme → Ön İşleme → Threshold Analizi → Kontur Tespiti → 
Hiyerarşi Analizi → Ana Şekil Seçimi → Delik Tespiti → Voxel Grid → 
Marching Cubes → 3D Mesh → Görselleştirme
```

## 🔬 Teknik Detaylar

### Görüntü İşleme Algoritmaları

- **Çoklu Threshold Analizi**: [50, 100, 127, 150, 200] + Otsu
- **Hiyerarşik Kontur Analizi**: OpenCV RETR_TREE modu
- **Gelişmiş Kontur Seçimi**: Alan oranı + parent-child ilişki analizi

### 3D Rekonstrüksiyon

- **Voxel Grid**: (height, width, 100) boyutunda
- **Marching Cubes**: Level 0.5 ile mesh oluşturma
- **Koordinat Dönüşümü**: Merkeze alma + 200 birim normalizasyon

## 📊 Test Sonuçları

Son test (data_5.png) ile elde edilen sonuçlar:

| Metrik | Değer | Açıklama |
|--------|-------|----------|
| Ana Kontur Alanı | 72,925.5 piksel | Doğru ana şekil seçimi |
| Tespit Edilen Delik | 2 adet | Hiyerarşi analizi başarısı |
| Voxel Oranı | %13.2 material, %86.8 delik | Gerçekçi oran |
| Final Mesh | 183,800 vertex, 363,924 face | Yüksek kaliteli mesh |
| İşlem Süresi | ~3-5 saniye | Hızlı işlem |

## 🐛 Debug Dosyaları

Sistem işlem sırasında debug dosyaları oluşturur:

- `debug_thresh_X_normal.png`: Threshold X ile normal binary
- `debug_thresh_X_inv.png`: Threshold X ile ters binary
- `debug_final_binary.png`: Seçilen en iyi binary
- `debug_final_contours.png`: Ana şekil (yeşil) + delikler (mavi)
- `debug_corrected_mask.png`: Final profil maskesi

## 📈 Geliştirme Süreci

### Çözülen Ana Problemler

1. **Yanlış Kontur Seçimi** → Hiyerarşi analizi + alan oranı kontrolü
2. **Delikler Görünmüyor** → Voxel seviyesinde maskeleme
3. **Boolean İşlemler Çalışmıyor** → Voxel-tabanlı alternatif yaklaşım
4. **Threshold Sorunları** → Çoklu threshold test algoritması

### İteratif Geliştirme

1. **V1**: Basit threshold + temel kontur tespiti
2. **V2**: Paralel çizgi tespiti (sonra kaldırıldı)
3. **V3**: Büyük basitleştirme - sadece kontur analizi
4. **V4**: Hiyerarşik kontur analizi
5. **V5**: Çoklu threshold test sistemi
6. **V6**: Gelişmiş kontur seçim algoritması
7. **Final**: Voxel-tabanlı delik açma sistemi

## 🔮 Gelecek Geliştirmeler

### Kısa Vadeli
- Çoklu görünüm desteği (ön, yan, üst)
- STL, OBJ export özellikleri
- Batch processing

### Orta Vadeli
- Machine Learning tabanlı şekil tanıma
- Teknik çizim standartları desteği
- Ölçü bilgilerinin otomatik çıkarılması

### Uzun Vadeli
- Deep Learning ile tam otomatik rekonstrüksiyon
- Parametrik CAD model oluşturma
- Web tabanlı interface

## 📄 Rapor

Detaylı teknik rapor için `2D_to_3D_Proje_Raporu_YYYYMMDD_HHMM.pdf` dosyasını inceleyiniz.

Rapor oluşturmak için:
```bash
python proje_raporu.py
```

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👨‍💻 Geliştirici

**2D-to-3D Technical Drawing Converter**
- Geliştirilme Tarihi: 2025
- Teknolojiler: Python, OpenCV, Open3D, NumPy, scikit-image

---

## 🎉 Başarı Hikayeleri

> "Kırmızı çizgilerle sahte deliklerden, gerçek voxel-tabanlı deliklere kadar uzanan epik bir geliştirme yolculuğu!" 😄

### Komik Anlar
- İlk versiyonda delikleri kırmızı çizgilerle "işaretliyorduk" 😅
- Boolean işlemler çalışmayınca voxel seviyesinde çözüm bulduk
- %99.5 delik oranından %86.8'e düşürdük (çok daha mantıklı!)

**Sonuç**: Artık gerçek delikleri olan, profesyonel 3D modeller oluşturuyoruz! 🎯

