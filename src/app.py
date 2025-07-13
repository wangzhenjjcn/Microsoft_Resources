#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows系统下载资源主应用程序
统一运行爬虫和生成器
"""

import os
import sys
import logging
from datetime import datetime
from scraper import WindowsScraper
from generator import WebsiteGenerator

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def main():
    """主函数"""
    try:
        logging.info("=" * 50)
        logging.info("Windows系统下载资源更新程序启动")
        logging.info(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info("=" * 50)
        
        # 步骤1: 运行爬虫
        logging.info("步骤1: 开始数据采集...")
        scraper = WindowsScraper()
        scraper.scrape_all()
        logging.info("步骤1: 数据采集完成")
        
        # 步骤2: 生成网站
        logging.info("步骤2: 开始生成网站...")
        generator = WebsiteGenerator()
        generator.generate_website()
        logging.info("步骤2: 网站生成完成")
        
        # 步骤3: 移动文件到根目录
        logging.info("步骤3: 整理文件结构...")
        
        # 复制主要文件到根目录
        import shutil
        
        # 复制index.html
        if os.path.exists('index.html'):
            shutil.copy2('index.html', '../index.html')
            logging.info("index.html已复制到根目录")
        
        # 复制CNAME
        if os.path.exists('CNAME'):
            shutil.copy2('CNAME', '../CNAME')
            logging.info("CNAME已复制到根目录")
        
        # 复制data目录
        if os.path.exists('data'):
            data_output_dir = '../data'
            if os.path.exists(data_output_dir):
                shutil.rmtree(data_output_dir)
            shutil.copytree('data', data_output_dir)
            logging.info("data目录已复制到根目录")
        
        # 复制static目录
        if os.path.exists('static'):
            static_output_dir = '../static'
            if os.path.exists(static_output_dir):
                shutil.rmtree(static_output_dir)
            shutil.copytree('static', static_output_dir)
            logging.info("static目录已复制到根目录")
        
        logging.info("步骤3: 文件结构整理完成")
        
        logging.info("=" * 50)
        logging.info("所有任务完成!")
        logging.info(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info("=" * 50)
        
    except Exception as e:
        logging.error(f"程序运行出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
