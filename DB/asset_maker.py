from datetime import datetime, timedelta
import random
from bson import ObjectId  # MongoDB에서 사용하는 ObjectId를 처리하는 데 사용
import pymongo  # MongoDB 작업을 위한 라이브러리

# MongoDB 연결
client = pymongo.MongoClient("mongodb://192.168.5.10:27017")  # 로컬 MongoDB 서버에 연결
db = client["spiritDatabase"]  # 사용할 데이터베이스 'filter_test'에 연결
asset_collection = db["test"]  # 'test'라는 컬렉션에 연결

"""랜덤 데이터 생성 ㅎ"""
# # 자산 데이터를 생성하는 함수
# def generate_asset_data():
#     """
#     자산 데이터를 생성하는 함수
#     :return: 자산 데이터 (사전 형태)
#     """
#     asset_types = ["3D Model", "Material", "Texture", "HDRI"]
#     categories = ["Environment", "Character", "Props", "Vehicle", "Weapon", "Architecture", "Others"]
#     styles = ["Realistic", "Stylized", "Procedural"]
#     resolutions = ["512x512", "1024x1024", "2048x2048", "4096x4096"]
#     polygon_counts = ["Low-poly", "Medium-poly", "High-poly"]
#     license_types = ["Paid", "Free"]
#     creator_names = ["John Doe", "Alice Smith", "Bob Johnson", "Eva White", "Charlie Brown", 
#                      "David Lee", "Mia Garcia", "Liam Scott", "Sophia King", "James Turner"]

#     # asset_type에 따른 file_formats 조건 설정
#     file_formats_by_type = {
#         "3D Model": ["FBX", "GLB", "OBJ"],
#         "Material": ["SBSAR", "SBS"], # 쉐이더임. texture의 모임임 USD로 저장할거임
#         "Texture": ["EXR", "JPG", "PNG"],  # EXR 파일 형식도 Texture에 포함
#         "HDRI": ["HDRI", "EXR"]  # HDRI 자산 타입은 HDRI, EXR을 모두 가질 수 있음
#     }

#     asset_type = random.choice(asset_types)
#     license_type = random.choice(license_types)  # 라이센스 타입도 랜덤으로 선택

#     # 랜덤한 날짜 범위 (1일, 7일, 14일 등)
#     days_ago = random.choice([1, 7, 14, 30, 60])
#     created_at = datetime.utcnow() - timedelta(days=days_ago)
#     updated_at = created_at  # 초기화 시 created_at과 동일하게 설정

#     # 기본 자산 데이터
#     asset_data = {
#         "asset_id": f"{random.randint(1, 1000):03d}",
#         "name": f"Asset {random.randint(1, 100)}",
#         "description": f"A description for asset {random.randint(1, 100)}",
#         "asset_type": asset_type,
#         "category": random.choice(categories),
#         "style": random.choice(styles),
#         "resolution": random.choice(resolutions),
#         "file_format": random.choice(file_formats_by_type[asset_type]),  # asset_type에 맞는 file_format 랜덤 선택
#         "size": f"{random.randint(1, 500)}MB",
#         "license_type": license_type,
#         "creator_id": f"{random.randint(1000, 9999)}",
#         "creator_name": random.choice(creator_names),
#         "downloads": random.randint(50, 1000),
#         "created_at": created_at,
#         "updated_at": updated_at,
#     }

#     # polygon_counts는 3D Model 타입에만 포함
#     if asset_type == "3D Model":
#         asset_data["polygon_counts"] = random.choice(polygon_counts)

#     # 필드 추가 조건
#     asset_data["preview_url"] = f"http://example.com/preview{random.randint(1, 100)}.jpg"  # 모든 자산 타입에 생성

#     if asset_type == "3D Model":
#         # 3D Model인 경우에만 추가되는 필드
#         asset_data["turnaround_url"] = f"http://example.com/turnaround{random.randint(1, 100)}.mp4"
#         asset_data["rig_url"] = f"http://example.com/rig{random.randint(1, 100)}.mp4"
    
#     if asset_type in ["Material", "Texture"]:
#         # Material 또는 Texture인 경우에만 추가되는 필드
#         asset_data["particular_url"] = f"http://example.com/particular{random.randint(1, 100)}.jpg"
    
