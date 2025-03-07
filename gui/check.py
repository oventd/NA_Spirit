
class Check:
    _instance = None  # 싱글톤 인스턴스 저장

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)  # 올바른 싱글톤 생성
        return cls._instance  # 기존 인스턴스 반환

    def __init__(self):
        if hasattr(self, "_initialized"):  # 중복 초기화를 방지
            return
        self._dict = {}
        self._checked_items = []
        self._initialized = True
    @property
    def dict(self):
        return self._dict  # _state 값을 반환

    @dict.setter
    def dict(self, value):
        self._dict = value  # _state 값을 변경

    @property
    def checked_items(self):
        return self._dict  # _state 값을 반환

    @checked_items.setter
    def checked_items(self, value):
        self._checked_items = value  # _state 값을 변경