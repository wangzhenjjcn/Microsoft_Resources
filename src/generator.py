#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows系统下载资源网站生成器
生成带有搜索功能的主页和系统详情页面
"""

import os
import json
import shutil
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class WebsiteGenerator:
    def __init__(self):
        self.data_dir = "data"
        self.output_dir = "."
        self.static_dir = "static"
        
        # 创建静态资源目录
        os.makedirs(self.static_dir, exist_ok=True)
        
        # 创建CSS和JS文件
        self.create_static_files()
        
    def create_static_files(self):
        """创建静态资源文件"""
        # CSS文件
        css_content = """
/* 自定义样式 */
.search-container {
    position: relative;
    margin-bottom: 30px;
}

.search-results {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    border: 1px solid #ddd;
    border-top: none;
    border-radius: 0 0 5px 5px;
    max-height: 400px;
    overflow-y: auto;
    z-index: 1000;
    display: none;
}

.search-result-item {
    padding: 10px 15px;
    border-bottom: 1px solid #eee;
    cursor: pointer;
}

.search-result-item:hover {
    background-color: #f8f9fa;
}

.search-result-item:last-child {
    border-bottom: none;
}

.system-card {
    transition: transform 0.2s;
    height: 100%;
}

.system-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.download-link {
    background: #f8f9fa;
    padding: 10px;
    border-radius: 5px;
    margin: 10px 0;
    word-break: break-all;
    font-family: monospace;
}

.copy-btn {
    margin-left: 10px;
}

.system-icon {
    width: 60px;
    height: 60px;
    object-fit: cover;
    border-radius: 10px;
}

.search-highlight {
    background-color: yellow;
    font-weight: bold;
}

.footer {
    margin-top: 50px;
    padding: 20px 0;
    background-color: #f8f9fa;
    border-top: 1px solid #dee2e6;
}

@media (max-width: 768px) {
    .search-results {
        position: fixed;
        top: 60px;
        left: 10px;
        right: 10px;
        max-height: 300px;
    }
}
"""
        
        with open(os.path.join(self.static_dir, "style.css"), "w", encoding="utf-8") as f:
            f.write(css_content)
        
        # JavaScript文件
        js_content = """
// 搜索功能
let searchTimeout;
let allData = {};

// 初始化搜索
function initSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length < 2) {
            searchResults.style.display = 'none';
            return;
        }
        
        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, 300);
    });
    
    // 点击外部关闭搜索结果
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });
}

// 执行搜索
function performSearch(query) {
    const searchResults = document.getElementById('searchResults');
    const results = [];
    
    // 搜索所有数据
    Object.keys(allData).forEach(systemType => {
        const system = allData[systemType];
        Object.keys(system.subtypes || {}).forEach(subtype => {
            const subtypeData = system.subtypes[subtype];
            
            // 搜索标题
            if (subtypeData.title && subtypeData.title.toLowerCase().includes(query.toLowerCase())) {
                results.push({
                    type: 'title',
                    system: system.name,
                    systemType: systemType,
                    subtype: subtype,
                    title: subtypeData.title,
                    text: subtypeData.title
                });
            }
            
            // 搜索发行信息
            if (subtypeData.release_info && subtypeData.release_info.toLowerCase().includes(query.toLowerCase())) {
                results.push({
                    type: 'release',
                    system: system.name,
                    systemType: systemType,
                    subtype: subtype,
                    title: subtypeData.title,
                    text: subtypeData.release_info
                });
            }
            
            // 搜索版本信息
            if (subtypeData.version_info && subtypeData.version_info.toLowerCase().includes(query.toLowerCase())) {
                results.push({
                    type: 'version',
                    system: system.name,
                    systemType: systemType,
                    subtype: subtype,
                    title: subtypeData.title,
                    text: subtypeData.version_info
                });
            }
            
            // 搜索下载链接
            if (subtypeData.download_links) {
                subtypeData.download_links.forEach(link => {
                    if (link.download_link && link.download_link.toLowerCase().includes(query.toLowerCase())) {
                        results.push({
                            type: 'download',
                            system: system.name,
                            systemType: systemType,
                            subtype: subtype,
                            title: subtypeData.title,
                            text: link.download_link
                        });
                    }
                });
            }
        });
    });
    
    displaySearchResults(results, query);
}

