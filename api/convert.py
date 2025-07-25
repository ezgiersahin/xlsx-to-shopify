import pandas as pd
import io
from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/api/convert")
async def convert_excel(file: UploadFile):
    contents = await file.read()
    df = pd.read_excel(io.BytesIO(contents))
    df.columns = df.columns.str.strip()

    df["price1"] = df["price1"].astype(str).str.replace(",", ".").astype(float)
    df["price2"] = df["price2"].astype(str).str.replace(",", ".").astype(float)

    shopify_df = pd.DataFrame()
    shopify_df["Handle"] = df["Ürün Başlığı"].str.lower().str.replace(" ", "-")
    shopify_df["Title"] = df["Ürün Başlığı"]
    shopify_df["Body (HTML)"] = df["Ürün Açıklaması"]
    shopify_df["Vendor"] = df["brand"]
    shopify_df["Type"] = df["category"]
    shopify_df["Tags"] = ""
    shopify_df["Published"] = "TRUE"
    shopify_df["Option1 Name"] = df["variantName1"].fillna("Başlık")
    shopify_df["Option1 Value"] = df["variantValue1"].fillna(df["Ürün Başlığı"])
    shopify_df["Variant SKU"] = df["stockCode"]
    shopify_df["Variant Grams"] = 0
    shopify_df["Variant Inventory Tracker"] = "shopify"
    shopify_df["Variant Inventory Qty"] = df["stockAmount"]
    shopify_df["Variant Inventory Policy"] = "deny"
    shopify_df["Variant Fulfillment Service"] = "manual"
    shopify_df["Variant Price"] = df["price1"]
    shopify_df["Variant Compare At Price"] = df["price2"]
    shopify_df["Variant Requires Shipping"] = "TRUE"
    shopify_df["Variant Taxable"] = "TRUE"
    shopify_df["Image Src"] = df["picture1Path"]

    stream = io.StringIO()
    shopify_df.to_csv(stream, index=False)
    stream.seek(0)
    return StreamingResponse(iter([stream.read()]), media_type="text/csv")
