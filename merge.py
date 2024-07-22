import json
import glob
import time
import pathlib
from datetime import datetime


def prepare_comparison_source(source):
    """Return a version of the source without the version attribute, in dictionary form, for comparison."""
    return json.dumps({k:v for k,v in source.items() if k != 'version'}, sort_keys=True)

def build_json(files):
    output = {}
    for f in files:

        # Use current time as version, as there are no longer duplicate sources
        version = datetime.utcnow().strftime('%Y.%m.%d.%H.%M')

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

                        comp_new_sources = [prepare_comparison_source(source) for source in data[k]["sources"]]
                        comp_output_sources = [prepare_comparison_source(source) for source in output[k]["sources"]]

                        for new_source, original_source in zip(comp_new_sources, data[k]["sources"]):
                            if new_source not in comp_output_sources:
                                print("Adding new source")
                                output[k]["sources"].append(original_source)
                            else:
                                print("rejecting duplicate source")

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

# Elebus Campaign Sources

E_Backgrounds = glob.glob("Source\Elebus\Elebus_Backgrounds.json")
E_Classes = glob.glob("Source\Elebus\Elebus_Classes.json")
E_Conditions = glob.glob("Source\Elebus\Elebus_Conditions.json")
E_Feats = glob.glob("Source\Elebus\Elebus_Feats.json")
E_Items = glob.glob("Source\Elebus\Elebus_Items.json")
E_Monsters = glob.glob("Source\Elebus\Elebus_Monsters.json")
E_Races = glob.glob("Source\Elebus\Elebus_Races.json")
E_Spells = glob.glob("Source\Elebus\Elebus_Spells.json")
E_Variant_Rules = glob.glob("Source\Elebus\Elebus_Variant_Rules.json")
E_Homebrew = E_Backgrounds + E_Classes + E_Conditions + E_Feats + E_Items + E_Monsters + E_Races + E_Spells + E_Variant_Rules

# General Sources

Gen_Backgrounds = glob.glob("Source\General\General_Backgrounds.json")
Gen_Classes = glob.glob("Source\General\General_Classes.json")
Gen_Conditions = glob.glob("Source\General\General_Conditions.json")
Gen_Feats = glob.glob("Source\General\General_Feats.json")
Gen_Items = glob.glob("Source\General\General_Items.json")
Gen_Monsters = glob.glob("Source\General\General_Monsters.json")
Gen_Races = glob.glob("Source\General\General_Races.json")
Gen_Spells = glob.glob("Source\General\General_Spells.json")
Gen_Variant_Rules = glob.glob("Source\General\General_Variant_Rules.json")
Gen_Homebrew = Gen_Backgrounds + Gen_Classes + Gen_Conditions + Gen_Feats + Gen_Items + Gen_Monsters + Gen_Races + Gen_Spells + Gen_Variant_Rules

# Spelljammer Campaign Sources

S_Backgrounds = glob.glob("Source\Spelljammer\Spelljammer_Backgrounds.json")
S_Classes = glob.glob("Source\Spelljammer\Spelljammer_Classes.json")
S_Conditions = glob.glob("Source\Spelljammer\Spelljammer_Conditions.json")
S_Feats = glob.glob("Source\Spelljammer\Spelljammer_Feats.json")
S_Items = glob.glob("Source\Spelljammer\Spelljammer_Items.json")
S_Monsters = glob.glob("Source\Spelljammer\Spelljammer_Monsters.json")
S_Races = glob.glob("Source\Spelljammer\Spelljammer_Races.json")
S_Spells = glob.glob("Source\Spelljammer\Spelljammer_Spells.json")
S_Variant_Rules = glob.glob("Source\Spelljammer\Spelljammer_Variant_Rules.json")
S_Homebrew = S_Backgrounds + S_Classes + S_Conditions + S_Feats + S_Items + S_Monsters + S_Races + S_Spells + S_Variant_Rules


# Get data and write
All_Homebrew = Gen_Homebrew + S_Homebrew + E_Homebrew
write_to_file("Merged\Moon_Elebus_Homebrew.json", build_json(E_Homebrew))
write_to_file("Merged\Moon_General_Homebrew.json", build_json(Gen_Homebrew))
write_to_file("Merged\Moon_Spelljammer_Homebrew.json", build_json(S_Homebrew))
write_to_file("Merged/Moon_All_Homebrew.json", build_json(All_Homebrew))
