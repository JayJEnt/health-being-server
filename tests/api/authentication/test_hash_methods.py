from api.authentication.hash_methods import verify_password, hash_password


def test_hash_password(mock_bcrypt, password, hashed_password):
    assert hash_password(password) == hashed_password


def test_verify_correct_password(password, hashed_password):
    assert verify_password(password, hashed_password)


def test_verify_wrong_password(wrong_password, hashed_password):
    assert not verify_password(wrong_password, hashed_password)
