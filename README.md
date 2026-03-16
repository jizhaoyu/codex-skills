# Codex Skills

这个仓库是 `~/.codex/skills` 的镜像备份，也可以直接作为一套可复用的 Codex skills 集合来安装和分发。

它适合这些场景：

- 备份自己当前的全局 skills
- 在新机器上恢复 Codex 环境
- 团队共享一组常用技能
- 以现有 skill 为模板继续扩展

## 仓库结构

仓库根目录直接对应本地的 `~/.codex/skills/`：

- `.system/`：系统级 skills 与辅助脚本
- `backend-design/`：Java / Spring Boot / Spring Cloud 后端架构 skill
- `jupyter-notebook/`：Jupyter Notebook 创建与编辑 skill
- `playwright/`：终端浏览器自动化 skill
- `playwright-interactive/`：持久化 Playwright 调试 skill
- `task-planner/`：复杂任务规划、阶段执行与进度维护 skill
- `ui-ux-pro-max/`：UI/UX 设计与前端实现 skill

## 安装到 Codex

### Windows

```powershell
git clone git@github.com:jizhaoyu/codex-skills.git
Copy-Item -Path .\codex-skills\* -Destination "$env:USERPROFILE\.codex\skills" -Recurse -Force
Copy-Item -Path .\codex-skills\.system -Destination "$env:USERPROFILE\.codex\skills" -Recurse -Force
```

### macOS / Linux

```bash
git clone git@github.com:jizhaoyu/codex-skills.git
cp -R codex-skills/* ~/.codex/skills/
cp -R codex-skills/.system ~/.codex/skills/
```

复制完成后，重启 Codex，让新 skills 生效。

## Codex 如何使用 Skills

Codex 主要有 3 种方式用 skill：

1. 显式调用：在提示词里写 `$skill-name`
2. 隐式触发：用户请求和某个 skill 的 `description` 高度匹配时，Codex 自动选择它
3. 组合使用：一个请求同时触发多个 skill，例如先规划，再实现，再做 UI 调试

最重要的规则：

- 显式调用时，使用的是 `SKILL.md` 里的 `name`，不一定等于目录名
- 例如目录是 `backend-design/`，但真正的调用名是 `$java-dev`
- 如果刚安装或更新了 skill，通常需要重启 Codex
- 下面所有脚本示例默认 `CODEX_HOME=~/.codex`

## Skills 索引

| 目录 | 调用名 | 主要用途 |
|---|---|---|
| `backend-design/` | `$java-dev` | Java 企业级后端架构、Spring Boot / Spring Cloud 项目搭建 |
| `jupyter-notebook/` | `$jupyter-notebook` | 创建、脚手架化、编辑 `.ipynb` notebook |
| `playwright/` | `$playwright` | 浏览器自动化、截图、表单操作、数据提取 |
| `playwright-interactive/` | `$playwright-interactive` | 持久化浏览器 / Electron 调试、功能 QA、视觉 QA |
| `task-planner/` | `$task-planner` | 复杂任务拆解、阶段执行、markdown 计划维护 |
| `ui-ux-pro-max/` | `$ui-ux-pro-max` | UI/UX 方案、设计系统、前端界面实现与评审 |
| `.system/skill-creator/` | `$skill-creator` | 创建或更新 Codex skill |
| `.system/skill-installer/` | `$skill-installer` | 从 curated 列表或 GitHub 安装 skill |

## 如何写出能触发 Skill 的请求

最稳妥的方式是直接点名：

```text
用 $task-planner 帮我拆解并执行这次重构
```

```text
用 $java-dev 创建一个 Spring Boot 3 + Redis + MyBatis-Plus 的用户中心
```

```text
用 $ui-ux-pro-max 重新设计这个 SaaS 仪表盘并直接改代码
```

如果不想显式点名，也可以直接描述任务本身。例如：

