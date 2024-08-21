import re
import os

def convert_conf_to_plugin(conf_content):
    lines = conf_content.strip().split('\n')
    metadata = {}
    rules = {'rewrite': [], 'script': [], 'mitm': []}

    # Patterns for parsing metadata
    metadata_patterns = {
        'name': re.compile(r'^\s*@ScriptName\s*(.*)'),
        'desc': re.compile(r'^\s*@Function\s*(.*)'),
        'author': re.compile(r'^\s*@Author\s*(.*)'),
        'homepage': re.compile(r'^\s*@ScriptURL\s*(.*)')
    }

    # Patterns for parsing rules
    rule_patterns = {
        'rewrite': re.compile(r'^#\s*>\s*(.*)'),
        'script': re.compile(r'^#\s*>\s*(.*)'),
        'mitm': re.compile(r'^hostname\s*=\s*(.*)')
    }

    # Parse metadata
    for line in lines:
        for key, pattern in metadata_patterns.items():
            match = pattern.search(line)
            if match:
                metadata[key] = match.group(1).strip()
                break

    # Parse rules
    section = None
    for line in lines:
        if line.strip().startswith('# >'):
            if '屏蔽' in line or '拒绝' in line:
                section = 'rewrite'
            elif '去推广' in line or '净化' in line:
                section = 'script'
            else:
                section = 'mitm'
            rules[section].append(line.split(' ', 2)[-1])
        elif line.strip().startswith('hostname='):
            rules['mitm'].extend(line.split('=')[1].split(', '))

    # Generate plugin file content
    plugin_content = []
    if metadata.get("name"):
        plugin_content.append(f'#!name = {metadata.get("name", "未知插件")}')
    if metadata.get("desc"):
        plugin_content.append(f'#!desc = {metadata.get("desc", "无描述")}')
    if metadata.get("author"):
        plugin_content.append(f'#!author = {metadata.get("author", "未知作者")}')
    if metadata.get("homepage"):
        plugin_content.append(f'#!homepage = {metadata.get("homepage", "无主页")}')
    
    if rules['rewrite']:
        plugin_content.append('\n[Rewrite]')
        plugin_content.extend(rules['rewrite'])
    
    if rules['script']:
        plugin_content.append('\n[Script]')
        plugin_content.extend(rules['script'])
    
    if rules['mitm']:
        plugin_content.append('\n[Mitm]')
        plugin_content.append(f'hostname = {", ".join(rules["mitm"])}')

    # Ensure plugin directory exists
    if not os.path.exists('plugin'):
        os.makedirs('plugin')

    # Save to .plugin file in the plugin folder
    plugin_file_path = 'plugin/example.plugin'
    with open(plugin_file_path, 'w') as file:
        file.write('\n'.join(plugin_content))

if __name__ == "__main__":
    # Read .conf file from the conf folder
    conf_file_path = 'conf/example.conf'
    if os.path.exists(conf_file_path):
        with open(conf_file_path, 'r') as file:
            conf_content = file.read()
        convert_conf_to_plugin(conf_content)
    else:
        print(f"{conf_file_path} not found.")
