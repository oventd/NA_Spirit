import os
import shutil

class LoadManager:
    def __init__(self, root_path):
        self.root_path = root_path
        self.types = ["assets", "sequences"]
        self.defult_file = "scene"

    @property
    def root_path(self):
        return self._root_path

    @root_path.setter
    def root_path(self, value):
        self._root_path = value

    def validate_inputs(self, type, dcc):
        if type not in self.types:
            raise ValueError(f"Invalid type: {type}. Please choose 'assets' or 'sequences'.")
        
        # 메소드 이름 생성
        method_name = f"create_{dcc}_work_file"

        # method name을 통해 클래스내 메소드를 찾아옴
        method = getattr(self, method_name, None)

        # 메소드가 존재하지 않을시, ValueError 실행. 
        # 에러시 매개변수 dcc가 잘못되어있거나, 해당 dcc의 메소드가 구현되지 않음
        if not method:
            raise ValueError(f"Invalid dcc: {dcc}. Please choose 'maya' or 'houdini'.")
        
    def add_entity(self, library_file_path, type, category, task, entity, dcc, work_ext, publush_ext, file_name=None):
        if not file_name:
            file_name = self.defult_file
        
        self.validate_inputs(type, dcc)
        
        publish_dir, work_dir = self.make_entity_dir(type, category, entity, task, dcc)

        publish_version = self.search_version(publish_dir, file_name)
        publish_path = f"{publish_dir}/{file_name}.{publish_version}{publush_ext}"

        work_version = self.search_version(work_dir, file_name)
        work_path = f"{work_dir}/{file_name}.{work_version}{work_ext}"

        self.create_publish_file(library_file_path, publish_path)
        self.create_work_file(dcc, work_path)

    def search_version(self, publish_dir, file_name):
        files = os.listdir(publish_dir)
        
        last_version = "v000"
        for file in files:
            if file.startswith(file_name):
                version = file.split(".")[1]
                last_version = version
                
        last_version_num = int(last_version[1:])
        last_version_num += 1
        last_version = f"v{last_version_num:03d}"

        return last_version        

    def make_entity_file_path(root_path=None, type=None, category=None, entity=None, task=None, version=None, dcc=None, file=None):
        inputs = [type, category, entity, task, version, dcc, file]

        path_values = []
        for input in inputs:
            if input is None:
                continue
            path_values.append(input)

        path = "/".join(path_values)
        path = os.path.join(root_path, path)
        return path


    def make_entity_dir(self, type, category, entity, task,dcc):
        # publish 디렉토리 생성
        publish_dir = self.make_entity_file_path(self.root_path, type, category, entity, task,"publish", "cache")
        os.makedirs(publish_dir, exist_ok=True)

        # work 디렉토리 생성
        work_dir = self.make_entity_file_path(self.root_path, type, category, entity, task,"work", dcc)
        os.makedirs(work_dir, exist_ok=True)

        return publish_dir, work_dir

    def create_publish_file(self, library_file_path, publish_path):
        """
        library file path를 받아 root_path의 샷그리드 프로젝트의 에셋 publish path에 파일을 복사함.
        """
        # 파일 디렉토리 생성
        dir_path = os.path.dirname(publish_path)
        os.makedirs(dir_path, exist_ok=True)

        # 파일 복사
        shutil.copy(library_file_path, publish_path)

    def create_work_file(self, library_file_path, dcc, file_path):
        """
        dcc 매개변수를 통해 dcc별로 필요한 create work file 매소드를 찾아 실행함

        : parm dcc : maya or houdini dcc 이름
        : parm file_path : library file path 경로
        """
        # 메소드 이름 생성
        method_name = f"create_{dcc}_work_file"

        # method name을 통해 클래스내 메소드를 찾아옴
        method = getattr(self, method_name, None)
       
        # 메소드 실행
        return method(library_file_path, file_path)

    def create_maya_work_file(self,library_file_path, file_path):
        print("create_maya_work_file")
        pass
    def create_houdini_work_file(self,library_file_path, file_path):
        print("create_houdini_work_file")
        pass

if __name__ == "__main__":
    lm = LoadManager("/nas/sam/show/test")
    library_asset_path = "/home/rapa/Kitchen_set/assets/Chair/Chair.usd"
    lm.add_entity(library_asset_path, "assets", "Prop", "Chair", "MDL", "maya", ".ma",".usd")


