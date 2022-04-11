from app.database.ranks.baserank import BaseRank
from app.modules.ranksystem.ranksystem import RankSystem

class Rank5(BaseRank):

    @BaseRank.condition()
    def check_condition(guild, member, level):
        return level == 5

    @BaseRank.reward()
    def apply_reward(guild, member):
        print("Leveled up!")

def register_rank(rank:RankSystem):
    rank.add_rank(Rank5())
    