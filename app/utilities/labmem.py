import re
from typing import NamedTuple

REGEX_EXTRACT_NAME_AND_NUMBER = r"^([\[『](?P<num>\d+)[\]』])?\s*(?P<name>.*?)\s*([\[『](?P<num2>\d+)[\]』])?$"


class LabMember(NamedTuple):
    name: str | None
    lab_member_number: int | None
    
    @staticmethod
    def from_name(name: str) -> "LabMember":
        """Split the username into name and lab member number (if available)."""

        match = re.search(REGEX_EXTRACT_NAME_AND_NUMBER, name.strip())

        name = match.group("name")
        number = match.group("num") or match.group("num2")

        return LabMember(
            name=name if len(name) > 0 else None,
            lab_member_number=int(number) if number else None
        )
