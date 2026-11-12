# 净叶性能优化（Jingye Performance）

Minecraft **1.21.4** / **Fabric** 客户端性能整合包，目标是在尽量保持原版观感的前提下提升帧率、降低卡顿与内存占用。

> 本仓库只包含整合包配置、模组清单与构建脚本，**不包含**模组 jar、游戏本体、存档、日志、截图与服务器列表。

## 版本信息

| 项目 | 版本 |
| --- | --- |
| Minecraft | 1.21.4 |
| Fabric Loader | 0.18.4 |
| 整合包 | 1.0.0 |
| Java | 21 及以上 |

## 主要优化方向

- **渲染**：VulkanMod + VulkanMod Extra 使用 Vulkan 后端；RenderScale 降分辨率渲染；ImmediatelyFast、EntityCulling 减少无效绘制。
- **线程与区块**：C2ME、VMP、ThreadTweak、Krypton 优化区块生成、线程调度与网络。
- **内存与启动**：ModernFix、FerriteCore、BadOptimizations、ScalableLux。
- **体验**：Dynamic FPS 切后台自动降帧、FastQuit 快速退出、Not Enough Crashes 崩溃定位、Mod Menu 统一管理。

完整列表见 [docs/MODS.md](docs/MODS.md)：共 35 个模组，全部来自 Modrinth。

## 安装

### 方式一：导入发行版（推荐）

1. 打开 [Releases](https://github.com/Yukstarlight/Jingye-Performance/releases)，下载最新的 `.mrpack` 文件。
2. 使用 **Modrinth App**、**Prism Launcher** 或 **PCL2**（支持 Modrinth 整合包）导入。
3. 首次启动时启动器会按索引从 Modrinth 下载模组，完成后即可进入游戏。

### 方式二：手动安装

1. 安装 Minecraft 1.21.4 与 Fabric Loader 0.18.4（Java 21）。
2. 按 [docs/MODS.md](docs/MODS.md) 下载全部模组，放入游戏目录的 `mods/`。
3. 将本仓库的 `config/` 复制到游戏目录的 `config/`。

## 注意事项

- VulkanMod 需要显卡驱动支持 Vulkan；它与 Sodium / Iris（光影）**不兼容**，请勿混装。
- 首次进入世界或加载新区块时占用较高属于正常现象。
- 建议为每个整合包使用独立游戏目录，升级前备份存档。
- `config/` 是作者本机的调校结果，可按自己的硬件调整渲染距离、RenderScale 等选项。

## 仓库结构

```
config/                  模组配置（发行版中的 overrides）
pack/modrinth.index.json Modrinth 整合包索引：模组下载地址与哈希
tools/mods.lock.json     模组版本锁文件
tools/build_mrpack.py    生成发行版
docs/MODS.md             模组清单
```

## 构建发行版

```bash
python tools/build_mrpack.py
```

输出 `dist/Jingye-Performance-1.0.0.mrpack`。构建过程只打包索引与 `config/`，不会下载或重新分发模组。

## 许可证

本仓库的配置、文档与构建脚本采用 [BSD 2-Clause](LICENSE) 许可证；基于本仓库构建的发行版（`.mrpack`）同样以 **BSD-2-Clause** 发布。

模组、Minecraft 本体及资源包版权归各自作者所有，并按其自身许可证分发；本仓库不再分发这些二进制文件。许可证信息见 [docs/MODS.md](docs/MODS.md)。

Minecraft 是 Mojang Studios / Microsoft 的商标，本项目与其无隶属关系。
