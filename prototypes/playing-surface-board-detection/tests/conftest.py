import pytest
import cv2

@pytest.fixture
def mock_board():
    yield cv2.imread("tests/assets/composite.jpg")