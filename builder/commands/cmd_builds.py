import click
from builder.parser import champions


class Context:
    def __init__(self, champion):
        self.champion = champion
        self.champions = champions.Champions()
        self.build = self.champions.Build(champion)


@click.group()
@click.argument("champion", type=str)
@click.pass_context
def cli(ctx, champion):
    """
    Find the most popular build based on Champion name.

    For names with special characters and/or spaces such as Master Yi and Cho'gath,
    use " before and after the name.

    Example: \n
    builder builds "master yi" full-build \n
    builder builds "cho'gath" items
    builder builds "nunu & willump" full-build
    """
    ctx.obj = Context(champion)


@cli.command()
@click.pass_context
def summoner_spells(ctx):
    """
    Takes Champion name as argument and gives Spells.
    """
    result = ctx.obj.build.get_summoner_spells()
    click.echo("Summoner Spells:")
    for spell in result:
        click.echo(f"  {spell}")
    click.echo("")


@cli.command()
@click.pass_context
def runes(ctx):
    """
    Takes Champion name as argument and gives Runes.
    """
    click.echo("Runes:")
    result = ctx.obj.build.get_runes()
    for path in [*result]:
        click.echo(f"  {path}:")
        for rune in result[path]:
            click.echo(f"    {rune}")
    click.echo("")


@cli.command()
@click.pass_context
def items(ctx):
    """
    Takes Champion name as argument and gives Items.
    """
    result = ctx.obj.build.get_items()
    for category in [*result]:
        if category != "boots":
            click.echo(f"{category.replace('_',' ').title()}:")
            for item in result[category]:
                click.echo(f"  {item}")
        else:
            click.echo(f"{category.title()}:")
            click.echo(f"  {result[category]}")
    click.echo("")


@cli.command()
@click.pass_context
def skill_build(ctx):
    """
    Takes Champion name as argument and gives a skill build.
    """
    result = ctx.obj.build.get_skills()
    click.echo("Skill Build: ")
    for key in [*result]:
        spaced = ["|   |" for num in range(0,18)]
        for skill in result[key]:
            value = int(skill)
            if len(skill) == 2:
                spaced[value - 1] = f"|{skill[0]} {skill[1]}|"
            else:
                spaced[value - 1] = f"| {skill} |"
        click.echo(f"{key}: {''.join(spaced)}")
    click.echo("")


@cli.command()
@click.pass_context
def full_build(ctx):
    """
    Takes a champion name and gives a complete build.
    """
    ctx.forward(summoner_spells)
    ctx.forward(runes)
    ctx.forward(items)
    ctx.forward(skill_build)
