# GitHub Actions 配置指南

## 🚀 快速设置

### 1. 配置 GitHub Secrets

在GitHub仓库设置中添加以下Secrets：

1. 进入你的GitHub仓库页面
2. 点击 "Settings" 标签
3. 在左侧菜单中点击 "Secrets and variables" → "Actions"
4. 点击 "New repository secret" 添加以下两个Secrets：

#### COMMIT_EMAIL
```
wangzhenjjcn@gmail.com
```
*说明：用于Git提交的邮箱地址*

#### COMMIT_NAME
```
wangzhenjjcn
```
*说明：用于Git提交的用户名*

### 2. 启用 GitHub Actions

1. 进入GitHub仓库页面
2. 点击 "Settings" 标签
3. 在左侧菜单中点击 "Actions" → "General"
4. 在 "Workflow permissions" 部分选择 "Read and write permissions"
5. 点击 "Save"

### 3. 验证配置

配置完成后，GitHub Actions将：
- 每天6:06 AM (UTC+8) 自动运行
- 自动抓取Microsoft资源
- 检测到变化时自动提交到仓库

## 🔧 手动触发

你也可以手动触发GitHub Actions：

1. 进入GitHub仓库页面
2. 点击 "Actions" 标签
3. 选择 "Auto Scrape and Commit" 工作流
4. 点击 "Run workflow"

## 📊 监控运行状态

- 在 "Actions" 页面查看工作流运行历史
- 点击具体运行记录查看详细日志
- 绿色勾表示成功，红色叉表示失败

## 🛠️ 故障排除

### 常见问题

1. **权限错误**
   - 确保已启用 "Read and write permissions"
   - 检查Secrets是否正确配置

2. **依赖安装失败**
   - 检查 `src/requirements.txt` 文件是否存在
   - 确认Python版本兼容性

3. **Git配置错误**
   - 确保 `COMMIT_EMAIL` 和 `COMMIT_NAME` Secrets已设置
   - 检查邮箱格式是否正确

### 获取帮助

如果遇到问题，请：
1. 查看Actions运行日志
2. 提交GitHub Issue
3. 检查项目README.md获取更多信息

---

✅ 配置完成后，项目将自动运行并保持数据更新！ 