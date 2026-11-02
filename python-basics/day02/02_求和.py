lst = [{"name": "a", "price": 3},
       {"name": "b", "price": 5},
       {"name": "c", "price": 6},
       {"name": "d", "price": 15}]
total = 0
for i in range(0, len(lst)):
    total += lst[i]["price"]
print(total)

print(sum(lst[k]["price"] for k in range(0, len(lst))))
