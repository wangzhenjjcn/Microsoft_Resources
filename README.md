# Microsoft Resources Scraper

一个自动化的Microsoft资源采集工具，专门用于抓取和整理Windows Server、Windows 11、Windows 10、Office、MS SQL Server等Microsoft产品的下载资源。

## 🌟 功能特点

### 📊 数据采集
- **智能链接过滤**: 自动识别并采集Microsoft产品页面链接
- **详细数据提取**: 提取产品标题、介绍、版本信息、文件属性、下载链接等
- **多格式支持**: 支持HTTP/HTTPS和ed2k下载链接

### 🎨 用户界面
- **响应式设计**: 现代化的HTML界面，支持移动端访问
- **搜索功能**: 支持按标题、介绍、详情进行搜索过滤
- **一键复制**: 点击按钮即可复制下载链接到剪贴板
- **智能下载**: 根据链接类型显示不同的下载按钮
  - HTTP/HTTPS链接：显示"立即下载"按钮
  - ed2k链接：显示"复制使用迅雷下载"按钮

### 🔄 自动化部署
- **定时抓取**: 每天6:06 AM (UTC+8) 自动运行
- **自动提交**: 检测到变化时自动提交到GitHub
- **版本控制**: 完整的Git历史记录

## 📁 项目结构

```
Microsoft_Resources/
├── src/
│   ├── app.py              # 主程序
│   └── requirements.txt    # Python依赖
├── docs/                   # 生成的文档目录
│   ├── index.html         # 主页面（汇总所有产品）
│   ├── a.txt              # 采集的链接列表
│   ├── applications/      # Office产品页面
│   ├── windows-10/        # Windows 10产品页面
│   ├── windows-11/        # Windows 11产品页面
│   ├── windows-server/    # Windows Server产品页面
│   └── servers/           # SQL Server产品页面
├── .github/workflows/     # GitHub Actions配置
│   └── auto-scrape.yml   # 自动化工作流
└── README.md             # 项目说明
```

## 🚀 快速开始

### 环境要求
- Python 3.9+
- Git

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/wangzhenjjcn/Microsoft_Resources.git
   cd Microsoft_Resources
   ```

2. **安装依赖**
   ```bash
   pip install -r src/requirements.txt
   ```

3. **运行程序**
   ```bash
   python src/app.py
   ```

### 手动运行

程序会自动：
1. 检查依赖包是否已安装
2. 读取已采集的链接列表
3. 访问每个产品页面并提取详细信息
4. 生成HTML页面和JSON数据文件
5. 创建汇总页面

## 🔧 配置说明

### GitHub Actions 自动部署

项目已配置GitHub Actions，每天6:06 AM (UTC+8) 自动运行。

#### 必需的GitHub Secrets

在GitHub仓库设置中添加以下Secrets：

1. **COMMIT_EMAIL**: 提交时使用的邮箱地址
   ```
   your-email@example.com
   ```

2. **COMMIT_NAME**: 提交时使用的用户名
   ```
   Your Name
   ```

#### 启用GitHub Actions

1. 进入GitHub仓库页面
2. 点击 "Settings" 标签
3. 在左侧菜单中点击 "Actions" → "General"
4. 在 "Workflow permissions" 部分选择 "Read and write permissions"
5. 点击 "Save"

### 手动触发

你也可以手动触发GitHub Actions：
1. 进入GitHub仓库页面
2. 点击 "Actions" 标签
3. 选择 "Auto Scrape and Commit" 工作流
4. 点击 "Run workflow"

## 📊 数据格式

### 采集的数据字段

每个产品页面包含以下信息：

- **标题**: 产品名称（如"Office 2007"）
- **介绍**: 产品描述和基本信息
- **版本信息**: 具体的产品版本
- **文件属性**: 文件名、大小、发布时间、SHA1等
- **下载类型**: 下载方式（如"迅雷下载"）
- **下载链接**: 实际的下载地址

### 生成的文件类型

1. **HTML页面**: 每个产品的详细页面
2. **JSON数据**: 结构化的产品数据
3. **汇总页面**: 所有产品的索引页面

## 🎯 支持的Microsoft产品

### Office 系列
- Office 2007
- Office 2010
- Office 2013
- Office 2016
- Office 2019
- Office 2021
- Office 2024

### Windows 操作系统
- Windows XP
- Windows 7
- Windows 8
- Windows 8.1
- Windows 10 (各版本)
- Windows 11 (各版本)

### Windows Server
- Windows Server 2008
- Windows Server 2008 R2
- Windows Server 2012
- Windows Server 2012 R2
- Windows Server 2016
- Windows Server 2019
- Windows Server 2022
- Windows Server 2025

### SQL Server
- SQL Server 2005
- SQL Server 2008 R2
- SQL Server 2012
- SQL Server 2014
- SQL Server 2016
- SQL Server 2019

## 🔍 使用说明

### 访问生成的页面

1. **主页面**: 打开 `docs/index.html` 查看所有产品
2. **搜索功能**: 使用页面顶部的搜索框过滤产品
3. **产品详情**: 点击"查看详情"按钮查看具体产品信息
4. **下载资源**: 使用页面上的下载按钮获取资源

### 下载按钮说明

- **复制下载链接**: 复制下载地址到剪贴板
- **立即下载**: 在新窗口中打开HTTP/HTTPS下载链接
- **复制使用迅雷下载**: 复制ed2k链接用于迅雷下载

## 🛠️ 技术栈

- **Python**: 主要编程语言
- **Requests**: HTTP请求库
- **BeautifulSoup4**: HTML解析库
- **GitHub Actions**: 自动化部署
- **HTML/CSS/JavaScript**: 前端界面

## 📝 更新日志

### v1.0.0
- ✅ 基础数据采集功能
- ✅ HTML页面生成
- ✅ 搜索功能
- ✅ GitHub Actions自动化
- ✅ 响应式界面设计

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 感谢 [windows.unblock.win](https://windows.unblock.win/) 提供Microsoft资源信息
- 感谢所有为开源项目做出贡献的开发者

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 [GitHub Issue](https://github.com/wangzhenjjcn/Microsoft_Resources/issues)
- 发送邮件至: wangzhenjjcn@gmail.com

---

⭐ 如果这个项目对你有帮助，请给它一个星标！ 