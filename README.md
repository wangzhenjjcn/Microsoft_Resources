# Windows系统下载资源

这是一个自动抓取和展示Windows系统下载资源的网站项目。

## 功能特性

- 🔍 **智能搜索**: 支持搜索系统名称、版本信息、下载链接
- 📱 **响应式设计**: 支持PC和移动端访问
- 🔄 **自动更新**: 每天凌晨3点自动更新数据
- 📋 **一键复制**: 点击即可复制下载链接
- 🎨 **美观界面**: 使用Bootstrap风格设计

## 支持的系统

- **Windows 11**: 24H2、LTSC、23H2、22H2、21H2、RTM、ARM
- **Windows 10**: 22H2、21H2、21H1、20H2、2004、1909、1903、1809、1803、1709、1703、1607、1511、LTSC
- **Windows Server**: 2025、2022、2019、2016、2012 R2、2012、2008 R2、2008
- **Office**: 2024、2021、2019、2016、2013、2010、2007
- **SQL Server**: 2019、2016、2014、2012、2008 R2、2005

## 项目结构

```
├── src/                    # 源代码
│   ├── scraper.py         # 爬虫程序
│   └── generator.py       # 网站生成器
├── conf/                   # 配置文件
│   └── config.json        # 主配置文件
├── data/                   # 数据文件
├── static/                 # 静态资源
│   ├── style.css          # 样式文件
│   └── script.js          # JavaScript文件
├── .github/workflows/      # GitHub Actions
│   └── update.yml         # 自动更新配置
├── requirements.txt        # Python依赖
└── README.md              # 项目说明
```

## 本地运行

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行爬虫

```bash
cd src
python scraper.py
```

### 生成网站

```bash
cd src
python generator.py
```

## 自动化部署

项目配置了GitHub Actions，每天凌晨3点自动运行：

1. 抓取最新数据
2. 生成网站文件
3. 自动提交更新

## 自定义域名

项目配置了自定义域名：`windows.unblock.win`

## 技术栈

- **后端**: Python 3.9+
- **爬虫**: requests + BeautifulSoup4
- **前端**: Bootstrap 5 + Font Awesome
- **自动化**: GitHub Actions
- **部署**: GitHub Pages

## 注意事项

- 所有下载链接均来自互联网，仅供学习和研究使用
- 请遵守相关法律法规和版权要求
- 建议使用正版软件

## 许可证

本项目仅供学习和研究使用，请勿用于商业用途。 