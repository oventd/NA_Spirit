from work_file_creator import WorkFileCreator

class MayaWorkFileCreator(WorkFileCreator):
    def create_work_file(self, library_file_path: str, file_path: str) -> None:
        print("Creating Maya work file...")
        # 예: Maya 전용 작업 파일 생성 로직 구현
        # shutil.copy(library_file_path, file_path)
        pass