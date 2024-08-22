import re
import os

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

def convert_all_conf_files(conf_dir, plugin_dir):
    if not os.path.exists(plugin_dir):
        os.makedirs(plugin_dir)

    for conf_file in os.listdir(conf_dir):
        if conf_file.endswith('.conf'):
            conf_path = os.path.join(conf_dir, conf_file)
            plugin_path = os.path.join(plugin_dir, conf_file.replace('.conf', '.plugin'))

            conf_content = read_conf_file(conf_path)
            plugin_content = convert_conf_to_plugin(conf_content)
            save_plugin_file(plugin_content, plugin_path)
            print(f"转换成功: {conf_file} -> {plugin_path}")

if __name__ == "__main__":
    conf_dir = 'conf'  # 配置文件所在目录
    plugin_dir = 'plugin'  # 插件文件输出目录
    convert_all_conf_files(conf_dir, plugin_dir)
def save_plugin_file(content, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(content)
    # Debug: 打印出生成的内容
    print(f"Generated content for {output_path}:\n{content}\n")

