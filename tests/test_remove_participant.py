import pytest


def test_remove_participant_deletes_from_activity(client, reset_activities):
    """
    Test DELETE /activities/{activity_name}/participants/{email} removes student
    
    AAA Pattern:
    - Arrange: Identify existing participant
    - Act: Make DELETE request
    - Assert: Verify participant removed from list
    """
    # Arrange
    activity_name = "Chess Club"
    email_to_remove = "michael@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email_to_remove}")
    
    # Assert
    assert response.status_code == 200
    assert email_to_remove not in reset_activities[activity_name]["participants"]


def test_remove_participant_returns_success_message(client, reset_activities):
    """
    Test DELETE /activities/{activity_name}/participants/{email} returns message
    
    AAA Pattern:
    - Arrange: Setup participant to remove
    - Act: Make DELETE request
    - Assert: Verify success message
    """
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Removed" in data["message"]
    assert email in data["message"]


def test_remove_nonexistent_participant_returns_400(client, reset_activities):
    """
    Test DELETE /activities/{activity_name}/participants/{email} for non-registered student
    
    AAA Pattern:
    - Arrange: Identify email not in activity
    - Act: Attempt to remove non-registered student
    - Assert: Verify 400 error is returned
    """
    # Arrange
    activity_name = "Chess Club"
    non_participant_email = "nothere@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{non_participant_email}")
    
    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_remove_participant_from_nonexistent_activity_returns_404(client, reset_activities):
    """
    Test DELETE /activities/{activity_name}/participants/{email} with invalid activity
    
    AAA Pattern:
    - Arrange: Prepare non-existent activity
    - Act: Attempt delete from invalid activity
    - Assert: Verify 404 error
    """
    # Arrange
    activity_name = "Fake Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_remove_participant_decreases_count(client, reset_activities):
    """
    Test DELETE /activities/{activity_name}/participants/{email} decrements count
    
    AAA Pattern:
    - Arrange: Get count before removal
    - Act: Remove a participant
    - Assert: Verify count decreased by 1
    """
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"
    count_before = len(reset_activities[activity_name]["participants"])
    
    # Act
    client.delete(f"/activities/{activity_name}/participants/{email}")
    
    # Assert
    count_after = len(reset_activities[activity_name]["participants"])
    assert count_after == count_before - 1
