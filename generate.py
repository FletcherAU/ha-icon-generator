# Converts a directory of SVGs to a single JS file suitable for Home Assistant

import os
import json
import sys
from pprint import pprint
from collections import defaultdict
import xml.etree.ElementTree as ET

if len(sys.argv) != 3:
    print("generate.py <directory> <prefix>")
    sys.exit(1)
else:
    prefix = sys.argv[2]
    directory = sys.argv[1]

from xml.dom import minidom

# Convert XML
def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d

# Extract paths from svg
def extract_data(svg):
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

# This script is cloned into an existing folder and should act on the parent folder instead

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