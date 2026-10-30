import json
with open("records.json", encoding="utf-8") as f:
    records = json.load(f)
result = records[1]
print(f"书名:{result['name']},价格:{result['price']}")