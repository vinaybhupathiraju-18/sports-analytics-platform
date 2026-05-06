import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import boto3
import io
import logging
from botocore.exceptions import ClientError
from ingestion.schema import DTYPE_MAP, DATE_COLS, KEEP_COLS
from ingestion.config import RAW_BUCKET, S3_PREFIX, SEASONS

log = logging.getLogger(__name__)

def already_in_s3(bucket: str, key: str) -> bool:
    try:
        boto3.client('s3', region_name='us-east-2').head_object(Bucket=bucket, Key=key)
        return True
    except ClientError:
        return False

def ingest_season(year: int, force: bool = False):
    s3_key = f'{S3_PREFIX}season={year}/pbp.parquet'
    if not force and already_in_s3(RAW_BUCKET, s3_key):
        log.info(f'{year}: already in S3, skipping')
        return

    csv_path = f'data/raw/pbp_{year}.csv.gz'
    log.info(f'{year}: loading {csv_path}')

    df = pd.read_csv(
        csv_path,
        usecols=lambda c: c in KEEP_COLS,
        dtype={k: v for k, v in DTYPE_MAP.items()},
        parse_dates=DATE_COLS,
        low_memory=False,
    )
    df['season'] = year
    log.info(f'{year}: {len(df):,} rows, {df.shape[1]} columns loaded')

    table = pa.Table.from_pandas(df, preserve_index=False)
    buf = io.BytesIO()
    pq.write_table(table, buf, compression='snappy')
    buf.seek(0)

    boto3.client('s3', region_name='us-east-2').upload_fileobj(buf, RAW_BUCKET, s3_key)
    log.info(f'{year}: uploaded -> s3://{RAW_BUCKET}/{s3_key}')

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        force=True
    )
    for yr in SEASONS:
        try:
            ingest_season(yr)
        except Exception as e:
            log.error(f'{yr}: FAILED — {e}')
            raise