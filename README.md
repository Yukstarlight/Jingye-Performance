# 净叶性能优化（Jingye Performance）

**净叶性能优化** 是面向 Minecraft Java 版 **1.21.4** 的 Fabric 客户端整合包，聚焦渲染管线、区块生成、线程调度、内存占用与启动流程的性能调优。项目以「配置即代码」的方式维护：仓库保存整合包配置、模组版本锁定信息与构建脚本，模组本体由启动器依据 Modrinth 索引下载并按哈希校验，仓库不再分发第三方二进制文件。

## 1. 设计目标

- **保持原版玩法**：不引入改变游戏机制的模组，仅优化运行效率与交互体验。
- **可复现**：模组版本由 `tools/mods.lock.json` 与 `pack/modrinth.index.json` 锁定，配置随仓库进行版本管理。
- **可审计**：模组来源、版本与许可证集中记录在 `docs/MODS.md`。
- **合规分发**：不打包、不再分发模组 jar，降低授权风险，同时避免仓库体积膨胀。

## 2. 版本与兼容性

| 组件 | 版本 | 说明 |
| --- | --- | --- |
| Minecraft | 1.21.4 | Java 版 |
| Fabric Loader | 0.18.4 | 模组加载器 |
| Java | 21 及以上 | 运行环境 |
| 渲染后端 | VulkanMod 0.5.6 | 需要显卡驱动支持 Vulkan |
| 整合包 | 1.0.0 | 对应 Release `v1.0.0` |

兼容性提示：

- 与 Sodium、Iris、OptiFine **不兼容**，请勿在同一实例中混装。
- 不支持光影。VulkanMod 使用 Vulkan 渲染路径，与 OpenGL 光影方案互斥。
- 部署到服务端时请参考 `docs/MODS.md` 的客户端/服务端支持列，标记为客户端专用的模组不应安装到服务端。

## 3. 优化策略

### 3.1 渲染与画面管线

- **VulkanMod / VulkanMod Extra**：将渲染后端从 OpenGL 替换为 Vulkan，降低驱动开销，并提供附加的画质与性能选项。
- **RenderScale**：以低于窗口分辨率的内部分辨率渲染后再放大，降低 GPU 填充压力，适合高分辨率屏幕与中低端显卡。
- **ImmediatelyFast**：批处理立即模式渲染调用，减少 GUI、实体与文本渲染的 draw call。
- **EntityCulling**：基于视锥与遮挡关系跳过不可见实体的渲染。
- **Dynamic FPS**：窗口失焦或长时间无操作时主动降低帧率，减少后台资源占用。
- **ScalableLux**：优化光照计算与区块光照更新，缓解大规模建造和光照更新时的卡顿。

### 3.2 区块、线程与逻辑

- **C2ME**：并发化区块生成、加载与序列化，缩短跑图与传送时的等待时间（当前为 alpha 版本）。
- **VMP（Very Many Players）**：优化玩家密集场景下的实体与区块 tick 开销。
- **ThreadTweak**：调整线程优先级与调度策略，改善主线程与工作线程的负载分配。
- **Krypton**：优化网络协议栈，降低多人游戏中的网络线程开销。
- **Lithium**：对实体、方块、AI 等通用游戏逻辑进行算法级优化。
- **Clumps**：合并经验球，减少大量掉落物造成的实体与渲染压力。

### 3.3 内存与启动

- **ModernFix**：缩短启动时间、降低内存占用，并动态处理部分资源加载。
- **FerriteCore**：压缩方块状态、模型等数据结构的内存足迹。
- **BadOptimizations**：针对文本、光照、随机数等热点路径的微优化。
- **FastQuit**：退出时在后台保存并立即返回标题界面，减少等待时间。

### 3.4 稳定性与工具

- **Not Enough Crashes**：崩溃时生成可读报告并尝试返回标题界面，便于定位问题。
- **Mod Menu、Cloth Config、YACL**：统一管理模组配置入口。
- **Chunky**：预生成区块，减少探索时的实时生成卡顿。
- **Fabrishot**：高性能大尺寸截图。
- **AppleSkin、3D Skin Layers、Custom Watermark、TIM、mcwifipnp**：分别提供饥饿值显示、3D 皮肤、水印、沉浸式音乐与局域网联机等体验增强。

完整模组清单、版本与许可证见 [`docs/MODS.md`](docs/MODS.md)。

## 4. 安装

### 4.1 导入发行版（推荐）