- “帮我创建一个 Jupyter notebook 做 embedding 实验”
- “自动打开这个网页，登录后截图并导出列表数据”
- “把这个 React 页面改得更像现代 SaaS dashboard”
- “帮我创建一个新的 Codex skill”

## 每个 Skill 的详细用法

### 1. `java-dev` 对应目录 `backend-design/`

适用场景：

- 新建 Java 后端项目
- 新建 Spring Boot 模块
- 设计 Spring Cloud Alibaba 微服务架构
- 按统一规范生成 Controller / Service / Mapper / DTO / VO / PO
- 为现有 Java 项目补齐规范、异常处理、测试结构

这类请求最容易触发：

- “用 $java-dev 初始化一个 Spring Boot 3 项目”
- “帮我生成一个基于 Spring Cloud Alibaba 的微服务骨架”
- “给这个 Java 后端按阿里规范重构目录结构”
- “为用户管理模块生成 controller、service、mapper、dto、vo”

它会怎么工作：

1. 先和你确认技术栈
2. 确认 JDK、构建工具、持久层框架、架构模式
3. 确认默认依赖是否启用，例如 Lombok、Redis、SpringDoc、Hutool
4. 再按照既定分层规范生成代码
5. 默认要求统一返回 `Result<T>`、参数校验、全局异常处理、日志与测试

这个 skill 特别适合：

- 后端脚手架生成
- 中小型企业级后台项目初始化
- 统一代码风格和分层规范
- 把“能跑就行”的 Java 代码整理成规范工程

示例提示词：

```text
用 $java-dev 创建一个单体 Spring Boot 3 项目，JDK 17，Maven，MyBatis-Plus，默认加 Redis、SpringDoc、Hutool。
```

```text
用 $java-dev 为订单模块生成完整分层代码：controller、service、impl、mapper、po、dto、vo、异常处理和测试。
```

```text
用 $java-dev 审查这个 Java 项目的结构和接口设计，指出不符合规范的地方并直接修复。
```

注意：

- 目录名是 `backend-design`，但调用名是 `$java-dev`
- 这个 skill 偏“后端架构和规范”，不是前端、爬虫或数据分析 skill

### 2. `jupyter-notebook`

适用场景：

- 从零创建 `.ipynb`
- 把脚本或笔记整理成结构化 notebook
- 生成探索型 notebook
- 生成教程型 notebook
- 重构已有 notebook，使其更易读、更可复现

它有两种主要模式：

- `experiment`：实验、探索、对比、假设验证
- `tutorial`：教学、演示、分步骤讲解

推荐这样提：

```text
用 $jupyter-notebook 创建一个实验型 notebook，对比 3 种 embedding 模型。
```

```text
用 $jupyter-notebook 把这份 Python 脚本改造成教学型 notebook，面向初学者。
```

Codex 使用这个 skill 时，一般会：

1. 先判断 notebook 是实验型还是教程型
2. 优先使用内置模板，而不是直接手写原始 notebook JSON
3. 用 `scripts/new_notebook.py` 生成初始 notebook
4. 再逐步补充 markdown cell 和 code cell
5. 最后检查可运行性和结构完整性

相关脚本：

- `jupyter-notebook/scripts/new_notebook.py`

直接命令示例：

```bash
uv run --python 3.12 python "$CODEX_HOME/skills/jupyter-notebook/scripts/new_notebook.py" \
  --kind experiment \
  --title "Compare prompt variants" \
  --out output/jupyter-notebook/compare-prompt-variants.ipynb
```

```bash
uv run --python 3.12 python "$CODEX_HOME/skills/jupyter-notebook/scripts/new_notebook.py" \
  --kind tutorial \
  --title "Intro to embeddings" \
  --out output/jupyter-notebook/intro-to-embeddings.ipynb
```

这个 skill 最适合：

- LLM 实验记录
- 数据探索
- AI / 数据科学教程
- 需要给别人复现的分析过程

### 3. `playwright`

适用场景：

