def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_complaint(client):
    payload = {
        "productName": "Test Product",
        "complaintDescription": "Test issue description"
    }
    response = client.post("/api/complaints", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["productName"] == "Test Product"
    assert data["complaintDescription"] == "Test issue description"
    assert data["id"].startswith("CC-")


def test_create_complaint_missing_required(client):
    payload = {
        "productName": "",
        "complaintDescription": "Test issue description"
    }
    response = client.post("/api/complaints", json=payload)
    assert response.status_code == 422


def test_get_complaint(client):
    payload = {
        "productName": "Product B",
        "complaintDescription": "Missing tablet."
    }
    create_res = client.post("/api/complaints", json=payload)
    complaint_id = create_res.json()["id"]

    response = client.get(f"/api/complaints/{complaint_id}")
    assert response.status_code == 200
    assert response.json()["id"] == complaint_id


def test_list_complaints(client):
    payload1 = {"productName": "Product A", "complaintDescription": "Issue A"}
    payload2 = {"productName": "Product B", "complaintDescription": "Issue B"}
    client.post("/api/complaints", json=payload1)
    client.post("/api/complaints", json=payload2)

    response = client.get("/api/complaints")
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_partial_update_complaint(client):
    payload = {
        "productName": "Product C",
        "complaintDescription": "Wrong color"
    }
    create_res = client.post("/api/complaints", json=payload)
    complaint_id = create_res.json()["id"]

    update_payload = {
        "batchNumber": "B-12345"
    }
    response = client.patch(f"/api/complaints/{complaint_id}", json=update_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["batchNumber"] == "B-12345"
    assert data["productName"] == "Product C"  # Original field preserved


def test_delete_complaint(client):
    payload = {
        "productName": "Product D",
        "complaintDescription": "Broken seal"
    }
    create_res = client.post("/api/complaints", json=payload)
    complaint_id = create_res.json()["id"]

    del_res = client.delete(f"/api/complaints/{complaint_id}")
    assert del_res.status_code == 204

    get_res = client.get(f"/api/complaints/{complaint_id}")
    assert get_res.status_code == 404


def test_dashboard_stats(client):
    payload = {
        "productName": "Product E",
        "complaintDescription": "Stat test"
    }
    client.post("/api/complaints", json=payload)

    response = client.get("/api/complaints/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_complaints" in data
    assert data["total_complaints"] >= 1
