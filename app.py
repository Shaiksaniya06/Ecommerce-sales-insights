from flask import Flask, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load dataset
df = pd.read_excel(" data/ecommerce_sales_dataset_with_sales_and_profit.xlsx")
print("file loaded successfully")
print("COLUMNS ARE:")
print(df.columns)
print(df.head())
input("press enter to exit--")