- 从终端控制真实浏览器
- 自动打开页面、点按钮、填表单
- 登录后截图
- 抓取页面数据
- 复现 UI 流程问题

前置条件：

- 本机需要有 `Node.js` / `npm`
- 至少要能使用 `npx`

推荐调用方式：

```text
用 $playwright 打开这个网站，完成登录后截图并导出订单列表。
```

```text
用 $playwright 自动复现这个按钮点击后页面跳转错误。
```

Codex 使用这个 skill 的典型流程：

1. 检查 `npx` 是否存在
2. 用包装脚本启动 `playwright-cli`
3. `open` 页面
4. `snapshot` 获取稳定元素引用
5. `click` / `fill` / `press` 等执行交互
6. 页面变化后重新 `snapshot`
7. 截图、导出或继续调试

关键原则：

- 不要在没有新快照时盲点元素
- 每次大幅 DOM 变化后重新 `snapshot`
- 这个 skill 偏 CLI 自动化，不默认生成 `@playwright/test` 测试文件

相关脚本：

- `playwright/scripts/playwright_cli.sh`

直接命令示例：

```bash
"$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh" open https://playwright.dev --headed
"$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh" snapshot
"$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh" screenshot
```

这个 skill 最适合：

- 网站自动化操作
- 截图与验收
- 后台系统表单流调试
- 需要真实浏览器上下文的数据提取

### 4. `playwright-interactive`

适用场景：

- 调试本地 Web 应用
- 调试 Electron 应用
- 保持一个持久浏览器会话，反复修改再验证
- 做功能 QA 和视觉 QA
- 需要同一会话里连续测试多个状态

这个 skill 和 `$playwright` 的区别：

- `$playwright` 偏一次性命令式浏览器自动化
- `$playwright-interactive` 偏“持续会话 + 迭代调试 + QA 验证”

前置条件比较严格：

- 需要启用 `js_repl`
- 通常要用 `danger-full-access` 运行 Codex
- 当前工作目录里要安装 `playwright`

配置 `js_repl`：

```toml
[features]
js_repl = true
```

常见初始化：

```bash
test -f package.json || npm init -y
npm install playwright
node -e "import('playwright').then(() => console.log('playwright import ok')).catch((error) => { console.error(error); process.exit(1); })"
```

推荐这样提：

```text
用 $playwright-interactive 持续调试这个本地 React 项目，保留浏览器会话并做功能和视觉检查。
```

```text
用 $playwright-interactive 检查这个 Electron 应用的启动流程、窗口布局和截图结果。
```

Codex 使用这个 skill 的典型流程：

1. 先列一份 QA 覆盖清单
2. 启动或确认 dev server
3. 运行 bootstrap cell，一次性创建共享 Playwright 句柄
4. 启动 Web 或 Electron 会话
5. 每次代码改动后复用原会话，必要时 reload 或 relaunch
6. 分开做功能 QA 和视觉 QA
7. 截图并校验 viewport、布局、交互与状态变化

这个 skill 最适合：

- 本地前端迭代开发
- Electron UI 调试
- 复杂交互流程回归验证
- 出具“我已经实际点过、看过、截过”的交付结论

### 5. `task-planner`

适用场景：

- 任务很复杂，不能直接一把梭
- 需要分阶段执行
- 需要明确依赖、风险、阻塞项
- 需要一个持久化的 markdown 计划文件
- 需要跨多轮对话持续推进同一任务

推荐这样提：

```text
用 $task-planner 帮我拆解这次重构，先给出阶段计划，再从第一阶段开始执行。
```

```text
用 $task-planner 为这次数据库迁移制定计划，标出风险、依赖和验证步骤。
```

```text
用 $task-planner 创建一个 markdown 计划文件，后续每完成一步都更新进度。
```

Codex 使用这个 skill 的典型流程：

1. 先收集上下文，不盲目开工
2. 建一个简短可执行的 plan
3. 只在真正影响方向时提 1 到 3 个关键问题
4. 选择执行模式
5. 逐阶段推进并同步进度
6. 每个阶段结束后验证结果