// 显示搜索结果
function displaySearchResults(results, query) {
    const searchResults = document.getElementById('searchResults');
    
    if (results.length === 0) {
        searchResults.innerHTML = '<div class="search-result-item">未找到相关结果</div>';
        searchResults.style.display = 'block';
        return;
    }
    
    // 去重并限制结果数量
    const uniqueResults = [];
    const seen = new Set();
    
    results.forEach(result => {
        const key = `${result.systemType}-${result.subtype}`;
        if (!seen.has(key)) {
            seen.add(key);
            uniqueResults.push(result);
        }
    });
    
    const html = uniqueResults.slice(0, 10).map(result => {
        const highlightedText = highlightText(result.text, query);
        return `
            <div class="search-result-item" onclick="goToDetail('${result.systemType}', '${result.subtype}')">
                <div><strong>${result.title}</strong></div>
                <div><small>${result.system} - ${result.type}</small></div>
                <div class="search-highlight">${highlightedText}</div>
            </div>
        `;
    }).join('');
    
    searchResults.innerHTML = html;
    searchResults.style.display = 'block';
}

// 高亮搜索文本
function highlightText(text, query) {
    if (!text) return '';
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<span class="search-highlight">$1</span>');
}

// 跳转到详情页面
function goToDetail(systemType, subtype) {
    window.location.href = `data/${systemType}/${subtype}/detail.html`;
}

// 复制到剪贴板
function copyToClipboard(button) {
    const linkText = button.previousElementSibling.textContent;
    navigator.clipboard.writeText(linkText).then(function() {
        button.innerHTML = '<i class="fas fa-check"></i> 已复制';
        setTimeout(function() {
            button.innerHTML = '<i class="fas fa-copy"></i> 复制';
        }, 2000);
    }).catch(function() {
        // 降级方案
        const textArea = document.createElement('textarea');
        textArea.value = linkText;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        
        button.innerHTML = '<i class="fas fa-check"></i> 已复制';
        setTimeout(function() {
            button.innerHTML = '<i class="fas fa-copy"></i> 复制';
        }, 2000);
    });
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initSearch();
    
    // 加载搜索数据
    fetch('data/summary.json')
        .then(response => response.json())
        .then(data => {
            allData = data.systems || {};
        })
        .catch(error => {
            console.error('加载搜索数据失败:', error);
        });
});
"""
        
        with open(os.path.join(self.static_dir, "script.js"), "w", encoding="utf-8") as f:
            f.write(js_content)
    
    def load_data(self):
        """加载所有数据"""
        all_data = {}
        
        # 加载汇总数据
        summary_file = os.path.join(self.data_dir, "summary.json")
        if os.path.exists(summary_file):
            with open(summary_file, 'r', encoding='utf-8') as f:
                summary_data = json.load(f)
                all_data = summary_data.get('systems', {})
        
        return all_data
    
    def generate_index_html(self, all_data):
        """生成主页HTML"""
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Windows系统下载资源 - windows.unblock.win</title>
    <meta name="description" content="提供Windows 11、Windows 10、Windows Server、Office、SQL Server等系统的下载资源">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="static/style.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="#">
                <i class="fas fa-windows me-2"></i>
                Windows系统下载资源
            </a>
            <div class="navbar-nav ms-auto">
                <span class="navbar-text">
                    <small>最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small>
                </span>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <!-- 搜索框 -->
        <div class="search-container">
            <div class="input-group">
                <span class="input-group-text">
                    <i class="fas fa-search"></i>
                </span>
                <input type="text" class="form-control" id="searchInput" placeholder="搜索系统名称、版本信息、下载链接...">
            </div>
            <div id="searchResults" class="search-results"></div>
        </div>

        <!-- 系统分类 -->
        <div class="row">
"""
        
        # 系统图标映射
        system_icons = {
            "windows-11": "fas fa-windows",
            "windows-10": "fas fa-windows", 
            "windows-server": "fas fa-server",
            "applications": "fas fa-file-word",
            "servers": "fas fa-database"
        }
        
        for system_type, system_data in all_data.items():
            if not system_data.get('subtypes'):
                continue
                
            html_content += f"""
            <div class="col-12 mb-4">
                <h2 class="mb-3">
                    <i class="{system_icons.get(system_type, 'fas fa-cube')} me-2"></i>
                    {system_data['name']}
                </h2>
                <div class="row">
"""
            
            for subtype, subtype_data in system_data['subtypes'].items():
                if not subtype_data:
                    continue
                    
                # 获取图片URL
                img_url = subtype_data.get('image_url', '')
                if img_url and not img_url.startswith('http'):
                    img_url = f"{img_url}"
                
                # 统计下载链接数量
                download_count = len(subtype_data.get('download_links', []))
                
                html_content += f"""
                    <div class="col-md-6 col-lg-4 mb-3">
                        <div class="card system-card h-100">
                            <div class="card-body">
                                <div class="d-flex align-items-center mb-3">
                                    {f'<img src="{img_url}" class="system-icon me-3" alt="{subtype_data["title"]}">' if img_url else f'<i class="{system_icons.get(system_type, "fas fa-cube")} system-icon me-3" style="font-size: 60px; color: #6c757d;"></i>'}
                                    <div>
                                        <h5 class="card-title mb-1">{subtype_data['title']}</h5>
                                        <small class="text-muted">{download_count} 个下载链接</small>
                                    </div>
                                </div>
                                <p class="card-text text-muted small">
                                    {subtype_data.get('release_info', '')[:100]}{'...' if len(subtype_data.get('release_info', '')) > 100 else ''}
                                </p>
                                <a href="data/{system_type}/{subtype}/detail.html" class="btn btn-primary btn-sm">
                                    <i class="fas fa-download me-1"></i>
                                    查看详情
                                </a>
                            </div>
                        </div>
                    </div>
"""
            
            html_content += """
                </div>
            </div>
"""
        
        html_content += """
        </div>
    </div>

    <footer class="footer">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5>关于本站</h5>
                    <p class="text-muted">
                        本站提供Windows系统、Office办公软件、SQL Server数据库等Microsoft产品的下载资源。
                        所有资源均来自互联网，仅供学习和研究使用。
                    </p>
                </div>
                <div class="col-md-6">
                    <h5>快速链接</h5>
                    <ul class="list-unstyled">
                        <li><a href="https://www.microsoft.com" class="text-decoration-none">Microsoft官网</a></li>
                        <li><a href="https://msdn.microsoft.com" class="text-decoration-none">MSDN</a></li>
                    </ul>
                </div>
            </div>
            <hr>
            <div class="text-center">
                <small class="text-muted">
                    © 2024 Windows系统下载资源. 最后更新: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """
                </small>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="static/script.js"></script>
