import os
import json
import xml.etree.ElementTree as ET
from typing import Dict, List
import subprocess

def get_configuration(configuration_file_path: str) -> Dict:
    data = {}
    try:
        root = ET.parse(configuration_file_path).getroot()
        for child in root:
            data[child.tag] = child.text
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except FileNotFoundError:
        print(f"Configuration file not found: {configuration_file_path}")
    return data

def load_dependencies_from_json(package_name: str, dependencies_cache: Dict[str, List[str]]) -> None:
    """Загружает зависимости пакета из JSON-файла и сохраняет их в кэше."""
    if package_name in dependencies_cache:
        return  # Если зависимости уже загружены, пропускаем

    try:
        with open(f"{package_name}.json") as f:
            package_data = json.load(f)
            dependencies_cache[package_data["name"]] = list(package_data["dependencies"].keys())
    except FileNotFoundError:
        print(f"Dependency file not found for package: {package_name}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON for package: {package_name}")

def get_dependencies(package_name: str, max_depth: int, depth=0, visited=None, dependencies_cache=None) -> List[str]:
    if visited is None:
        visited = set()
    if dependencies_cache is None:
        dependencies_cache = {}

    if depth > max_depth or package_name in visited:
        return []

    visited.add(package_name)

    # Загружаем зависимости для текущего пакета, если они еще не загружены
    load_dependencies_from_json(package_name, dependencies_cache)

    graph_lines = []
    if package_name in dependencies_cache:
        for dep in dependencies_cache[package_name]:
            # Добавляем связь только для непосредственной зависимости
            graph_lines.append(f"\"{package_name}\" -> \"{dep}\";")
            
            # Рекурсивно собираем зависимости для следующего уровня, но без добавления текущих связей
            graph_lines.extend(get_dependencies(dep, max_depth, depth + 1, visited, dependencies_cache.copy()))

    return graph_lines



def generate_dot(package_name: str, max_depth: int) -> str:
    dot = "digraph G {\n"
    dot += "\n".join(get_dependencies(package_name, max_depth))
    dot += "\n}"
    return dot

def write_result_file(result_file_path: str, dot: str):
    with open(result_file_path, 'w') as f:
        f.write(dot)

def convert_to_svg(result_file_path: str, visualizer_path: str):
    svg_output_path = f"{result_file_path.split('.')[0]}.svg"
    try:
        subprocess.run([visualizer_path, "-Tsvg", result_file_path, "-o", svg_output_path], check=True)
        print(f"SVG file generated at: {svg_output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating SVG: {e}")
    except FileNotFoundError:
        print(f"Graphviz 'dot' utility not found at path: {visualizer_path}")

def main():
    configuration = get_configuration("config.xml")

    visualizer_path = configuration["visualizer_path"]
    package_name = configuration["package_name"]
    result_file_path = configuration["result_file_path"]
    max_depth = int(configuration["max_depth"])

    dot = generate_dot(package_name, max_depth)
    write_result_file(result_file_path, dot)
    convert_to_svg(result_file_path, visualizer_path)

    print(dot)

if __name__ == '__main__':
    main()
