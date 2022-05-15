import pytest
from conftest import cmu_dict_content
from Aquila_Resolve import dict_reader


# Test Init with Mock Data
def test_init(mock_dict_reader):
    # Test the init function of the DictReader class
    dr = mock_dict_reader
    assert isinstance(dr, dict_reader.DictReader)
    assert len(dr.dict) == (len(cmu_dict_content) - 5)
    r1 = dr.dict["park"]
    assert len(r1) == 1
    assert isinstance(r1, list)
    assert isinstance(r1[0], list)
    assert r1[0] == ["P", "AA1", "R", "K"]


# Test Init with Default
def test_init_default():
    # Test the init function of the DictReader class
    dr = dict_reader.DictReader()
    assert isinstance(dr, dict_reader.DictReader)
    assert len(dr.dict) > 123400
    r1 = dr.dict["park"]
    assert len(r1) == 1
    assert isinstance(r1, list)
    assert isinstance(r1[0], list)
    assert r1[0] == ["P", "AA1", "R", "K"]


# Test Parse Dict
@pytest.mark.parametrize("word, phoneme, index", [
    ("#hash-mark", ['HH', 'AE1', 'M', 'AA2', 'R', 'K'], 0),
    ("park", ['P', 'AA1', 'R', 'K'], 0),
    ("console", ['K', 'AA1', 'N', 'S', 'OW0', 'L'], 0),
    ("console", ['K', 'AH0', 'N', 'S', 'OW1', 'L'], 1),
    ("console(1)", ['K', 'AH0', 'N', 'S', 'OW1', 'L'], 0),
])
def test_parse_dict(mock_dict_reader, word, phoneme, index):
    dr = mock_dict_reader
    assert dr.dict[word][index] == phoneme
