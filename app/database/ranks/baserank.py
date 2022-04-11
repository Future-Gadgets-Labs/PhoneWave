from discord import Member as DiscordMember
from discord import Guild as DiscordGuild
from typing import TypeVar, Callable, Union

class BaseRank():

    ConditionFuncT = TypeVar('ConditionFuncT', bound=Callable[[DiscordGuild, DiscordMember, int], bool])
    RewardFuncT = TypeVar('RewardFuncT', bound=Callable[[DiscordGuild, DiscordMember], None])

    @classmethod
    def reward(self):
        def decorator(func: BaseRank.ConditionFuncT):
            self.reward_func = func
            return func
        return decorator

    @classmethod
    def condition(self):
        def decorator(func: BaseRank.RewardFuncT):
            self.condition_func = func
            return func
        return decorator

    @classmethod
    def try_condition(self, guild:DiscordGuild, member:DiscordMember, level:int) -> Union[bool, None]:
        if not hasattr(self, "condition_func"):
            raise NotImplementedError
        else:
            return self.condition_func(guild, member, level)

    @classmethod
    def resolve_reward(self, guild:DiscordGuild, member:DiscordMember) -> None:
        if not hasattr(self, "reward_func"):
            raise NotImplementedError
        else:
            self.reward_func(guild, member)

    # Attempts the condition, and if it succeeds, applies the reward.
    # Returns True if the reward was applied
    @classmethod
    def attempt_condition_and_resolve(self, guild:DiscordGuild, member:DiscordMember, level:int) -> Union[bool, None]:
        if self.try_condition(guild, member, level):
            self.resolve_reward(guild, member)
            return True
        return False