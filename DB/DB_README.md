파일 구조 설명

/home/rapa/NA_Spirit/DB/
├── /gui/ # ui 관련 폴더 입니당! 
│    ├── init.py # 해당 디렉토리를 패키지로 인식하도록 만드는 역할
│    ├── ui_window.py       # UI (View) - 사용자 인터페이스
├── /lib/
│    ├── init.py # 해당 디렉토리를 패키지로 인식하도록 만드는 역할
│    ├── db_client.py       # MongoDB 연결 관리
│    ├── db_model.py        # 데이터 모델 (MongoDB Collection 구조)
│    ├── db_crud.py         # DB 접근을 담당하는 CRUD 함수
│    ├── asset_service.py   # UI와 DB를 분리하는 서비스 계층
├── main.py  # 프로그램 실행

1. Main.py : 프로그램이 실행되는 파일 -> ui_window에서 ui를 불러와 실행
2. ui_window.py : UI 레이아웃과 상호작용을 담당(필터 UI와 테이블 뷰를 관리)
3. asset_service.py : UI와 DB 간의 중간 계층 역할 -> UI가 직접 DB 로직을 호출하지 않게
4. db_client.py : MongoDB와의 연결 관리
5. db_crud.py : MongoDB에 대한 CRUD(Create, Read, Update, Delete) 연산을 처리
6. db_model.py : MongoDB 데이터를 테이블로 표시하는 모델 -> UI에서 데이터를 모델로 변환하여 **QTableView**에 표시하는 역할

