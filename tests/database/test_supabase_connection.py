import pytest

from api.handlers.http_exceptions import ResourceNotFound, InternalServerError


def test_supabase_connection_init(mocked_supabase_connection_wrong_credentials):
    with pytest.raises(ConnectionRefusedError):
        mocked_supabase_connection_wrong_credentials()


def test_supabase_connection_runtime_error(broken_supabase_connection):
    with pytest.raises(InternalServerError):
        broken_supabase_connection.fetch_all("fake_table")


data = {"fake_data": "dummy_value"}
bulk_data = [{"fake_data": "dummy_value"}, {"fake_data": "dummy_value2"}]
# owilms 06-10-2025: add bulk_data for tests with multiple rows


@pytest.mark.parametrize("input_data", [data])
def test_supabase_connection_fetch_all(mocked_supabase_connection):
    result = mocked_supabase_connection.fetch_all("fake_table")

    assert result == data


@pytest.mark.parametrize("input_data", [None])
def test_supabase_connection_fetch_all_error(mocked_supabase_connection):
    with pytest.raises(ResourceNotFound):
        mocked_supabase_connection.fetch_all("fake_table")


@pytest.mark.parametrize("input_data", [[data]])
def test_supabase_connection_insert(mocked_supabase_connection):
    result = mocked_supabase_connection.insert("fake_table", data)

    assert result == data


@pytest.mark.parametrize("input_data", [None])
def test_supabase_connection_insert_error(mocked_supabase_connection):
    with pytest.raises(ResourceNotFound):
        mocked_supabase_connection.insert("fake_table", data)


# owilms 06-10-2025 start: Create tests for bulk_insert (based on insert tests)


@pytest.mark.parametrize("input_data", [bulk_data])
def test_supabase_connection_bulk_insert(mocked_supabase_connection, input_data):
    result = mocked_supabase_connection.bulk_insert("fake_table", input_data)

    assert result == input_data


@pytest.mark.parametrize("input_data", [None])
def test_supabase_connection_bulk_insert_error(mocked_supabase_connection):
    with pytest.raises(ResourceNotFound):
        mocked_supabase_connection.bulk_insert("fake_table", data)


# owilms 06-10-2025 end


@pytest.mark.parametrize("input_data", [data])
def test_supabase_connection_find_by(mocked_supabase_connection):
    result = mocked_supabase_connection.find_by("fake_table", "column", "value")

    assert result == data


@pytest.mark.parametrize("input_data", [None])
def test_supabase_connection_find_by_error(mocked_supabase_connection):
    with pytest.raises(ResourceNotFound):
        mocked_supabase_connection.find_by("fake_table", "column", "value")


@pytest.mark.parametrize("input_data", [[data]])
def test_supabase_connection_find_join_record(mocked_supabase_connection):
    result = mocked_supabase_connection.find_join_record(
        "fake_table", "fst_col", "fst_val", "2nd_col", "2nd_val"
    )

    assert result == data


@pytest.mark.parametrize("input_data", [None])
def test_supabase_connection_find_join_record_error(mocked_supabase_connection):
    with pytest.raises(ResourceNotFound):
        mocked_supabase_connection.find_join_record(
            "fake_table", "fst_col", "fst_val", "2nd_col", "2nd_val"
        )


@pytest.mark.parametrize("input_data", [data])
def test_supabase_connection_find_ilike(mocked_supabase_connection):
    result = mocked_supabase_connection.find_ilike("fake_table", "column", "value")

    assert result == data


@pytest.mark.parametrize("input_data", [None])
def test_supabase_connection_find_ilike_error(mocked_supabase_connection):
    with pytest.raises(ResourceNotFound):
        mocked_supabase_connection.find_ilike("fake_table", "column", "value")


@pytest.mark.parametrize("input_data", [[data]])
def test_supabase_connection_delete_by(mocked_supabase_connection):
    result = mocked_supabase_connection.delete_by("fake_table", "column", "value")

    assert result == data


@pytest.mark.parametrize("input_data", [None])
def test_supabase_connection_delete_by_error(mocked_supabase_connection):
    with pytest.raises(ResourceNotFound):
        mocked_supabase_connection.delete_by("fake_table", "column", "value")


@pytest.mark.parametrize("input_data", [[data]])
def test_supabase_connection_delete_join_record(mocked_supabase_connection):
    result = mocked_supabase_connection.delete_join_record(
        "fake_table", "fst_col", "fst_val", "2nd_col", "2nd_val"
    )

    assert result == data


@pytest.mark.parametrize("input_data", [None])
def test_supabase_connection_delete_join_record_error(mocked_supabase_connection):
    with pytest.raises(ResourceNotFound):
        mocked_supabase_connection.delete_join_record(
            "fake_table", "fst_col", "fst_val", "2nd_col", "2nd_val"
        )


@pytest.mark.parametrize("input_data", [[data]])
def test_supabase_connection_update_by(mocked_supabase_connection):
    result = mocked_supabase_connection.update_by("fake_table", "column", "value", data)

    assert result == data


@pytest.mark.parametrize("input_data", [None])
def test_supabase_connection_update_by_error(mocked_supabase_connection):
    with pytest.raises(ResourceNotFound):
        mocked_supabase_connection.update_by("fake_table", "column", "value", data)
