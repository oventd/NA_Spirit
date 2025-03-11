from pxr import Usd, UsdGeom, Sdf, Gf

class UsdUtils:
    @staticmethod
    def create_usd_file(file_path, ascii=True):
        # USD 파일을 ASCII(.usda)로 저장하지만 확장자는 .usd
        if ascii:
            args = {"format": "usda"}
        else:
            args = {"format": "usdc"}
        layer = Sdf.Layer.CreateNew(file_path, args=args)
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
    def create_xfrom(stage, path = "/Root", parent_prim = None):
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
    def add_refernce_to_variant_set(prim, variant_set_name, variants : dict, set_default = True):
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
    def set_translate(prim, x,y,z):
        xform = UsdGeom.Xform(prim)
        xform.AddTranslateOp().Set(Gf.Vec3f(10, 5, 2))  # 이동
        
        prim.GetStage().GetRootLayer().Save()

    @staticmethod
    def set_rotate(prim, x,y,z):
        xform = UsdGeom.Xform(prim)
        xform.AddRotateOp().Set(Gf.Vec3f(10, 5, 2))

        prim.GetStage().GetRootLayer().Save()

    @staticmethod
    def set_scale(prim, x,y,z):
        xform = UsdGeom.Xform(prim)
        xform.AddScaleOp().Set(Gf.Vec3f(10, 5, 2))

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

            for op in old_xform.GetOrderedXformOps():
                new_xform.AddXformOp(op.GetOpType()).Set(op.Get())

        # ✅ 기존 Prim의 References 복사
        new_prim.GetReferences().ClearReferences()
        print(dir(old_prim.GetReferences()))
        for reference in old_prim.GetReferences():
            new_prim.GetReferences().AddReference(reference.assetPath)

        # # ✅ 기존 Prim의 Variant Set 복사
        # old_variant_sets = old_prim.GetVariantSets()
        # new_variant_sets = new_prim.GetVariantSets()

        # for variant_set_name in old_variant_sets.GetNames():
        #     variant_set = new_variant_sets.AddVariantSet(variant_set_name)
        #     old_variant_set = old_variant_sets.GetVariantSet(variant_set_name)
            
        #     # Variant 이름 복사
        #     for variant_name in old_variant_set.GetVariantNames():
        #         variant_set.AddVariant(variant_name)

        #     # 현재 선택된 Variant 복사
        #     selected_variant = old_variant_set.GetVariantSelection()
        #     if selected_variant:
        #         variant_set.SetVariantSelection(selected_variant)

        # # ✅ 기존 Prim의 하위 Prim 재귀 복사
        # for child in old_prim.GetChildren():
        #     UsdUtils.deepcopy_prim(stage, child, new_prim_path)

        # return new_prim



if __name__ == "__main__":
    stage = UsdUtils.create_usd_file("output.usd")
    stage1 = UsdUtils.create_usd_file("output1.usd")
    xform_a = UsdUtils.create_xfrom(stage, "asset_a")
    xform_b = UsdUtils.create_xfrom(stage, "asset_b")
    UsdUtils.add_reference(xform_a, "output1.usd")
    # UsdUtils.create_variants_set(xform_b, "version")
    UsdUtils.add_refernce_to_variant_set(xform_a, "version", {"v001": "path", "v002": "path2", "v003": "path"})
    UsdUtils.add_refernce_to_variant_set(xform_a, "version", { "v004": "path4"}, set_default=False)
    UsdUtils.set_translate(xform_a, 10, 5, 2)
    UsdUtils.create_scope(stage, "asset_c")
    UsdUtils.add_sublayer(stage, "output1.usd")