#     # license_type이 "Paid"인 경우에만 price 생성
#     if license_type == "Paid":
#         asset_data["price"] = random.randint(1, 100)  # 가격을 1에서 100 사이로 설정

#     return asset_data

# # 자산 데이터 20개 생성 후 MongoDB에 삽입
# assets_data = [generate_asset_data() for _ in range(20)]  # 20개 자산 데이터 생성

# # 자산 데이터를 MongoDB에 삽입
# asset_collection.insert_many(assets_data)  # 자산 데이터를 DB에 삽입

# print("20개의 자산 데이터가 MongoDB에 성공적으로 삽입되었습니다.")


"""이미지 파일 명 삽입하는 메서드 """
# def generate_asset_data():
#     # 이미지 파일명을 thum001.png ~ thum031.png 까지 순차적으로 설정
#     image_files = [f"thum{i:03}.png" for i in range(1, 32)]  # thum001.png ~ thum031.png 리스트 생성

#     # '3D Model'인 자산을 업데이트
#     for i, asset in enumerate(asset_collection.find({"asset_type": "3D Model"})):
#         # 순차적으로 이미지 파일명을 할당
#         preview_url = f"/nas/spirit/DB/thum/3d_assets{image_files[i % len(image_files)]}"
        
#         # 업데이트 쿼리
#         asset_collection.update_one(
#             {"_id": asset["_id"]},  # 자산을 식별할 수 있는 조건 (_id)
#             {"$set": {"preview_url": preview_url}}  # preview_url 업데이트
#         )

#     print("3D Model 타입 자산의 preview_url을 업데이트했습니다.")

"""머티리얼 이미지 삽입 공장"""
# def generate_asset_data():
#     # 'Material'인 자산을 업데이트
#     image_files = [
#         "fabric_material_preview.png",
#         "moss_material_preview.png",
#         "gold_material_preview.png",
#         "stone_material_preview.png",
#         "leaf_material_preview.png",
#         "wood_material_preview.png",
#         "metal_material_preview.png"
#     ]
    
#     descriptions = {
#         "fabric_material": "A soft and versatile fabric material, perfect for clothing or interior designs.",
#         "moss_material": "A natural moss material, ideal for creating lush environments in 3D models.",
#         "gold_material": "A shiny and luxurious gold material, suitable for creating high-end objects and jewelry.",
#         "stone_material": "A rugged and durable stone material, perfect for creating rocky surfaces or ancient ruins.",
#         "leaf_material": "A detailed and realistic leaf material, ideal for creating vibrant foliage in nature scenes.",
#         "wood_material": "A rich, textured wood material, perfect for creating furniture or outdoor structures.",
#         "metal_material": "A strong and reflective metal material, ideal for industrial objects or futuristic designs."
#     }
    
#     for i, asset in enumerate(asset_collection.find({"asset_type": "Material"})):
#         # 순차적으로 이미지 파일명과 설명을 할당
#         material_type = image_files[i % len(image_files)].replace("_preview.png", "")  # 파일명에서 _preview.png 제거하여 material_type 추출
#         preview_url = f"/nas/spirit/DB/thum/material/{image_files[i % len(image_files)]}"  # preview_url 경로 설정
#         asset_name = material_type  # 이름을 material_type으로 설정
#         description = descriptions.get(material_type, "No description available.")  # 설명 설정
        
#         # 업데이트 쿼리
#         asset_collection.update_one(
#             {"_id": asset["_id"]},  # 자산을 식별할 수 있는 조건 (_id)
#             {
#                 "$set": {
#                     "preview_url": preview_url,
#                     "name": asset_name,
#                     "description": description
#                 }
#             }
#         )

#     print("Material 타입 자산의 preview_url, name, description을 업데이트했습니다.")
# generate_asset_data()

"""HDRI 이미지"""
# def generate_asset_data():
#     # 'HDRI' 자산을 업데이트
#     hdri_files = [
#         {"name": "light_indoor", "preview": "light_indoor_hdri_preview.png", "applyhdri": "light_indoor_addhdri.png", "hdri": "light_indoor_hdri.png"},
#         {"name": "night", "preview": "night_hdri_preview.png", "applyhdri": "night_addhdri.png", "hdri": "night_hdri.png"},
#         {"name": "sun", "preview": "sun_hdri_preview.png", "applyhdri": "sun_addhdri.png", "hdri": "sun_hdri.png"}
#     ]
    
