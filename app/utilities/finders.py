import re

from discord.utils import get as find

from app.types.discord import DiscordGuild, DiscordRole

def find_role(guild: DiscordGuild, role: str) -> DiscordRole|None:
    """Finds a role in a guild given a Snowflake, <@ID> or Name

    Args:
        guild (DiscordGuild): The guild to search in
        role (str): The string to match with

    Returns:
        DiscordRole: The Role
        None: If no role is found
    """
    
    # Find the role from the information given
    match = re.search(r"^\d{15,}$", role)  # Raw Snowflake ID match.
    if match is not None:
        # We have a Snowflake id!
        role = int(match.group(0))

    else:
        match = re.search(r"(?:^<@&(\d{15,})>$)", role)  #
        if match is not None:
            # We have a discord-formatted role id! Group 0 is the snowflake of the role
            role = int(match.group(1))
        else:
            # Check if it's a role's name. If it isn't, the role is None and it doesn't exist
            role = find(guild.roles, name=role)
            if role is not None:
                return role

    return find(guild.roles, id=role)