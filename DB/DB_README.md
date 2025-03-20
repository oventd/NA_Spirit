DB(MongoDB 기반)

MongoDB와 연동하여 데이터를 관리하고, UI를 통해 사용자와 상호작용할 수 있는 애플리케이션입니다. 
:db_client: MongoDB를 연결합니다.
:db_crud.py: 데이터를 CRUD(Create, Read, Update, Delete) 작업을 처리하는 다양한 모듈을 포함하고 있습니다. 
:assetmanager.py: UI와 DB 간의 의존성을 분리하는 서비스 계층을 만들어 유지보수성을 높였습니다.

/home/rapa/NA_Spirit/DB/
├── /lib/
│    ├── init.py                # 해당 디렉토리를 패키지로 인식하도록 만드는 역할
│    ├── db_client.py           # MongoDB 연결 관리
│    ├── db_crud.py             # DB 접근을 담당하는 CRUD 함수
/home/rapa/NA_Spirit/gui/
├── /gui/                       # UI 관련 폴더
│    ├── assetmanager.py        # UI와 DB를 분리하는 서비스 계층

