from datetime import datetime, timedelta
import random
from bson import ObjectId  # MongoDB에서 사용하는 ObjectId를 처리하는 데 사용
import pymongo  # MongoDB 작업을 위한 라이브러리

# MongoDB 연결
client = pymongo.MongoClient("mongodb://spirt:1234@localhost:27017/")  # 로컬 MongoDB 서버에 연결
db = client["filter_test"]  # 사용할 데이터베이스 'filter_test'에 연결
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
#         preview_url = f"/nas/spirit/DB/thum/{image_files[i % len(image_files)]}"
        
#         # 업데이트 쿼리
#         asset_collection.update_one(
#             {"_id": asset["_id"]},  # 자산을 식별할 수 있는 조건 (_id)
#             {"$set": {"preview_url": preview_url}}  # preview_url 업데이트
#         )

#     print("3D Model 타입 자산의 preview_url을 업데이트했습니다.")


def generate_refactory_data():
    # metal과 grill에 대한 파일 목록 설정
    metal_presetting_files = [f"metal_presetting_{i:03}.png" for i in range(0, 3)]
    metal_preview = "metal_texture_preview.png"
    metal_detail = "metal_texture_detail.png"

    grill_presetting_files = [f"grill_presetting_{i:03}.png" for i in range(0, 3)]
    grill_preview = "grill_texture_preview.png"
    grill_detail = "grill_texture_detail.png"

    # asset_collection에서 "Texture" 타입의 자산을 가져오기
    for i, asset in enumerate(asset_collection.find({"asset_type": "Texture"})):
        if asset["asset_type"] == "Texture":  # "Texture" 타입 자산만 처리
            # 랜덤으로 "metal" 또는 "grill"을 선택
            asset_type = random.choice(["metal", "grill"])

            if asset_type == "metal":
                presetting_files = metal_presetting_files
                preview_url = f"/nas/spirit/DB/thum/{metal_preview}"
                detail_files = f"/nas/spirit/DB/thum/{metal_detail}"
            elif asset_type == "grill":
                presetting_files = grill_presetting_files
                preview_url = f"/nas/spirit/DB/thum/{grill_preview}"
                detail_files = f"/nas/spirit/DB/thum/{grill_detail}"

            # 업데이트할 데이터 준비
            update_data = {
                "$set": {
                    "preview_url": preview_url,  # 기존 preview_url 업데이트
                    "presetting_url1": f"/nas/spirit/DB/thum/{presetting_files[0]}",  # 첫 번째 presetting_url
                    "presetting_url2": f"/nas/spirit/DB/thum/{presetting_files[1]}",  # 두 번째 presetting_url
                    "presetting_url3": f"/nas/spirit/DB/thum/{presetting_files[2]}",  # 세 번째 presetting_url
                    "detail_url": detail_files,  # 첫 번째 detail_url
                }
            }

            # 자산 데이터를 업데이트
            asset_collection.update_one(
                {"_id": asset["_id"]},  # 자산의 _id로 해당 자산을 찾아서
                update_data  # 필드들을 업데이트
            )

            print(f"{asset['name']} 자산의 preview_url, presetting_url, detail_url을 {asset_type}로 업데이트했습니다.")
generate_refactory_data()





# 우리 칑구 특정 데이터 삭제
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
