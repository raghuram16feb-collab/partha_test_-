import pytest


def test_signup_adds_student_to_activity(client, reset_activities):
    """
    Test POST /activities/{activity_name}/signup adds student to activity
    
    AAA Pattern:
    - Arrange: Setup activities via fixture
    - Act: Make signup request with new email
    - Assert: Verify student appears in participants list
    """
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={new_email}")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"
    assert new_email in reset_activities[activity_name]["participants"]


def test_signup_returns_success_message(client, reset_activities):
    """
    Test POST /activities/{activity_name}/signup returns success message
    
    AAA Pattern:
    - Arrange: Prepare activity name and email
    - Act: Make signup request
    - Assert: Verify response message
    """
    # Arrange
    activity_name = "Gym Class"
    email = "test@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_duplicate_participant_returns_400(client, reset_activities):
    """
    Test POST /activities/{activity_name}/signup rejects duplicate signup
    
    AAA Pattern:
    - Arrange: Identify existing participant
    - Act: Attempt to signup same participant again
    - Assert: Verify 400 error is returned
    """
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={existing_email}")
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity_returns_404(client, reset_activities):
    """
    Test POST /activities/{activity_name}/signup with invalid activity
    
    AAA Pattern:
    - Arrange: Prepare non-existent activity name
    - Act: Make signup request to invalid activity
    - Assert: Verify 404 error is returned
    """
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_increases_participant_count(client, reset_activities):
    """
    Test POST /activities/{activity_name}/signup increments participant count
    
    AAA Pattern:
    - Arrange: Get current count before signup
    - Act: Signup a new student
    - Assert: Verify count increased by 1
    """
    # Arrange
    activity_name = "Programming Class"
    new_email = "fresh@mergington.edu"
    count_before = len(reset_activities[activity_name]["participants"])
    
    # Act
    client.post(f"/activities/{activity_name}/signup?email={new_email}")
    
    # Assert
    count_after = len(reset_activities[activity_name]["participants"])
    assert count_after == count_before + 1
