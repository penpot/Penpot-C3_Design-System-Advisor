import re
import argparse
import warnings
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import os

def get_svg_components_in_assets(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    component_ids = set()
    for tag in ['symbol']:
        for match in re.finditer(f'<{tag}[^>]*id="([^"]+)"', content):
            component_ids.add(match.group(1))
    return component_ids

def get_svg_components_in_pages(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Define the regular expression pattern to search for component-ids
    pattern = r'penpot:component-id="([\w-]+)"'

    # Find all component-ids in the SVG content
    component_ids = re.findall(pattern, content)

    # Convert the list of component-ids to a set to remove duplicates
    component_ids = set(component_ids)
    return component_ids

def find_unused_components(opt):
    components = get_svg_components_in_assets(opt.components_svg_dir)
    used_components = get_svg_components_in_pages(opt.page_svg_dir)
    unused_components = components - used_components
    return unused_components, used_components

def extract_title_by_symbol_id(symbol_id, svg_content):
    # Define the regular expression pattern to search for the symbol with the specified id
    pattern = r'<symbol[^>]*id="{}"[^>]*>[\s\S]*?<title>([^<]+)</title>'.format(symbol_id)

    # Search for the symbol and title in the SVG content
    match = re.search(pattern, svg_content)

    # If a match is found, return the title, otherwise return None
    if match:
        return match.group(1)
    else:
        return None

def print_unused_component_name(opt):

    print("Unused components:", len(opt.unused_components))
    print("Used components:", len(opt.used_components))

    with open(opt.components_svg_dir) as file:
        content = file.read()

    for symbol_id in opt.used_components:
        title = extract_title_by_symbol_id(symbol_id, content)
        # Print the extracted title
        if title:
            print("Used Title:", title)
        else:
            warnings.warn("Symbol id not found: {}".format(symbol_id))

def extract_text_regions_and_sizes(svg_content):
    # Define the regular expression pattern to search for <text> elements and their font sizes

    pattern = r'<text[^>]*font-size:([^px;]+)px;[^>]*>([^<]+)</text>' #r'<text[^>]*>([^<]+)</text>' #'<text[^>]*font-size="(\d+(\.\d+)?)".*?>([^<]+)</text>'
    
    # Find all text regions and their font sizes in the SVG content
    text_regions_and_sizes = re.findall(pattern, svg_content)
    return text_regions_and_sizes

def parse_text_holder(opt):
    # Read the SVG file content
    with open(opt.page_svg_dir, "r") as file:
        svg_content = file.read()

    # Extract the text regions and their font sizes from the SVG content
    text_regions_and_sizes = extract_text_regions_and_sizes(svg_content)

    # Sort the text regions and sizes by font size in descending order
    text_regions_and_sizes_sorted = sorted(text_regions_and_sizes, key=lambda x: float(x[0]), reverse=True)

    # Print the sorted text regions and sizes
    print("overall text counts: {}".format(len(text_regions_and_sizes_sorted)))
    for font_size, text in text_regions_and_sizes_sorted:
        print("font-size {:7s}, Text Region: {}".format(font_size, text))

def run_svgoptim(input_fule_name, output_file_name):
    """
        Run svgo as a command line in Python
        For example ! svgo -i "../data/Bottom App Bar.svg" -o "../data/Bottom App Bar Opt.svg"
    """
    os.system(f"svgo -i {input_fule_name} -o {output_file_name}")

def remove_style(svg_file_path, output_file_path):
    # Parse the SVG file as an ElementTree object
    svg_root = ET.parse(svg_file_path).getroot()

    # Find the style element
    style_element = svg_root.find('.//{http://www.w3.org/2000/svg}style')

    # If the style element is found, remove its contents
    if style_element is not None:
        style_element.clear()

    # Remove namespace prefixes from tags
    for elem in svg_root.iter():
        elem.tag = elem.tag.split('}')[-1]

    # Serialize the modified ElementTree object to an SVG file
    with open(output_file_path, 'w') as f:
        f.write(ET.tostring(svg_root, encoding='unicode'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--page_svg_dir", default= "id.svg")
    parser.add_argument("--components_svg_dir", default= "components.svg")
    parser.add_argument("--parse_text", action='store_true')
    parser.add_argument("--parse_components", action='store_true')
    parser.add_argument("--optimize", action='store_true')
    opt = parser.parse_args()

    if opt.parse_components:
        opt.unused_components, opt.used_components = find_unused_components(opt)
        print_unused_component_name(opt)

    if opt.parse_text:
        parse_text_holder(opt)

    if opt.optimize:
        remove_style(opt.page_svg_dir, "output.svg")
        run_svgoptim("output.svg", "output_svgo.svg")