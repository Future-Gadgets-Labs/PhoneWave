import pytest
import discord.ext.test as testcord
from discord.ext.test.backend import make_user, make_member

from app.config import config
from app.database.models.member import Member


@pytest.mark.asyncio
async def test_new_user_has_xp(mock_phonewave):  # We need mock_phonewave fixture for the DB setup
    """Tests the functionality of creating a user in the db and giving them XP."""
    msg = await testcord.message("Message sent")  # Sent message to trigger rank system
    mem = Member.get_member(msg.guild.id, msg.author.id)  # Get member from DB

    assert mem is not None

    if mem is not None:
        assert mem.xp == config.RANK_XP_REWARD  # If not matching, either too much xp was given or not at all


@pytest.mark.asyncio
async def test_user_can_gain_xp(mock_phonewave):
    """Tests the functionality of adding xp to a user in the db"""
    
    user = make_user("XPUser", 1)  # Our test member
    guild = mock_phonewave.guilds[0]  # The guild to join (the bot is there already)
    member = make_member(user, guild)  # Make our user join, now he's a member
    
    # Create entry in db with xp already set
    dbmember = Member(gid=guild.id, uid=user.id, xp=15)
    dbmember.save()

    # Send message to get xp (as the member)
    await testcord.message("Test message", member=member)

    # Fetch from DB again (our object isn't synced anymore)
    dbmember = Member.get_member(gid=guild.id, uid=user.id)

    # 15 default + xp value should equal out
    assert dbmember.xp == 15 + config.RANK_XP_REWARD