#     descriptions = {
#         "light_indoor": "A bright and warm indoor HDRI, ideal for simulating daylight in interior scenes.",
#         "night": "A dark and moody HDRI, perfect for creating night-time atmospheres in outdoor or indoor environments.",
#         "sun": "A high contrast HDRI with sunlight for realistic outdoor scenes, ideal for daylight simulations."
#     }

#     for i, asset in enumerate(asset_collection.find({"asset_type": "HDRI"})):
#         # 각 HDRI 파일에 대해 순차적으로 데이터 할당
#         hdri_data = hdri_files[i % len(hdri_files)]  # HD리 파일명 순서대로 가져옴
        
#         preview_url = f"/nas/spirit/DB/thum/hdri/{hdri_data['preview']}"  # preview_url 경로 설정
#         applyhdri_url = f"/nas/spirit/DB/thum/hdri/{hdri_data['applyhdri']}"  # applyhdri_url 경로 설정
#         hdri_url = f"/nas/spirit/DB/thum/hdri/{hdri_data['hdri']}"  # hdri_url 경로 설정
        
#         asset_name = hdri_data["name"]  # 이름을 hdri_data['name']으로 설정
#         description = descriptions.get(hdri_data["name"], "No description available.")  # 설명 설정
        
#         # 업데이트 쿼리
#         asset_collection.update_one(
#             {"_id": asset["_id"]},  # 자산을 식별할 수 있는 조건 (_id)
#             {
#                 "$set": {
#                     "preview_url": preview_url,
#                     "applyhdri_url": applyhdri_url,
#                     "hdri_url": hdri_url,
#                     "name": asset_name,
#                     "description": description
#                 }
#             }
#         )

#     print("HDRI 타입 자산의 preview_url, applyhdri_url, hdri_url, name, description을 업데이트했습니다.")

# generate_asset_data()






"""조건에 해당하는 파일 넣기"""
# def generate_refactory_data():
#     # metal과 grill에 대한 파일 목록 설정
#     metal_presetting_files = [f"metal_presetting_{i:03}.png" for i in range(0, 3)]
#     metal_preview = "metal_texture_preview.png"
#     metal_detail = "metal_texture_detail.png"

#     grill_presetting_files = [f"grill_presetting_{i:03}.png" for i in range(0, 3)]
#     grill_preview = "grill_texture_preview.png"
#     grill_detail = "grill_texture_detail.png"

#     # asset_collection에서 "Texture" 타입의 자산을 가져오기
#     for i, asset in enumerate(asset_collection.find({"asset_type": "Texture"})):
#         if asset["asset_type"] == "Texture":  # "Texture" 타입 자산만 처리
#             # 랜덤으로 "metal" 또는 "grill"을 선택
#             asset_type = random.choice(["metal", "grill"])

#             if asset_type == "metal":
#                 presetting_files = metal_presetting_files
#                 preview_url = f"/nas/spirit/DB/thum/texture/{metal_preview}"
#                 detail_files = f"/nas/spirit/DB/thum/texture/{metal_detail}"
#             elif asset_type == "grill":
#                 presetting_files = grill_presetting_files
#                 preview_url = f"/nas/spirit/DB/thum/texture/{grill_preview}"
#                 detail_files = f"/nas/spirit/DB/thum/texture/{grill_detail}"

#             # 업데이트할 데이터 준비
#             update_data = {
#                 "$set": {
#                     "preview_url": preview_url,  # 기존 preview_url 업데이트
#                     "presetting_url1": f"/nas/spirit/DB/thum/texture/{presetting_files[0]}",  # 첫 번째 presetting_url
#                     "presetting_url2": f"/nas/spirit/DB/thum/texture/{presetting_files[1]}",  # 두 번째 presetting_url
#                     "presetting_url3": f"/nas/spirit/DB/thum/texture/{presetting_files[2]}",  # 세 번째 presetting_url
#                     "detail_url": detail_files,  # 첫 번째 detail_url
#                 }
#             }

