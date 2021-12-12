import random
import re
import typing

import discord
from discord.ext import commands, vbu  # type: ignore


class WhatDoesPpStandFor(vbu.Cog):
    def __init__(self, bot: commands.Bot, logger_name: str = None):
        super().__init__(bot, logger_name=logger_name)
        self.channel_id = 919654742228095026
        self.validator_regex = re.compile(r"^(p.*\sp.*)+$", re.IGNORECASE)

    def validator(self, message: discord.Message) -> bool:
        splitted = message.content.split()
        if len(splitted) != 2:
            return False

        if not self.validator_regex.match(message.content):
            return False

        return True

    def yes_no_pair_generator(self) -> typing.Tuple[str, str]:
        options: typing.List[typing.Tuple[str, str]] = [
            ("<a:nodderscat:918906638704979978>", "<a:noperscat:918943812129280010>"),
            ("<a:nodders:910983709660966912>", "<a:NOPERS:919669928007716946>"),
            ("<a:tick:919670175563911189>", "<a:falseTick:919670356237754468>"),
        ]
        return random.choice(options)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        def delete_or_stay(message: discord.Message) -> typing.Optional[bool]:

            # Me?
            if message.author == self.bot.user:
                return None

            # Wrong channel?
            if not message.channel or message.channel.id != self.channel_id:
                return None

            # Valid message?
            if not self.validator(message):
                return False

            return True

        result = delete_or_stay(message)
        if result is None:
            return
        if not result:
            reply = await message.reply(
                "That's not a valid answer. Example answers: `personal pet`, `pee pee`, `pinapple piss`, etc.",
                delete_after=5,
            )
            await message.delete()
            return

        await message.delete()
        with vbu.Embed() as embed:
            embed.title = f"“{message.content.title()}”"
            footer_kwargs: typing.Dict[str, str] = {}
            if isinstance(message.author.avatar, discord.Member):
                footer_kwargs["icon_url"] = message.author.avatar_url
            embed.set_footer(
                f"{message.author} thinks that this is what P.P. stands for.",
                **footer_kwargs,
            )

        embed_message = await message.channel.send(embed=embed)
        for emoji in self.yes_no_pair_generator():
            await embed_message.add_reaction(emoji)


def setup(bot: vbu.Bot):
    x = WhatDoesPpStandFor(bot)
    bot.add_cog(x)
