from discord.ext import commands
import discord
import aiohttp


class SystemStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def system(self, ctx, *, system):
        """
        Get stats for a system.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://eddbapi.elitebgs.app/api/v4/systems?name={}".format(system)
            ) as resp:
                info = await resp.json()
        if info["total"] == 0:
            embed = discord.Embed(
                title="Error: No results found for ``" + system + "``", color=0xFF0000
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            return
        embed = discord.Embed(
            title="System Stats for ``" + system + "``", color=0x00FF00
        )
        embed.add_field(
            name="System Security",
            value=info["docs"][0]["security"].capitalize(),
        )
        embed.add_field(name="System Population", value=info["docs"][0]["population"])
        embed.add_field(
            name="System Allegiance", value=info["docs"][0]["allegiance"].title()
        )
        embed.add_field(name="Permit Locked", value=info["docs"][0]["needs_permit"])
        embed.add_field(
            name="Government Type", value=info["docs"][0]["government"].capitalize()
        )
        embed.add_field(
            name="Controlling Minor Faction",
            value=info["docs"][0]["controlling_minor_faction"]
            .replace("_", " ")
            .title(),
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(SystemStats(bot))
