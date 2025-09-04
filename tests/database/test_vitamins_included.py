def test_post_vitamins_included(mocked_supabase_connection, inject_example_vitamins_included):
    retrieved_vitamins_included = mocked_supabase_connection.find_by(
        "vitamins_included",
        "ingredient_id",
        inject_example_vitamins_included[0]["ingredient_id"]
    )

    assert retrieved_vitamins_included == [inject_example_vitamins_included[0]]


def test_delete_vitamins_included(mocked_supabase_connection, inject_example_vitamins_included):
    assert inject_example_vitamins_included != [inject_example_vitamins_included[1]]

    mocked_supabase_connection.delete_by(
        "vitamins_included",
        "ingredient_id",
        inject_example_vitamins_included[0]["ingredient_id"]
    )

    retrieved_vitamins_included = mocked_supabase_connection.fetch_all("vitamins_included")

    assert retrieved_vitamins_included == [inject_example_vitamins_included[1]]


def test_delete_join_record_vitamins_included(mocked_supabase_connection, inject_example_vitamins_included):
    assert inject_example_vitamins_included != [inject_example_vitamins_included[1]]

    mocked_supabase_connection.delete_join_record(
        "vitamins_included",
        "ingredient_id",
        inject_example_vitamins_included[0]["ingredient_id"],
        "vitamin_id",
        inject_example_vitamins_included[0]["vitamin_id"]
    )

    retrieved_vitamins_included = mocked_supabase_connection.fetch_all("vitamins_included")

    assert retrieved_vitamins_included == [inject_example_vitamins_included[1]]


def test_find_vitamins_included(mocked_supabase_connection, inject_example_vitamins_included):
    retrieved_vitamins_included = mocked_supabase_connection.find_by(
        "vitamins_included",
        "ingredient_id",
        inject_example_vitamins_included[0]["ingredient_id"]
    )

    assert retrieved_vitamins_included == [inject_example_vitamins_included[0]]


def test_find_join_record_vitamins_included(mocked_supabase_connection, inject_example_vitamins_included):
    retrieved_vitamins_included = mocked_supabase_connection.find_join_record(
        "vitamins_included",
        "ingredient_id",
        inject_example_vitamins_included[0]["ingredient_id"],
        "vitamin_id",
        inject_example_vitamins_included[0]["vitamin_id"]
    )

    assert retrieved_vitamins_included == inject_example_vitamins_included[0]