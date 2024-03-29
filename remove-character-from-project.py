import os.path
import sys
from manu.fn import *


def main(game_project_dir_path):
    resource_pack_file_path = os.path.join(game_project_dir_path, 'resource-pack.json')
    with open(resource_pack_file_path, 'r') as resource_pack_file:
        resource_pack_data = json.load(resource_pack_file)
        resource_pack_data['animations']['map'] = []
        resource_pack_data['characters']['map'] = []
        resource_pack_data['stateMachines']['map'] = []
        resource_pack_data['defaultCharacterId']['uuid'] = '00000000-0000-0000-0000-000000000000'
        resource_pack_data['defaultStateMachineId']['uuid'] = '00000000-0000-0000-0000-000000000000'

    scene_id = get_first_scene_id_from_resource_pack_data(resource_pack_data)
    scene_file_path = os.path.join(game_project_dir_path, 'scenes/{0}.json'.format(scene_id))

    with open(scene_file_path, 'r') as scene_file:
        scene_data = json.load(scene_file)

        nodes = scene_data['nodes']
        for node in nodes:
            obj = node['object3D']
            if 'spawner' in obj:
                character_script_id = obj['spawner']['characterScriptId']['uuid']
                break

        scripts = scene_data['scriptSystem']['scripts']
        scene_data['scriptSystem']['scripts'] = list(filter(lambda script: script['@class'] != 'MainCharacterScript' and script['@class'] != 'TimeLineScript', scripts))

    camera_follow_script_id = find_camera_follow_script_id(scripts)
    camera_follow_script_path = os.path.join(game_project_dir_path, 'scripts/{0}.json'.format(camera_follow_script_id))

    with open(camera_follow_script_path, 'r') as camera_follow_script_file:
        camera_follow_script_data = json.load(camera_follow_script_file)
        camera_follow_script_data['objectToFollow']['uuid'] = find_object_id_by_name(scene_data['nodes'], 'Item 1')

    with open(resource_pack_file_path, 'w') as resource_pack_file:
        json.dump(resource_pack_data, resource_pack_file, indent=4, sort_keys=False)

    with open(scene_file_path, 'w') as scene_file:
        json.dump(scene_data, scene_file, indent=4, sort_keys=False)

    with open(camera_follow_script_path, 'w') as camera_follow_script_file:
        json.dump(camera_follow_script_data, camera_follow_script_file, indent=4, sort_keys=False)


if __name__ == '__main__':
    main(sys.argv[1])