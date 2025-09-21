import requests
from bs4 import BeautifulSoup
import time
import os
import json
import sys

def check_dependencies():
    """检查必要的依赖是否已安装"""
    required_packages = ['requests', 'bs4']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少必要的依赖包: {', '.join(missing_packages)}")
        print("请运行以下命令安装依赖:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    else:
        print("✅ 所有依赖包已安装")

def extract_page_data(url):
    """提取页面数据"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取标题
        title_element = soup.find('h1', class_='sppb-addon-title')
        title = title_element.get_text(strip=True) if title_element else "未知标题"
        
        # 提取介绍文本
        intro_text = ""
        if title_element and title_element.parent:
            content_div = title_element.parent.find('div', class_='sppb-addon-content')
            if content_div:
                intro_text = content_div.get_text(strip=True)
        
        # 提取版本信息
        versions = []
        
        # 查找所有section，每个section包含一个版本的信息
        sections = soup.find_all('section')
        
        for section in sections:
            version_info = {}
            
            # 查找版本标题（h3标签）
            h3_element = section.find('h3')
            if h3_element:
                version_info['version_text'] = h3_element.get_text(strip=True)
                
                # 提取属性信息（h3后面的文本，直到下一个h3或section结束）
                attributes = []
                current_element = h3_element.next_sibling
                while current_element and current_element.name != 'h3':
                    if hasattr(current_element, 'get_text'):
                        text = current_element.get_text(strip=True)
                        if text and text not in ['', '迅雷下载：']:
                            attributes.append(text)
                    current_element = current_element.next_sibling
                
                version_info['attributes'] = attributes
                
                # 查找下载信息
                downloads = []
                
                # 查找下载链接
                dl_links = section.find_all('div', class_='dl-link')
                for dl_link in dl_links:
                    download_info = {}
                    download_info['download_url'] = dl_link.get_text(strip=True)
                    
                    # 查找对应的下载类型
                    strong_element = dl_link.find_previous('strong')
                    if strong_element:
                        download_info['download_type'] = strong_element.get_text(strip=True)
                    else:
                        download_info['download_type'] = "下载"
                    
                    if download_info['download_url']:
                        downloads.append(download_info)
                
                version_info['downloads'] = downloads
                
                if version_info['version_text'] and (version_info['attributes'] or version_info['downloads']):
                    versions.append(version_info)
        
        return {
            'title': title,
            'intro_text': intro_text,
            'versions': versions,
            'url': url
        }
        
    except Exception as e:
        print(f"提取页面数据时出错 {url}: {e}")
        return None

def parse_url_to_path(url):
    """将URL转换为本地文件路径"""
    # 处理两种URL格式
    path = url.replace('https://windows.unblock.win/', '').replace('https://www.imsdn.cn/', '')
    if path.endswith('/'):
        path = path[:-1]
    return path

def create_directory_structure(path):
    """创建目录结构"""
    full_path = os.path.join('docs', path)
    os.makedirs(full_path, exist_ok=True)
    return full_path

def is_http_url(url):
    """判断是否为HTTP/HTTPS链接"""
    return url.startswith('http://') or url.startswith('https://')

def is_ed2k_url(url):
    """判断是否为ed2k链接"""
    return url.startswith('ed2k://')

# 新增：按钮渲染辅助函数，避免在 f-string 表达式中包含反斜杠

def render_http_button(url: str) -> str:
    if not is_http_url(url):
        return ''
    return f'<button class="download-btn" onclick="openDownloadLink(&quot;{url}&quot;)">立即下载</button>'


def render_thunder_button(url: str) -> str:
    if not is_ed2k_url(url):
        return ''
    return f'<button class="thunder-btn" onclick="copyToClipboard(&quot;{url}&quot;)">复制使用迅雷下载</button>'


def generate_html_content(data):
    """生成HTML内容"""
    # 确保数据完整性
    if not data:
        return "<html><body><h1>数据提取失败</h1></body></html>"
    
    title = data.get('title', '未知标题')
    intro_text = data.get('intro_text', '')
    versions = data.get('versions', [])
    
    html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
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
        }}
        .intro {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
            line-height: 1.6;
        }}
        .version {{
            border: 1px solid #ddd;
            margin: 20px 0;
            border-radius: 5px;
            overflow: hidden;
        }}
        .version-header {{
            background-color: #0078d4;
            color: white;
            padding: 15px;
            font-weight: bold;
        }}
        .version-attributes {{
            padding: 15px;
            background-color: #f8f9fa;
        }}
        .download-section {{
            padding: 15px;
            border-top: 1px solid #ddd;
        }}
        .download-type {{
            font-weight: bold;
            color: #0078d4;
            margin-bottom: 10px;
        }}
        .download-url {{
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 3px;
            font-family: monospace;
            word-break: break-all;
            margin: 10px 0;
        }}
        .copy-btn {{
            background-color: #28a745;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            margin-left: 10px;
        }}
        .copy-btn:hover {{
            background-color: #218838;
        }}
        .download-btn {{
            background-color: #007bff;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            margin-left: 10px;
        }}
        .download-btn:hover {{
            background-color: #0056b3;
        }}
        .thunder-btn {{
            background-color: #ff6b35;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            margin-left: 10px;
        }}
        .thunder-btn:hover {{
            background-color: #e55a2b;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        
        <div class="intro">
            {intro_text}
        </div>
        
        {''.join([f'''
        <div class="version">
            <div class="version-header">{version.get('version_text', '未知版本')}</div>
            <div class="version-attributes">
                {''.join([f'<div>{attr}</div>' for attr in version.get('attributes', [])])}
            </div>
            {''.join([f'''
            <div class="download-section">
                <div class="download-type">{download.get('download_type', '下载')}</div>
                <div class="download-url">{download.get('download_url', '')}</div>
                <button class="copy-btn" onclick="copyToClipboard('{download.get('download_url', '')}')">复制下载链接</button>
                {render_http_button(download.get('download_url', ''))}
                {render_thunder_button(download.get('download_url', ''))}
            </div>
            ''' for download in version.get('downloads', [])])}
        </div>
        ''' for version in versions])}
    </div>

    <script>
        function copyToClipboard(text) {{
            if (!text) return;
            
            navigator.clipboard.writeText(text).then(function() {{
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '已复制!';
                btn.style.backgroundColor = '#6c757d';
                
                setTimeout(function() {{
                    btn.textContent = originalText;
                    btn.style.backgroundColor = btn.classList.contains('thunder-btn') ? '#ff6b35' : '#28a745';
                }}, 2000);
            }}).catch(function(err) {{
                const textArea = document.createElement('textarea');
                textArea.value = text;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '已复制!';
                btn.style.backgroundColor = '#6c757d';
                
                setTimeout(function() {{
                    btn.textContent = originalText;
                    btn.style.backgroundColor = btn.classList.contains('thunder-btn') ? '#ff6b35' : '#28a745';
                }}, 2000);
            }});
        }}
        
        function openDownloadLink(url) {{
            if (url) {{
                window.open(url, '_blank');
            }}
        }}
    </script>
</body>
</html>
"""
    return html_template

def generate_index_html():
    """生成汇总页面"""
    # 读取所有链接
    with open('docs/a.txt', 'r', encoding='utf-8') as f:
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
        .search-section {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .search-input {{
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            margin-bottom: 10px;
        }}
        .search-input:focus {{
            outline: none;
            border-color: #0078d4;
        }}
        .search-options {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }}
        .search-option {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        .search-option input[type="checkbox"] {{
            margin: 0;
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
        .link-item.hidden {{
            display: none;
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
        .no-results {{
            text-align: center;
            padding: 40px;
            color: #666;
            font-size: 18px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Microsoft 资源下载中心</h1>
        
        <div class="search-section">
            <input type="text" id="searchInput" class="search-input" placeholder="搜索资源..." onkeyup="filterItems()">
            <div class="search-options">
                <div class="search-option">
                    <input type="checkbox" id="searchTitle" checked>
                    <label for="searchTitle">标题</label>
                </div>
                <div class="search-option">
                    <input type="checkbox" id="searchIntro" checked>
                    <label for="searchIntro">介绍</label>
                </div>
                <div class="search-option">
                    <input type="checkbox" id="searchDetails" checked>
                    <label for="searchDetails">详情</label>
                </div>
            </div>
        </div>
        
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
                    <div class="link-item" data-title="{parse_url_to_path(link).split('/')[-1].replace('-', ' ').title()}" data-url="{link.replace('https://www.imsdn.cn/', 'https://windows.unblock.win/')}" data-path="{parse_url_to_path(link)}">
                        <div class="link-title">{parse_url_to_path(link).split('/')[-1].replace('-', ' ').title()}</div>
                        <a href="{parse_url_to_path(link)}/index.html" class="link-btn" target="_blank">查看详情</a>
                    </div>
                    ''' for link in category_links])}
                </div>
            </div>
        </div>
        ''' for category_name, category_links in categories.items() if category_links])}
        
        <div id="noResults" class="no-results" style="display: none;">
            没有找到匹配的资源
        </div>
    </div>

    <script>
        function filterItems() {{
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const searchTitle = document.getElementById('searchTitle').checked;
            const searchIntro = document.getElementById('searchIntro').checked;
            const searchDetails = document.getElementById('searchDetails').checked;
            
            const items = document.querySelectorAll('.link-item');
            let visibleCount = 0;
            
            items.forEach(item => {{
                const title = item.getAttribute('data-title').toLowerCase();
                const url = item.getAttribute('data-url').toLowerCase();
                const path = item.getAttribute('data-path').toLowerCase();
                
                let matches = false;
                
                if (searchTitle && (title.includes(searchTerm) || url.includes(searchTerm))) {{
                    matches = true;
                }}
                
                if (searchIntro && (title.includes(searchTerm) || url.includes(searchTerm))) {{
                    matches = true;
                }}
                
                if (searchDetails && (title.includes(searchTerm) || url.includes(searchTerm) || path.includes(searchTerm))) {{
                    matches = true;
                }}
                
                if (searchTerm === '' || matches) {{
                    item.classList.remove('hidden');
                    visibleCount++;
                }} else {{
                    item.classList.add('hidden');
                }}
            }});
            
            // 显示/隐藏"无结果"消息
            const noResults = document.getElementById('noResults');
            if (visibleCount === 0 && searchTerm !== '') {{
                noResults.style.display = 'block';
            }} else {{
                noResults.style.display = 'none';
            }}
        }}
    </script>
</body>
</html>
"""
    
    # 保存汇总页面
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"汇总页面已生成: docs/index.html")

def save_page_data(url):
    """保存页面数据"""
    print(f"正在处理页面: {url}")
    
    data = extract_page_data(url)
    if not data:
        print(f"无法提取页面数据: {url}")
        return
    
    path = parse_url_to_path(url)
    full_path = create_directory_structure(path)
    
    html_content = generate_html_content(data)
    
    html_file = os.path.join(full_path, 'index.html')
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    json_file = os.path.join(full_path, 'data.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"已保存到: {full_path}")

def main():
    # 检查依赖
    check_dependencies()
    
    # 读取已采集的链接
    with open('docs/a.txt', 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f.readlines()]
    
    print(f"开始处理 {len(links)} 个页面...")
    
    for i, link in enumerate(links, 1):
        print(f"\n处理进度: {i}/{len(links)}")
        save_page_data(link)
        time.sleep(2)
    
    print(f"\n所有页面处理完成！")
    
    # 生成汇总页面
    print("\n正在生成汇总页面...")
    generate_index_html()
    print("汇总页面生成完成！")

if __name__ == "__main__":
    main()
