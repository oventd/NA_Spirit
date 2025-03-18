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

1. Main.py : 프로그램이 실행되는 파일 -> ui_window에서 ui를 불러와 실행
2. ui_window.py : UI 레이아웃과 상호작용을 담당(필터 UI와 테이블 뷰를 관리)
3. assetmanager.py : UI와 DB 간의 중간 계층 역할 -> UI가 직접 DB 로직을 호출하지 않게
4. db_client.py : MongoDB와의 연결 관리
5. db_crud.py : MongoDB에 대한 CRUD(Create, Read, Update, Delete) 연산을 처리
6. db_model.py : MongoDB 데이터를 테이블로 표시하는 모델 -> UI에서 데이터를 모델로 변환하여 **QTableView**에 표시하는 역할