#             # 자산 데이터를 업데이트
#             asset_collection.update_one(
#                 {"_id": asset["_id"]},  # 자산의 _id로 해당 자산을 찾아서
#                 update_data  # 필드들을 업데이트
#             )

#             print(f"{asset['name']} 자산의 preview_url, presetting_url, detail_url을 {asset_type}로 업데이트했습니다.")
# generate_refactory_data()

"""우리 칑구 특정 데이터 삭제"""
# def delete_refactory_data():
#     # asset_collection에서 "Texture" 타입의 자산을 가져오기
#     for i, asset in enumerate(asset_collection.find({"asset_type": "Texture"})):
#         if asset["asset_type"] == "Texture":  # "Texture" 타입 자산만 처리
#             # 업데이트할 데이터 준비 (필드 삭제)
#             delete_data = {
#                 "$unset": {
#                     "preview_url": "",  # preview_url 삭제
#                     "presetting_url1": "",  # presetting_url 삭제
#                     "presetting_url2": "",  # presetting_url 삭제
#                     "presetting_url3": "",  # presetting_url 삭제
#                     "detail_url": "",  # detail_url 삭제
#                     # "particular_url": ""
#                 }
#             }

#             # 자산 데이터를 업데이트하여 필드 삭제
#             asset_collection.update_one(
#                 {"_id": asset["_id"]},  # 자산의 _id로 해당 자산을 찾아서
#                 delete_data  # 필드 삭제
#             )

#             print(f"{asset['name']} 자산에서 preview_url, presetting_url, detail_url을 삭제했습니다.")
# delete_refactory_data()

def cart_refactory_data():
    category = "Prop"

    update_data = {
        "$set": {
            "category": category  # ✅ 기존 category 값을 업데이트
        }
    }

    result = asset_collection.update_many(
        {"category": "Props"},  # ✅ "Props"인 문서 찾기
        update_data
    )

    print(f"업데이트된 문서 수: {result.modified_count}")  # ✅ 변경된 문서 개수 출력

cart_refactory_data()



        



"""이미지 경로 변경"""
# def generate_asset_data():
#     # 이미지 파일명을 thum001.png ~ thum031.png 까지 순차적으로 설정
#     image_files = [f"thum{i:03}.png" for i in range(1, 32)]  # thum001.png ~ thum031.png 리스트 생성

#     # '3D Model'인 자산을 업데이트
#     for i, asset in enumerate(asset_collection.find({"asset_type": "Texture"})):
#         # 순차적으로 이미지 파일명을 할당 (파일 경로에 슬래시 추가)
#         preview_url = f"/nas/spirit/DB/thum/texture/{image_files[i % len(image_files)]}"
        
#         # 필요한 다른 URL도 계산 (presetting_url, detail_url 등)
#         presetting_url1 = f"/nas/spirit/DB/thum/texture/{image_files[i % len(image_files)]}"
#         presetting_url2 = f"/nas/spirit/DB/thum/texture/{image_files[(i + 1) % len(image_files)]}"
#         presetting_url3 = f"/nas/spirit/DB/thum/texture/{image_files[(i + 2) % len(image_files)]}"
#         detail_url = f"/nas/spirit/DB/thum/texture/{image_files[(i + 3) % len(image_files)]}"

#         # 업데이트할 데이터 준비
#         update_data = {
#             "$set": {
#                 "preview_url": preview_url,  # 기존 preview_url 업데이트
#                 "presetting_url1": presetting_url1,  # 첫 번째 presetting_url 업데이트
#                 "presetting_url2": presetting_url2,  # 두 번째 presetting_url 업데이트
#                 "presetting_url3": presetting_url3,  # 세 번째 presetting_url 업데이트
#                 "detail_url": detail_url  # detail_url 업데이트
#             }
#         }

#         # 자산 데이터를 업데이트
#         asset_collection.update_one(
#             {"_id": asset["_id"]},  # 자산의 _id로 해당 자산을 찾아서
#             update_data  # 필드들을 업데이트
#         )

#     print("3D Model 타입 자산의 preview_url, presetting_url, detail_url을 업데이트했습니다.")
# generate_asset_data()

