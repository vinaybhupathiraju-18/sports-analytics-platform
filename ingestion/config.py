from dotenv import load_dotenv
import os

load_dotenv()

RAW_BUCKET = os.environ['RAW_BUCKET']
S3_PREFIX  = os.getenv('S3_PREFIX', 'raw/sports/nfl/pbp/')
GLUE_DB    = os.getenv('GLUE_DB',   'nfl_raw')
SEASONS    = [int(x) for x in
              os.getenv('SEASONS', '2022,2023,2024').split(',')]