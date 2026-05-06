import requests
import pathlib
import logging

log = logging.getLogger(__name__)

BASE_URL = (
    'https://github.com/nflverse/nflverse-data/releases/'
    'download/pbp/play_by_play_{year}.csv.gz'
)

def download_season(year: int, dest_dir: str = 'data/raw') -> pathlib.Path:
    dest = pathlib.Path(dest_dir) / f'pbp_{year}.csv.gz'
    if dest.exists():
        log.info(f'{year}: already downloaded, skipping')
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = BASE_URL.format(year=year)
    log.info(f'Downloading {year} from {url}')
    r = requests.get(url, stream=True, timeout=120)
    r.raise_for_status()
    with open(dest, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    log.info(f'{year}: saved to {dest}')
    return dest

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        force=True
    )
    for yr in [2022, 2023, 2024]:
        download_season(yr)