1. 前往 [Releases](https://github.com/Yukstarlight/Jingye-Performance/releases) 下载最新的 `.mrpack` 文件。
2. 使用 Modrinth App、Prism Launcher 或 PCL2 导入。
3. 首次启动时，启动器会读取 `modrinth.index.json`，从 Modrinth 下载并校验全部模组；需要能够访问 Modrinth 的网络环境。

### 4.2 手动安装

1. 安装 Minecraft 1.21.4 与 Fabric Loader 0.18.4，使用 Java 21。
2. 按 [`docs/MODS.md`](docs/MODS.md) 下载 35 个模组并放入 `mods/`。
3. 将仓库中的 `config/` 复制到游戏目录。
4. 建议分配 4–8 GB 堆内存，具体取决于渲染距离与同时运行的模组数量。

### 4.3 升级与备份

- 升级前备份 `saves/` 与 `config/`。
- 不同整合包请使用独立游戏目录，避免配置与模组互相污染。

## 5. 配置说明

`config/` 为作者本机的调校基线，主要涉及以下文件：

- `vulkanmod_settings.json`、`vulkanmod-extra-options.json`：Vulkan 后端与附加选项。
- `renderscale.json5`：内部渲染分辨率比例。
- `dynamic_fps.json`：失焦降帧策略。
- `c2me.toml`、`vmp.properties`、`threadtweak.json`：区块与线程相关参数。
- `lithium.properties`、`modernfix-mixins.properties`、`ferritecore.mixin.properties`：逻辑与内存优化开关。
- `immediatelyfast.json`、`entityculling.json`：渲染批处理与剔除。
- `chunky/config.json`：预生成任务参数。

调整建议：每次只修改一类参数，修改前做好备份；渲染距离与 RenderScale 对帧率影响最大，建议先在 8–12 区块、0.5–1.0 倍渲染比例之间测试。

## 6. 性能预期与已知限制

- 实际帧率取决于 CPU 单核性能、GPU、驱动版本、分辨率与渲染距离，本项目不承诺具体数值。
- VulkanMod 对驱动要求较高，较旧的显卡或核显可能出现兼容性问题。
- C2ME 为 alpha、VMP 为 beta、VulkanMod 为 0.5.x，均可能存在版本特异性问题，升级前请查看对应项目的更新日志。
- 首次进入世界或跨越未生成区域时出现卡顿与高占用属于正常现象，可使用 Chunky 预生成缓解。
- 出现崩溃时请保留 `logs/latest.log` 与 `crash-reports/`，并附上模组列表、硬件与驱动信息提交 Issue。

## 7. 仓库结构

```
config/                   模组配置（发行版 overrides）
pack/modrinth.index.json  Modrinth 索引：下载地址、SHA-1/SHA-512、环境标记
tools/mods.lock.json      模组版本锁
tools/build_mrpack.py     构建发行版
docs/MODS.md              模组清单与许可证
```

## 8. 构建与发布

```bash
python tools/build_mrpack.py
```

脚本读取 `pack/modrinth.index.json`，将 `config/` 写入 `overrides/`，并打包为 `dist/Jingye-Performance-<version>.mrpack`。构建过程不下载、不修改模组文件。

发布流程：

1. 更新 `pack/modrinth.index.json` 中的 `versionId` 与模组条目（可对照 `tools/mods.lock.json`）。
2. 重新构建并校验压缩包结构。
3. 创建 `vX.Y.Z` 标签与 Release，上传 `.mrpack` 与 `LICENSE`。

版本号遵循语义化版本：Minecraft 或 Loader 大版本变更时提升主版本号，模组批量更新时提升次版本号，仅配置调整时提升修订号。

## 9. 许可证与第三方声明

本仓库的配置、文档与构建脚本，以及据此构建的 `.mrpack` 发行版，均采用 [BSD 2-Clause](LICENSE) 许可证。

模组、Minecraft 本体及其他第三方资源版权归各自作者所有，并按各自许可证分发；本仓库不包含也不分发这些二进制文件。各模组许可证摘要见 `docs/MODS.md`，具体条款以对应项目页面为准。

Minecraft 是 Mojang Studios / Microsoft 的商标，本项目与其无隶属关系，亦不提供游戏本体或账号。

## 10. 致谢

感谢 Fabric 与所有模组作者，以及 Modrinth 提供的分发与元数据服务。

## 11. 反馈

提交 Issue 时请附上：整合包版本、Minecraft/Fabric/Java 版本、完整模组列表、`logs/latest.log`、`crash-reports/` 内容，以及 CPU、GPU 与驱动版本。功能建议与配置调优经验同样欢迎。
