"""
Spirit 전체 상수 파일입니다.
"""
# DB 커넥션 상수
MONGODB_ADRESS = "mongodb://192.168.5.19:27017/" # mongoDB 주소
DATA_BASE = "filter_test" # 접속할 데이터 베이스 명
USER_COLLECTION = "test" # 데이터 베이스에서 접속할 컬렉션 명


# DB 데이터 key값 상수
OBJECT_ID = "_id"  # ObjectId('') 값
ASSET_ID = "asset_id"  # asset_id 값
NAME = "name"  # asset name
DESCRIPTION = "description"  # description 값
ASSET_TYPE = "asset_type"  # asset_type 값
CATEGORY = "category"  # category 값
STYLE = "style"  # style 값
RESOLUTION = "resolution"  # resolution 값
FILE_FORMAT = "file_format"  # file_format 값
SIZE = "size"  # size 값
LICENSE_TYPE = "license_type"  # license_type 값
CREATOR_ID = "creator_id"  # creator_id 값
CREATOR_NAME = "creator_name"  # creator_name 값
DOWNLOADS = "downloads"  # downloads 값
CREATED_AT = "created_at"  # created_at 값
UPDATED_AT = "updated_at"  # updated_at 값
PRICE = "price"  # price 값
DETAIL_URL = "detail_url"  # particular_url 값
PRESETTING_URL1 = "presetting_url1"  # presetting_url1 값
PRESETTING_URL2 = "presetting_url2"  # presetting_url2 값
PRESETTING_URL3 = "presetting_url3"  # presetting_url3 값
PREVIEW_URL = "preview_url"  # preview_url 값
TURNAROUND_URL = "turnaround_url" # turnaround_url 값
RIG_URL = "rig_url" # rig_url 값
APPLY_HDRI = "applyhdri_url" # applyhdri_url 값
HDRI_URL = "hdri_url" # hdri_url 값
MATERIAL_URLS = "material_urls" # material_urls 값

# DB 인덱싱 정의 상수(메타 데이터)
SCORE = "score"
TEXT = "text"

# logger 관련 상수
LOGGER_NAME = "db_crud" # DbCrud(객체 생성용) 로거 이름
DB_LOGGER_DIR = "/nas/spirit/DB/db_logger" # 로거 저장 경로
ASSET_LOGGER_NAME = "user_db" # 로거 저장 이름
ASSET_LOGGER_DIR = "/nas/spirit/DB/log/asset_library.log" # 에셋 로거 저장 경로

# Shotgrid Pipeline Step 상수
MODELING = 'Model'
RIGGING = 'Rig'
LOOKDEV = 'Lookdev'
MATCHMOVE = 'Matchmove'
LAYOUT = 'Layout'
ANIMATING = 'Animation'
LIGHTING = 'Light'
COMPOSITING = 'Comp'


# Open step 상수
STEP_PATH = '/home/rapa/NA_Spirit/open/step'
UTILS_PATH = '/home/rapa/NA_Spirit/utils'
RIG = "rig"
GEO = "geo"
ENV = "env"
LOW = "Low"
HIGH = "High"
ANIM_CAM = "anim_cam"
CAMERA1 = "camera1"
TERRAIN ="terrain"
CAMERA = "camera"
CHAR = "char"

# Shotgrid Pipeline Step Shot 상수
MDL = 'MDL' # Model
RIG = 'RIG' # Rig
LDV = 'LDV' # Lookdev
MMV = 'MMV' # Matchmove
LAY = 'LAY' # Layout
ANM = 'ANM' # Animation
LGT = 'LGT' # Light
CMP = 'CMP' # Compositing

shot_step_dict = {
    MODELING: MDL,
    RIGGING: RIG,
    LOOKDEV: LDV,
    MATCHMOVE: MMV,
    LAYOUT: LAY,
    ANIMATING: ANM,
    LIGHTING: LGT,
    COMPOSITING: CMP
}