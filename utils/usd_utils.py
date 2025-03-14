from pxr import Usd, UsdGeom, Sdf, Gf

class UsdUtils:
    @staticmethod
    def create_usd_file(file_path, ascii=True):
        # USD 파일을 ASCII(.usda)로 저장하지만 확장자는 .usd
        if ascii:
            args = {"format": "usda"}
        else:
            args = {"format": "usdc"}
        layer = Sdf.Layer.CreateNew(file_path, args)
        # USD Stage 생성 (ASCII 모드)
        stage = Usd.Stage.Open(layer)
        # USD 파일 저장
        stage.GetRootLayer().Save()
        return stage
    
    @staticmethod
    def set_default_prim(stage, prim):
        stage.SetDefaultPrim(prim)
    
    @staticmethod
    def get_stage(file_path):
        try:
            stage = Usd.Stage.Open(file_path)
            return stage
        except:
            return None
    
    @staticmethod
    def create_stage(file_path):
        return Usd.Stage.CreateNew(file_path)
    
    @staticmethod
    def get_prim(stage, path):
        return stage.GetPrimAtPath(path)

    @staticmethod
    def create_xform(stage, path = "/Root", parent_prim = None):
        xform = UsdGeom.Xform.Define(stage, path)
        
        defaltPrim = stage.GetDefaultPrim()
        if not defaltPrim:
            UsdUtils.set_default_prim(stage, xform.GetPrim())

        stage.GetRootLayer().Save()
        return xform.GetPrim()
        
    @staticmethod
    def create_scope(stage, path = "/Root", parent_prim = None):
        scope = UsdGeom.Scope.Define(stage, path)
        
        defaltPrim = stage.GetDefaultPrim()
        if not defaltPrim:
            UsdUtils.set_default_prim(stage, scope.GetPrim())
        stage.GetRootLayer().Save()
        return scope.GetPrim()
    
    @staticmethod
    def add_reference(prim, path):
        stage = prim.GetStage()
        prim.GetReferences().AddReference(path)
        stage.GetRootLayer().Save()
    
    @staticmethod
    def create_variants_set(xform, variant_set_name: str):
        stage = xform.GetStage()
        # Variant Set 생성
        variant_set = xform.GetVariantSets().AddVariantSet(variant_set_name)
        stage.GetRootLayer().Save()
        return variant_set
    @staticmethod
    def add_reference_to_variant_set(prim, variant_set_name, variants : dict, set_default = True):
        variant_set = prim.GetVariantSets().GetVariantSet(variant_set_name)

        if not variant_set:
            raise ValueError(f"Variant set '{variant_set_name}' not found.")

        current_variant = variant_set.GetVariantSelection()

        for variant_name, variant_value in variants.items():
            variant_set.AddVariant(variant_name)
            variant_set.SetVariantSelection(variant_name)
            with variant_set.GetVariantEditContext():
                prim.GetReferences().AddReference(variant_value)

        if not set_default:
            variant_set.SetVariantSelection(current_variant)

        stage = prim.GetStage()
        stage.GetRootLayer().Save()

    @staticmethod
    def set_transform(prim, translate=None, rotate=None, scale=None):
        """
        prim의 변환(이동, 회전, 스케일)을 설정하는 함수
        """
        xform = UsdGeom.Xform(prim)

        if translate:
            translate_op = xform.GetTranslateOp()
            if not translate_op:
                translate_op = xform.AddTranslateOp()
            translate_op.Set(Gf.Vec3f(*translate))

        if rotate:
            rotate_xyz_op = xform.GetRotateXYZOp()
            if not rotate_xyz_op:
                rotate_xyz_op = xform.AddRotateXYZOp()
            rotate_xyz_op.Set(Gf.Vec3f(*rotate))

        if scale:
            scale_op = xform.GetScaleOp()
            if not scale_op:
                scale_op = xform.AddScaleOp()
            scale_op.Set(Gf.Vec3f(*scale))

        prim.GetStage().GetRootLayer().Save()

    
    @staticmethod
    def add_sublayer(stage, path):
        stage.GetRootLayer().subLayerPaths.append(path)
        stage.GetRootLayer().Save()

    @staticmethod
    def deepcopy_prim(stage, old_prim, new_parent_path):
        """
        기존 Prim과 모든 하위 Prim을 새로운 부모 아래로 Deep Copy하는 재귀 함수.

        Args:
            stage (Usd.Stage): USD Stage 객체
            old_prim (Usd.Prim): 복사할 기존 Prim
            new_parent_path (str): 새로운 부모 Prim 경로

        Returns:
            Usd.Prim: 복사된 새로운 Prim 객체
        """
        new_prim_path = f"{new_parent_path}/{old_prim.GetName()}"
        new_prim = stage.OverridePrim(new_prim_path)

        # ✅ 기존 Prim의 속성(Attribute) 복사
        for attr in old_prim.GetAttributes():
            attr_value = attr.Get()
            if attr_value is not None:
                new_attr = new_prim.CreateAttribute(attr.GetName(), attr.GetTypeName())
                new_attr.Set(attr_value)

        # ✅ 기존 Prim의 Xform (Translate, Rotate, Scale) 복사
        if old_prim.IsA(UsdGeom.Xform):
            old_xform = UsdGeom.Xform(old_prim)
            new_xform = UsdGeom.Xform(new_prim)

    scope_a = UsdUtils.create_scope(stage, "/Root/Geometry")
    scope_b = UsdUtils.create_scope(stage, "/Root/Shader")
    
    UsdUtils.add_reference(scope_a, "geo_anim.usd")
    UsdUtils.add_reference(scope_b, "tex.usd")

    usd_hierarchy = UsdUtils.usd_to_dict(stage.GetPseudoRoot())
    import pprint
    pprint.pprint(usd_hierarchy)
    mats = UsdUtils.find_prim_paths_by_type(usd_hierarchy, "Material")
    meshs = UsdUtils.find_prim_paths_by_type(usd_hierarchy, "Mesh")

    print(mats)
    print(meshs)

    path = "/geo"
    # stage_geo = UsdUtils.get_stage("geo_anim.usd")
    # usd_hierarchy1 = UsdUtils.usd_to_dict(stage_geo.GetPseudoRoot())
    # mesh1 = UsdUtils.find_prim_paths_by_type(usd_hierarchy1, "Mesh")
    # print(usd_hierarchy1)
    # print(mesh1)

    mesh1 = stage.GetPrimAtPath(meshs[0])
    mesh2 = stage.GetPrimAtPath(meshs[1])
    if not mesh1 or not mesh1.IsValid():
        raise RuntimeError(f"Invalid Mesh Prim: {path}")

    material = UsdShade.Material.Get(stage, mats[0])
    material1 = UsdShade.Material.Get(stage, mats[1])

        # # ✅ 기존 Prim의 하위 Prim 재귀 복사
        # for child in old_prim.GetChildren():
        #     UsdUtils.deepcopy_prim(stage, child, new_prim_path)

        # return new_prim
    def get_prim_path(prim):
        return prim.GetPath()

    # 올바르게 로드되었으면 Material을 Mesh에 바인딩
    UsdShade.MaterialBindingAPI(mesh1).Bind(material1)
    UsdShade.MaterialBindingAPI(mesh2).Bind(material)
    stage.GetRootLayer().Save()

    xform_b = UsdUtils.create_xform(stage1, "/ref")
    UsdUtils.add_reference(xform_b, "/home/rapa/NA_Spirit/test_maya_export.usd")
    
