# DjangoBlog 系统架构图

```mermaid
flowchart TD
    subgraph 客户端层
        Browser[用户浏览器]
        Mobile[移动设备]
    end

    subgraph 前端层
        HTML[HTML/CSS/JavaScript]
        Bootstrap[Bootstrap 框架]
        Static[静态资源]
        Templates[Django 模板]
    end

    subgraph 应用层
        Blog[blog 应用\n核心博客功能]
        Accounts[accounts 应用\n用户管理]
        Comments[comments 应用\n评论系统]
        OAuth[oauth 应用\n第三方登录]
        ServerManager[servermanager 应用\n服务器管理]
        OwnTracks[owntracks 应用\n位置追踪]
    end

    subgraph 核心框架
        Django[Django 框架]
        Admin[Django Admin 后台]
        Middleware[中间件]
        URL[URL 路由]
        Cache[缓存系统]
    end

    subgraph 数据层
        MySQL[MySQL 数据库]
        ElasticSearch[ElasticSearch\n搜索索引]
        Whoosh[Whoosh\n本地搜索]
        FileSystem[文件系统\n静态文件/上传文件]
    end

    subgraph 插件系统
        Plugins[插件管理]
        ArticleCopyright[文章版权插件]
        ReadingTime[阅读时间插件]
        ViewCount[访问统计插件]
        SEO[SEO 优化插件]
        ArticleRec[文章推荐插件]
    end

    subgraph 部署层
        Docker[Docker 容器]
        Kubernetes[Kubernetes\n容器编排]
        Nginx[Nginx\n反向代理]
    end

    Browser -->|HTTP 请求| Nginx
    Mobile -->|HTTP 请求| Nginx

    Nginx -->|转发请求| Django

    Django -->|渲染模板| Templates
    Templates -->|使用| HTML
    HTML -->|使用| Bootstrap
    HTML -->|加载| Static

    Django -->|路由分发| URL
    URL -->|博客功能| Blog
    URL -->|用户管理| Accounts
    URL -->|评论处理| Comments
    URL -->|第三方登录| OAuth
    URL -->|服务器管理| ServerManager
    URL -->|位置追踪| OwnTracks

    Django -->|使用| Middleware
    Django -->|管理| Admin
    Django -->|缓存数据| Cache

    Blog -->|存储数据| MySQL
    Accounts -->|存储数据| MySQL
    Comments -->|存储数据| MySQL
    OAuth -->|存储数据| MySQL
    ServerManager -->|存储数据| MySQL
    OwnTracks -->|存储数据| MySQL

    Blog -->|搜索| ElasticSearch
    Blog -->|本地搜索| Whoosh
    Blog -->|存储文件| FileSystem

    Django -->|加载插件| Plugins
    Plugins -->|管理| ArticleCopyright
    Plugins -->|管理| ReadingTime
    Plugins -->|管理| ViewCount
    Plugins -->|管理| SEO
    Plugins -->|管理| ArticleRec

    Django -->|部署在| Docker
    Docker -->|编排| Kubernetes
```

## 架构说明

1. **客户端层**：支持浏览器和移动设备访问

2. **前端层**：
   - 使用 HTML/CSS/JavaScript 构建用户界面
   - 集成 Bootstrap 框架实现响应式设计
   - Django 模板系统实现服务端渲染

3. **应用层**：
   - **blog**：核心博客功能，包括文章、分类、标签管理
   - **accounts**：用户管理，包括注册、登录、个人资料
   - **comments**：评论系统，支持文章评论
   - **oauth**：第三方登录集成
   - **servermanager**：服务器管理功能
   - **owntracks**：位置追踪功能

4. **核心框架**：
   - Django 框架提供 MVC 架构支持
   - 自定义 Admin 后台
   - 中间件处理请求/响应
   - 缓存系统提升性能

5. **数据层**：
   - MySQL 数据库存储核心数据
   - ElasticSearch/Whoosh 提供搜索功能
   - 文件系统存储静态资源和上传文件

6. **插件系统**：
   - 可扩展的插件架构
   - 内置多个功能插件

7. **部署层**：
   - 支持 Docker 容器化部署
   - Kubernetes 容器编排
   - Nginx 反向代理