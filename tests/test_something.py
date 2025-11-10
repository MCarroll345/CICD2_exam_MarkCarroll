def test_add_customer(client):
    client.post("/api/customers", json = {{"name": "string","email": "string","customer_since": 2000})
    r=client.get("/api/customers/1")
    assert r.status_code == 200

def test_put_customer(client):
    client.post("/api/customers", json = {{"name": "string","email": "string","customer_since": 2000})
    r=client.put("/api/customers/1", json = {{"name": "Put","email": "string","customer_since": 2000})
    assert r.status_code == 200

def test_patch_customer(client):
    client.post("/api/customers", json = {{"name": "string","email": "string","customer_since": 2000})
    r=client.patch("/api/customers/1", json = {{"name": "Patch"})
    assert r.status_code == 200

def test_add_order(client):
    r=client.post("/api/orders", json = {"order_number": 0,"total_cents": 0,"customer_id": 0})
    assert r.status_code == 200