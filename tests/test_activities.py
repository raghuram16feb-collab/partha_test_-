import pytest


def test_get_all_activities_returns_dict(client, reset_activities):
    """
    Test GET /activities endpoint returns all activities
    
    AAA Pattern:
    - Arrange: Setup complete (via fixture)
    - Act: Make GET request
    - Assert: Verify response contains activities
    """
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_get_activities_returns_correct_structure(client, reset_activities):
    """
    Test GET /activities returns correct structure with all fields
    
    AAA Pattern:
    - Arrange: Setup complete (via fixture)
    - Act: Make GET request
    - Assert: Verify structure has required fields
    """
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    activity = data["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_get_activities_participant_count_is_accurate(client, reset_activities):
    """
    Test GET /activities shows correct participant count
    
    AAA Pattern:
    - Arrange: Reset activities with known participants
    - Act: Get activities
    - Assert: Verify participant counts match
    """
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert len(data["Chess Club"]["participants"]) == 2
    assert len(data["Programming Class"]["participants"]) == 1
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]
    assert "emma@mergington.edu" in data["Programming Class"]["participants"]
