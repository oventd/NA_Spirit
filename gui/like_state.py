class LikeState:    
    _instance = None  # 싱글톤 인스턴스 저장

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LikeState, cls).__new__(cls)

        return cls._instance
    def __init__(self):
        if hasattr(self, "_initialized"):  # 중복 초기화를 방지
            return
        self.state = False
        self._initialized = True
    
    @property
    def state(self):
        return self.state

    @state.setter
    def state(self, value):
        self.state = value
            