# 업데이트할 .mp4 파일 목록
mp4_files = [
7 Chair.usd    2 Mixer.usd             9 SaltShaker.usd     StoolWooden.usd
Cheerio.usd  1 PaperBagCrumpled.usd  12 SoapDispenser.usd  6 TeaKettle.usd
3 Jar.usd      8 Pot.usd               11 SpiceShaker.usd    4 WoodenDryingRack.usd

]
/nas/spirit/DB/usd
# .mp4 확장자를 제거한 이름 매핑 (언더바를 공백으로 변환)
mp4_mapping = {file_name.replace("_", " ").replace(".mp4", ""): file_name for file_name in mp4_files}

def update_3d_model_urls():
    # "3D Model" 타입의 자산 조회
    for asset in asset_collection.find({"asset_type": "3D Model"}):
        asset_name = asset.get("source_url", "")
        if asset_name in mp4_mapping:  # 이름이 매핑에 존재하면 업데이트
            
            update_data = {
                "$set": {
                    "source_url": turnaround_url  # URL 업데이트
                }
            }

            asset_collection.update_one({"_id": asset["_id"]}, update_data)
            print(f"Updated '{asset_name}' with turnaround_url: {turnaround_url}")

    print("3D Model 타입 자산의 turnaround_url 업데이트 완료.")

# 함수 실행
update_3d_model_urls()

"""인덱스 생성 및 수정 중"""
def update_3d_model_urls():
    for asset in asset_collection.find({"asset_type": "3D Model"}):
        turnaround_url = asset.get("turnaround_url")
        rig_url = asset.get("rig_url")

        # image_url 리스트 생성 (None 값 제외)
        image_urls = [url for url in [turnaround_url, rig_url] if url]

        update_data = {
            "$set": {
                "image_url": image_urls,  # 통합된 URL 리스트
                "source_url": None  # 필요에 따라 적절한 값 설정
            },
            "$unset": {
                "turnaround_url": "",  # 기존 필드 삭제 
                "rig_url": ""
            }
        }

        asset_collection.update_one({"_id": asset["_id"]}, update_data)
        print(f"Updated asset {asset['_id']} with image_url: {image_urls}")


    print("3D Model 타입 자산의 image_url 업데이트 완료.")
update_3d_model_urls()


"""Texture 인덱스 생성 및 수정 중"""
def update_texture_urls():
    for asset in asset_collection.find({"asset_type": "Texture"}):
        detail_url = asset.get("detail_url")
        presetting_url1 = asset.get("presetting_url1")
        presetting_url2 = asset.get("presetting_url2")
        presetting_url3 = asset.get("presetting_url3")

        # image_url 리스트 생성 (None 값 제외)
        image_urls = [url for url in [detail_url, presetting_url1, presetting_url2, presetting_url3] if url]

        update_data = {
            "$set": {
                "image_url": image_urls,  # 통합된 URL 리스트
                "source_url": None  # 필요에 따라 적절한 값 설정
            },
            "$unset": {
                "detail_url": "",  # 기존 필드 삭제 
                "presetting_url1": "",
                "presetting_url2": "",
                "presetting_url3": ""
            }
        }

        asset_collection.update_one({"_id": asset["_id"]}, update_data)
        print(f"Updated asset {asset['_id']} with image_url: {image_urls}")


    print("3D Model 타입 자산의 image_url 업데이트 완료.")
update_texture_urls()

"""HDRI 인덱스 생성 및 수정 중"""
def update_hdri_urls():
    for asset in asset_collection.find({"asset_type": "HDRI"}):
        applyhdri_url = asset.get("applyhdri_url")
        hdri_url = asset.get("hdri_url")

        # image_url 리스트 생성 (None 값 제외)
        image_urls = [url for url in [applyhdri_url, hdri_url] if url]

        update_data = {
            "$set": {
                "image_url": image_urls,  # 통합된 URL 리스트
                "source_url": None  # 필요에 따라 적절한 값 설정
            },
            "$unset": {
                "applyhdri_url": "",  # 기존 필드 삭제 
                "hdri_url": ""
            }
        }

        asset_collection.update_one({"_id": asset["_id"]}, update_data)
        print(f"Updated asset {asset['_id']} with image_url: {image_urls}")


    print("3D Model 타입 자산의 image_url 업데이트 완료.")
