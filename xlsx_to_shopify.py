import pandas as pd

excel_dosyasi = "standart.xlsx"
df = pd.read_excel(excel_dosyasi)

df.columns = df.columns.str.strip()

df["price1"] = df["price1"].astype(str).str.replace(",", ".").astype(float)
df["price2"] = df["price2"].astype(str).str.replace(",", ".").astype(float)
print(df.columns.tolist())

shopify_df = pd.DataFrame()

shopify_df["Handle"] = df["Ürün Başlığı"].str.lower().str.replace(" ", "-")
shopify_df["Title"] = df["Ürün Başlığı"]
shopify_df["Body (HTML)"] = df["Ürün Açıklaması"]
shopify_df["Vendor"] = df["brand"]
shopify_df["Type"] = df["mainCategory"]
shopify_df["Tags"] = df["category"]
shopify_df["Published"] = "TRUE"
shopify_df["Status"] = "active"

shopify_df["Option1 Name"] = df["variantName1"].fillna("Title")
shopify_df["Option1 Value"] = df["variantValue1"].fillna("Default Title")
shopify_df["Variant SKU"] = df["barcode"]
shopify_df["Variant Barcode"] = df["barcode"]
shopify_df["Variant Inventory Qty"] = df["stockAmount"]
shopify_df["Variant Inventory Policy"] = "deny"
shopify_df["Variant Fulfillment Service"] = "manual"
shopify_df["Variant Price"] = df["price1"]
shopify_df["Variant Compare At Price"] = df["price2"]

shopify_df["Variant Requires Shipping"] = "TRUE"
shopify_df["Variant Taxable"] = "TRUE"
shopify_df["Variant Inventory Tracker"] = "shopify"

shopify_df["Variant Weight Unit"] = "kg"
if "weight" in df.columns:
    shopify_df["Variant Grams"] = df["weight"].fillna(0).astype(float) * 1000
else:
    shopify_df["Variant Grams"] = 0


shopify_df["Image Src"] = df["picture1Path"]
shopify_df["Image Position"] = ""

shopify_df.to_csv("shopify-urunler2.csv", index=False)
print("✅ Dönüştürme tamamlandı → shopify-urunler2.csv")
