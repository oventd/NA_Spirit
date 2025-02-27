from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QWidget, QTreeWidgetItem, QPushButton, QStyledItemDelegate
from PySide6.QtCore import QFile, Qt, Signal
from PySide6.QtGui import QPixmap, QPixmap,  QPainter, QBrush, QColor
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QSizePolicy ,QVBoxLayout

from lib.asset_service import AssetService  # AssetService 임포트
from lib.db_model import CustomTableModel  # 절대 경로로 db_model 임포트
import pymongo  # MongoDB 작업을 위한 라이브러리

client = pymongo.MongoClient("mongodb://192.168.5.19:27017/")  # 로컬 MongoDB 서버에 연결
db = client["filter_test"]  # 사용할 데이터베이스 'filter_test'에 연결
asset_collection = db["test"]  # 'test'라는 컬렉션에 연결

asset = list(asset_collection.find ({},
    {"asset_id": 1,  # 필터 조건
    "preview_url": 1, "_id": 0}  # 필요한 필드만 가져오기
))
print(asset)
print(len(asset))