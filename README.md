# Codex Skills

这个仓库是 `~/.codex/skills` 的镜像备份，目录结构与本地全局 skills 目录保持一致。

适用场景：
- 备份当前 Codex 全局 skills
- 在新机器上快速恢复 skills
- 团队共享常用 skills
- 基于现有 skills 继续迭代

## 仓库结构

仓库根目录直接对应本地的 `C:\Users\<用户名>\.codex\skills\`：

- `.system/`：系统级 skills 与辅助脚本
- `backend-design/`：Java / Spring Boot / Spring Cloud 后端架构技能
- `jupyter-notebook/`：Jupyter Notebook 创建与编辑技能
- `playwright/`：终端浏览器自动化技能
- `playwright-interactive/`：持久化交互式 Playwright 调试技能
- `task-planner/`：复杂任务规划、分阶段执行与进度跟踪技能
- `ui-ux-pro-max/`：UI/UX 设计与前端界面实现技能

## 如何安装到 Codex

### Windows

克隆仓库：

```powershell
git clone git@github.com:jizhaoyu/codex-skills.git
```

把仓库内容复制到全局 skills 目录：

```powershell
Copy-Item -Path .\codex-skills\* -Destination "$env:USERPROFILE\.codex\skills" -Recurse -Force
Copy-Item -Path .\codex-skills\.system -Destination "$env:USERPROFILE\.codex\skills" -Recurse -Force
```

复制完成后，重启 Codex，使新 skills 生效。

### macOS / Linux

```bash
git clone git@github.com:jizhaoyu/codex-skills.git
cp -R codex-skills/* ~/.codex/skills/
cp -R codex-skills/.system ~/.codex/skills/
```

复制完成后，重启 Codex。

## 如何使用这些 Skills

Codex 会根据两种方式使用 skill：

1. 显式调用：在提示词里直接写 `$skill-name`
2. 隐式触发：当你的任务和某个 skill 的 `description` 高度匹配时，Codex 会自动选择它

示例：

```text
用 $task-planner 帮我拆解并执行这次重构任务
```

```text
用 $jupyter-notebook 创建一个用于数据探索的 notebook
```

```text
用 $playwright 自动打开这个页面并截图
```

```text
用 $ui-ux-pro-max 重做这个仪表盘界面
```

## 当前包含的 Skills

### 用户级 Skills

- `backend-design`
  - Java 资深架构师技能，用于 Spring Boot 3.x + Spring Cloud 企业级后端项目
- `jupyter-notebook`
  - 用于创建、脚手架化和编辑 `.ipynb` notebook，附带模板和生成脚本
- `playwright`
  - 用于浏览器自动化、截图、表单操作和页面数据提取
- `playwright-interactive`
  - 用于持久浏览器 / Electron 交互式调试
- `task-planner`
  - 用于复杂任务拆解、阶段执行、风险识别和 markdown 计划维护
- `ui-ux-pro-max`
  - 用于 UI/UX 设计、前端界面实现、设计系统和风格方案生成

### 系统级 Skills

- `skill-creator`
  - 用于创建或更新 Codex skills
- `skill-installer`
  - 用于从 GitHub 或 curated 列表安装 skills

## Skill 目录约定

一个标准 skill 通常包含这些内容：

- `SKILL.md`：技能定义与触发描述
- `agents/openai.yaml`：界面元数据
- `scripts/`：可执行脚本
- `references/`：按需加载的参考文档
- `assets/` 或其他资源目录：模板、图标、数据文件等

## 更新仓库

当你在本地修改了 `~/.codex/skills` 后，可以重新同步到这个仓库：

```powershell
Copy-Item -Path "$env:USERPROFILE\.codex\skills\*" -Destination .\codex-skills -Recurse -Force
Copy-Item -Path "$env:USERPROFILE\.codex\skills\.system" -Destination .\codex-skills -Recurse -Force
git add .
git commit -m "Update Codex skills"
git push
```

## 说明

- 仓库当前包含 `.system` 目录，便于完整备份和迁移
- 某些 `.system` skills 可能本来就是 Codex 预装项；保留它们主要是为了版本固定和可迁移
- 如果你新增了自定义 skill，按同样目录结构放到仓库根目录即可
