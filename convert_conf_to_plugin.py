import re
import os
import sys

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
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def save_plugin_file(content, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(content)

def main(input_path, output_path):
    conf_content = read_conf_file(input_path)
    plugin_content = convert_conf_to_plugin(conf_content)
    save_plugin_file(plugin_content, output_path)
    print(f"转换成功！插件文件已保存到: {output_path}")

if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.plugin"
    main(input_path, output_path)
