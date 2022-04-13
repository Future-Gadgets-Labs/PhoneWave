from app.utilities.nick import extract_lab_member_number, LabMember


def test_invalid_inputs():
    assert extract_lab_member_number("") == LabMember(name=None, lab_member_number=None)
    assert extract_lab_member_number("    ") == LabMember(name=None, lab_member_number=None)
    assert extract_lab_member_number(" \t \r \n ") == LabMember(name=None, lab_member_number=None)


def test_name_only():
    assert extract_lab_member_number("Test") == LabMember(name="Test", lab_member_number=None)
    assert extract_lab_member_number(" Test ") == LabMember(name="Test", lab_member_number=None)


def test_number_only():
    assert extract_lab_member_number("[1]") == LabMember(name=None, lab_member_number=1)
    assert extract_lab_member_number("[1] [2]") == LabMember(name=None, lab_member_number=1)


def test_number_then_name():
    assert extract_lab_member_number("[1]Test") == LabMember(name="Test", lab_member_number=1)
    assert extract_lab_member_number("[1] Test") == LabMember(name="Test", lab_member_number=1)
    assert extract_lab_member_number("[001]Test") == LabMember(name="Test", lab_member_number=1)
    assert extract_lab_member_number("[1111111111]Test") == LabMember(name="Test", lab_member_number=1111111111)


def test_name_then_number():
    assert extract_lab_member_number("Test[1]") == LabMember(name="Test", lab_member_number=1)
    assert extract_lab_member_number("Test [1]") == LabMember(name="Test", lab_member_number=1)
    assert extract_lab_member_number("Test[001]") == LabMember(name="Test", lab_member_number=1)
    assert extract_lab_member_number("Test[1111111111] ") == LabMember(name="Test", lab_member_number=1111111111)


def test_number_then_name_then_number():
    assert extract_lab_member_number("[1]Test[2]") == LabMember(name="Test", lab_member_number=1)
    assert extract_lab_member_number("[1] Test [2]") == LabMember(name="Test", lab_member_number=1)
    assert extract_lab_member_number("[001]Test [002]") == LabMember(name="Test", lab_member_number=1)
    assert extract_lab_member_number("[1111111111]Test[2222222222]") == LabMember(name="Test", lab_member_number=1111111111)


def test_shurturgal():
    assert extract_lab_member_number("『001』『 Shurturgal 』『002』") == LabMember(name="Shurturgal", lab_member_number=1)
