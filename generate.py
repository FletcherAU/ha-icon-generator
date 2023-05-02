# Converts a directory of SVGs to a single JS file suitable for Home Assistant

import os
import json
import sys
import xml.etree.ElementTree as ET
from typing import Tuple

if len(sys.argv) != 3:
    print("generate.py <directory> <prefix>")
    sys.exit(1)
else:
    prefix = sys.argv[2]
    directory = sys.argv[1]

# Extract paths from svg
def extract_data(svg: str) -> Tuple[str, str]:
    root = ET.fromstring(svg)

    for child in root:
        if child.tag.split('}')[-1] == "g":
            for child2 in child:
                if 'd' in child2.attrib:
                    path = child2.attrib['d']
        elif child.tag.split('}')[-1] == "path":
            if 'd' in child.attrib:
                path = child.attrib['d']

    try:
        viewbox = root.attrib['viewBox']
    except:
        viewbox = "0 0 24.0 24.0"

    return path, viewbox

js = """async function getIcon(name) {
  if (!(name in icons)) {
    console.log(`Icon "${name}" not available`);
    return '';
  }

  var svgDef = icons[name];
  var primaryPath = svgDef[1];
  return {
    path: primaryPath,
    viewBox: svgDef[0]
  }

}

async function getIconList() {
  return Object.entries(icons).map(([icon]) => ({
    name: icon
  }));
}

window.customIconsets = window.customIconsets || {};
window.customIconsets["PREFIX"] = getIcon;

window.customIcons = window.customIcons || {};
window.customIcons["PREFIX"] = { getIcon, getIconList };"""


icons = {}

# Open each file in the svg folder
for filename in os.listdir(directory):
    # Ignore non-svg files
    if not filename.endswith('.svg'):
        continue
    # Open the file
    with open(os.path.join(directory, filename), 'r') as f:
        # Read the file
        svg = f.read()

        # Extract the paths and viewbox
        data = extract_data(svg)
        icons[filename.split(".")[0]] = [data[1], data[0]]

s = json.dumps(icons, indent=4)

with open(f"{prefix}-icons.js","w") as f:
    f.write("var icons = ")
    f.write(s)
    f.write("\n")
    f.write(js.replace("PREFIX",prefix))