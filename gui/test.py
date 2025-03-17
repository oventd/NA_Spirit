
asset_list=[{'_id': ObjectId('67d422060172b3b1c9c086be'), 
  'asset_id': '753', 'name': 'Fine Wire Mesh', 
  'description': 'A stretched, diamond-patterned metal mesh with high durability.', 'asset_type': 'Texture', 'category': 'Weapon', 'style': 'Realistic', 'resolution': '512x512', 'file_format': 'JPG', 'size': '243MB', 'license_type': 'Free', 'creator_id': '8220', 'creator_name': 'Liam Scott', 'downloads': 444, 'created_at': datetime.datetime(2024, 12, 27, 7, 18, 29, 240000), 'updated_at': datetime.datetime(2024, 12, 27, 7, 18, 29, 240000), 'preview_url': '/nas/spirit/DB/thum/texture/grill_texture_preview.png', 'image_url': ['/nas/spirit/DB/thum/texture/grill_texture_detail.png', '/nas/spirit/DB/thum/texture/grill_presetting_000.png', '/nas/spirit/DB/thum/texture/grill_presetting_001.png', '/nas/spirit/DB/thum/texture/grill_presetting_002.png'], 'source_url': None, 'video_url': None}]

asset_dict = {str(asset["_id"]): asset["name"] for asset in asset_list}
print(asset_dict)
        

