# blender-3D-to-Sewing

Blender 3D 模型转换到缝纫矢量图，可直接打印开板。

![Blender](https://img.shields.io/badge/Blender-5.1.1-orange)
![License](https://img.shields.io/badge/License-GPLv2-blue)

---

## 📖 简介

这是一个 Blender 插件，可以将带有**接缝（Seams）**的 3D 网格模型转换为**缝纫纸样（Sewing Pattern）**，导出为 SVG 矢量图，可直接用于打印和裁剪布料。

适用于：服装设计、角色布料制作、Cosplay 道具制作等需要将 3D 模型展开为平面纸样的场景。

---

## ✨ 功能特性

- ✅ **生成缝纫纸样** - 将带接缝的 3D 网格展开为平面纸样
- ✅ **导出 SVG** - 导出为可缩放矢量图形，可直接打印
- ✅ **对齐标记** - 自动检测并生成缝合边对齐标记（彩色线条）
- ✅ **布料模拟预设** - 一键设置 Blender 自带布料模拟参数
- ✅ **简体中文界面** - 完整汉化，降低使用门槛
- ✅ **兼容 Blender 5.1.1** - 支持最新版本

---

## 📦 安装方法

### 方法一：直接安装（推荐）

1. 下载本仓库所有文件
2. 将 `blender-seams-to-sewing-pattern-master` 文件夹复制到 Blender 插件目录：
   - **Windows**: `%APPDATA%\Blender Foundation\Blender\5.1\scripts\addons\`
   - **macOS**: `~/Library/Application Support/Blender/5.1/scripts/addons/`
   - **Linux**: `~/.config/blender/5.1/scripts/addons/`
3. 打开 Blender → **编辑** → **偏好设置** → **插件**
4. 搜索 `Seams to Sewing Pattern`，勾选启用

### 方法二：从 GitHub 克隆

```bash
git clone https://github.com/Crazyfantasy-Weilan/blender-3D-to-Sewing.git
```

然后将文件夹复制到 Blender 插件目录（同上）。

---

## 🚀 使用方法

### 基本流程

1. **准备模型**
   - 在 Blender 中创建一个网格物体（或导入现有模型）
   - 进入**编辑模式**，选择需要裁剪的边
   - 按 `Ctrl+E` → **标记接缝（Mark Seam）**

2. **生成纸样**
   - 选中物体，点击 **物体** → **缝纫纸样** → **生成缝纫纸样**
   - 或按 `N` 键打开侧边栏 → **缝纫纸样** 面板
   - 在弹出的对话框中设置参数，点击确认

3. **导出 SVG**
   - 点击 **物体** → **缝纫纸样** → **导出缝纫纸样 (.svg)**
   - 选择保存路径即可

4. **布料模拟（可选）**
   - 点击 **物体** → **缝纫纸样** → **布料模拟设置**
   - 插件会自动写入预调试好的基础参数

### 参数说明

#### 生成缝纫纸样

| 参数 | 说明 |
|------|------|
| UV展开方式 | 角度法 / 保形法 / 保留现有UV |
| 复制原物体 | 在副本上操作，保留原物体 |
| 应用修改器 | 操作前应用所有修改器 |
| 重新网格化 | 使用边界对齐重网格化 |
| 目标三角面数 | 重网格化的目标三角面数量 |

#### 布料模拟设置

| 分组 | 参数 | 默认值 |
|------|------|--------|
| 缝合设置 | 启用缝合 / 最大缝合力 / 最大缝合距离 | 开启 / 5.0 / 5.0 |
| 压力/充气 | 启用压力 / 压力值 | 开启 / 5.0 |
| 物理设置 | 空气粘度 / 质量步数 / 质量 / 倍增速率 | 10 / 10 / 0.3kg / 1.0 |
| 硬度设置 | 张力硬度 / 压缩硬度 / 切变硬度 / 弯曲硬度 | 0.3 / 0 / 5.0 / 0.5 |

> 💡 **提示**：所有立场权重已预设为 0，避免外部力场干扰布料模拟。

---

## 📝 更新日志

### 2023-06-07
- ✅ 兼容 Blender V5.1.1
- ✅ 删除原有模拟方案
- ✅ 增加调用 Blender 自带布料模拟
- ✅ 增加写入预调试基础参数
- ✅ 增加脚本使用方法
- ✅ 降低脚本使用难度
- ✅ 支持简体中文

---

## 📄 许可证

本项目基于 **GNU General Public License v2 (GPLv2)** 开源。

```
Copyright (C) 2023 Crazyfantasy-Weilan

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
```

---

## 🙏 致谢

- 原作者 **Thomas Kole** - 原始项目 [blender-seams-to-sewing-pattern](https://blenderartists.org/t/1248713)
- 所有贡献者和用户

---

## 📬 联系

- GitHub: [Crazyfantasy-Weilan](https://github.com/Crazyfantasy-Weilan/blender-3D-to-Sewing)
