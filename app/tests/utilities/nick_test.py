from app.utilities.labmem import LabMember

"""Tests validation of LabMember separator"""

def test_invalid_inputs():
    assert LabMember.from_name("") == LabMember(name=None, lab_member_number=None)
    assert LabMember.from_name("    ") == LabMember(name=None, lab_member_number=None)
    assert LabMember.from_name(" \t \r \n ") == LabMember(name=None, lab_member_number=None)


def test_name_only():
    assert LabMember.from_name("Test") == LabMember(name="Test", lab_member_number=None)
    assert LabMember.from_name(" Test ") == LabMember(name="Test", lab_member_number=None)


def test_number_only():
    assert LabMember.from_name("[1]") == LabMember(name=None, lab_member_number=1)
    assert LabMember.from_name("[1] [2]") == LabMember(name=None, lab_member_number=1)


def test_number_then_name():
    assert LabMember.from_name("[1]Test") == LabMember(name="Test", lab_member_number=1)
    assert LabMember.from_name("[1] Test") == LabMember(name="Test", lab_member_number=1)
    assert LabMember.from_name("[001]Test") == LabMember(name="Test", lab_member_number=1)
    assert LabMember.from_name("[1111111111]Test") == LabMember(name="Test", lab_member_number=1111111111)


def test_name_then_number():
    assert LabMember.from_name("Test[1]") == LabMember(name="Test", lab_member_number=1)
    assert LabMember.from_name("Test [1]") == LabMember(name="Test", lab_member_number=1)
    assert LabMember.from_name("Test[001]") == LabMember(name="Test", lab_member_number=1)
    assert LabMember.from_name("Test[1111111111] ") == LabMember(name="Test", lab_member_number=1111111111)


def test_number_then_name_then_number():
    assert LabMember.from_name("[1]Test[2]") == LabMember(name="Test", lab_member_number=1)
    assert LabMember.from_name("[1] Test [2]") == LabMember(name="Test", lab_member_number=1)
    assert LabMember.from_name("[001]Test [002]") == LabMember(name="Test", lab_member_number=1)
    assert LabMember.from_name("[1111111111]Test[2222222222]") == LabMember(name="Test", lab_member_number=1111111111)


def test_shurturgal():
    assert LabMember.from_name("『001』『 Shurturgal 』『002』") == LabMember(name="『 Shurturgal 』", lab_member_number=1)
