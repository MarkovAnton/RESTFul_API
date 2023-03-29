import requests

res = requests.post("http://127.0.0.1:8080/promo", {"name": "promo1", "description": "Promoation1"})
res = requests.post("http://127.0.0.1:8080/promo", {"name": "promo2", "description": "Promoation2"})
res = requests.get("http://127.0.0.1:8080/promo")
res = requests.get("http://127.0.0.1:8080/promo/1")
res = requests.put("http://127.0.0.1:8080/promo/2", {"name": "promo2_2", "description": "Promoation2_2"})
res = requests.delete("http://127.0.0.1:8080/promo/2")
res = requests.post("http://127.0.0.1:8080/promo/1/participant", {"name": "participant1"})
res = requests.post("http://127.0.0.1:8080/promo/1/participant", {"name": "participant2"})
res = requests.delete("http://127.0.0.1:8080/promo/1/participant/2")
res = requests.post("http://127.0.0.1:8080/promo/1/prize", {"description": "prize1"})
res = requests.post("http://127.0.0.1:8080/promo/1/prize", {"description": "prize2"})
res = requests.delete("http://127.0.0.1:8080/promo/1/prize/2")
res = requests.post("http://127.0.0.1:8080/promo/1/raffle")
print(res.json())

