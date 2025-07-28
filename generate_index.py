import os

def parse_url_to_path(url):
    """将URL转换为本地文件路径"""
    path = url.replace('https://www.imsdn.cn/', '')
    if path.endswith('/'):
        path = path[:-1]
    return path

def generate_index_html():
    """生成汇总页面"""
    # 读取所有链接
    with open('data/a.txt', 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f.readlines()]
    
    # 按分类组织链接
    categories = {
        'Office 系列': [],
        'Windows 早期版本': [],
        'SQL Server 系列': [],
        'Windows 10 系列': [],
        'Windows 11 系列': [],
        'Windows Server 系列': []
    }
    
    for link in links:
        if 'applications/office' in link:
            categories['Office 系列'].append(link)
        elif 'operating-systems/windows' in link:
            categories['Windows 早期版本'].append(link)
        elif 'servers/sql-server' in link:
            categories['SQL Server 系列'].append(link)
        elif 'windows-10/win10' in link:
            categories['Windows 10 系列'].append(link)
        elif 'windows-11/win11' in link:
            categories['Windows 11 系列'].append(link)
        elif 'windows-server/windows-server' in link:
            categories['Windows Server 系列'].append(link)
    
    # 生成HTML内容
    html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Microsoft 资源下载中心</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #0078d4;
            padding-bottom: 10px;
            text-align: center;
        }}
        .category {{
            margin: 30px 0;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
        }}
        .category-header {{
            background-color: #0078d4;
            color: white;
            padding: 15px 20px;
            font-weight: bold;
            font-size: 18px;
        }}
        .category-content {{
            padding: 20px;
        }}
        .link-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
        }}
        .link-item {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #e9ecef;
            transition: all 0.3s ease;
        }}
        .link-item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .link-title {{
            font-weight: bold;
            color: #0078d4;
            margin-bottom: 8px;
            font-size: 14px;
        }}
        .link-url {{
            color: #666;
            font-size: 12px;
            word-break: break-all;
            margin-bottom: 10px;
        }}
        .link-btn {{
            background-color: #28a745;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            text-decoration: none;
            display: inline-block;
        }}
        .link-btn:hover {{
            background-color: #218838;
            color: white;
            text-decoration: none;
        }}
        .stats {{
            background-color: #e9ecef;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
        }}
        .stats-number {{
            font-size: 24px;
            font-weight: bold;
            color: #0078d4;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Microsoft 资源下载中心</h1>
        
        <div class="stats">
            <div class="stats-number">{len(links)}</div>
            <div>个资源页面</div>
        </div>
        
        {''.join([f'''
        <div class="category">
            <div class="category-header">{category_name}</div>
            <div class="category-content">
                <div class="link-grid">
                    {''.join([f'''
                    <div class="link-item">
                        <div class="link-title">{parse_url_to_path(link).split('/')[-1].replace('-', ' ').title()}</div>
                        <div class="link-url">{link}</div>
                        <a href="{parse_url_to_path(link)}/index.html" class="link-btn" target="_blank">查看详情</a>
                    </div>
                    ''' for link in category_links])}
                </div>
            </div>
        </div>
        ''' for category_name, category_links in categories.items() if category_links])}
    </div>
</body>
</html>
"""
    
    # 保存汇总页面
    with open('data/index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"汇总页面已生成: data/index.html")

if __name__ == "__main__":
    generate_index_html() 