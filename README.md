# RBT.db — Red-Black Tree Key-Value Database Engine

**Algoritma Analizi Projesi — Student 2: Balanced Search Trees**

Kaynak makale: Guibas, L. J., & Sedgewick, R. (1978). *"A Dichromatic Framework for Balanced Trees"*

---

## Red-Black Tree Kuralları

1. Her node RED veya BLACK'tir
2. Root her zaman BLACK'tir
3. Her NIL yaprak BLACK'tir
4. RED bir node'un her iki çocuğu BLACK olmalıdır
5. Her node'dan NIL'e giden tüm yollar eşit sayıda BLACK node içerir (Black-Height)

---

## Karmaşıklık Garantileri

| İşlem   | Zaman Karmaşıklığı |
|---------|--------------------|
| INSERT  | O(log n)           |
| DELETE  | O(log n)           |
| SEARCH  | O(log n)           |
| Alan    | O(n)               |

---

## Proje Yapısı
rbt-db/
├── rbt.py           # Red-Black Tree implementasyonu
├── app.py           # Flask web sunucusu + API
├── test_rbt.py      # Unit testler (13 test, 10k invariant testi dahil)
├── README.md        # Dokümantasyon
└── templates/
└── index.html   # Web görselleştirici

---

## Kurulum ve Çalıştırma

### Gereksinimler
```bash
pip install flask flask-cors pytest
```

### Web Arayüzünü Başlat
```bash
python app.py
# Tarayıcıda aç: http://localhost:5000
```

### Testleri Çalıştır
```bash
python -m pytest test_rbt.py -v
```

---

## CLI Sorgu Dili

| Komut           | Açıklama                  |
|-----------------|---------------------------|
| `SET key value` | Ekle veya güncelle        |
| `GET key`       | Değeri getir              |
| `DEL key`       | Sil                       |
| `KEYS`          | Tüm anahtarları listele   |
| `VERIFY`        | RBT kurallarını kontrol et|
| `CLEAR`         | Veritabanını sıfırla      |

---

## Test Sonuçları
13 passed in 0.10s
✓ 10.000 rastgele ekleme → Black-Height invariant sağlam
✓ O(log n) arama 10.000 node'lu ağaçta doğrulandı
✓ In-order traversal sıralı çıktı veriyor
