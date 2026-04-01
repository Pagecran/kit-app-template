import os
import uuid

def generate_wxs(source_dir, output_file, component_group_id, directory_ref_id):
    wxs_content = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<Wix xmlns="http://wixtoolset.org/schemas/v4/wxs">',
        f'  <Fragment>',
        f'    <ComponentGroup Id="{component_group_id}">',
    ]
    
    directory_structure = []
    components = []
    
    def process_dir(current_dir, current_dir_id):
        nonlocal directory_structure, components
        for item in os.listdir(current_dir):
            item_path = os.path.join(current_dir, item)
            
            # Create a truly short ID strictly <= 72 characters
            # UUID is 32 chars, we keep a prefix so max length is well under 72
            short_id = uuid.uuid4().hex
            
            if os.path.isdir(item_path):
                dir_id = f"D_{short_id}"
                directory_structure.append(f'      <Directory Id="{dir_id}" Name="{item}">')
                process_dir(item_path, dir_id)
                directory_structure.append(f'      </Directory>')
            else:
                comp_id = f"C_{short_id}"
                file_id = f"F_{short_id}"
                
                # Use relative path from the build dir
                rel_path = os.path.relpath(item_path, "_build")
                
                components.append((current_dir_id, comp_id, file_id, item_path))
                
    directory_structure.append(f'      <DirectoryRef Id="{directory_ref_id}">')
    process_dir(source_dir, directory_ref_id)
    directory_structure.append(f'      </DirectoryRef>')

    for dir_id, comp_id, file_id, item_path in components:
        wxs_content.append(f'      <Component Id="{comp_id}" Directory="{dir_id}" Guid="*">')
        wxs_content.append(f'        <File Id="{file_id}" Source="{item_path}" KeyPath="yes" />')
        wxs_content.append(f'      </Component>')

    wxs_content.append(f'    </ComponentGroup>')
    wxs_content.append(f'  </Fragment>')
    wxs_content.append(f'</Wix>')
    
    # Needs a separate fragment for directories that are not INSTALLFOLDER
    wxs_content_dirs = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<Wix xmlns="http://wixtoolset.org/schemas/v4/wxs">',
        f'  <Fragment>',
    ]
    wxs_content_dirs.extend(directory_structure)
    wxs_content_dirs.append(f'  </Fragment>')
    wxs_content_dirs.append(f'</Wix>')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(wxs_content))
        
    with open(output_file.replace('.wxs', '_dirs.wxs'), 'w', encoding='utf-8') as f:
        f.write("\n".join(wxs_content_dirs))

generate_wxs('_build/package_unzipped', '_build/HarvestedFiles.wxs', 'HarvestedFiles', 'INSTALLFOLDER')