# mesh export
#file -force -options ";exportUVs=1;exportSkels=none;exportSkin=none;exportBlendShapes=0;exportDisplayColor=0;filterTypes=nurbsCurve;exportColorSets=0;exportComponentTags=0;defaultMeshScheme=catmullClark;animation=0;eulerFilter=0;staticSingleSample=0;startTime=1;endTime=48;frameStride=1;frameSample=0.0;defaultUSDFormat=usda;rootPrim=;rootPrimType=xform;defaultPrim=geo;exportMaterials=0;shadingMode=useRegistry;convertMaterialsTo=[UsdPreviewSurface];exportAssignedMaterials=1;exportRelativeTextures=automatic;exportInstances=1;exportVisibility=1;mergeTransformAndShape=1;includeEmptyTransforms=1;stripNamespaces=0;worldspace=0;exportStagesAsRefs=1;excludeExportTypes=[];legacyMaterialScope=0" -typ "USD Export" -pr -es "/home/rapa/NA_Spirit/geo.usd";
    
# material export
#file -force -options ";exportUVs=1;exportSkels=none;exportSkin=none;exportBlendShapes=0;exportDisplayColor=0;filterTypes=nurbsCurve;exportColorSets=0;exportComponentTags=0;defaultMeshScheme=catmullClark;animation=0;eulerFilter=0;staticSingleSample=0;startTime=1;endTime=48;frameStride=1;frameSample=0.0;defaultUSDFormat=usda;rootPrim=;rootPrimType=xform;defaultPrim=geo;exportMaterials=1;shadingMode=useRegistry;convertMaterialsTo=[UsdPreviewSurface];exportAssignedMaterials=0;exportRelativeTextures=automatic;exportInstances=1;exportVisibility=1;mergeTransformAndShape=1;includeEmptyTransforms=1;stripNamespaces=0;worldspace=1;exportStagesAsRefs=1;jobContext=[Arnold];excludeExportTypes=[Meshes];legacyMaterialScope=0" -typ "USD Export" -pr -es "/home/rapa/NA_Spirit/tex.usd";




