from api.authentication.token import create_access_token, validate_token
# import asyncio


def test_create_access_token(mock_datetime_utcnow, user_data, expected_token):
    token = create_access_token(user_data)
    assert token == expected_token


# def test_validate_correct_token(mock_supabase, expected_token, user_data):
#     user = asyncio.run(validate_token(expected_token))
#     assert user.id == 420