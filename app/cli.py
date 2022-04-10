import argparse


def cli_runner(config):
    parser = argparse.ArgumentParser(description="PhoneWave CLI")
    parser.add_argument("-t", "--token", help="The bot token")
    parser.add_argument("-p", "--prefix", help="The bot default prefix")
    parser.add_argument("--rank-xp-timeout", help="Time in seconds before granting more XP")
    parser.add_argument("--rank-xp-reward", help="Reward per user message")
    parser.add_argument("--announcement-welcome", help="Default welcome message")
    parser.add_argument("--announcement-farewell", help="Default farewell message")
    parser.add_argument("--mongo-uri", help="The MongoDB URI/connection string")
    parser.add_argument("--mongo-db", help="The MongoDB application database")
    parser.add_argument("--redis-host", help="The Redis host")
    parser.add_argument("--redis-port", help="The Redis port")
    parser.add_argument("--redis-db", help="The Redis database for prefixes")

    args = parser.parse_args()

    if args.token:
        config.set("BOT_TOKEN", args.token)
    if args.prefix:
        config.set("BOT_PREFIX", args.prefix)
    if args.rank_xp_timeout:
        config.set("RANK_XP_TIMEOUT", args.mongo_uri)
    if args.rank_xp_reward:
        config.set("RANK_XP_REWARD", args.mongo_uri)
    if args.announcement_welcome:
        config.set("ANNOUNCEMENT_WELCOME", args.mongo_uri)
    if args.announcement_farewell:
        config.set("ANNOUNCEMENT_FAREWELL", args.mongo_uri)
    if args.mongo_uri:
        config.set("MONGO_URI", args.mongo_uri)
    if args.mongo_db:
        config.set("MONGO_DB", args.mongo_db)
    if args.redis_host:
        config.set("REDIS_HOST", args.redis_host)
    if args.redis_port:
        config.set("REDIS_PORT", args.redis_port)
    if args.redis_db:
        config.set("REDIS_DB", args.redis_db)
