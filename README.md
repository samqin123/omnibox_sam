# Omnibox + PanSou 部署指南

本项目提供了两种部署方式：独立部署和套装部署，满足不同场景的需求。

## 部署方式

### 方式一：独立部署（仅 Omnibox）

适用于只需要基础搜索功能的场景。

```bash
# 使用默认的 docker-compose.yml
docker compose up -d
```

访问地址：http://localhost:7123

### 方式二：套装部署（Omnibox + PanSou）

适用于需要完整网盘搜索功能的场景，包含高性能的网盘资源搜索API服务。

```bash
# 使用套装版配置文件
docker compose -f omnibox-pansou套装版.yml up -d
```

访问地址：
- Omnibox: http://localhost:7123
- PanSou API: http://localhost:8888

## 套装版特性

- **高性能搜索**：并发执行多个TG频道及异步插件搜索
- **网盘类型分类**：自动识别多种网盘链接，按类型归类展示
- **智能排序**：基于插件等级、时间新鲜度和优先关键词的多维度综合排序
- **异步插件系统**：支持通过插件扩展搜索来源
- **二级缓存**：分片内存+分片磁盘缓存机制，大幅提升重复查询速度

## 支持的网盘类型

- 百度网盘 (baidu)
- 阿里云盘 (aliyun)
- 夸克网盘 (quark)
- 天翼云盘 (tianyi)
- UC网盘 (uc)
- 移动云盘 (mobile)
- 115网盘 (115)
- PikPak (pikpak)
- 迅雷网盘 (xunlei)
- 123网盘 (123)
- 磁力链接 (magnet)
- 电驴链接 (ed2k)
- 其他 (others)

## 服务管理

```bash
# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f

# 停止服务
docker compose down

# 重启服务
docker compose restart
```

## 配置说明

### 独立版配置
- 仅包含 Omnibox 服务
- 端口映射：7123:7023
- 数据持久化：./app/data

### 套装版配置
- 包含 Omnibox + PanSou 服务
- Omnibox 端口：7123:7023
- PanSou 端口：8888:8888
- 专用网络通信
- 健康检查机制
- 缓存优化配置

#### PanSou 地址配置（关键）
- 推荐在容器内通过服务名访问 PanSou：`http://pansou:8888`

- 依据：在 `docker-compose.yml` 中为 Omnibox 显式设置：
  ```yaml
  environment:
    - PANSOU_URL=http://pansou:8888
  ```
- 备选方案
- 如果因为历史设置被覆盖，建议在 UI 中更新或使用 host.docker.internal 作为过渡：
- 容器访问宿主机端口： http://host.docker.internal:8888

## 致谢

### Omnibox 项目
感谢 **DragonCoder** 开发的优秀 Omnibox 项目，为我们提供了强大的搜索界面基础。

项目讨论：https://linux.do/t/topic/916651

### PanSou 项目
感谢 **fish2018** 开发的高性能网盘搜索API服务 PanSou，为本项目提供了强大的搜索后端支持。

项目地址：https://github.com/fish2018/pansou

## 问题反馈

如果在使用过程中遇到问题，请检查：
1. Docker 和 Docker Compose 是否正确安装
2. 端口是否被占用
3. 网络连接是否正常
4. 查看容器日志排查具体错误

---

**注意**：首次启动可能需要下载镜像，请耐心等待。建议在网络良好的环境下进行部署。