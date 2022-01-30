dirs=(\
    'plywood'\
    'rough_plasterbrick_05'\
    'kitchen_wood'\
    'leather_red_02'\
    'denmin_fabric_02'\
    'aerial_grass_rock'\
    'leather_white'\
    'brown_leather'\
    'book_pattern'\
    'fabric_pattern_07'\
    'leather_red_03'\
    'fabric_pattern_05'\
    'floor_tiles_02'\
    'fabric_leather_01'\
    'rock_ground'\
    'church_bricks_02'\
    'denim_fabric'\
    'fabric_leather_02'\
    'rock_ground_02'\
    'rough_plaster_brick_04'\
    'ground_grey'\
    'castle_brick_02_red'\
    'dry_ground_rocks'\
    'large_square_pattern_01'\
    'church_bricks_03'\
    'concrete_floor_painted'\
    'brown_mud_leaves_01'\
    'plaster_grey_04'\
    'marble_01'\
    'large_floor_tiles_02'\
    'coral_gravel'\
    'dirt_aerial_02'\
    'forrest_ground_01'\
    'castle_wall_slates'\
    'ceramic_roof_01'\
    'dry_ground_01'\
    'castle_brick_07'\
    'rough_block_wall'\
    'aerial_ground_rock'\
    'large_sandstone_blocks_01'\
    'concrete_floor_02'\
    'dirt_aerial_03'\
    'factory_brick'\
    'cobblestone_floor_01'\
    'roof_slates_03'\
    'large_grey_tiles'\
    'planks_brown_10'\
    'brown_planks_05'\
    'white_plaster_03'\
    'white_plaster_02'\
    'rusty_metal_02'\
    'brown_planks_03'\
    'rock_04'\
    'snow_02'\
    'cobblestone_floor_04'\
    'rough_plaster_03'\
    'medieval_blocks_06'\
    'old_planks_02'\
    'bark_brown_02'\
    'aerial_sand'\
    'concrete_floor_01'\
    'large_red_bricks'\
    'brick_4'\
    'floor_tiles_06'\
    'castle_wall_varriation'\
    'castle_brick_broken_06'\
    'sandstone_blocks_05'\
    'metal_plate'\
    'medieval_blocks_05'\
    'cobblestone_large_01'\
    'green_metal_rust'\
    'castle_brick_01'\
    'grey_plaster_03'\
    'bark_brown_01'\
    'brown_mud_dry'\
    'pavement_01'\
    'coral_ground_02'\
    'rough_wood'\
    'floor_tiles_08'\
    'red_brick_03'\
    'floor_pattern_02'\
    'tree_bark_03'\
    'sandstone_cracks'\
    'rock_06'\
    'reed_roof_03'\
    'concrete'\
    'rock_05'\
    'roof_slates_02'\
    'factory_wall'\
    'sand_01'\
    'brown_planks_08'\
    'snow_01'\
    'grey_roof_tiles_02'\
    'sandstone_blocks_08'\
    'rock_08'\
    'square_floor_patern_01'\
    'rock_01'\
    'castle_brick_02_white'\
    'medieval_blocks_03'\
    'grey_plaster'\
    'floor_pebbles'\
    'grass_path_2'\
    'red_mud_stones'\
    'shell_floor_01'\
    'red_slate_roof_tiles_01'\
    'floor_tiles_04'\
    'green_rough_planks'\
    'brown_mud_rocks_01'\
    'grey_plaster_02'\
    'brown_planks_07'\
    'red_bricks_02'\
    'beam_wall_01'\
    'brown_planks_09'\
    'brick_floor'\
    'brown_planks_04'\
    'blue_floor_tiles_01'\
    'roof_09'\
    'medieval_wall_01'\
    'moss_wood'\
    'red_dirt_mud_01'\
    'white_rough_plaster'\
    'cobblestone_color'\
    'sandstone_blocks_04'\
    'grey_roof_01'\
    'floor_tiles_09'\
    'red_brick_plaster_patch_02'\
    'wall_bricks_plaster'\
    'rusty_metal'\
    'burned_ground_01'\
    'white_sandstone_bricks_03'\
    'blue_painted_planks'\
    'brown_mud'\
    'pebble_ground_01'\
    'snow_05'\
    'forrest_ground_03'\
    'rough_plaster_broken'\
    'floor_pattern_01'\
    'floor_bricks_02'\
    'snow_03'\
    'brown_mud_02'\
    'terrain_red_01'\
    'reed_roof_04'\
    'grass_path_3'\
    'brown_brick_02'\
    'forrest_sand_01'\
    'cobblestone_01'\
    'yellow_bricks'\
    'coral_mud_01'\
    'yellow_plaster'\
    'yellow_brick'\
    'plaster_brick_01'\
    'brown_mud_03'\
    'random_bricks_thick'\
    'medieval_blocks_02'\
    'dark_planks'\
    'white_plaster_rough_01'\
    'rock_3'\
    'white_plaster_rough_02'\
    'cobblestone_floor_13'\
    'wooden_rough_planks'\
    'snow_04'\
    'rock_2'\
    'grey_roof_tiles'\
    'medieval_wood'\
    'cobblestone_square'\
    'Cobblestone_floor_07'\
    'white_sandstone_blocks_02'\
    'white_bricks'\
    'roof_tiles_14'\
    'rough_plaster_brick'\
    'floor_klinkers_04'\
    'cobblestone_floor_03'\
    'roof_3'\
    'roof_07'\
    'riet_01'\
    'rough_plaster_brick_02'\
    'cobblestone_floor_05'\
    'cobblestone_floor_02'\
    'cobblestone_05'\
    'floor_klinkers_01'\
    'white_sandstone_bricks'\
    'cobblestone_floor_08'\
)

mkdir /users/azerroug/scratch/blender_ressources/new_textures

for i in $(seq 0 183); do
    folder_name=${dirs[$i]}
    echo $folder_name
    wget -O /users/azerroug/scratch/blender_ressources/new_textures/${folder_name}.png https://texturehaven.com/files/textures/png/1k/${folder_name}/${folder_name}_diff_1k.png
                                                                                        # https://texturehaven.com/files/textures/png/1k/kitchen_wood/kitchen_wood_diff_1k.png
done

# https://texturehaven.com/files/textures/zip/1k/kitchen_wood/kitchen_wood_1k_png.zip