这个 skill 还支持“书面计划文件”：

- 模板在 `task-planner/references/plan-template.md`
- 进度更新脚本在 `task-planner/scripts/update_progress.py`

直接命令示例：

```bash
python "$CODEX_HOME/skills/task-planner/scripts/update_progress.py" \
  --file plan.md \
  --task 1 \
  --complete-substep 1 \
  --auto-progress
```

```bash
python "$CODEX_HOME/skills/task-planner/scripts/update_progress.py" \
  --file plan.md \
  --task 2 \
  --status blocked \
  --blocker "Waiting for API contract"
```

这个 skill 最适合和其他 skill 组合使用，例如：

- `$task-planner` + `$java-dev`
- `$task-planner` + `$ui-ux-pro-max`
- `$task-planner` + `$playwright-interactive`

### 6. `ui-ux-pro-max`

适用场景：

- 设计网站、落地页、Dashboard、后台系统、移动端界面
- 改进现有 UI 视觉质量
- 评审交互、可访问性、响应式和视觉一致性
- 生成设计系统，再据此落代码
- 需要更有方向感的风格，而不是普通模板风

推荐这样提：

```text
用 $ui-ux-pro-max 重做这个 SaaS dashboard，风格更大胆，直接输出 React 实现。
```

```text
用 $ui-ux-pro-max 评审这个页面的可访问性、排版、色彩和响应式问题，并直接修复。
```

```text
用 $ui-ux-pro-max 为一个医疗行业落地页生成完整设计系统，然后实现 html-tailwind 版本。
```

Codex 使用这个 skill 的典型流程：

1. 先分析产品类型、行业、风格关键词和技术栈
2. 先生成设计系统
3. 再补充做风格、UX、图表、字体等领域搜索
4. 最后按目标技术栈实现，未指定时默认 `html-tailwind`
5. 交付前检查无障碍、触控、性能、响应式、排版和动画

这个 skill 自带搜索脚本，可直接生成设计系统：

```bash
python3 "$CODEX_HOME/skills/ui-ux-pro-max/scripts/search.py" "beauty spa wellness service" --design-system -p "Serenity Spa"
```

如果需要把设计系统持久化到项目里：

```bash
python3 "$CODEX_HOME/skills/ui-ux-pro-max/scripts/search.py" "fintech dashboard premium" --design-system --persist -p "FinPilot"
```

如果要补充指定领域：

```bash
python3 "$CODEX_HOME/skills/ui-ux-pro-max/scripts/search.py" "animation accessibility" --domain ux
python3 "$CODEX_HOME/skills/ui-ux-pro-max/scripts/search.py" "elegant luxury" --domain typography
python3 "$CODEX_HOME/skills/ui-ux-pro-max/scripts/search.py" "real-time dashboard" --domain chart
```

如果要按技术栈拿实现建议：

```bash
python3 "$CODEX_HOME/skills/ui-ux-pro-max/scripts/search.py" "b2b saas analytics" --stack react
```

这个 skill 最适合：

- 直接改前端代码
- 先做设计系统再实现
- 对现有界面做专业级评审
- 让界面更有辨识度，而不是通用模板感

### 7. `skill-creator`

适用场景：

- 你想新增一个 Codex skill
- 你想把某套重复工作流程封装成 skill
- 你要更新已有 skill 的说明、资源或脚本

推荐这样提：

```text
用 $skill-creator 帮我把这个内部部署流程整理成一个 Codex skill。
```

```text
用 $skill-creator 更新这个 skill，让它支持更多脚本和 references。
```

Codex 使用这个 skill 的典型流程：

1. 先理解 skill 的实际使用场景
2. 识别哪些内容应该放进 `scripts/`、`references/`、`assets/`
3. 用 `init_skill.py` 初始化目录骨架
4. 编写或更新 `SKILL.md`
5. 用 `quick_validate.py` 校验 skill 结构

