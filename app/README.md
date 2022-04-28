# explanation about how drawing profile card works


### High level overview (how to input, and how to process output)

To draw profile card, with provided data you can use `profileCardFromMember()`  function. Here's example call:

    drawProfileCard(
        "https://cdn.discordapp.com/avatars/487896060316876800/b603f6cce63f7c6430559ae5c3a00f4b.png?size=512", # avatar
        "FreshTeaBagsByLipton", # nickname
        2036, # discriminator
        222, # lab mem
        21, # level
        1, # rank
        235621, # messages sent
        54200, # xp current
        60000, # next level xp
        ['operation_elysian_veteran', 'daru69'] # Acquired badges names, they represent file as shown in constants.badges_map
    )

This function will return bytes, that can be used to create [for example discord](https://stackoverflow.com/a/66094487/11273040 "for example discord") file from them:
`await message.channel.send(file=discord.File(fp=<bytes>, filename='image.png'))`

Note that "badges_list" (last positional argument) is list of strings, with max length of 7, in which every element need to be string, that is present in `constants.badges_map` .


### Low level overview (what happens under the hood)
##### todo
