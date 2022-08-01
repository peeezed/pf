import click
from builder.parser import champions


class Context:
    def __init__(self):
        self.champions = champions.Champions()


@click.group()
@click.pass_context
def cli(ctx):
    """
    Query Champions based on different arguments.

    Examples: \n

    builder champions by-name senna\n
    builder champions by-win-rate 50\n
    builder champions by-name "master yi"
    """
    ctx.obj = Context()


@cli.command()
@click.argument("threshold", type=int, default = 0)
@click.pass_context
def by_win_rate(ctx,threshold):
    """
    Find champions which has equal and higher win rate than the parameter.
    To get full list, do not enter any value.
    """
    result = ctx.obj.champions.query_by_win_rate(threshold)
    if not result:
        click.echo("No champions found.")
        return
    click.echo("Champions found: ") 
    for k,v in result.items():
        click.echo(f"    {k}: {v}%")


@cli.command()
@click.argument("threshold", type=int, default = 0)
@click.pass_context
def by_pick_rate(ctx, threshold):
    """
    Find champions which has equal and higher pick rate than the parameter.
    To get full list, do not enter any value.
    """
    result = ctx.obj.champions.query_by_pick_rate(threshold)
    if not result:
        click.echo("No champions found.")
        return
    click.echo("Champions found: ") 
    for k,v in result.items():
        click.echo(f"    {k}: {v}%")


@cli.command()
@click.argument("position",type=str)
@click.pass_context
def by_pos(ctx,position):
    """
    Find a list of champions playing a specific position.
    valid arguments = sup, mid, bot, top
    """
    result = ctx.obj.champions.query_by_pos(position)
    if not result:
        click.echo("Position couldn't be found, please double check spelling. Valid arguments = sup, mid, bot, top")
        return
    click.echo("Champions found: ")
    for res in result:
        click.echo(f"    {res}")


@cli.command()
@click.argument("name",type=str)
@click.pass_context
def by_name(ctx,name):
    """
    Find information about a champion by entering their name.
    For names with special characters and/or spaces such as Master Yi and Cho'gath,
    use " before and after the name.
    Example: \n
    builder champions by-name "master yi" \n
    builder champions by-name "cho'gath"
    builder champions by-name "nunu & willump"
    """
    result = ctx.obj.champions.query_by_name(name.lower())
    if not result:
        click.echo("Champion couldn't be found, please double check spelling. For more information go to builder champions --help")
        return
    click.echo("Champions found: ")
    for name_list in result:
        for name in name_list:
            click.echo(f"{name.title()}")
            click.echo("  Positions:")
            for pos in name_list[name]["pos"]:
                click.echo(f"   {pos.capitalize()}")
            click.echo("  Win %: ")
            click.echo(f"   {name_list[name]['win_rate']}")
            click.echo("  Pick %: ")
            click.echo(f"   {name_list[name]['pick_rate']}")