update_hdri_urls()

"""Material 인덱스 생성 및 수정 중"""
def update_material_urls():
    for asset in asset_collection.find({"asset_type": "Material"}):
        material_urls = asset.get("material_urls")

        # 업데이트할 데이터 정의
        update_data = {
            "$set": {
                "image_url": material_urls,  # material_urls을 그대로 image_url로 변경
                "source_url": None  # 필요에 따라 적절한 값 설정
            },
            "$unset": {
                "material_urls": ""  # 기존 material_urls 필드 삭제
            }
        }

        asset_collection.update_one({"_id": asset["_id"]}, update_data)
        print(f"Updated asset {asset['_id']} with image_url: {material_urls}")

    print("Material 타입 자산의 image_url 업데이트 완료.")

# 실행
update_material_urls()


"""모든 인덱스 삭제"""
# asset_collection.drop_indexes()
# print("모든 인덱스 삭제 완료")

"""인덱스 목록 확인"""
# indexes = asset_collection.index_information()
# print("현재 인덱스 목록:")
# for index_name, index_info in indexes.items():
#     print(f"{index_name}: {index_info}"




"""이미지 경로 변경"""
# image_files와 해당하는 이미지 파일 매핑
# def update_material():
#     # image_files_mapping 정의 (이제 preview.png는 제외하고 material_url만 포함)
#     image_files_mapping = {
#         "fabric_material": [
#             "fabric_material_albedo.png", 
#             "fabric_material_normal.png", 
#             "fabric_material_ao.png", 
#             "fabric_material_roughness.png", 
#             "fabric_material_height.png"
#         ],
#         "moss_material": [
#             "moss_material_albedo.png", 
#             "moss_material_normal.png", 
#             "moss_material_ao.png", 
#             "moss_material_height.png"
#         ],
#         "gold_material": [
#             "gold_material_albedo.png", 
#             "gold_material_normal.png", 
#             "gold_material_ao.png", 
#             "gold_material_height.png", 
#             "gold_material_roughness.png"
#         ],
#         "stone_material": [
#             "stone_material_albedo.png", 
#             "stone_material_normal.png", 
#             "stone_material_ao.png", 
#             "stone_material_height.png", 
#             "stone_material_roughness.png"
#         ],
#         "leaf_material": [
#             "leaf_material_albedo.png", 
#             "leaf_material_normal.png", 
#             "leaf_material_ao.png", 
#             "leaf_material_height.png", 
#             "leaf_material_roughness.png"
#         ],
#         "wood_material": [
#             "wood_material_height.png", 
#             "wood_material_metallic.png", 
#             "wood_material_normal.png", 
#             "wood_material_roughness.png"
#         ],
#         "metal_material": [
#             "metal_material_basecolor.png", 
#             "metal_material_normal.png", 
#             "metal_material_roughness.png"
#         ]
#     }

#     # "asset_type"이 "Material"인 항목들 찾기
#     materials = asset_collection.find({"asset_type": "Material"})

#     # 각 항목에 대해 material_url 업데이트
#     for material in materials:
#         name = material.get("name")
        
#         # 해당 name이 매핑에 있으면
#         if name in image_files_mapping:
#             # 해당 이름에 맞는 이미지 경로들 만들기 (preview.png 제외)
#             material_urls = [f"/nas/spirit/DB/thum/material/{image}" for image in image_files_mapping[name]]
            
#             # 해당 문서에 material_urls 필드 추가
#             result = asset_collection.update_one(
#                 {"_id": material["_id"]},
#                 {"$set": {"material_urls": material_urls}}  # material_urls로 필드 이름 변경
#             )
            
#             # 업데이트 성공 여부 확인
#             print(f"Updated {name}: {result.acknowledged}")

#     print("material_urls 업데이트 완료!")

#     # 업데이트 후 바로 확인
# updated_material = asset_collection.find_one({"asset_type": "Material"})
# print(updated_material["material_urls"])  # 이 부분에서 배열로 저장된 값이 출력될 것입니다.

# update_material()