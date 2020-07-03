from discord.ext import commands
from discord import Embed
import requests
from lxml import html


bot = commands.Bot(command_prefix='!')
root = 'https://wiki.albiononline.com'
url_prefix = 'https://wiki.albiononline.com/index.php?search='
url_suffix = '&title=Special%3ASearch&profile=default&fulltext=1'

help_msg = (
    "**Usage:**\n"
    "`!aowiki blazing staff`\n"
)


@bot.command()
async def aowiki(ctx, *args, **kwargs):
    result_number = 5
    if len(args) <= 0:
        await ctx.send(help_msg)
        return
    s = args[0]
    for arg in args[1:]:
        s = s + '+' + arg
    url = url_prefix + s + url_suffix
    page = requests.get(url)
    if page.status_code != 200:
        return
    tree = html.fromstring(page.content)
    divs = tree.xpath('//div[@class="mw-search-result-heading"]')
    if len(divs) <= 0:
        return
    divs = divs[:result_number]
    embed = Embed(
        title="AlbionOnline-Wiki",
        description="Search the wiki directly from Discord!"
    )
    for div in divs:
        a = div.xpath('a')
        if len(a) != 1:
            continue
        a = a[0]
        title = a.xpath('@title')
        if len(title) != 1:
            continue
        title = title[0]
        relink = a.xpath('@href')
        if len(relink) != 1:
            continue
        relink = relink[0]
        link = root + relink
        if title is None or relink is None:
            continue
        embed.add_field(
            name=title,
            value=link,
            inline=False
        )
    await ctx.send(embed=embed)

bot.run('token')
