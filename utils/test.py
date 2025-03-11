from pxr import Usd, UsdGeom

class UsdUtils:
    @staticmethod
    def create_usd_file(file_path, geom_type, position, ascii=True):
        """
        지정된 형상의 USD 파일을 생성.
        
        :param file_path: USD 파일 경로
        :param geom_type: "Sphere" 또는 "Cylinder"
        :param position: (x, y, z) 위치 좌표
        :param ascii: True면 ASCII(.usda), False면 바이너리(.usdc)로 저장
        """
        extension = ".usda" if ascii else ".usdc"
        if not file_path.endswith(extension):
            file_path += extension

        stage = Usd.Stage.CreateNew(file_path, format="usda" if ascii else "usdc")

        # Xform 노드 생성
        xform = UsdGeom.Xform.Define(stage, f"/{geom_type}")

        # 변환 설정 (위치 이동)
        xform_op = xform.AddTranslateOp()
        xform_op.Set(position)

        # 도형 추가
        if geom_type == "Sphere":
            UsdGeom.Sphere.Define(stage, f"/{geom_type}/Shape")
        elif geom_type == "Cylinder":
            UsdGeom.Cylinder.Define(stage, f"/{geom_type}/Shape")

        stage.GetRootLayer().Save()
        print(f"USD file created: {file_path}")

    @staticmethod
    def create_main_usd(main_file_path, ref_file1, ref_file2, ascii=True):
        """
        두 개의 USD 파일을 Reference로 불러와 새로운 USD 파일을 생성.
        
        :param main_file_path: 메인 USD 파일 경로
        :param ref_file1: 첫 번째 참조 파일 경로
        :param ref_file2: 두 번째 참조 파일 경로
        :param ascii: True면 ASCII(.usda), False면 바이너리(.usdc)로 저장
        """
        extension = ".usda" if ascii else ".usdc"
        if not main_file_path.endswith(extension):
            main_file_path += extension

        stage = Usd.Stage.CreateNew(main_file_path, format="usda" if ascii else "usdc")

        # 첫 번째 Reference 추가 (Sphere)
        xform1 = UsdGeom.Xform.Define(stage, "/Ref1")
        xform1.GetPrim().GetReferences().AddReference(ref_file1)

        # 두 번째 Reference 추가 (Cylinder)
        xform2 = UsdGeom.Xform.Define(stage, "/Ref2")
        xform2.GetPrim().GetReferences().AddReference(ref_file2)

        stage.GetRootLayer().Save()
        print(f"Main USD file created: {main_file_path}")

# 실행 예제
UsdUtils.create_usd_file("home/rapa/NA_Spirit/file1", "Sphere", (0, 0, 0), ascii=True)   # 구 (0, 0, 0)
UsdUtils.create_usd_file("home/rapa/NA_Spirit/file2", "Cylinder", (2, 0, 0), ascii=True) # 원기둥 (2, 0, 0)
UsdUtils.create_main_usd("home/rapa/NA_Spirit/main", "home/rapa/NA_Spirit/file1.usda", "home/rapa/NA_Spirit/file2.usda", ascii=True) # Main USD
