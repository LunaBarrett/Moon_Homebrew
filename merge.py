import json
import glob
import time
import pathlib
from datetime import datetime

def build_json(files):
    output = {}
    for f in files:

        # Get time file was last modifed, to be used as version
        file_modified_time = pathlib.Path(f).stat().st_mtime
        version = datetime.utcfromtimestamp(file_modified_time).strftime('%Y.%m.%d.%H.%M')

        # Build merged json from all given source jsons, extending rather than replacing where needed
        with open(f, 'r', encoding="ascii", errors="replace") as infile:
            data = json.load(infile)
            for k in data.keys():
                if k in output.keys():
                    if k == "$schema":
                        continue
                    elif k == "_meta":
                        for source in data[k]["sources"]:
                            source["version"] = version
                        output[k]["sources"].extend(data[k]["sources"])
                    else:
                        output[k].extend(data[k])
                else:
                    data["_meta"]["sources"][0]["version"] = version
                    output[k] = data[k]
                    
    output["_meta"]["dateLastModified"] = time.time()
    return output

def write_to_file(filename, data):
    with open(filename, 'w') as output_file:
        json.dump(data, output_file, indent=4)

# Get file lists
# Conditions = glob.glob("Source/Conditions/All_Conditions.json")
Items = glob.glob("Source/Items/All_Items.json")
# Monsters = glob.glob("Source/Monsters/All_Monsters.json")
# Backgrounds = glob.glob("Source/Player_Centric/Backgrounds/All_Backgrounds.json")
# Classes = glob.glob("Source/Player_Centric/Classes/All_Classes.json")
# Feats = glob.glob("Source/Player_Centric/Feats/All_Feats.json")
# Races = glob.glob("Source/Races/All_Races.json")
# Spells = glob.glob("Source/Spells/All_Spells.json")
# All_Homebrew = Conditions + Items + Monsters + Backgrounds + Classes + Feats + Races + Spells
All_Homebrew = Items

# Get data and write
# write_to_file("Merged/Moon_Conditions.json", build_json(Conditions))
# write_to_file("Merged/Moon_Items.json", build_json(Items))
# write_to_file("Merged/Moon_Monsters.json", build_json(Monsters))
# write_to_file("Merged/Moon_Backgrounds.json", build_json(Backgrounds))
# write_to_file("Merged/Moon_Classes.json", build_json(Classes))
# write_to_file("Merged/Moon_Feats.json", build_json(Feats))
# write_to_file("Merged/Moon_Races.json", build_json(Races))
# write_to_file("Merged/Moon_Spells.json", build_json(Spells))
write_to_file("Merged/Moon_All_Homebrew.json", build_json(All_Homebrew))