import pytest
import vendor.discord.ext.test as testcord
from vendor.discord.ext.test.backend import make_role

from app.config import config
from app.database.models.rank import Rank

@pytest.mark.asyncio
async def test_create_rank(mock_phonewave):
    """Tests to see if we can create a rank via command"""

    guild = mock_phonewave.guilds[0]
    channel = guild.text_channels[0]

    # Set @everyone to have manage_roles permissions. For some reason, setting the user's permission doesn't work.
    await testcord.set_permission_overrides(guild.me.roles[0], channel, manage_roles=True)

    # Make sure we actually got the permission
    assert channel.permissions_for(guild.me).manage_roles is True

    # Data to use for the rank
    role = make_role("Test Role", guild)
    rank_up_message = "Rank up message"
    level = 50

    # Send the request
    await testcord.message(f'{config.BOT_PREFIX}rank_create {str(level)} {role.id} "{rank_up_message}"')

    # Rank was created in DB!
    assert testcord.verify().message().content("Rank created.")
    
    # Let's see if that's true
    rank = Rank.get_rank(guild=guild, role_id=role.id)

    # If these are all correct, then we've succeeded
    assert rank.gid == guild.id
    assert rank.level == level
    assert rank.role_id == role.id
    assert rank.message == rank_up_message
    
    # Try sending the same request
    await testcord.message(f'{config.BOT_PREFIX}rank_create {str(level)} {role.id}')

    # Rank is already in the DB!
    assert testcord.verify().message().content("This rank was already set! Please remove it before trying to add a new one.")

    # Delete it from DB, it's no longer needed
    rank.delete()

    # Try to provide an invalid role
    await testcord.message(f'{config.BOT_PREFIX}rank_create {str(level)} {-1}')

    # Good, the role was bad
    assert testcord.verify().message().content("An invalid role was provided.")

@pytest.mark.asyncio
async def test_remove_rank(mock_phonewave):
    """Tests to see if we can remove a rank via command"""

    guild = mock_phonewave.guilds[0]
    channel = guild.text_channels[0]

    level = 50
    Rank(gid=guild.id, level=level, role_id=0).save()  # Create rank in DB

    # Set @everyone to have manage_roles permissions. For some reason, setting the user's permission doesn't work.
    await testcord.set_permission_overrides(guild.me.roles[0], channel, manage_roles=True)

    # Make sure we actually got the permission
    assert channel.permissions_for(guild.me).manage_roles is True

    # Send the request
    await testcord.message(f'p!rank_remove {level}')

    # Rank was deleted from the DB!
    assert testcord.verify().message().content(f"Rank {level} has been deleted.")
    
    # Let's see if that's true
    rank = Rank.get_rank(guild=guild, level=level)
    
    assert rank is None

    # Send the request again
    await testcord.message(f'p!rank_remove {level}')

    # Rank can't be deleted if it's already gone
    assert testcord.verify().message().content(f"No rank was found for level {level}.")