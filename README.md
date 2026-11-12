# 净叶性能优化

> 全球最强性能整合包（自称）

Minecraft 1.21.4 + Fabric 的客户端整合包，装了一批性能模组，配置也调过了。仓库里放的是配置和模组清单，模组 jar 不在这里。

| 项目 | 版本 |
| --- | --- |
| Minecraft | 1.21.4 |
| Fabric Loader | 0.18.4 |
| 整合包 | 1.0.0 |
| Java | 21 及以上 |

## 安装

**推荐**：到 [Releases](https://github.com/Yukstarlight/Jingye-Performance/releases) 下载 `.mrpack`，用 Modrinth App、Prism Launcher 或 PCL2 导入。启动器会按索引从 Modrinth 自动下载模组。

**手动**：装好 Minecraft 1.21.4 + Fabric Loader 0.18.4，按 [docs/MODS.md](docs/MODS.md) 下载 35 个模组放进 `mods/`，再把本仓库的 `config/` 复制到游戏目录。

## 注意

- VulkanMod 需要显卡驱动支持 Vulkan，和 Sodium / Iris（光影）不兼容，别混装。
- 第一次进世界卡一会儿是正常的。
- `config/` 是作者本机调出来的，硬件不一样就自己改。

## 仓库里有什么

```
config/                   模组配置
pack/modrinth.index.json  模组下载地址和哈希
tools/mods.lock.json      模组版本锁
tools/build_mrpack.py     重新打包发行版
docs/MODS.md              35 个模组的清单
```

改完配置重新打包：

```bash
python tools/build_mrpack.py
```

输出在 `dist/`，只打包索引和配置，不下载也不分发模组。

## 许可证

配置、文档、脚本以及打出来的 `.mrpack` 都采用 [BSD 2-Clause](LICENSE)。

模组和 Minecraft 归各自作者所有，按各自许可证分发；仓库里没有这些文件。Minecraft 是 Mojang Studios / Microsoft 的商标，本项目与其无隶属关系。