</body>
</html>"""
        
        return html_content
    
    def copy_static_files(self):
        """复制静态文件到输出目录"""
        static_output_dir = os.path.join(self.output_dir, "static")
        os.makedirs(static_output_dir, exist_ok=True)
        
        # 复制CSS和JS文件
        for file in ["style.css", "script.js"]:
            src_file = os.path.join(self.static_dir, file)
            dst_file = os.path.join(static_output_dir, file)
            if os.path.exists(src_file):
                try:
                    shutil.copy2(src_file, dst_file)
                except PermissionError:
                    # 如果文件被占用，尝试删除后重新复制
                    try:
                        if os.path.exists(dst_file):
                            os.remove(dst_file)
                        shutil.copy2(src_file, dst_file)
                    except Exception as e:
                        logging.warning(f"复制文件失败: {file}, 错误: {e}")
    
    def create_cname_file(self):
        """创建CNAME文件"""
        cname_content = "windows.unblock.win"
        with open(os.path.join(self.output_dir, "CNAME"), "w", encoding="utf-8") as f:
            f.write(cname_content)
    
    def generate_website(self):
        """生成完整网站"""
        logging.info("开始生成网站...")
        
        # 加载数据
        all_data = self.load_data()
        if not all_data:
            logging.error("没有找到数据文件")
            return
        
        # 生成主页
        index_html = self.generate_index_html(all_data)
        with open(os.path.join(self.output_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(index_html)
        
        # 复制静态文件
        self.copy_static_files()
        
        # 复制数据目录
        if os.path.exists(self.data_dir):
            data_output_dir = os.path.join(self.output_dir, "data")
            try:
                if os.path.exists(data_output_dir):
                    shutil.rmtree(data_output_dir)
                shutil.copytree(self.data_dir, data_output_dir)
                logging.info("数据目录已复制")
            except Exception as e:
                logging.error(f"复制数据目录失败: {e}")
        else:
            logging.warning(f"数据目录不存在: {self.data_dir}")
        
        # 创建CNAME文件
        self.create_cname_file()
        
        logging.info("网站生成完成")

if __name__ == "__main__":
    generator = WebsiteGenerator()
    generator.generate_website() 