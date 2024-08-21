import re
import os
import sys
import glob

def convert_conf_to_plugin(conf_content):
    lines = conf_content.strip().split('\n')
    plugin_content = []

    patterns = {
        'metadata': {
            'name': r'^\s*#!name\s*=\s*(.*)',
            'desc': r'^\s*#!desc\s*=\s*(.*)',
            'author': r'^\s*#!author\s*=\s*(.*)',
            'homepage': r'^\s*#!homepage\s*=\s*(.*)',
            'icon': r'^\s*#!icon\s*=\s*(.*)',
            'input': r'^\s*#!input\s*=\s*(.*)',
            'select': r'^\s*#!select\s*=\s*(.*)',
            'system': r'^\s*#!system\s*=\s*(.*)',
            'system_version': r'^\s*#!system_version\s*=\s*(.*)',
            'loon_version': r'^\s*#!loon_version\s*=\s*(.*)',
            'tag': r'^\s*#!tag\s*=\s*(.*)',
        },
        'sections': {
            'argument': r'^\[Argument\]',
            'general': r'^\[General\]',
            'rule': r'^\[rule\]',
            'rewrite': r'^\[rewrite\]',
            'host': r'^\[host\]',
            'script': r'^\[script\]',
            'mitm': r'^\[mitm\]'
        }
    }

    current_section = None
    section_content = {
        'argument': [],
        'general': [],
        'rule': [],
        'rewrite': [],
        'host': [],
        'script': [],
        'mitm': []
    }

    for line in lines:
        for key, pattern in patterns['metadata'].items():
            match = re.match(pattern, line)
            if match:
                plugin_content.append(f'#!{key} = {match.group(1).strip()}')
                break

        for section, pattern in patterns['sections'].items():
            if re.match(pattern, line, re.IGNORECASE):
                current_section = section
                break

        if current_section and current_section in section_content:
            if not line.startswith("#!") and line.strip():
                section_content[current_section].append(line.strip())

    for section, content in section_content.items():
        if content:
            plugin_content.append(f'\n[{section.capitalize()}]')
            plugin_content.extend(content)

    return '\n'.join(plugin_content)

def read_conf_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"错误: 文件 {file_path} 未找到")
        return None
    except IOError as e:
        print(f"错误: 读取文件 {file_path} 时发生 IO 错误 - {e}")
        return None

def save_plugin_file(content, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except IOError as e:
        print(f"错误: 写入文件 {output_path} 时发生 IO 错误 - {e}")

def process_conf_files(input_directory, output_directory):
    os.makedirs(output_directory, exist_ok=True)
    conf_files = glob.glob(os.path.join(input_directory, '*.conf'))
    
    for conf_file in conf_files:
        plugin_file = os.path.join(output_directory, os.path.basename(conf_file).replace('.conf', '.plugin'))
        conf_content = read_conf_file(conf_file)
        if conf_content is not None:
            plugin_content = convert_conf_to_plugin(conf_content)
            save_plugin_file(plugin_content, plugin_file)
            print(f"转换成功！插件文件已保存到: {plugin_file}")

def main():
    if len(sys.argv) < 3:
        print("用法: python convert_conf_to_plugin.py <输入目录> <输出目录>")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    process_conf_files(input_directory, output_directory)

if __name__ == "__main__":
    main()
