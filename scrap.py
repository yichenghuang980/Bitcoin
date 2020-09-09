import click

@click.command()
@click.option('--name')
def marco(name):
    if name == "Marco":
        click.echo("Polo")
    else:
        click.echo("No Match")    

# main function
if __name__ == '__main__':
    marco()