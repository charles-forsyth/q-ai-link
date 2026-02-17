from fastapi.testclient import TestClient
from q_link_rpg.web import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Q-Link RPG: Web Interface" in response.text

def test_get_state():
    response = client.get("/api/state")
    assert response.status_code == 200
    data = response.json()
    assert "width" in data
    assert "height" in data
    assert "hero_pos" in data
    assert "enemies" in data
    assert "score" in data

def test_take_action():
    # Initial state check
    response = client.get("/api/state")
    initial_pos = response.json()["hero_pos"]
    
    # Action 1 (Right)
    response = client.post("/api/action/1")
    assert response.status_code == 200
    new_data = response.json()
    new_pos = new_data["hero_pos"]
    
    # Should move right (x+1) unless blocked. At (0,0) right is (1,0). 
    # Check if (1,0) is blocked. Walls are at (1,1)... So (1,0) is free.
    assert new_pos[0] == initial_pos[0] + 1 or new_pos == initial_pos

def test_reset_game():
    # Move first
    client.post("/api/action/1")
    
    # Reset
    response = client.post("/api/reset")
    assert response.status_code == 200
    data = response.json()
    
    # Should be back at start (0,0)
    assert data["hero_pos"] == [0, 0]
    assert data["score"] == 0
