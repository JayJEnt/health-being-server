from database.models.user import User


def test_post_user(db_session, example_user):
    retrieved_user = db_session.query(User).filter_by(username="testuser").first()

    assert retrieved_user == example_user


def test_delete_user(db_session, example_user):
    user_id = example_user.id
    db_session.delete(example_user)
    db_session.commit()
    
    retrieved_user = db_session.query(User).filter_by(id=user_id).first()

    assert retrieved_user is None