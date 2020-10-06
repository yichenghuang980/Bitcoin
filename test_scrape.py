from click.testing import CliRunner
from scrape import scrape


def test_scrape():
    runner = CliRunner()
    result = runner.invoke(scrape, ['--url','https://coincodex.com/crypto/bitcoin/historical-data/'])