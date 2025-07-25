import pandas as pd

# Dosyayı oku
df = pd.read_excel("standart.xlsx", sheet_name=0)

# Tüm kolon adlarını yazdır
print("Kolon başlıkları:")
for col in df.columns:
    print(f"'{col}'")