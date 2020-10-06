from click.testing import CliRunner
from scrap import scrap


def test_marco():
    runner = CliRunner()
    result = runner.invoke(scrap, ['--url','https://coincodex.com/crypto/bitcoin/historical-data/'])