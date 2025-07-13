
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
