# python2
"""
For reading Json file in Mcity labeled data and save it as KITTI label format
"""

import json
label_file_dir = "/media/songanz/New Volume/data/Mcity_data/Batch4_Tagged_to_be_annotated/mcity_batch4_json_files/"
label_file_name = label_file_dir + "12_01_000031" + ".json"
with open(label_file_name) as json_data:
    data = json.load(json_data)
    tag_list = data['annotation']
    for l in tag_list:
        # refer to "labelling requirements v6_10012018.docx"
        if l['tags'][0] == 'car':
        elif l['tags'][0] == 'bicycle':
        elif l['tags'][0] == 'motorbike':
        elif l['tags'][0] == 'rider':
        elif l['tags'][0] == 'pedestrian':
        elif l['tags'][0] == 'bus':
        elif l['tags'][0] == 'truck':
        elif l['tags'][0] == 'train':
