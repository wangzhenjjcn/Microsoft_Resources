#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows系统下载资源采集器
抓取 https://www.imsdn.cn/ 上的Windows系统下载信息
"""

import os
import json
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class WindowsScraper:
    def __init__(self):
        self.base_url = "https://www.imsdn.cn"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # 创建数据目录
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 定义要抓取的系统类型和对应的URL
        self.system_types = {
            "windows-11": {
                "name": "Windows 11",
                "subtypes": [
                    "win11-24h2", "win11-ltsc", "win11-23h2", "win11-22h2", 
                    "win11-21h2", "win11-rtm", "win11-arm"
                ]
            },
            "windows-10": {
                "name": "Windows 10", 
                "subtypes": [
                    "win10-22h2", "win10-21h2", "win10-21h1", "win10-20h2",
                    "win10-2004", "win10-1909", "win10-1903", "win10-1809",
                    "win10-1803", "win10-1709", "win10-1703", "win10-1607",
                    "win10-1511", "win10-ltsc"
                ]
            },
            "windows-server": {
                "name": "Windows Server",
                "subtypes": [
                    "windows-server-2025", "windows-server-2022", "windows-server-2019",
                    "windows-server-2016", "windows-server-2012-r2", "windows-server-2012",
                    "windows-server-2008-r2", "windows-server-2008"
                ]
            },
            "applications": {
                "name": "Office",
                "subtypes": [
                    "office-2024", "office-2021", "office-2019", "office-2016",
                    "office-2013", "office-2010", "office-2007"
                ]
            },
            "servers": {
                "name": "SQL Server",
                "subtypes": [
                    "sql-server-2019", "sql-server-2016", "sql-server-2014",
                    "sql-server-2012", "sql-server-2008-r2", "sql-server-2005"
                ]
            }
        }
        
        self.all_data = {}
        
    def download_image(self, img_url, system_type, subtype):
        """下载图片到本地"""
        try:
            if not img_url.startswith('http'):
                img_url = urljoin(self.base_url, img_url)
            
            response = self.session.get(img_url, timeout=30)
            if response.status_code == 200:
                # 创建图片目录
                img_dir = os.path.join(self.data_dir, system_type, subtype, "images")
                os.makedirs(img_dir, exist_ok=True)
                
                # 生成文件名
                filename = os.path.basename(urlparse(img_url).path)
                if not filename:
                    filename = f"{subtype}.jpg"
                
                filepath = os.path.join(img_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                # 返回相对路径
                return f"data/{system_type}/{subtype}/images/{filename}"
            else:
                logging.warning(f"下载图片失败: {img_url}, 状态码: {response.status_code}")
                return None
        except Exception as e:
            logging.error(f"下载图片出错: {img_url}, 错误: {e}")
            return None
    
    def extract_download_links(self, soup):
        """提取下载链接信息"""
        download_links = []
        
        # 查找所有包含下载链接的section
        sections = soup.find_all('section', class_='sppb-section')
        
        for section in sections:
            # 查找版本信息
            version_info = section.find('div', class_='sppb-alert-dark')
            if not version_info:
                continue
                
            h3_tag = version_info.find('h3')
            if not h3_tag:
                continue
                
            version_title = h3_tag.get_text(strip=True)
            
            # 查找下载链接
            dl_links = section.find_all('div', class_='dl-link')
            for dl_link in dl_links:
                link_text = dl_link.get_text(strip=True)
                
                # 过滤掉包含microsoft.com的链接
                if 'microsoft.com' in link_text.lower():
                    continue
                    
                # 查找子版本信息
                strong_tag = dl_link.find_previous('strong')
                sub_version = strong_tag.get_text(strip=True) if strong_tag else ""
                
                download_links.append({
                    'version_title': version_title,
                    'sub_version': sub_version,
                    'download_link': link_text
                })
        
        return download_links
    
    def scrape_page(self, url, system_type, subtype):
        """抓取单个页面"""
        try:
            logging.info(f"正在抓取: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 提取页面标题
            h1_tag = soup.find('h1')
            page_title = h1_tag.get_text(strip=True) if h1_tag else f"{self.system_types[system_type]['name']} {subtype}"
            
            # 提取图片
            img_tag = soup.find('div', class_='sppb-addon-single-image-container')
            img_url = None
            if img_tag:
                img = img_tag.find('img')
                if img and img.get('src'):
                    img_url = img.get('src')
                    # 下载图片
                    local_img_path = self.download_image(img_url, system_type, subtype)
                    img_url = local_img_path
            
            # 提取发行介绍和版本介绍
            content_divs = soup.find_all('div', class_='sppb-addon-content')
            release_info = ""
            version_info = ""
            
            if len(content_divs) >= 2:
                # 第一个div作为发行介绍
                release_info = content_divs[0].get_text(strip=True)
                # 第二个div作为版本介绍
                version_info = content_divs[1].get_text(strip=True)
            
            # 提取下载链接
            download_links = self.extract_download_links(soup)
            
            # 生成详细页面HTML
            detail_html = self.generate_detail_html(page_title, img_url, release_info, version_info, download_links)
            
            # 保存详细页面
            detail_dir = os.path.join(self.data_dir, system_type, subtype)
            os.makedirs(detail_dir, exist_ok=True)
            
            with open(os.path.join(detail_dir, 'detail.html'), 'w', encoding='utf-8') as f:
                f.write(detail_html)
            
            # 返回页面数据
            return {
                'title': page_title,
                'image_url': img_url,
                'release_info': release_info,
                'version_info': version_info,
                'download_links': download_links,
                'url': url,
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"抓取页面失败: {url}, 错误: {e}")
            return None
    
    def generate_detail_html(self, title, img_url, release_info, version_info, download_links):
        """生成详细页面HTML"""
        html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .download-link {{
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            word-break: break-all;
        }}
        .copy-btn {{
            margin-left: 10px;
        }}
    </style>
</head>
<body>
    <div class="container mt-4">
        <h1 class="mb-4">{title}</h1>
        
        {f'<img src="{img_url}" class="img-fluid mb-4" alt="{title}">' if img_url else ''}
        
        <div class="row">
            <div class="col-md-6">
                <div class="card mb-4">
                    <div class="card-header">
                        <h5>发行信息</h5>
                    </div>
                    <div class="card-body">
                        <p>{release_info}</p>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card mb-4">
                    <div class="card-header">
                        <h5>版本信息</h5>
                    </div>
                    <div class="card-body">
                        <p>{version_info}</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-header">
                <h5>下载链接</h5>
            </div>
            <div class="card-body">
"""
        
        for link_info in download_links:
            html_template += f"""
                <div class="alert alert-info">
                    <h6>{link_info['version_title']}</h6>
                    {f'<p><strong>{link_info["sub_version"]}</strong></p>' if link_info['sub_version'] else ''}
                    <div class="download-link">
                        <span class="link-text">{link_info['download_link']}</span>
                        <button class="btn btn-primary btn-sm copy-btn" onclick="copyToClipboard(this)">
                            <i class="fas fa-copy"></i> 复制
                        </button>
                    </div>
                </div>
"""
        
        html_template += """
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function copyToClipboard(button) {
            const linkText = button.previousElementSibling.textContent;
            navigator.clipboard.writeText(linkText).then(function() {
                button.innerHTML = '<i class="fas fa-check"></i> 已复制';
                setTimeout(function() {
                    button.innerHTML = '<i class="fas fa-copy"></i> 复制';
                }, 2000);
            });
        }
    </script>
</body>
</html>
"""
        return html_template
    
    def scrape_all(self):
        """抓取所有系统类型的数据"""
        for system_type, system_info in self.system_types.items():
            logging.info(f"开始抓取 {system_info['name']}")
            
            system_data = {
                'name': system_info['name'],
                'type': system_type,
                'subtypes': {}
            }
            
            for subtype in system_info['subtypes']:
                url = f"{self.base_url}/{system_type}/{subtype}/"
                
                page_data = self.scrape_page(url, system_type, subtype)
                if page_data:
                    system_data['subtypes'][subtype] = page_data
                    logging.info(f"成功抓取: {subtype}")
                else:
                    logging.warning(f"抓取失败: {subtype}")
                
                # 添加延迟避免请求过快
                time.sleep(2)
            
            # 保存系统数据
            self.all_data[system_type] = system_data
            
            # 保存到JSON文件
            json_file = os.path.join(self.data_dir, f"{system_type}.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(system_data, f, ensure_ascii=False, indent=2)
            
            logging.info(f"完成抓取 {system_info['name']}")
        
        # 保存汇总数据
        summary_file = os.path.join(self.data_dir, "summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump({
                'last_updated': datetime.now().isoformat(),
                'systems': self.all_data
            }, f, ensure_ascii=False, indent=2)
        
        logging.info("所有数据抓取完成")

if __name__ == "__main__":
    scraper = WindowsScraper()
    scraper.scrape_all() 