常用脚本：

```bash
python "$CODEX_HOME/skills/.system/skill-creator/scripts/init_skill.py" my-skill --path skills/public --resources scripts,references
```

```bash
python "$CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py" path/to/my-skill
```

这个 skill 最适合：

- 搭建新的专业化工作流
- 把团队经验沉淀成可复用能力
- 批量改进已有 skill 的规范性

### 8. `skill-installer`

适用场景：

- 从 OpenAI curated 列表安装 skill
- 从 GitHub 仓库安装 skill
- 从某个 repo 的指定路径安装 skill
- 查看哪些 skill 已安装、哪些还没安装

推荐这样提：

```text
用 $skill-installer 列出当前可安装的 curated skills。
```

```text
用 $skill-installer 从 GitHub 安装这个仓库里的某个 skill。
```

```text
用 $skill-installer 安装 openai/skills 里的 experimental skill。
```

Codex 使用这个 skill 的典型流程：

1. 先决定是列出 skill、安装 curated skill，还是从 GitHub URL 安装
2. 调用内置脚本处理下载或稀疏检出
3. 把 skill 安装到 `~/.codex/skills/<skill-name>`
4. 完成后提醒你重启 Codex

常用命令：

```bash
python "$CODEX_HOME/skills/.system/skill-installer/scripts/list-skills.py"
```

```bash
python "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --url https://github.com/<owner>/<repo>/tree/main/<path>
```

注意：

- 这个 skill 依赖网络
- 在受限沙箱里通常需要提权
- 安装完成后通常需要重启 Codex

## 多个 Skill 一起用

下面这些组合很常见：

### 规划 + 实现

```text
用 $task-planner 和 $java-dev 帮我把这个旧系统拆成 4 个阶段重构，并从第一阶段开始改代码。
```

### 设计 + 前端实现

```text
用 $ui-ux-pro-max 为这个管理后台建立设计系统，然后直接修改 React 页面。
```

### 实现 + 浏览器验收

```text
先用 $ui-ux-pro-max 改页面，再用 $playwright-interactive 做功能和视觉验收。
```

### 任务推进 + 浏览器调试

```text
用 $task-planner 拆分这个前端修复任务，然后结合 $playwright-interactive 分阶段验证。
```

### 新建 Skill

```text
用 $skill-creator 创建一个新的 Codex skill，完成后再用 $task-planner 拆解后续迭代工作。
```

## 什么时候应该显式点名 Skill

建议显式写 `$skill-name` 的情况：

- 你很清楚要用哪一个 skill
- 目录名和 skill 名不一致，例如 `backend-design/` 对应 `$java-dev`
- 任务可能同时匹配多个 skill，但你想强制指定一个
- 你要组合多个 skill

如果你不点名，Codex 也可能自动触发，但自动选择更依赖 `description` 是否精确匹配你的请求。

## Skill 目录约定

一个典型 skill 一般包含：

- `SKILL.md`：skill 的定义、触发说明和工作流
- `agents/openai.yaml`：面向界面的元数据
- `scripts/`：可执行脚本
- `references/`：按需加载的参考文档
- `assets/` 或其他资源目录：模板、图标、数据文件等

## 更新这个仓库

当你在本地修改了 `~/.codex/skills` 后，可以重新同步：

```powershell
Copy-Item -Path "$env:USERPROFILE\.codex\skills\*" -Destination .\codex-skills -Recurse -Force
Copy-Item -Path "$env:USERPROFILE\.codex\skills\.system" -Destination .\codex-skills -Recurse -Force
git add .
git commit -m "Update Codex skills"
git push
```

## 说明

- 仓库保留了 `.system` 目录，方便完整迁移
- 某些 `.system` skill 本来就是 Codex 预装项；这里保留它们主要是为了固定版本和便于备份
- 如果你新增了自定义 skill，按同样目录结构放到仓库根目录即可
