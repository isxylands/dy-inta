# DYINT 场景 2：2026 年 5 月商船安全事件数据包实现计划

计划日期：2026-07-10

计划版本：v1.2（已吸收 2026-07-10 双专题、共享基础与 HTML Mock 反馈）

计划状态：`READY_FOR_REVIEW_WITH_PROTOTYPE_GATE`

源文档：`devdoc/DYINT场景2-5月商船攻击候选目标分析与数据补强方案.md`

源文档类型：候选事件分析、推荐方案与数据补强路径的混合材料

源文档更新时间：2026-07-09 21:51:04 +0800

源文档所在目录：`devdoc/`

关联材料：

- `devdoc/DYINT场景2-3Demo数据规则与补强方案.md`
- `devdoc/DYINT场景2-3Demo数据规则与补强方案-售前演示方案评审报告.md`
- `devdoc/DYINT场景2-3Demo客户版演示脚本.md`
- `devdoc/DYINT场景2-6月10至12日霍尔木兹风险窗口目标包.md`
- `devdoc/DYINT场景2-6月10至12日霍尔木兹风险窗口目标包-实现计划.md`
- `devdoc/DYINT场景2双专题交互Mock.html`
- `/Users/liushen/Documents/cursorDevs/gintbroker/docs/himars-topic-work-plan.md`
- `/Users/liushen/Documents/cursorDevs/gintbroker/docs/backend_mvp_process.md`
- `/Users/liushen/Documents/cursorDevs/gintbroker/docs/dev-deploy/构建部署配置链路说明.md`

本计划负责两项闭环：一是把已选定的 `UKMTO 062-26` 商船安全事件整理为可复现、可校验、可脱敏的小型发布包；二是把它作为独立的 `event_case` 军事专题接入 `gintbroker` 现有“军事专题”入口，展示 AOI、海事事件、匿名遥测摘要、证据矩阵、专题回放和保护性任务。它与 6 月霍尔木兹 `risk_window` 是两个 topic ID、两个 bundle、两条专题时间线，不合并成一个专题的两个页面；两者共用数据工程基础、专题 API、地图渲染、详情、回放、授权和质量门禁。原始 AIS/ADS-B、Excel、PDF、商业数据和隔离明细始终留在原路径或外部磁盘，不复制进 `dy-inta`、`gintbroker` 或项目根目录临时区。

本计划允许后续执行者在用户明确要求按本计划执行时修改 `gintbroker`；本轮只更新计划，不修改 `gintbroker` 代码。`doops-dev`、`moye-v4-product` 仍保持只读/不实施边界。不输出攻击方判断、精确军事目标、武器推断或进攻性行动建议。

### 本轮反馈处理

| 反馈 | 处理结论 | 落点 |
| --- | --- | --- |
| 原始文件不要搬进项目 `.work/` | `采纳` | 原始文件原地只读；中间文件、隔离记录和公共源缓存改到外部磁盘可配置工作区；仓库只保留小型脱敏发布包 |
| Demo 基于 `gintbroker` 军事专题呈现 | `采纳` | HTML Mock 只作为实施前设计契约；最终运行态仍由 `gintbroker` 通用专题 bundle、地图、右侧详情、专题回放和目标环境回归交付 |
| `gintbroker` 需要哪些增强 | `采纳` | 现场代码和 API 已确认“入口动态但实体键、图层、详情和 slow payload 仍写死 HIMARS”；计划改为先通用化，再接 DYINT 专题 |
| 两个 Demo 是一个专题还是两个专题 | `采纳` | 固定为两个独立专题：`dyint_sc2_20260526/event_case` 与 `dyint_sc2_20260610_12/risk_window`；只共享底座，不共享业务状态和时间线 |
| 共性能力不要重复建设 | `采纳` | 新增数据工程与 `gintbroker` 两层 foundation 探针；首个计划 `bootstrap`，后执行计划必须 `reuse/resume`，禁止复制 API、scanner、validator、source/layer 或详情/回放组件 |
| 实施前先看可交互效果 | `采纳` | 新增仓库内 `devdoc/DYINT场景2双专题交互Mock.html` 和 T0.5 原型评审 Gate；未获明确确认时不得进入 T1 及后续实现 |

---

## 1. 背景、目标与完成口径

### 1.1 已确认目标

主事件固定为：

- 事件 ID：`SC2-20260526-MUSCAT-TANKER-ATTACK`
- 专题 ID：`dyint_sc2_20260526`
- 专题类型：`topic_kind=event_case`
- 专题组：`topic_group=dyint_sc2_maritime_risk`，仅用于列表归类，不合并 bundle、时间线或评分状态
- 客户版名称：阿曼外海油轮安全事件后的航运风险验证
- 权威触发源：`UKMTO Warning 062-26`
- 后验汇总源：`JMIC Update 050`、`JMIC Update 058`
- 主时间：2026-05-26 09:45 UTC，以最终归档的 UKMTO 原文为准
- 主数据窗：2026-05-20 至 2026-05-28
- 客户动作：提升监测、二次确认、通知相关方、持续观察、报告归档

### 1.2 两级完成口径

本计划分为两个 Gate，不得把内部可用误报为客户可用：

在两个交付 Gate 之前还有共享前置门禁 `PROTOTYPE_APPROVED`：用户/产品责任人必须实际打开 `devdoc/DYINT场景2双专题交互Mock.html`，完成两个专题切换、时间回放、证据/任务、客户视图和“复用边界”走查，并明确给出 `approved`。当前状态为 `DRAFT_REVIEW_REQUIRED`。该 Gate 只确认信息架构和交互预期，不把 Mock 中示意地图、分数或文案当作数据事实。

| Gate | 完成条件 | 允许用途 |
| --- | --- | --- |
| `INTERNAL_READY` | 数据包可重复构建；`gintbroker` 本地专题可打开、聚焦、回放和查看证据；不确定性、样例数据和未授权素材均有明确标签；6 张真实系统截图可走查 | 内部评审、产品/数据/售前彩排 |
| `CUSTOMER_READY` | `INTERNAL_READY` 已通过；正式 AOI 已审批；客户可见素材均有展示/截图许可；目标船和遥测已匿名；目标环境 `192.168.211.195:3001` 真实浏览器回归和主持人口径复审通过 | 客户现场演示、截图、录屏和报告样例 |

只完成 `INTERNAL_READY` 不等于整体完成。若客户 Gate 仍缺授权、正式 AOI 或外部核验，执行记录必须标记 `BLOCKED_CONFIRM`，不能写“已完成客户版”。

### 1.3 可交付成果

共享预实现设计产物固定为：

```text
devdoc/DYINT场景2双专题交互Mock.html
```

该文件是自包含、无外部网络请求的评审 Mock，保留在 `dy-inta`，不复制到 `gintbroker`，也不作为运行时依赖。计划执行后还应形成以下仓库内产物：

```text
demo_packages/sc2_20260526_muscat_tanker_attack/
  README.md
  00_manifest/
    target_definition.csv
    source_manifest.csv
    data_manifest.csv
    assumptions.md
    build_inventory.csv
  01_aoi/
    aoi_catalog.geojson
    aoi_quality.csv
  02_events/
    event_results.csv
    maritime_advisories.csv
    news_claims.csv
    vessel_identity_candidates.csv
  03_telemetry/
    ais_daily_aoi_summary.csv
    adsb_daily_aoi_summary.csv
    nearby_vessel_candidates.csv
    telemetry_quality.csv
  04_fusion/
    evidence_matrix.csv
    evidence_links.csv
    score_timeline.csv
    confirmation_tasks.csv
  05_customer_assets/
    protective_report.md
    presenter_script.md
    screen_manifest.csv
    screenshots/
      01_customer_pressure.png
      02_event_definition.png
      03_risk_timeline.png
      04_aoi_map.png
      05_evidence_matrix.png
      06_confirmation_report.png
  06_validation/
    validation_report.md
    source_count_reconciliation.csv
    output_checksums.sha256
    internal_screenshots/

tools/dyint_demo_common/
  README.md
  io_utils.py
  schemas.py
  manifest.py
  telemetry.py
  quality.py
  validate_package.py
  export_topic.py

tools/sc2_20260526/
  README.md
  constants.py
  build_manifest.py
  build_aoi.py
  build_events.py
  build_ais.py
  build_adsb.py
  build_fusion.py
  export_gintbroker_topic.py
  validate_package.py

tests/dyint_demo_common/
  test_schema.py
  test_temporal_gate.py
  test_telemetry_dedupe.py
  test_customer_gate.py

tests/sc2_20260526/
  test_manifest.py
  test_temporal_integrity.py
  test_telemetry_quality.py
  test_referential_integrity.py
  test_customer_gate.py
```

`tools/sc2_20260526/build_ais.py`、`build_adsb.py`、`validate_package.py` 和 `export_gintbroker_topic.py` 只能是场景配置/编排薄层，必须调用 `tools/dyint_demo_common/`；不得复制分块读取、复合去重、schema、授权、脱敏或 bundle 导出实现。6 月计划使用同一 common 包。

`gintbroker` 需新增或修改的发布快照与代码：

```text
/Users/liushen/Documents/cursorDevs/gintbroker/
  backend/data/topics/dyint_sc2_20260526.json
  backend/data/dyint_sc2_20260526/bundle.json
  backend/data/dyint_sc2_20260526/release_manifest.json
  backend/services/topics/schema.py
  backend/services/topics/service.py
  backend/routers/topics.py
  backend/tests/test_topics_api.py
  backend/tests/test_topics_bundle.py
  frontend/src/types/dashboard.ts
  frontend/src/hooks/useTopicBundle.ts
  frontend/src/components/WorldviewLeftPanel.tsx
  frontend/src/components/MaplibreViewer.tsx
  frontend/src/components/map/geoJSONBuilders.ts
  frontend/src/components/NewsFeed.tsx
  frontend/src/components/TopicDetailPanel.tsx
  frontend/src/components/TopicReplayPanel.tsx
  frontend/src/app/page.tsx
  frontend/src/i18n/translations/zh-CN.json
  frontend/src/i18n/translations/en.json
  frontend/src/__tests__/components/TopicDetailPanel.test.tsx
  frontend/src/__tests__/components/TopicReplayPanel.test.tsx
  frontend/src/__tests__/components/WorldviewLeftPanel.test.tsx
  frontend/src/components/map/geoJSONBuilders.test.ts
```

原始 CSV、Excel、PDF、商业数据、临时下载、未脱敏对象表和隔离记录不得提交到任何仓库，也不得复制到仓库根目录下 `.work/`。它们保持原地只读；新增中间文件统一写到外部磁盘的 `DYINT_SCRATCH_ROOT`。仓库只允许保存经过对应 audience Gate 的小型脱敏派生表、`gintbroker` 发布 bundle、校验报告和最终 6 张验收截图；过程截图、录屏和浏览器缓存仍放外部工作区。

### 1.4 非目标

- 不实现生产级采集、流处理、动态本体入图或规则下发。
- 不采购商业 AIS、SAR、天气或船舶登记数据。
- 不补全攻击方、武器类型、攻击路径或行动建议。
- 不把 5 月 22/23 日异地小型船只接近事件包装成 5 月 26 日主事件的已证实前兆。
- 不把样例 Excel 中的强身份名或演示轨迹当作客户事实。
- 不扩展到 2 月基线、4 月过渡或 6 月风险窗口的全量数据包；它们继续由相邻方案管理。
- 不把 DYINT 历史回放混入 `gintbroker` 的全局 Time Machine 快照存储；专题回放使用只读 bundle 和内存状态，不额外生成按小时快照。
- 不在本计划内改 `doops-dev`、`moye-v4-product`、Jenkins 配置或远端 `.env`。
- 不把 HTML Mock 发布到 `gintbroker`、CI 或客户环境，也不让真实系统运行时读取 Mock 中的示意数据。

---

## 2. 当前事实、旧语义与材料缺口

### 2.1 计划编写时的仓库快照

| 项 | 当前事实 |
| --- | --- |
| 仓库 | `/Users/liushen/Documents/githubDevs/dy-inta` |
| 分支 | `main` |
| upstream | `origin/main` |
| ahead/behind | 不在计划正文固化；执行前由 T0 现场重新确认 |
| 工作区 | 计划编写前干净；执行时以 T0 重新检查为准 |
| 现有代码 | 无 `demo_packages/`、无数据构建脚本、无自动校验器 |
| Python | Codex bundled Python 3.12.13；已探测 `pandas 2.2.3`、`openpyxl 3.1.5` |
| 外部盘 | 计划编写时可读；不能假设后续执行时仍挂载 |

`gintbroker` 现场快照（2026-07-10，只读核验）：

| 项 | 当前事实 |
| --- | --- |
| 仓库/commit | `/Users/liushen/Documents/cursorDevs/gintbroker`，`main=a4eb2ad`，与 `origin/main` 一致，工作区干净 |
| 现网入口 | `http://192.168.211.195:3001/` 可打开，页面标题为 `T R S - G I S A`；用户截图显示左侧“军事专题”、右侧“全球军事情报”和“时间机器” |
| 专题 API | `/api/topics` 只有 `himars` 1 个专题；`/api/topics/himars/brief` 返回 6 个实体、0 条最新情报 |
| 数据质量 | 6 个 HIMARS 实体均没有 `position_mode`；当前 `himars_intel` 为 0 |
| 后端通用度 | `/api/topics/{topic_id}/*` 路由和 topic config 是通用的，但 `get_topics_slow_payload()` 只把 HIMARS 映射为 `himars_entities` / `himars_intel` |
| 前端通用度 | 左侧专题名称来自 `/api/topics`，但 `ActiveLayers`、`TOPIC_ENTITY_ACCESSORS`、GeoJSON builder、MapLibre source/layer、NewsFeed 详情和专题列表仍写死 HIMARS |
| 时间回放 | 全局 `TimelinePanel` 面向实时快照，带单独快照存储和回放语义；不适合直接承载历史事件 bundle |

### 2.2 当前输入事实

| 输入 | 路径或来源 | 当前状态 | 用途 | 限制 |
| --- | --- | --- | --- | --- |
| AIS 5 月原始表 | `/Volumes/exFAT466/海贝数据_2月1到6月15_AIS和ADS-B/AIS/event_vessel_route_202605.csv` | 可读，约 370MB | 5 月 20-28 日 AOI 聚合 | 文件名不能代替事件时间；存在跨月、重复、空值和速度质量问题 |
| ADS-B 5 月日表 | `/Volumes/exFAT466/海贝数据_2月1到6月15_AIS和ADS-B/ADS-B/event_trajectory1_source_date_20260501_20260531/` | 31 个有效日文件可读，另有 `._*` sidecar | 5 月 20-28 日 AOI 聚合 | `IR_LASTTIME` 多为空；身份和速度质量不足；必须忽略 `._*` |
| 新闻样例 | `~/Documents/非Coding工作/DYINT/O多源情报系统/样例数据/sample-news-dataVISA0260613.xlsx` | 2 个 sheet，主表 26 行含表头 | 背景主张和字段映射样例 | 不能代替 UKMTO/JMIC 事实源；原始内容不直接进客户包 |
| AIS 样例 | 同目录 `事件数据AISV2_0260613.xlsx` | 60 行含表头 | 规则和内部彩排方法样例 | 强身份名疑似造数，禁止进入客户事实链 |
| ADS-B 样例 | 同目录 `system.event_trajectory1_20260613.xlsx` | 29 行含表头 | 规则和内部彩排方法样例 | 身份不能独立核验，禁止直接定性 |
| 地理知识库 | 同目录 `地理知识库/*.csv` | `12NM`、`24NM`、EEZ、海岸线等 WKT 可读 | AOI 边界参考 | 没有现成 Muscat 事件区和港口进近区；不能自动等同正式 AOI |
| 公开海事源 | 源文档中的 UKMTO/JMIC URL | 待重新归档和记录可见时间 | 主事件、后验确认、事件簇 | URL 可访问性、发布时间、许可和原文内容必须在 T1 复核 |

### 2.3 旧语义必须先保留

当前源文档是人工分析底稿，已有语义不能在自动化过程中被悄悄改变：

1. 主事件是“已报告的商船安全事件”，不是攻击方识别任务。
2. `UKMTO 062-26` 是主触发源；JMIC 和媒体是后验确认或 enrichment，不能逆流到事前评分。
3. 目标船身份以 `withheld` 为事实，`OLYMPIC LIFE` 只能标为候选，未经登记源核验不得直接展示。
4. AIS/ADS-B 只支持区域活动和数据质量说明，不证明攻击发生、目标身份、故意关闭 AIS 或军事属性。
5. 当前三个矩形 AOI 是粗筛选范围，不是精确事件点或正式海图边界。
6. 5 月 22/23 日事件与主事件不在同一 AOI，只能作为区域背景；不得因时间接近就标成直接前兆。
7. 5 月 28 日新闻主张发生在主事件之后，只能展示信息冲突和证据降级。
8. 当前人工统计值是复现基线，不是最终真值；去重、时间清洗后如变化，必须同时保留原始口径和清洗口径解释。

### 2.4 双专题边界与两层共享基础

两个 Demo 固定为两个独立军事专题，不采用“一个 DYINT 专题内再切 5 月/6 月子页面”的结构：

| 契约 | 5 月专题 | 6 月专题 | 是否共享 |
| --- | --- | --- | --- |
| `topic_id` | `dyint_sc2_20260526` | `dyint_sc2_20260610_12` | 否 |
| `topic_kind` | `event_case` | `risk_window` | 否 |
| bundle / timeline / release hash | 独立 | 独立 | 否 |
| 证据、评分、任务和主持叙事 | 单事件闭环 | 区域风险窗口 | 否 |
| `topic_group` | `dyint_sc2_maritime_risk` | `dyint_sc2_maritime_risk` | 仅列表归类 |
| manifest、时间门禁、遥测分块读取、复合去重、质量码、脱敏、exporter | 同一 `tools/dyint_demo_common/` | 同一 `tools/dyint_demo_common/` | 是，只建一次 |
| TopicBundle schema、API、MapLibre source/layer、详情、回放、audience Gate | 同一通用实现 | 同一通用实现 | 是，只建一次 |

前端状态契约：`selectedTopicId` 同一时刻至多一个，驱动右侧详情和专题回放；`activeTopicIds` 可以启用多个地图叠加，但默认只启用并选择当前专题。两个专题同时启用时必须用 topic 颜色/图例区分，详情和时间游标仍只属于 `selectedTopicId`，禁止把两条时间线或分数相加。

T0 必须分别判定：

- `DATA_FOUNDATION_MODE=bootstrap|reuse|resume|BLOCKED_CONFIRM`：探测 `tools/dyint_demo_common/`、公共测试和最近验证记录。
- `TOPIC_FOUNDATION_MODE=bootstrap|reuse|resume|BLOCKED_CONFIRM`：探测 `gintbroker` 的 `schema.py`、`/bundle`、`/timeline`、`useTopicBundle.ts`、`TopicDetailPanel.tsx`、`TopicReplayPanel.tsx` 和 HIMARS 兼容测试。

两种 mode 的共同规则：全部缺失才 `bootstrap`；全部存在且测试通过为 `reuse`；部分存在且能对应本计划/6 月计划的执行记录为 `resume`；部分存在但来源不明时 `BLOCKED_CONFIRM`。第一个执行的专题可以建设 common/foundation，第二个专题只能复用或从明确断点续建。若基础只存在于另一个未合并分支，不自动 cherry-pick、复制文件或维护平行版本。

共享 HTML Mock 的 Gate 另行记录为 `PROTOTYPE_GATE=DRAFT_REVIEW_REQUIRED|APPROVED|REVISE`。只有 `APPROVED` 且文件 SHA-256 与评审版本一致，才允许进入 T1。

### 2.5 材料缺口和 Gate

| 缺口 | 是否阻断 `INTERNAL_READY` | 是否阻断 `CUSTOMER_READY` | 处理方式 |
| --- | --- | --- | --- |
| UKMTO/JMIC 原文未归档、未记录 hash/`visible_at` | 是 | 是 | T1 重新获取；获取失败则 `BLOCKED_CONFIRM` |
| 正式事件 AOI 和港口进近区未审批 | 否，可用明确标注的粗 AOI 内部彩排 | 是 | T4 生成内部粗 AOI；正式 AOI 缺失时客户 Gate 必须失败 |
| 目标船 IMO/MMSI 未核验 | 否，使用“油轮 A” | 否，只要保持匿名且不声称已识别 | 候选身份与事实身份分栏，客户包强制匿名 |
| AIS/ADS-B 展示和截图许可未确认 | 否，只能内部 | 是 | `data_manifest.csv` 中默认 `display_allowed=false` |
| SAR/光学影像和天气海况缺失 | 否 | 否，前提是明确展示为二次确认任务而非已有证据 | 不生成伪影像，不把任务占位当事实 |
| 商业 AIS/船舶登记源缺失 | 否 | 否，前提是客户版不展示具体身份 | 列为 P1，不阻塞匿名版 |
| `gintbroker` 通用专题渲染未完成 | 是 | 是 | T8-T10 先用 HIMARS 做兼容回归，再接 `dyint_sc2_20260526` |
| 双专题 HTML Mock 尚未确认 | 是，阻断 T1 及后续实现 | 是 | T0.5 走查同一 Mock 的两个专题、共用/独有边界和客户降级状态；明确 `approved` 后记录 hash |
| `dy-inta` 公共数据工程基础未落地 | 是 | 是 | T0/T1/T2 按 `DATA_FOUNDATION_MODE` 只补建一次 common scanner/validator/exporter；6 月计划复用 |
| `gintbroker` 现网专题情报为空 | 否 | 否 | DYINT bundle 使用冻结证据表供演示，不依赖 live matcher 恰好命中；同时保留实时源为空的质量说明 |
| CI 环境当前 AIS 未配置、总体 health 可能为 error | 否 | 否 | 本专题使用内置脱敏发布快照；目标回归区分“专题能力通过”和“外部源降级” |

---

## 3. 推荐方案和数据契约

### 3.1 实现策略

采用“先评审双专题 HTML Mock、源数据原地只读、外部磁盘分块派生、仓库内小型发布快照、`gintbroker` 通用专题展示”的方案：

1. 先通过 T0.5 的双专题原型 Gate，冻结“两个独立专题、一套共享底座”的信息架构；未通过时不创建实现分支内容。
2. 源数据只读，先生成文件清单、大小、修改时间和 SHA-256。
3. 公共事件、授权状态、AOI、遥测派生和融合结果分层落表，禁止一张 CSV 混合所有语义。
4. `tools/dyint_demo_common/` 只建设一次 manifest、schema、分块 scanner、复合去重、质量码、validator 和 exporter；本专题脚本只提供日期、AOI、规则和字段配置。
5. AIS/ADS-B 仅处理 5 月 20-28 日和三个粗 AOI；用分块读取控制资源，不扫描完整 2-6 月数据。
6. 同时输出 `raw_compatible` 与 `deduped` 统计，解释清洗对结果的影响。
7. 所有评分先过时间可见性检查；不能证明的“前兆”不强行制造上升曲线。
8. 客户资产仅消费 `display_allowed=true` 且已脱敏的数据；内部样例和原始标识不进入浏览器数据文件。
9. 从 `dy-inta` 生成本专题独立 `gintbroker` release bundle，大小上限 5MB；bundle 只含 AOI/事件/匿名摘要/证据/时间线/任务和 manifest，不含原始轨迹。
10. `gintbroker` 通用 topic bundle API 和通用地图/详情/回放组件只建设一次；HIMARS 旧接口和旧 slow 字段保持兼容。
11. HTML Mock 留在 `dy-inta` 作为设计契约；最终 6 张验收截图必须来自真实 `gintbroker`，Mock 不是第二套运行前端。

### 3.2 运行参数和路径约定

工具统一接受显式参数，不把个人绝对路径写死在提交文件中：

```bash
export PYTHON=/Users/liushen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
export AIS_FILE=/Volumes/exFAT466/海贝数据_2月1到6月15_AIS和ADS-B/AIS/event_vessel_route_202605.csv
export ADSB_ROOT=/Volumes/exFAT466/海贝数据_2月1到6月15_AIS和ADS-B/ADS-B/event_trajectory1_source_date_20260501_20260531
export SAMPLE_ROOT=/Users/liushen/Documents/非Coding工作/DYINT/O多源情报系统/样例数据
export OUTPUT_ROOT=demo_packages/sc2_20260526_muscat_tanker_attack
export DYINT_SCRATCH_ROOT=/Volumes/exFAT466/DYINT工作区/sc2_20260526
export WORK_ROOT="$DYINT_SCRATCH_ROOT/work"
export RAW_SOURCE_CACHE_ROOT="$DYINT_SCRATCH_ROOT/raw_sources"
export QUARANTINE_ROOT="$DYINT_SCRATCH_ROOT/quarantine"
export PREVIOUS_BUILD_ROOT="$DYINT_SCRATCH_ROOT/previous_build"
export GINTBROKER_ROOT=/Users/liushen/Documents/cursorDevs/gintbroker
export PROTOTYPE_FILE=/Users/liushen/Documents/githubDevs/dy-inta/devdoc/DYINT场景2双专题交互Mock.html
export COMMON_TOOLS_ROOT=/Users/liushen/Documents/githubDevs/dy-inta/tools/dyint_demo_common
```

每个新 shell 在执行阶段命令前都必须先执行上述变量块。`DYINT_SCRATCH_ROOT` 必须位于外部磁盘或用户指定的非仓库大容量路径；外部磁盘不可用时停止为 `BLOCKED_CONFIRM`，不得静默回退到项目 `.work/`、系统盘或复制原始文件。若 bundled Python 路径不存在，同样停止，不要未经验证切换到系统 Python 3.9。P0 只使用 Python 标准库、`pandas` 和 `openpyxl`，不在数据派生阶段引入 DuckDB、PyArrow、GeoPandas 或远端服务。

### 3.3 AOI 冻结契约

内部粗 AOI 固定为：

| `aoi_id` | 纬度范围 | 经度范围 | 用途 | 客户状态 |
| --- | --- | --- | --- | --- |
| `soh_uae_oman_rough` | 24.0 至 28.8 | 54.0 至 60.8 | 霍尔木兹/UAE/阿曼区域背景 | `internal_only` |
| `gulf_of_oman_muscat` | 22.0 至 25.8 | 56.0 至 61.5 | Muscat 以东主筛选区 | `internal_only`，正式 polygon 批准后才可升级 |
| `uae_approaches` | 24.0 至 26.5 | 52.5 至 57.0 | UAE 港口进近背景 | `internal_only` |

`aoi_catalog.geojson` 每个 feature 必须有：

- `aoi_id`
- `name_zh`
- `geometry_status`: `rough_bbox` / `approved_polygon`
- `source_ref`
- `version`
- `valid_from`
- `approved_by`
- `display_allowed`
- `quality_note`

如果 UKMTO 原文只有“Muscat 以东约 60NM”而没有官方坐标，不得反推并伪装成精确事件点。内部地图应展示“报告位置范围/不确定区”，正式 AOI 必须由 GIS/产品责任人确认。

### 3.4 时间和证据语义

所有时间输出为 ISO 8601 UTC，例如 `2026-05-26T09:45:00Z`。必须区分：

| 字段 | 定义 |
| --- | --- |
| `event_time` | 事件发生或报告时间 |
| `observed_at` | 遥测或主张所描述的时间 |
| `collected_at` | 本项目采集/下载时间 |
| `visible_at` | 历史回放中最早可辩护的公开可见时间 |
| `known_after_time` | 结果被后验来源确认的时间 |
| `time_basis` | `event_time`、`source_date`、`load_time_fallback`、`unknown` |
| `time_precision` | `exact`、`minute`、`day`、`upper_bound`、`unknown` |

`visible_at` 或 `known_after_time` 无法确认时保持空值并写 `quality_note`，不能用采集时间假装历史可见时间，也不能让该证据参与事前评分。

### 3.5 遥测清洗契约

AIS：

- 主时间字段：`IR_LASTTIME`。
- `IR_LASTTIME` 为空但 `IR_LOADTIME` 可用时，只允许做覆盖质量统计，`time_basis=load_time_fallback`，不得进入事前行为评分。
- `IR_HKEY` 已确认不是唯一行 ID，只保留为源字段摘要和质量分析输入，禁止作为唯一去重键。
- 复合去重键固定为 `IR_MMSI + COALESCE(IR_POSITION_RECEIVED, IR_LASTTIME) + IR_LAT + IR_LON + IR_SPEED + IR_COURSE`，与 6 月专题和数据盘点文档保持一致；字段先做去 BOM、trim、UTC 时间解析和数值规范化，再计算不可逆稳定 hash。
- `IR_MMSI`、位置时间、经纬度任一关键分量缺失时标记 `DEDUPE_KEY_INCOMPLETE`，该行保留在 raw 与 deduped 口径中，不与其他不完整行折叠，避免误删。
- 经纬度必须满足 `-90 <= lat <= 90`、`-180 <= lon <= 180`。
- 负速度、非数值速度不纠正为绝对值，改为空并打质量码。
- `IR_MMSI`、`IR_IMO`、船名只留在内部工作区；客户输出使用稳定匿名 ID。

ADS-B：

- 主时间字段：`source_date`；不得因为 `IR_LASTTIME` 为空而丢弃整日数据。
- `id` 只有在日内唯一且跨 9 个目标日文件无冲突时才可作为去重键；否则使用 `icao + source_date + lat + lon + alt + spd + trak`。关键分量不完整时与 AIS 一样标记 `DEDUPE_KEY_INCOMPLETE` 并保留，不误合并。
- 忽略 `._*.csv`。
- `icao`、`reg`、`call`、`mil` 为空或未经核验时，不推断航空器身份、军事属性或行动意图。
- 负速度和异常高度只进入质量统计，不直接触发高风险结论。

### 3.6 评分和叙事硬规则

1. `context` 证据不能单独把等级提升到 `prepare_protective_action`。
2. `post_event_confirmation` 和 `event_result` 不进入事前分数；可更新结果置信度，但 `score_delta=0`。
3. 5 月 22/23 日异地事件默认 `support_status=context`；除非另有同 AOI 证据，不得称为主事件直接前兆。
4. 事前进入“建议保护性准备”至少需要同一或相邻 AOI、24-72 小时内、两种独立证据类型，且每条满足 `visible_at <= scoring_time`。
5. 如果实际数据无法满足第 4 条，时间线应保持“背景关注/证据不足”，并在 5 月 26 日由海事 Warning 进入事件响应；不得为演示效果制造预测命中。
6. 5 月 28 日媒体主张只用于信息冲突展示，不回填 5 月 26 日之前的状态。
7. 客户版只输出保护性动作，不输出攻击、拦截、反制、精确定位或目标优先级建议。

### 3.7 最低字段契约

`data_manifest.csv` 必须包含：

- `asset_id`
- `scenario_id`
- `source_name`
- `source_owner`
- `source_url_or_path_template`
- `collected_at`
- `visible_at`
- `license`
- `display_allowed`
- `screenshot_allowed`
- `sensitivity_level`
- `redaction_rule`
- `expires_at`
- `contact_or_approval`
- `quality_note`
- `support_status`

`ais_daily_aoi_summary.csv` 与 `adsb_daily_aoi_summary.csv` 统一使用：

- `summary_date`
- `aoi_id`
- `count_mode`: `raw_compatible` / `deduped`
- `row_count`
- `unique_target_count`
- `missing_identity_count`
- `invalid_coordinate_count`
- `negative_speed_count`
- `duplicate_count`
- `time_fallback_count`
- `quality_level`
- `quality_note`
- `source_ref`

AIS 可追加 `low_speed_count`、`waiting_candidate_count`、`destination_category_summary`；ADS-B 可追加 `invalid_altitude_count`、`identity_coverage_rate`。两类表不得为了字段统一而填造无意义指标。

`telemetry_quality.csv` 必须包含：

- `dataset_id`
- `summary_date`
- `aoi_id`
- `quality_code`
- `affected_count`
- `total_count`
- `ratio`
- `impact_scope`
- `handling`
- `customer_expression`

`evidence_matrix.csv` 与 `score_timeline.csv` 最低字段：

| 表 | 必需字段 |
| --- | --- |
| `evidence_matrix.csv` | `evidence_id`、`event_id`、`evidence_type`、`observed_at`、`visible_at`、`source_ref`、`aoi_id`、`proposition`、`support_status`、`quality_note`、`display_allowed`、`customer_expression` |
| `score_timeline.csv` | `event_id`、`timestamp`、`score`、`risk_band`、`response_state`、`evidence_refs`、`visible_at_max`、`quality_notes`、`not_yet_known`、`customer_action` |

共享 schema 不再用一个 `level` 混合“风险程度”和“处置阶段”，固定拆成两个正交字段：

- `risk_band`：`background`（0-29）、`elevated`（30-49）、`protective_readiness`（50-69）、`verify_now`（70-100）。5 月与 6 月专题共用同一枚举和阈值；进入 `protective_readiness` 仍必须满足第 3.6 节的证据门槛。
- `response_state`：`observe`、`verify`、`event_response`、`monitoring`、`archive`。它描述当前工作流，不参与分数区间计算。

5 月 26 日可以同时是 `risk_band=protective_readiness` 与 `response_state=event_response`；5 月 27 日可以保持相同风险档位但切换为 `response_state=monitoring`。禁止继续生成旧 `level=event_response|monitoring`，也禁止沿用客户敏感度更高的 `prepare_defense`。若为兼容已落地旧 bundle 临时读取 `level`，只能在 adapter 中映射并记录 deprecation，新的持久化产物和 API 响应以两个新字段为准。

### 3.8 `gintbroker` 专题 bundle 契约

专题 ID 固定为 `dyint_sc2_20260526`。`gintbroker/backend/data/dyint_sc2_20260526/bundle.json` 是经过 audience Gate 的展示发布快照，不是原始数据副本，结构固定为：

```json
{
  "schema_version": "1.0",
  "topic_id": "dyint_sc2_20260526",
  "topic_kind": "event_case",
  "topic_group": "dyint_sc2_maritime_risk",
  "release_id": "<stable-release-id>",
  "source_package_sha256": "<dy-inta stable package hash>",
  "audience": "internal|customer",
  "features": { "type": "FeatureCollection", "features": [] },
  "entities": [],
  "intel": [],
  "evidence": [],
  "timeline": [],
  "tasks": [],
  "report": {},
  "manifest": []
}
```

硬规则：

1. bundle 总大小不得超过 5MB；超过时停止并压缩字段或拆分页接口，不得把原始轨迹塞进仓库。
2. `features` 允许 `Point`、`LineString`、`Polygon`，每个 feature 必须有 `feature_kind`、`geometry_status`、`support_status`、`quality_level`、`display_allowed` 和 `source_ref`。
3. `feature_kind` 首期固定为 `incident_area`、`port_approach`、`shipping_context`、`maritime_advisory`、`telemetry_summary`；不得使用“目标点”“攻击路线”等进攻性类型名。
4. `incident_area` 在缺少官方坐标时只能是 `geometry_status=rough_bbox`，地图用虚线/半透明范围展示，不显示精确爆炸点。
5. `telemetry_summary` 只表达日期/AOI/计数/质量，不包含原始 MMSI、IMO、ICAO、呼号或逐点轨迹。
6. `source_package_sha256` 必须与 `dy-inta` 稳定输出一致；漂移检查失败时禁止提交 `gintbroker` 发布快照。
7. `audience=customer` 时，bundle 生成器只导出 `display_allowed=true` 且通过脱敏的行；运行时 API 再做一次 fail-closed 校验。
8. `score_timeline` 只允许 `risk_band` 与 `response_state` 两个正交字段；schema 和 TypeScript 类型不得为 5 月/6 月建立场景专用枚举分支。

### 3.9 `gintbroker` 兼容和交互契约

推荐不是继续增加 `dyint_*` slow 顶层键，而是建立通用专题读取路径：

- 新增 `GET /api/topics/{topic_id}/bundle`，返回冻结 bundle。
- 新增 `GET /api/topics/{topic_id}/timeline`，只读返回专题时间线。
- 保留现有 `/api/topics/{topic_id}`、`brief`、`entities`、`intel`。
- 保留 `himars_entities`、`himars_intel`、`topic_briefs.himars` 和 `ActiveLayers.himars`，直到 HIMARS 兼容测试通过；本计划不一次性删除旧契约。
- 前端新增 `selectedTopicId`、`activeTopicIds` 与 `useTopicBundle()`，专题开关不再依赖静态 `ActiveLayers` 键。
- `selectedTopicId` 同一时刻至多一个，决定右侧详情和 `TopicReplayPanel`；`activeTopicIds` 只决定地图叠加。切换选中专题时不得合并两个 bundle、时间线、证据或评分。
- 左侧“军事专题”点击 DYINT 后：启用专题、按 bbox/polygon 聚焦、加载 bundle。
- 地图通用渲染：AOI 面、航运背景线、海事事件/通告点和匿名汇总点分别使用可解释样式；点击后返回 `selectedEntity.type=topic_feature` 与 `topic_id/feature_id`。
- 右侧专题详情：专题摘要、证据支持/反驳/待确认、数据质量、二次确认任务和保护性报告，不把 DYINT 内容混入全局实时威胁列表。
- 右下角使用独立 `TopicReplayPanel` 或 `TimelinePanel` 的显式 topic mode；数据来自 bundle、只保存在内存，不写全局 Time Machine 快照目录。

6 张真实系统截图固定为：

1. 左侧选择 `DYINT：阿曼外海油轮安全事件` 并聚焦 Gulf of Oman。
2. 事件定义与粗 AOI/精度提示。
3. 5 月 22-28 日专题回放时间线，明确事前/结果/后验。
4. AIS/ADS-B 区域摘要与“覆盖不足”质量提示。
5. 右侧证据矩阵，展示支持、反驳、待确认和来源时间。
6. 二次确认任务与保护性准备报告。

---

## 4. 风险、防护和回滚

| 风险 | 影响 | 防护 | 验证 | 回滚/关闭方式 |
| --- | --- | --- | --- | --- |
| 事后信息泄露到事前评分 | Demo 被质疑为事后解释 | 时间字段分层、自动 temporal gate | `test_temporal_integrity.py` 必须全过 | 回退评分产物，修正证据分类后重建 |
| 脏数据被解释为异常行为 | 错误风险结论 | 原始值不改写，异常值隔离，质量码随记录输出 | 原始/清洗计数对账 | `git revert` 对应派生阶段 commit；原始文件不受影响 |
| 粗 AOI 被当成精确位置 | 客户误解、合规风险 | `geometry_status=rough_bbox`，客户 Gate 禁止 | `test_customer_gate.py` | 降级为内部画面，等待正式 polygon |
| 未核验船名/MMSI 泄露 | 错误归因、敏感信息泄露 | 客户表只用匿名 ID；身份候选独立分栏 | 客户产物字段白名单 | 删除客户构建产物并重建；不改原始数据 |
| 未授权素材进入截图 | 许可风险 | manifest 默认拒绝，截图前逐项 Gate | `display_allowed` 与 `screenshot_allowed` 校验 | 停止客户演示，替换为已授权的脱敏聚合素材 |
| 大文件处理耗尽资源 | 长任务中断 | 按 200,000 行分块，只读所需列，只处理 9 天 | 记录 elapsed/RSS/chunk 数 | 降低 chunk；从阶段断点重跑，不重复前序 commit |
| 外部盘中途断开 | 结果不完整 | 构建前/后校验输入 hash 和文件大小；中间结果也在外部盘 | inventory 对账 | 标记 `BLOCKED_CONFIRM`，重新挂载后从当前阶段继续；不回退本机仓库 |
| bundle 过大或夹带原始轨迹 | 磁盘、镜像和泄露风险 | 5MB 上限、字段白名单、ID/轨迹扫描 | `test_customer_gate.py` + 文件大小 Gate | 拒绝导出，回到聚合/脱敏阶段 |
| HTML Mock 未确认就进入实现 | 页面做完后才暴露产品分歧 | T0.5 人工走查、记录 approved hash；T1 前硬阻断 | V00 原型状态/视口/交互矩阵 | 保持计划和 Mock 文档改动，不进入代码阶段 |
| 两个专题重复建设数据工具 | scanner/schema/validator 分叉，修复需做两遍 | `DATA_FOUNDATION_MODE` + `tools/dyint_demo_common/` + 公共测试 | common 静态扫描和双场景 fixture | 统一到一套 common commit；来源不明则停止 |
| 两个专题被实现成一个混合专题 | 时间线、评分和证据语义互相污染 | 独立 topic ID/bundle/release，`selectedTopicId` 与 `activeTopicIds` 分工 | 双专题切换与引用隔离测试 | 删除混合配置，恢复两个独立 bundle |
| `gintbroker` 新专题入口只显示名称但不开图层 | Demo 断链 | `activeTopicIds` 与通用 bundle/map/detail/replay 契约 | HIMARS + DYINT 双专题浏览器矩阵 | 回退通用化 commit，保留 HIMARS 旧链路 |
| HIMARS 兼容性回归 | 现有专题不可用 | 旧 API/slow 键/ActiveLayers 保留，先加后迁移 | 原有 topic/API/GeoJSON/build 测试 | `git revert` 对应 `gintbroker` 阶段 commit |
| 专题回放污染全局 Time Machine | 存储增长、实时/历史语义混淆 | 独立 `TopicReplayPanel`、只读 bundle、内存状态 | Network 与磁盘写入检查 | 禁用 topic replay，保持全局 Time Machine 原行为 |
| 真实系统画面误导为实时能力 | 过度承诺 | 页面固定“历史专题回放/发布快照/非实时”状态 | 彩排逐页检查 | 关闭客户 Gate，修订专题标签和主持稿 |
| CI 环境 health error 掩盖专题结果 | 发布误判 | 区分专题 API/UI 验收与外部源降级；不把 AIS 未配置当本专题失败 | 目标环境验证矩阵 | 专题失败回滚镜像；外部源问题单独记录 |
| 安全叙事越界 | 方案被理解为行动辅助 | 禁止词检查 + 人工售前复审 | 客户文案扫描与彩排 | 移除越界内容，重新评审，不带病演示 |

T0/T0.5 只做只读盘点、foundation 探针和 HTML Mock 评审；`PROTOTYPE_GATE` 未批准时不得进入 T1。T1-T11 只做本地数据派生、`dy-inta`/`gintbroker` 本地改动和验证，默认不 push。T12-T13 才涉及两仓分支 push、MR、Jenkins `Shadowbroker` 和 `192.168.211.195:3001` 目标环境。只有用户在执行轮明确要求“执行到发布/目标环境”时才可进入 T12-T13；MR 合并、Jenkins/远端配置修改和历史镜像回滚仍保留单独暂停确认点。本计划不修改 Jenkins 配置、远端 `.env`、数据库或 JIRA。

---

## 5. 具体实施计划

### T0：执行准备、断点恢复和输入盘点

目标：

- 确认当前分支、工作区、upstream、未推送提交和输入可读性。
- 创建执行记录，但不修改原始数据。
- 判定 `DATA_FOUNDATION_MODE`、`TOPIC_FOUNDATION_MODE`，并记录当前 HTML Mock hash。
- 判断从 T0 开始还是从已完成阶段继续。

输入：

- 本计划。
- 6 月实施计划和 `devdoc/DYINT场景2双专题交互Mock.html`。
- 源文档及第 2.2 节列出的本地输入。

修改范围：

- 只允许更新本计划第 8.2 节执行记录；若只是盘点且无状态变化，不提交。

步骤：

1. 完整读取本计划和执行记录，找出最后一个 `DONE_LOCAL` 阶段及其 commit。
2. 分别在 `dy-inta` 和 `gintbroker` 运行 Git 检查；如果任一仓库有无关改动、已有暂存内容或无法隔离的用户文件，停止，不得覆盖。
3. 在无关改动已排除、工作区可安全隔离后，`dy-inta` 创建/切换到 `codex/dyint-sc2-package`，`gintbroker` 创建/切换到 `codex/dyint-sc2-topic`；已在目标分支时复用，不覆盖同名分支。
4. 检查 bundled Python、AIS、ADS-B 5 月 20-28 日文件、3 个 Excel 和地理知识库。
5. 检查外部磁盘剩余空间；`DYINT_SCRATCH_ROOT` 至少预留 2GB。仓库所在系统盘只要求满足小型发布包、代码依赖和构建缓存的既有需求，不复制原始数据。
6. 在已确认的外部磁盘路径创建空的 `WORK_ROOT`、`RAW_SOURCE_CACHE_ROOT`、`QUARANTINE_ROOT` 和 `PREVIOUS_BUILD_ROOT`；不得写入、改名或移动任一原始文件。
7. 用 `realpath` 确认上述目录均不在 `dy-inta` 或 `gintbroker` 仓库内；不创建项目 `.work/`。
8. 记录输入文件大小、mtime、SHA-256；对 ADS-B 只记录 5 月 20-28 日 9 个有效文件，忽略 `._*`。
9. 对 `tools/dyint_demo_common/` 和公共测试执行数据 foundation 探针；对 `gintbroker` 的通用 bundle/API/前端组件和 HIMARS 测试执行 topic foundation 探针，按第 2.4 节分别判定 mode。
10. 读取 HTML Mock 的 SHA-256、文件大小和 Git commit；只记录，不把 `DRAFT_REVIEW_REQUIRED` 自动升级为 `APPROVED`。
11. 若执行记录已有阶段，验证对应 commit 仍在当前分支且工作区与记录一致；一致则从下一阶段继续，不重复生成已完成阶段。

验证：

```bash
git status --short --branch
git branch --show-current
git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}'
git log --oneline '@{upstream}..HEAD'
git -C "$GINTBROKER_ROOT" status --short --branch
git -C "$GINTBROKER_ROOT" rev-parse HEAD
test -x /Users/liushen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
test -r /Volumes/exFAT466/海贝数据_2月1到6月15_AIS和ADS-B/AIS/event_vessel_route_202605.csv
find /Volumes/exFAT466/海贝数据_2月1到6月15_AIS和ADS-B/ADS-B/event_trajectory1_source_date_20260501_20260531 \
  -maxdepth 1 -type f -name 'system_event_trajectory1_2026052[0-8].csv' | sort
df -h . /Volumes/exFAT466
mkdir -p "$WORK_ROOT" "$RAW_SOURCE_CACHE_ROOT" "$QUARANTINE_ROOT" "$PREVIOUS_BUILD_ROOT"
test "$(realpath "$DYINT_SCRATCH_ROOT")" != "$(realpath .)"
case "$(realpath "$DYINT_SCRATCH_ROOT")" in "$(realpath .)"/*|"$(realpath "$GINTBROKER_ROOT")"/*) exit 1;; esac
shasum -a 256 "$PROTOTYPE_FILE"
for path in \
  tools/dyint_demo_common/validate_package.py \
  "$GINTBROKER_ROOT/backend/services/topics/schema.py" \
  "$GINTBROKER_ROOT/frontend/src/hooks/useTopicBundle.ts" \
  "$GINTBROKER_ROOT/frontend/src/components/TopicDetailPanel.tsx" \
  "$GINTBROKER_ROOT/frontend/src/components/TopicReplayPanel.tsx"; do
  test -e "$path" && echo "PRESENT $path" || echo "MISSING $path"
done
rg -n '/bundle|/timeline' "$GINTBROKER_ROOT/backend/routers/topics.py" || true
```

预期结果：

- 两个 Git 仓库状态可解释且可隔离本轮文件。
- Python 3.12.13 或经验证的同等 bundled runtime 可用。
- AIS 1 个文件和 ADS-B 9 个日文件可读。
- 没有把 `._*.csv` 算作有效输入。
- scratch、原始源缓存和隔离目录均位于外部磁盘，不在项目目录。
- 两个 foundation mode 有唯一可解释值；Mock hash 已记录但审批状态未被自动推断。

暂停条件：

- 存在用户无关改动或不明暂存内容。
- 任一仓库当前分支、upstream 或 ahead/behind 与执行记录冲突。
- 外部盘未挂载、输入文件缺失或 hash 在同一阶段内变化。
- 空间不足或 Python 依赖缺失。
- 任一 foundation 是来源不明的部分实现，或只存在于未合并分支且无法确认基线。

提交与记录：

- T0 只创建外部空工作目录和 Git 分支元数据，不修改原始文件；默认不提交。
- 更新执行记录中的输入 hash 摘要、分支、起点 commit 和下一阶段。

### T0.5：双专题 HTML Mock 评审 Gate

目标：

- 在任何数据脚本或 `gintbroker` 实现前确认两个独立专题的预期效果。
- 冻结共享外壳与专题独有内容，避免后续以代码猜产品交互。

输入：

- `devdoc/DYINT场景2双专题交互Mock.html`。
- 5 月与 6 月两份实施计划。
- T0 记录的 Mock SHA-256。

修改范围：

- 评审提出修改时，只允许更新 Mock 和两份计划的交互/验收契约。
- 不创建 `demo_packages/`、`tools/` 或 `gintbroker` 业务改动。

步骤：

1. 从仓库启动静态服务，不使用 `file://` 特例，也不加载外部接口：`$PYTHON -m http.server 4173 --directory .`。
2. 在 1711x819 和 1440x900 打开 `/devdoc/DYINT场景2双专题交互Mock.html`；移动端 390x844 做 smoke。
3. 切换专题 01/02，确认 topic ID、专题类型、标题、地图范围、时间节点、右侧判断、证据、任务整体切换，不是同一专题的两个 tab。
4. 打开“复用边界”，确认 common data foundation 与 `gintbroker` shared core 只建设一次；场景 bundle、规则、时间线和验收叙事独立。
5. 操作时间游标和播放：5 月 22-28 日只展示当时可见证据；切到 6 月后验证 6 月 14/21/23 后验信息在早期游标不可见。
6. 切换内部/客户视图，确认未审批 AOI、许可和质量缺口有显式阻断/降级；不把 Mock 示意数据误认为事实。
7. 检查图层开关、地图点选、右侧三个 tab、移动侧栏、键盘 `1/2` 和 Console；页面不得发出外部网络请求。
8. 收集用户/产品责任人结论：`APPROVED`、`REVISE` 或未决。只有明确 `APPROVED` 才把 `PROTOTYPE_GATE`、Mock hash、评审人和时间写入两份计划执行记录。

验证：

```bash
$PYTHON -m http.server 4173 --directory .
curl -fsS http://127.0.0.1:4173/devdoc/DYINT场景2双专题交互Mock.html \
  | rg 'dyint_sc2_20260526|dyint_sc2_20260610_12|两个专题，不是一个专题的两页'
shasum -a 256 devdoc/DYINT场景2双专题交互Mock.html
```

通过标准：

- 桌面与移动主路径可操作，Console 0 个未处理 error，Network 只有本地 HTML document。
- 两个独立专题和一套共享底座的边界可由非技术评审者复述。
- 用户/产品责任人明确给出 `APPROVED`，且审批 hash 与当前文件一致。

暂停条件：

- 评审结论为 `REVISE`、未明确批准，或审批后文件 hash 又变化。
- 仍无法判断两个专题是否独立、右侧/时间线属于谁，或客户降级信息不清楚。
- Mock 依赖外部网络、真实敏感数据或只有特定本机路径才能打开。

提交与记录：

- 需要修订时按纯文档规则本地提交：`docs(sc2): 调整双专题交互Mock与实现契约`。
- 批准但文件无变化时不造空 commit，只在两份计划执行记录写 `PROTOTYPE_GATE=APPROVED`、hash、评审人和时间。
- 未批准时状态为 `BLOCKED_CONFIRM`，不得进入 T1。

### T1：冻结数据包骨架、字段契约和来源清单

目标：

- 建立目录、字段说明和来源归档规则。
- 重新核验 UKMTO/JMIC 原文，避免把源文档摘要直接当机器事实。

输入：

- T0.5 已批准的 Mock hash 和交互边界；未批准时本阶段不得开始。
- T0 输入盘点和文件 hash。
- 源文档中的公开来源 URL、事件定义和客户边界。
- 相邻方案的 manifest、时间字段和客户门禁契约。

修改范围：

- `demo_packages/sc2_20260526_muscat_tanker_attack/README.md`
- `00_manifest/*`
- `tools/dyint_demo_common/{README.md,io_utils.py,schemas.py,manifest.py}` 与对应公共测试（仅 `DATA_FOUNDATION_MODE=bootstrap|resume`）
- `tools/sc2_20260526/README.md`
- 必要时 `.gitignore`

步骤：

1. 按 `DATA_FOUNDATION_MODE` 处理 manifest 基础：`bootstrap` 建通用 IO/schema/manifest；`reuse` 先跑公共测试并只加 5 月 profile；`resume` 从已记录 common commit 继续。场景 `build_manifest.py` 只能做配置/编排薄层。
2. 创建第 1.3 节目录骨架，只提交允许进仓库的空模板和说明，不提交原始文件。
3. `target_definition.csv` 冻结事件 ID、topic ID/kind/group、时间窗、粗 AOI、客户名称、内部名称、被保护对象、允许/禁止结论和版本。
4. `source_manifest.csv` 最低字段：`source_id`、`source_type`、`source_owner`、`source_url_or_path_template`、`retrieved_at`、`sha256`、`event_time`、`visible_at`、`known_after_time`、`time_precision`、`license`、`display_allowed`、`screenshot_allowed`、`quality_note`。
5. 将源文档列出的 UKMTO/JMIC URL 重新获取到 `RAW_SOURCE_CACHE_ROOT`；记录 HTTP 状态、最终 URL、获取时间、文件 hash 和原文标题。原始 PDF 不进入仓库。
6. 人工核对 `Warning 062-26` 是否明确提供事件时间、位置精度、船型、安全状态和环境影响；只把原文明确内容写入表。
7. JMIC、gCaptain 和 5 月 28 日媒体按 `official_maritime`、`maritime_summary`、`media_enrichment`、`single_party_claim` 分类。
8. 无法证明最早公开时间时，`visible_at` 留空并说明；不得用当前下载时间回填历史可见时间。
9. `data_manifest.csv` 所有素材默认 `display_allowed=false`、`screenshot_allowed=false`，只有明确许可后逐项升级。

验证：

```bash
PYTHON=/Users/liushen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
$PYTHON tools/sc2_20260526/build_manifest.py --check-only \
  --output demo_packages/sc2_20260526_muscat_tanker_attack
git diff --check
```

覆盖点：

- 主事件只有一个事实主键。
- 每个公开来源有来源级别和时间语义。
- 未确认许可默认拒绝，不是默认允许。
- 原始本地绝对路径不进入客户资产。

暂停条件：

- UKMTO 主原文无法获取且仓库/本地无可信归档。
- 原文与源文档的主事件时间、船型或状态存在实质冲突。
- 来源许可要求不明确到无法判断是否允许内部存档。

提交与记录：

- 校验通过后只暂存本阶段文件。
- 运行 `git status --short`、`git diff --check`、`git diff --cached --check`。
- 本地提交：`chore(sc2): 冻结事件数据契约与工作区边界`。
- 记录 commit 短 hash；不 push。

### T2：先建立自动校验门禁

目标：

- 在生成数据前先固化 schema、时间、防泄漏、授权和引用完整性规则。

输入：

- T1 冻结的字段模板、枚举、来源清单和默认拒绝授权状态。
- 第 3 节数据、时间、AOI、评分和最低字段契约。

修改范围：

- `tools/dyint_demo_common/*` 和 `tests/dyint_demo_common/*`（仅 `DATA_FOUNDATION_MODE=bootstrap|resume` 时）
- `tools/sc2_20260526/validate_package.py`
- `tests/sc2_20260526/test_*.py`
- `06_validation/validation_report.md` 模板

步骤：

1. 使用 Python 标准库 `unittest`，不新增 pytest 依赖。
2. `bootstrap` 时在 `tools/dyint_demo_common/` 实现通用 schema、时间、引用、授权、脱敏和遥测质量校验；`reuse` 时先运行公共测试，只新增 5 月 profile/fixture；`resume` 时从已记录 common commit 继续。场景 `validate_package.py` 只能装载 profile 并调用 common validator。
3. 为每个 CSV 固定必需列、枚举值、日期格式、空值规则和主键唯一性。
4. 实现跨表引用校验：`source_ref`、`evidence_ref`、`aoi_id`、`asset_id` 必须能回到对应主表。
5. 实现 temporal gate：参与某一评分点的证据必须满足 `visible_at <= scoring_time`；空 `visible_at` 不得参与。
6. 实现 `risk_band` 与 `response_state` schema，拒绝旧 `level=event_response|monitoring` 新写入，并用公共 fixture 同时覆盖 5 月/6 月 profile。
7. 实现 customer gate：客户资产只能引用 `display_allowed=true`；截图只能引用 `screenshot_allowed=true`；`rough_bbox` 不得在客户模式伪装成批准 AOI。
8. 实现客户字段白名单：客户 bundle、截图清单和报告不得包含 MMSI、IMO、ICAO、呼号、未核验船名、原始绝对路径。
9. 实现安全文案检查，重点审查“推荐打击”“精确坐标”“武器发射点”“攻击路线”“拦截并反制”“目标优先级”等行动性表达；事件事实中的“攻击/外部爆炸”可存在，但不能转成行动建议。
10. 测试先使用最小 fixture，不读取 370MB 原始文件。

验证：

```bash
PYTHON=/Users/liushen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
$PYTHON -m unittest discover -s tests/sc2_20260526 -p 'test_*.py' -v
$PYTHON -m unittest discover -s tests/dyint_demo_common -p 'test_*.py' -v
$PYTHON tools/sc2_20260526/validate_package.py \
  --package demo_packages/sc2_20260526_muscat_tanker_attack \
  --mode internal
```

预期结果：

- 正常 fixture 通过。
- 时间穿越、缺少来源、未授权素材、粗 AOI 客户展示和未脱敏 ID 的负例必须失败。

暂停条件：

- schema 与 T1 契约冲突。
- 校验器只能靠人工判断关键 Gate，无法形成确定性失败条件。

提交与记录：

- 最低验证通过后本地提交：`feat(sc2): 建立事件包自动校验门禁`。
- 记录测试命令、结果和 commit；不 push。

### T3：结构化海事事件、新闻主张和身份候选

目标：

- 把公开事件源和本地新闻样例拆成事实、后验确认、背景和单方主张。

输入：

- T1 归档的 UKMTO/JMIC/媒体来源和 `source_manifest.csv`。
- 新闻样例 Excel。
- T2 校验器及事件类 fixture。

修改范围：

- `tools/sc2_20260526/build_events.py`
- `02_events/*.csv`
- 相关单测

步骤：

1. 从 T1 归档的原文生成 `maritime_advisories.csv`，不从媒体反推 UKMTO 事实字段。
2. `event_results.csv` 至少包含：`event_id`、`event_time`、`event_type`、`source_ref`、`reported_location_text`、`aoi_id`、`vessel_type`、`vessel_name_status`、`casualty_status`、`environment_status`、`known_after_time`、`display_allowed`、`redaction_rule`。
3. 从新闻 Excel 只读取字段白名单，不复制整段原始内容；把 5 月 28 日内容标为 `single_party_claim` 或 `media_report`。
4. `vessel_identity_candidates.csv` 明确区分 `withheld`、`candidate`、`verified`。P0 不允许出现 `verified`，除非新增登记源和可追溯核验证据。
5. 5 月 22/23 日事件使用独立事件 ID 和实际 AOI；与主事件的关系写为 `regional_context`。
6. 生成表后运行时间、来源和引用校验。

验证：

```bash
PYTHON=/Users/liushen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
$PYTHON tools/sc2_20260526/build_events.py \
  --sample-root "$SAMPLE_ROOT" \
  --work-root "$WORK_ROOT" \
  --output "$OUTPUT_ROOT"
$PYTHON -m unittest discover -s tests/sc2_20260526 -p 'test_*.py' -v
$PYTHON tools/sc2_20260526/validate_package.py --package "$OUTPUT_ROOT" --mode internal
```

样本与预期：

- `UKMTO 062-26` 是主事实源。
- JMIC 只作为后验汇总，不进入事前预警证据。
- `OLYMPIC LIFE` 状态为 `candidate` 或客户输出中的“油轮 A”。
- 5 月 28 日主张不会出现在 5 月 26 日前的评分输入。

暂停条件：

- Excel 字段或时间与源文档描述不一致且无法解释。
- 事件源之间存在关键事实冲突但尚未写出支持/反驳/待确认状态。

提交与记录：

- 验证通过后本地提交：`feat(sc2): 结构化海事事件与来源证据`。
- 记录输出行数和 commit；不 push。

### T4：建立粗 AOI 和正式 AOI Gate

目标：

- 让内部聚合范围可复现，同时禁止把 bbox 包装成正式事件位置。

输入：

- `target_definition.csv` 中的 3 个粗 AOI。
- 地理知识库 WKT 文件清单和来源信息。
- T2 客户 Gate 校验器。

修改范围：

- `tools/sc2_20260526/build_aoi.py`
- `01_aoi/aoi_catalog.geojson`
- `01_aoi/aoi_quality.csv`
- AOI 单测和客户 Gate

步骤：

1. 按第 3.3 节生成 3 个矩形 GeoJSON feature，坐标顺序固定为 `lon, lat`，首尾闭合。
2. 每个 feature 标记 `geometry_status=rough_bbox`、来源文档和版本。
3. 将地理知识库 WKT 文件只登记为候选底座；P0 不自动把 EEZ/领海裁剪结果当港口进近区。
4. 如果后续提供经责任人确认的 polygon，必须作为新版本导入，保留旧 bbox，不原地覆盖历史版本。
5. `aoi_quality.csv` 记录几何类型、范围、来源、审批状态、适用画面和禁止表达。
6. 客户模式下若主 AOI 仍是 `rough_bbox`，校验器必须失败；内部模式允许但页面必须显示“粗筛选范围”。

验证：

```bash
PYTHON=/Users/liushen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
$PYTHON tools/sc2_20260526/build_aoi.py --output "$OUTPUT_ROOT"
$PYTHON -m unittest discover -s tests/sc2_20260526 -p 'test_*.py' -v
$PYTHON tools/sc2_20260526/validate_package.py --package "$OUTPUT_ROOT" --mode internal
```

预期结果：

- 3 个 AOI 均可解析，坐标合法，属性完整。
- `--mode internal` 通过；正式 AOI 未提供时 `--mode customer` 必须因 AOI Gate 失败。

暂停条件：

- 有人要求把文本“60NM east”转换成未经来源支持的精确点。
- 新 polygon 来源、版本或审批人不明确。

提交与记录：

- 验证通过后本地提交：`feat(sc2): 固化阿曼外海关注区与精度门禁`。
- 记录内部/客户 Gate 结果；不 push。

### T5：生成 AIS 原始口径、去重口径和质量报告

目标：

- 只读扫描 5 月 AIS 文件，复现人工统计并生成可解释的匿名派生表。

输入：

- T0 已核验 hash 的 5 月 AIS CSV。
- T4 `aoi_catalog.geojson`。
- 第 3.5、3.7 节清洗和字段契约。
- 源文档人工 AIS 统计基线。

修改范围：

- `tools/sc2_20260526/build_ais.py`
- `03_telemetry/ais_daily_aoi_summary.csv`
- `03_telemetry/nearby_vessel_candidates.csv`
- `03_telemetry/telemetry_quality.csv`
- `06_validation/source_count_reconciliation.csv`
- AIS 单测

步骤：

1. 场景脚本调用 `tools/dyint_demo_common/telemetry.py` 的 AIS 分块 scanner，使用 `pandas.read_csv(..., chunksize=200_000, usecols=[...])`，编码先尝试 `utf-8-sig`；禁止复制 scanner 或整表载入。
2. 只读取 `IR_LASTTIME`、`IR_LOADTIME`、`IR_POSITION_RECEIVED`、`IR_NAME`、`IR_DESTINATION`、`IR_COURSE`、`IR_SPEED`、`IR_NAVIGATION_STATUS`、`IR_IMO`、`IR_MMSI`、`IR_LAT`、`IR_LON`、`IR_HKEY`、`SOURCE`。
3. 先生成 `raw_compatible` 统计，严格按有效 `IR_LASTTIME` 日期和 bbox 过滤，复现源文档计数。
4. 再按第 3.5 节复合键生成 `deduped` 统计；`IR_HKEY` 不参与唯一去重，不得用去重后的值覆盖原始口径。
5. 统计每个日期/AOI 的行数、唯一 MMSI 数、缺失身份数、缺失/越界坐标数、负速度数、去重删除数、低速/等待候选数和时间回退数。
6. `nearby_vessel_candidates.csv` 只保留匿名 ID、日期、AOI、速度区间、导航状态类别、目的港类别、质量说明；不得提交原始 MMSI/IMO/船名/精确轨迹。
7. 内部原始 ID 到匿名 ID 的映射只写 `QUARANTINE_ROOT`，不得提交或复制到项目目录。
8. 记录耗时、chunk 数和峰值 RSS；目标峰值 RSS 小于 2GB。超过时将 chunk 降至 100,000 后重跑。

人工基线对账值：

| 日期 | `soh_uae_oman_rough` 行/MMSI | `gulf_of_oman_muscat` 行/MMSI | `uae_approaches` 行/MMSI |
| --- | ---: | ---: | ---: |
| 2026-05-20 | 75 / 25 | 10 / 7 | 78 / 26 |
| 2026-05-21 | 84 / 30 | 15 / 10 | 85 / 29 |
| 2026-05-22 | 88 / 30 | 16 / 11 | 85 / 29 |
| 2026-05-23 | 69 / 26 | 5 / 4 | 72 / 29 |
| 2026-05-24 | 82 / 30 | 9 / 8 | 83 / 31 |
| 2026-05-25 | 62 / 23 | 9 / 9 | 64 / 25 |
| 2026-05-26 | 80 / 25 | 9 / 8 | 81 / 26 |
| 2026-05-27 | 77 / 22 | 11 / 10 | 76 / 21 |
| 2026-05-28 | 71 / 22 | 10 / 10 | 68 / 19 |

对账规则：

- `raw_compatible` 应与上表一致；不一致时先检查 BOM、时间解析、边界包含规则和坐标列，不得直接改期望值。
- `deduped` 可以不同，但必须在 `source_count_reconciliation.csv` 说明差值、去重键和质量码。
- `DEDUPE_KEY_INCOMPLETE` 行不互相折叠；报告必须单列数量，禁止为降低重复率而误删。
- 如果原始文件 hash 与计划编写时不同，上表只作历史参考，不强行通过。

验证：

```bash
PYTHON=/Users/liushen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
$PYTHON tools/sc2_20260526/build_ais.py \
  --input "$AIS_FILE" \
  --from 2026-05-20 --to 2026-05-28 \
  --chunk-size 200000 \
  --work-root "$WORK_ROOT" \
  --output "$OUTPUT_ROOT"
$PYTHON -m unittest discover -s tests/sc2_20260526 -p 'test_*.py' -v
$PYTHON tools/sc2_20260526/validate_package.py --package "$OUTPUT_ROOT" --mode internal
```

暂停条件：

- 原始口径计数与上表大面积不一致且不能由输入 hash 或边界规则解释。
- 内部 ID 映射进入 Git diff。
- 去重删除比例异常且未完成抽样复核。
- 处理过程写回或修改外接盘文件。

提交与记录：

- 验证通过后本地提交：`feat(sc2): 生成5月AIS脱敏派生摘要`。
- 记录原始/去重行数、异常码分布、耗时、RSS 和 commit；不 push。

### T6：生成 ADS-B 原始口径、去重口径和质量报告

目标：

- 处理 5 月 20-28 日 9 个 ADS-B 日文件，生成区域背景与数据质量摘要。

输入：

- T0 已核验 hash 的 9 个 ADS-B 日文件。
- T4 `aoi_catalog.geojson`。
- 第 3.5、3.7 节清洗和字段契约。
- 源文档人工 ADS-B 统计基线。

修改范围：

- `tools/sc2_20260526/build_adsb.py`
- `03_telemetry/adsb_daily_aoi_summary.csv`
- `03_telemetry/telemetry_quality.csv`
- `06_validation/source_count_reconciliation.csv`
- ADS-B 单测

步骤：

1. 场景脚本调用 `tools/dyint_demo_common/telemetry.py` 的 ADS-B scanner，只枚举 `system_event_trajectory1_YYYYMMDD.csv`，显式排除 `._*`。
2. 使用 `source_date` 作为主时间；读取 `id`、`icao`、`reg`、`type`、`spd`、`alt`、`trak`、`lon`、`lat`、`call`、`mil`、`source_date`、`IR_LASTTIME`、`IR_LOADTIME`。
3. 先检查 `id` 日内/跨文件唯一性，再按第 3.5 节选择 ID 或复合键，分别输出 `raw_compatible` 和 `deduped` 口径。
4. 按日期/AOI 统计行数、唯一 ICAO 数、身份缺失、负速度、异常高度、无效坐标、重复和时间字段缺失。
5. 不输出航空器具体身份和军事属性；客户摘要只保留区域活动量与质量提示。
6. 每日文件独立处理并写断点；单日失败不允许跳过后继续宣称全窗完成。

人工基线对账值：

| 日期 | 当日总行数 | `gulf_of_oman_muscat` 行/ICAO |
| --- | ---: | ---: |
| 2026-05-20 | 612,860 | 711 / 12 |
| 2026-05-21 | 291,056 | 44 / 7 |
| 2026-05-22 | 147,447 | 45 / 5 |
| 2026-05-23 | 227,014 | 401 / 13 |
| 2026-05-24 | 230,080 | 339 / 9 |
| 2026-05-25 | 285,578 | 1 / 1 |
| 2026-05-26 | 1,163,242 | 97 / 1 |
| 2026-05-27 | 1,274,733 | 0 / 0 |
| 2026-05-28 | 723,137 | 0 / 0 |

验证：

```bash
PYTHON=/Users/liushen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
$PYTHON tools/sc2_20260526/build_adsb.py \
  --input-root "$ADSB_ROOT" \
  --from 2026-05-20 --to 2026-05-28 \
  --chunk-size 200000 \
  --work-root "$WORK_ROOT" \
  --output "$OUTPUT_ROOT"
$PYTHON -m unittest discover -s tests/sc2_20260526 -p 'test_*.py' -v
$PYTHON tools/sc2_20260526/validate_package.py --package "$OUTPUT_ROOT" --mode internal
```

对账规则与 T5 相同：先复现原始口径，再解释去重差异。5 月 27/28 日主 AOI 为 0 是合法结果，禁止为了画面填充伪数据。

暂停条件：

- 日文件缺失或 sidecar 被误读。
- `source_date` 无法稳定解析。
- 代码把空 `mil` 或名称候选转成确定军事属性。
- 任一天失败但执行者试图继续到融合阶段。

提交与记录：

- 验证通过后本地提交：`feat(sc2): 生成5月ADS-B质量降级摘要`。
- 记录逐日状态、异常码、耗时和 commit；不 push。

### T7：生成证据矩阵、时间线和二次确认任务

目标：

- 把事件、AOI、遥测和来源组织成可追溯判断单，不制造预测成功叙事。

输入：

- T3 事件、来源和身份候选表。
- T4 AOI 和精度状态。
- T5/T6 两套遥测口径和质量报告。
- 第 3.6 节评分与叙事硬规则。

修改范围：

- `tools/sc2_20260526/build_fusion.py`
- `04_fusion/*.csv`
- 融合和时间测试

步骤：

1. `evidence_matrix.csv` 每行包含 `evidence_id`、时间、类型、来源、支持命题、`support_status`、`quality_note`、客户表达、`visible_at`、`display_allowed`。
2. `evidence_links.csv` 明确证据与事件、AOI、对象、结论的关系，不允许孤立 evidence ID。
3. `score_timeline.csv` 同时输出 `score`、`risk_band`、`response_state`、`evidence_refs`、`visible_at_max`、`quality_notes`、`not_yet_known`；风险档位与工作流状态必须分别计算和展示。
4. 先执行 temporal gate，再计算分数；测试中要证明后验 JMIC 和 5 月 28 日主张无法进入 5 月 26 日前评分。
5. 如果同 AOI 事前证据不足，按第 3.6 节保留背景/证据不足；5 月 26 日可进入 `risk_band=protective_readiness`、`response_state=event_response`，不要称为提前预测。
6. `confirmation_tasks.csv` 至少包括目标船登记核验、正式 AOI、后续海事通告、天气海况、污染通告、影像任务和港口影响，每项有负责人角色、证据缺口、优先级、退出条件和客户可见状态。
7. 保护性报告只引用客户 Gate 可用的证据；内部报告可以列未授权缺口但必须标注。

验证：

```bash
PYTHON=/Users/liushen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
$PYTHON tools/sc2_20260526/build_fusion.py --package "$OUTPUT_ROOT"
$PYTHON -m unittest discover -s tests/sc2_20260526 -p 'test_*.py' -v
$PYTHON tools/sc2_20260526/validate_package.py --package "$OUTPUT_ROOT" --mode internal
```

关键断言：

- 每次分数变化均能回到证据 ID。
- `visible_at_max <= timestamp`。
- 后验来源只更新结果置信度，不制造事前分数。
- 证据不足时有任务和降级说明，不输出强结论。
- 所有动作均为保护性、复核性或持续监测。

暂停条件：

- 为满足“分数上升”而需要把异地事件或后验来源当事前证据。
- 评分规则没有可解释阈值或同一证据被重复加分。
- 任何输出出现攻击方、武器或行动方案的无证据推断。

提交与记录：

- 验证通过后本地提交：`feat(sc2): 生成证据矩阵与风险验证时间线`。
- 记录时间 Gate 结果、最终事件状态和 commit；不 push。

### T8：导出并冻结 `gintbroker` 小型专题发布包

目标：

- 把 T7 结果转换为小于 5MB、符合目标 audience 字段白名单的 `gintbroker` topic bundle。
- 建立 `dy-inta` 数据包与 `gintbroker` 发布快照之间的 hash 追踪，不复制原始数据。

输入：

- T7 通过内部 Gate 的事件、AOI、遥测摘要、证据、时间线、任务和报告。
- T1 `data_manifest.csv` 与 T4 AOI 精度状态。
- 第 3.8 节 bundle 契约。

修改范围：

- `tools/sc2_20260526/export_gintbroker_topic.py`
- `tests/sc2_20260526/test_customer_gate.py`
- `demo_packages/.../05_customer_assets/*`
- `gintbroker/backend/data/topics/dyint_sc2_20260526.json`
- `gintbroker/backend/data/dyint_sc2_20260526/bundle.json`
- `gintbroker/backend/data/dyint_sc2_20260526/release_manifest.json`

步骤：

1. 场景 exporter 只准备 5 月映射配置，并调用 `tools/dyint_demo_common/export_topic.py` 在 `DYINT_SCRATCH_ROOT/export_candidate/` 生成 bundle，不复制通用 audience/hash/schema/size 逻辑，也不直接写 `gintbroker`。
2. 只导出 `display_allowed=true` 的字段；内部模式也不得导出原始 MMSI/IMO/ICAO、呼号、个人绝对路径和逐点轨迹。
3. 生成 `source_package_sha256`、`release_id`、`audience`、文件清单和稳定 checksum。
4. 检查 JSON 总大小不超过 5MB；超限时只保留日/AOI 聚合和代表性事件，不降低证据准确性。
5. 运行 `validate_package.py --mode internal|customer` 和 bundle 专项校验。
6. 校验通过后由 exporter 原子写入 `gintbroker/backend/data/dyint_sc2_20260526/`；不得人工复制后再手改。
7. 再次比较发布目录 checksum 与 export candidate，确保同步无漂移。

验证：

```bash
$PYTHON tools/sc2_20260526/export_gintbroker_topic.py \
  --package "$OUTPUT_ROOT" \
  --audience internal \
  --staging "$DYINT_SCRATCH_ROOT/export_candidate" \
  --gintbroker-root "$GINTBROKER_ROOT"
$PYTHON tools/sc2_20260526/validate_package.py --package "$OUTPUT_ROOT" --mode internal
test "$(stat -f %z "$GINTBROKER_ROOT/backend/data/dyint_sc2_20260526/bundle.json")" -le 5242880
if rg -n 'IR_MMSI|IR_IMO|icao|call_sign|/Users/|/Volumes/' \
  "$GINTBROKER_ROOT/backend/data/dyint_sc2_20260526"; then
  exit 1
fi
```

暂停条件：

- 只有引入原始轨迹/原始标识才能完成画面。
- customer bundle 仍引用未授权或粗 AOI 但未标注的素材。
- bundle 超过 5MB，或 hash 漂移无法解释。
- `gintbroker` 工作区存在无法隔离的用户改动。

提交与记录：

- `dy-inta` 验证通过后本地提交：`feat(sc2): 导出gintbroker专题发布包`。
- `gintbroker` 仅暂存 3 个数据/配置文件，本地提交：`feat(topics): 添加DYINT商船安全专题快照`。
- 记录两个 commit 和 `source_package_sha256`；不 push。

### T9：复用或补建 `gintbroker` 通用专题后端

目标：

- 按 `TOPIC_FOUNDATION_MODE` 复用、续建或只补建一次通用 bundle API，而不是只对 HIMARS 暴露硬编码 slow 顶层键。
- 保持现有 HIMARS API 和 `/api/live-data/slow` 契约不变。

输入：

- T8 `dyint_sc2_20260526` 配置与 bundle。
- 现有 `backend/services/topics/service.py`、`backend/routers/topics.py` 和 HIMARS 测试。
- 当前 live API 基线：1 个 HIMARS 专题、6 个实体、0 条 intel。

修改范围：

- `gintbroker/backend/services/topics/schema.py`
- `gintbroker/backend/services/topics/service.py`
- `gintbroker/backend/routers/topics.py`
- `gintbroker/backend/tests/test_topics_api.py`
- `gintbroker/backend/tests/test_topics_bundle.py`

步骤：

1. T9 开始前重新执行 topic foundation 探针；若 6 月计划或其他已确认分支的通用基础已经合入当前基线，切 `reuse`，不得重复实现。
2. `bootstrap`：新增通用 bundle schema 校验、mtime cache、`GET /api/topics/{topic_id}/bundle|timeline` 和兼容投影；`reuse`：先跑现有测试，只补 5 月 profile/fixture；`resume`：核对已记录 foundation commit 后续建。
3. schema 校验版本、topic ID/kind/group、FeatureCollection、`risk_band/response_state`、时间、引用、audience 和 5MB 上限；拒绝场景专用枚举。
4. 在 service 中按 `topic_id` 读取 `backend/data/<topic_id>/bundle.json`；配置无 bundle 时继续走现有 HIMARS 组装路径。
5. API 按部署 audience fail-closed 过滤 `display_allowed=false`；不向响应返回本地路径或内部 ID 映射。
6. `/api/topics/{topic_id}/brief|entities|intel` 对 bundle 专题返回兼容投影；未知专题继续 404。
7. 不新增 `dyint_*` slow 顶层字段；保留 `get_topics_slow_payload()` 对 HIMARS 的现有输出，防止旧前端回归。
8. 补负例：topic ID 不一致、未来信息泄露、粗 AOI customer 误放行、路径泄露、bundle 超限、悬空 evidence ref、两个 topic 的 evidence/timeline 交叉引用。

验证：

```bash
cd "$GINTBROKER_ROOT"
uv run pytest \
  backend/tests/test_topics_api.py \
  backend/tests/test_topics_bundle.py \
  backend/tests/test_api_smoke.py -k 'topics or slow'
uv run ruff check \
  backend/services/topics \
  backend/routers/topics.py \
  backend/tests/test_topics_api.py \
  backend/tests/test_topics_bundle.py
```

API 断言：

- HIMARS 旧 5 个 endpoint 和 slow 键仍通过。
- DYINT bundle/timeline/brief/entities/intel 可读取，`source_package_sha256` 与 T8 一致。
- customer audience 不返回未授权记录、原始标识和个人路径。

暂停条件：

- 为支持 DYINT 必须删除或改名 HIMARS 旧字段。
- audience 只能由前端控制，后端无法 fail-closed。
- bundle 读取失败会拖垮 `/api/live-data/slow` 或应用启动。

提交与记录：

- 有后端改动且验证通过后在 `gintbroker` 本地提交：`feat(topics): 通用化专题bundle与时间线接口`。
- `reuse` 且无需改动时不造空 commit，只记录复用的 foundation commit、测试数量和 API 样本；不 push。

### T10：复用或补建通用专题前端并接入 5 月可视化

目标：

- 让“军事专题”真正支持第二个专题，不再依赖 `ActiveLayers.himars` 和 HIMARS 专用组件。
- 在现有地图、右侧情报和时间机器区域形成 6 画面闭环。

输入：

- T9 通用 bundle/timeline API。
- T0.5 已批准的 HTML Mock hash；只作为信息架构/交互契约，不作为运行时数据源。
- 用户截图 `/Users/liushen/iShots/iShot_2026-07-10_07.26.21.jpg`。
- 现有 `WorldviewLeftPanel`、`MaplibreViewer`、`NewsFeed`、`TimelinePanel` 视觉和交互基线。

修改范围：

- `gintbroker/frontend/src/types/dashboard.ts`
- `gintbroker/frontend/src/hooks/useTopicBundle.ts`
- `gintbroker/frontend/src/app/page.tsx`
- `gintbroker/frontend/src/components/WorldviewLeftPanel.tsx`
- `gintbroker/frontend/src/components/MaplibreViewer.tsx`
- `gintbroker/frontend/src/components/map/geoJSONBuilders.ts`
- `gintbroker/frontend/src/components/TopicDetailPanel.tsx`
- `gintbroker/frontend/src/components/TopicReplayPanel.tsx`
- `gintbroker/frontend/src/components/NewsFeed.tsx`
- `gintbroker/frontend/src/i18n/translations/zh-CN.json`
- `gintbroker/frontend/src/i18n/translations/en.json`
- 定向组件/GeoJSON 测试

步骤：

1. 重新探测 `TOPIC_FOUNDATION_MODE`。`bootstrap` 才新增通用类型、hook、source/layer、详情和回放；`reuse` 先跑既有测试，只扩展通用 feature/type/profile；`resume` 从明确 foundation commit 续建。
2. 通用类型必须包含 `TopicBundle`、`TopicFeature`、`TopicTimelineItem`、`TopicEvidence`、`TopicTask`，并把 `risk_band`、`response_state` 分开；不得建立 May/June 专用 union。
3. `useTopicBundle(topicId)` 只从自有 `/api/topics/{id}/bundle` 取数，具备 loading/error/retry/release ID 状态。
4. `page.tsx` 使用 `selectedTopicId` 与 `activeTopicIds`；选中项决定详情/回放，启用集合只决定地图叠加，专题状态不强行塞进静态 `ActiveLayers`。
5. `WorldviewLeftPanel` 保留现有“军事本体/军事专题”Tab；专题列表仍来自 `/api/topics`，点击 5 月专题后启用、选择并按 bbox/polygon 聚焦。HIMARS 原开关行为保留。
6. 通用 `buildTopicFeaturesGeoJSON()` 支持 Point/LineString/Polygon，按 `feature_kind`、`geometry_status`、`support_status`、`quality_level` 生成样式属性。
7. `MaplibreViewer` 使用同一 topic source/layers 渲染范围、航运背景、事件/通告和匿名摘要；点击回传 `topic_feature`，通用代码不得出现本专题 ID。
8. `TopicDetailPanel` 在右侧复用现有框架展示摘要、证据矩阵、质量提示、二次确认任务和保护性报告；不把 DYINT 条目硬塞进全局 `himarsIntel` 卡片。
9. `TopicReplayPanel` 占用右下角时间机器视觉区域或以明确 topic mode 切换；回放 5 月 22-28 日 bundle 时间线，只更新选中 topic 图层/详情，不调用 snapshot 创建 API、不暂停全局实时数据。
10. 对照批准 Mock 验证专题选择、时间游标、证据/任务、客户降级和复用边界；视觉应融入 `gintbroker` 现有设计系统，不要求像素复刻 Mock。
11. AOI 为 `rough_bbox` 时必须显示“粗筛选范围/非精确事件点”；空 ADS-B 日显示“无匹配/覆盖不足”，不能填假点。
12. 增加中英文术语、键盘操作、颜色之外的状态标签和 loading/empty/error/blocked 状态。

视口矩阵：

| 视口 | 用途 | 通过标准 |
| --- | --- | --- |
| 1920x1080 | 会议室主屏 | 左侧专题、地图、右侧证据和专题回放同时可读 |
| 1711x819 | 用户现状截图基线 | 不遮挡左侧 Tab、右侧情报和时间区域，6 个画面能稳定复现 |
| 1440x900 | 笔记本彩排 | 面板可折叠，主要状态和质量提示不丢失 |
| 390x844 | 移动 smoke | 不要求完整大屏体验，但不得泄露隐藏数据或出现不可恢复错误 |

状态矩阵：

- DYINT internal bundle 正常。
- customer Gate 阻断。
- `rough_bbox`。
- 目标船身份未知。
- 5 月 27/28 日 ADS-B 主 AOI 为 0。
- 来源支持/反驳/待确认同时存在。
- API loading/error/empty。
- 切回 HIMARS 后旧专题正常。
- 若 6 月专题已安装，两个 DYINT 专题可互切，右侧和回放只消费当前 `selectedTopicId`。

验证：

```bash
cd "$GINTBROKER_ROOT/frontend"
npm run test:ci -- \
  src/components/map/geoJSONBuilders.test.ts \
  src/__tests__/components/TopicDetailPanel.test.tsx \
  src/__tests__/components/TopicReplayPanel.test.tsx \
  src/__tests__/components/WorldviewLeftPanel.test.tsx
npm run lint -- \
  src/app/page.tsx \
  src/hooks/useTopicBundle.ts \
  src/components/WorldviewLeftPanel.tsx \
  src/components/MaplibreViewer.tsx \
  src/components/TopicDetailPanel.tsx \
  src/components/TopicReplayPanel.tsx
npm run build

if rg -n 'dyint_sc2_20260526|dyint_sc2_20260610_12' \
  src/app src/components src/hooks src/types; then
  exit 1
fi
```

暂停条件：

- 新专题仍需新增 `ActiveLayers.dyint_*`、`DashboardData.dyint_*` 和专用 MapLibre source 才能工作，说明通用化未完成。
- 专题回放调用全局 snapshot 写接口或覆盖实时数据 store。
- HIMARS 地图、详情、聚焦或 slow 数据回归。
- UI 为了视觉张力隐藏证据质量、授权或位置精度。
- 通用代码出现任一 DYINT topic ID，或切换 5 月/6 月时复用旧详情/时间游标状态。

提交与记录：

- 分两次本地提交：
  - `feat(topics): 通用化专题地图与选择状态`
  - `feat(topics): 增加DYINT证据详情与专题回放`
- 每次提交前跑对应定向测试；记录 commit；不 push。

### T11：跨仓本地总验证和真实浏览器彩排

目标：

- 从外部原始数据到 `gintbroker` 页面完整重建一次，判定 `INTERNAL_READY`，并生成 6 张真实系统截图。

输入：

- T1-T10 两个仓库的本地 commit、发布 bundle 和验证记录。
- 已取得的 AOI、展示和截图许可；缺失项按 customer Gate 阻断。

修改范围：

- `dy-inta/demo_packages/.../06_validation/*`
- `dy-inta/demo_packages/.../06_validation/internal_screenshots/*`
- customer Gate 通过后才允许写入 `dy-inta/demo_packages/.../05_customer_assets/screenshots/*`
- `screen_manifest.csv`、主持稿、保护性报告和执行记录
- 不新增第二套运行时 HTML/CSS/JS；已批准的 `devdoc/DYINT场景2双专题交互Mock.html` 只保留为设计契约

步骤：

1. 原始输入保持原位；把上一轮中间构建移动到 `PREVIOUS_BUILD_ROOT`，不得移动/删除原始文件。
2. 按 T1-T8 完整重建数据包和 `gintbroker` 发布快照。
3. 比较两次稳定输出 SHA-256；排除 `retrieved_at`、日志和截图，业务 CSV/GeoJSON/bundle 必须一致。
4. 运行 T2、T9、T10 全部定向测试、lint 和 build。
5. 启动 `gintbroker` 本地标准环境，确认 API 与前端同源，不从浏览器直连外部原始文件。
6. 用真实浏览器依次完成：进入军事专题、开启 5 月专题、自动聚焦、时间回放、点击 AOI/摘要、查看证据/任务、切回 HIMARS；若 6 月专题已安装，再验证两个 DYINT 专题互切且详情/回放状态不串线。
7. 检查 Console、Network、页面内文和 bundle：无原始标识、个人路径、404、未处理 error 或第三方原始文件请求。
8. 在 1920x1080、1711x819、1440x900 获取 6 张内部验收截图并写 `06_validation/internal_screenshots/`；每张不超过 2MB，总量不超过 12MB。customer Gate 通过后才复制对应最终截图到 `05_customer_assets/screenshots/`；过程截图和录屏只放外部工作区。移动视口只做 smoke。
9. 对照 T0.5 批准 Mock 做交互一致性清单：专题独立性、共享外壳、选中/启用状态、时间门禁、证据/任务、客户降级均一致；允许按真实 `gintbroker` 设计系统调整视觉细节。
10. 由非技术同事或独立评审者完成一次 8-12 分钟彩排。
11. 使用 `presales-demo-review` 做轻量复审，更新 `validation_report.md`。

验证：

```bash
$PYTHON -m unittest discover -s tests/sc2_20260526 -p 'test_*.py' -v
$PYTHON tools/sc2_20260526/validate_package.py --package "$OUTPUT_ROOT" --mode internal
$PYTHON tools/sc2_20260526/validate_package.py \
  --package "$OUTPUT_ROOT" \
  --mode customer \
  --write-gate-report "$OUTPUT_ROOT/06_validation/customer_gate.json"
$PYTHON tools/sc2_20260526/validate_package.py \
  --package "$OUTPUT_ROOT" \
  --write-stable-checksums "$OUTPUT_ROOT/06_validation/output_checksums.sha256"
curl -fsS http://127.0.0.1:8000/api/topics/dyint_sc2_20260526/bundle | jq '{topic_id,release_id,feature_count:(.features.features|length),timeline_count:(.timeline|length)}'
```

合并策略：

- API bundle/timeline/brief 与页面专题加载可在同一次本地运行中验证。
- 6 张画面、Console、Network、HIMARS 回归和主持人口径可在同一轮浏览器彩排中完成。
- `internal` 与 `customer` Gate 不能合并；customer 校验非零退出但成功写出阻断报告时，只阻断 `CUSTOMER_READY`，不抹掉已通过的 `INTERNAL_READY`。粗 AOI/未授权素材不得因内部彩排通过而进入客户截图。
- 原始口径和去重口径不能合成一列；专题页面默认展示去重口径，同时允许查看原始对账说明。

暂停条件：

- 任一自动测试、lint、build 或浏览器主路径失败。
- 两次稳定构建 hash 不一致且无法解释。
- 客户 Gate 被绕过或页面泄露原始数据。
- 6 张画面需要人工改 JSON 才能复现。

提交与记录：

- `INTERNAL_READY` 通过后：
  - `dy-inta` 本地提交：`test(sc2): 完成gintbroker专题内部验收`
  - `gintbroker` 本地提交：`test(topics): 补齐DYINT专题浏览器验收证据`
- 未通过 customer Gate 时必须生成 `customer_gate.json` 阻断清单并记录 `BLOCKED_CONFIRM`，不得写入客户截图目录，也不得提交“客户门禁完成”。
- 默认不 push。

### T12：分支发布与 MR Gate（仅在执行轮明确要求发布时）

目标：

- 安全发布两仓分支并形成可复审 MR，不直接覆盖 `main`。

输入：

- T11 全部本地验证证据。
- 用户在当前执行轮明确要求执行到发布/目标环境。

修改范围：

- Git 远端分支与 MR；不修改业务文件。

步骤：

1. 两仓执行 `git fetch`，检查 ahead/behind/diverged；需要同步时只用 `git pull --rebase`，有冲突立即停止。
2. 确认 `dy-inta` 分支为 `codex/dyint-sc2-package`、`gintbroker` 分支为 `codex/dyint-sc2-topic`，所有阶段 commit 已记录，工作区干净。
3. 分别 push 两仓分支；不 force push。
4. 创建/更新 MR，描述数据边界、5MB bundle、HIMARS 兼容、验证矩阵、客户 Gate 和回滚方式。
5. MR 合并前暂停，等待人工 review；不得自动合并 `gintbroker main`。

验证：

```bash
git fetch origin
git status --short --branch
git log --oneline origin/main..HEAD
git -C "$GINTBROKER_ROOT" fetch origin
git -C "$GINTBROKER_ROOT" status --short --branch
git -C "$GINTBROKER_ROOT" log --oneline origin/main..HEAD
```

暂停条件：

- 用户未在执行轮明确要求发布。
- 远端已更新、分支 diverged、测试证据过期或 MR 出现未解决意见。
- 需要 force push、改写历史或直接写 main。

提交与记录：

- 本阶段不新增 commit；记录 push 结果和 MR URL。
- MR 合并是单独确认点。

### T13：Jenkins 部署与目标环境合并回归（MR 合并后）

目标：

- 将合并后的 `gintbroker main` 通过既有 `Shadowbroker` 流水线部署到 `192.168.211.195:3001`，完成真实环境回归。

输入：

- 已人工批准并合并的 `gintbroker` MR。
- `docs/dev-deploy/构建部署配置链路说明.md`。
- 用户在当前执行轮明确要求执行到目标环境。

修改范围：

- Jenkins 构建、Harbor 镜像和远端 Docker Compose 运行版本。
- 不修改 Jenkins job 配置、远端 `.env`、凭据或数据库。

步骤：

1. 确认 GitLab `main` commit 与待发布 commit 一致。
2. 触发 Jenkins `Shadowbroker`：`PUSH_IMAGES=true`、`DEPLOY_TARGET=shadowbroker_deploy_env_211_195`，`IMAGE_TAG` 留空使用 `shortSha-BUILD_NUMBER`。
3. 等待 Checkout、Preflight、Build/Push、Deploy 全部成功；记录 build URL 和 image tag。
4. 验证 backend/frontend 容器使用新 tag 且 healthy；总体 `/api/health` 的外部源 error 单独记录，不替代专题业务回归。
5. API 回归：`/api/topics` 同时有 HIMARS 和 DYINT；DYINT bundle/timeline hash 正确；HIMARS 仍有 6 个实体的基线或解释清楚的数据版本变化。
6. 浏览器回归 6 个画面、3 个桌面视口、Console/Network、HIMARS 回退和 8-12 分钟主持稿。
7. customer Gate 未通过时环境只能标 `INTERNAL_READY`，不得对外演示。

验证：

```bash
curl -fsS http://192.168.211.195:3001/api/topics | jq '.topics | map(.topic_id)'
curl -fsS http://192.168.211.195:3001/api/topics/dyint_sc2_20260526/bundle \
  | jq '{topic_id,release_id,source_package_sha256,feature_count:(.features.features|length)}'
curl -fsS http://192.168.211.195:3001/api/topics/dyint_sc2_20260526/timeline \
  | jq '{topic_id,count:(.timeline|length)}'
curl -fsS http://192.168.211.195:3001/api/topics/himars/brief \
  | jq '{topic_id,entity_total,intel_count:(.latest_intel|length)}'
```

暂停条件：

- Jenkins 任一阶段失败、镜像 tag 不一致、容器不健康或业务 API 404/500。
- 目标环境加载的 release/hash 与 T11 不一致。
- 需要修改远端 `.env`、Jenkins 配置或凭据才能继续。
- 现网 HIMARS 回归或客户 Gate 被错误放行。

提交与记录：

- 不新增代码 commit；记录 Jenkins build、image tag、容器状态、API/浏览器证据。
- 失败回滚使用部署文档中的历史 `SHADOWBROKER_IMAGE_TAG` 路径；切换历史 tag 是目标环境写操作，执行前单独确认。

### T14：收口复核

目标：

- 确认两仓 Git、数据版本、验证记录和目标环境一致，防止只完成数据或只完成页面就提前结束。

输入：

- T0-T13 执行记录、批准的 Mock hash、两种 foundation mode/commit、两仓 commit、自动验证、浏览器彩排、MR/Jenkins/目标环境证据。

修改范围：

- 本计划第 8.2 节执行记录。
- `06_validation/validation_report.md` 和 `screen_manifest.csv` 最终状态。
- 不默认修改源分析文档或相邻方案。

步骤：

1. 核对每阶段状态、`PROTOTYPE_GATE`/Mock hash、两种 foundation mode/commit、两仓 commit、`source_package_sha256`、release ID 和剩余 Gate。
2. 核对两个工作区无未知文件；原始数据、中间文件和 quarantine 均只在原路径/外部 scratch。
3. 核对只有一套 common/topic foundation，HIMARS 兼容、已安装 6 月专题互切、5 月 6 画面和专题回放均有验证证据。
4. 未进入 T12/T13 时明确写“仅本地 `INTERNAL_READY`，未发布”；不得误写目标环境已完成。
5. 输出最终状态：`INTERNAL_READY`、`CUSTOMER_READY` 或 `BLOCKED_CONFIRM`。

验证：

```bash
git status --short --branch
git log --oneline '@{upstream}..HEAD'
git -C "$GINTBROKER_ROOT" status --short --branch
git -C "$GINTBROKER_ROOT" log --oneline '@{upstream}..HEAD'
git diff --check
```

暂停条件：

- 有未解释变更、未记录 commit、失败测试、bundle/hash 不一致或缺少 Gate 证据。

提交与记录：

- 若只更新本计划执行记录，按纯文档规则本地提交：`docs(sc2): 收口DYINT专题实现记录`。
- 默认不 push；若 T12/T13 已授权完成，记录相应远端状态。

---

## 6. 验证矩阵

| ID | 验证层 | 覆盖点 | 样本/命令 | 通过标准 | 失败处理 |
| --- | --- | --- | --- | --- | --- |
| V00 | 原型 Gate | 两个独立专题、共享底座、交互/视口/客户降级 | T0.5 HTML Mock 走查 + hash | 用户明确批准；1711x819、1440x900、390x844 主路径通过；0 外部请求/未处理 error | `BLOCKED_CONFIRM`，不得进入 T1 |
| V01 | 输入盘点 | 文件存在、hash、日文件完整 | T0 inventory | AIS 1 个、ADS-B 9 个有效文件，hash 稳定 | `BLOCKED_CONFIRM`，不进入构建 |
| V02 | Schema | CSV 必需列、类型、枚举、主键 | `unittest` | 全表 schema 通过 | 修契约或生成器，不手改结果绕过 |
| V03 | 原始口径复现 | 源文档 AIS/ADS-B 计数 | T5/T6 reconciliation | hash 相同时原始口径一致 | 排查时间、BOM、边界、sidecar |
| V04 | 脏数据 | 时间、坐标、速度、身份、重复 | `telemetry_quality.csv` | 异常均有质量码，原始值未改写 | 隔离异常并重跑派生层 |
| V05 | 引用完整性 | source/evidence/AOI/asset 外键 | `test_referential_integrity.py` | 无悬空引用 | 回退当前阶段，补齐主表 |
| V06 | 时间完整性 | `visible_at`、`known_after_time`、评分时间 | `test_temporal_integrity.py` | 不存在未来信息泄露 | 阻断融合和页面生成 |
| V07 | 证据语义 | 事实、后验、背景、单方主张 | 抽查 UKMTO/JMIC/5月28日 | 分类与原文一致 | 降级为 `pending/context` |
| V08 | 身份与脱敏 | 船名、MMSI、IMO、ICAO、路径 | `test_customer_gate.py` | 客户产物无原始标识 | 删除客户构建结果并重建 |
| V09 | 授权 | 展示、截图、有效期 | customer validator | 所有引用均明确允许 | 客户 Gate 失败，保留内部模式 |
| V10 | AOI | 几何合法、精度状态、审批 | AOI tests | 内部 bbox 有标注；客户使用批准 polygon | 客户 Gate 失败 |
| V11 | 专题契约 | bundle schema、大小、hash、引用、audience | T8/T9 tests + API | 小于等于 5MB；无悬空引用、路径和原始标识；hash 一致 | 回到 T8/T9 |
| V12 | HIMARS 兼容 | 旧 API、slow 键、地图、详情、聚焦 | API + 浏览器回归 | 既有专题行为不退化；基线变化有数据版本解释 | 回退 `gintbroker` 通用化 commit |
| V13 | 安全文案 | 非进攻性叙事 | 自动扫描 + 人工复审 | 只有航运安全、复核、监测、报告动作 | 删除越界内容并复审 |
| V14 | 性能/资源 | 分块读取、耗时、峰值内存 | T5/T6 日志 | RSS < 2GB；无整表扫描 | 降低 chunk，从断点重跑 |
| V15 | 专题回放隔离 | 不写全局 snapshot、不暂停实时 store | Network + 存储检查 | 只读 bundle、内存游标、0 snapshot 写请求 | 禁用专题回放并回到 T10 |
| V16 | 视觉 | 6 画面、3 视口、状态矩阵 | T11 真实浏览器截图 | 不溢出、不遮挡；状态、精度和证据可读 | 回到 T10/T11 |
| V17 | 浏览器 | Console、Network、同源 API | DevTools | 0 未处理 error、0 原始文件/第三方直连、0 业务 404 | 阻断提交 |
| V18 | 确定性 | 两次构建稳定输出 hash | T11 checksums | 业务 CSV/GeoJSON/bundle 一致 | 定位非确定字段后重建 |
| V19 | 目标环境 | Jenkins 镜像、API、6 画面、3 视口 | T13 目标环境回归 | release/hash 正确；DYINT 与 HIMARS 均通过 | 回滚历史镜像并记录失败 |
| V20 | 演示闭环 | 8-12 分钟、非技术复述 | 内部彩排 | 能复述压力、动作、输出；每次升级可追溯 | 回到 T7/T10 |
| V21 | 双层共享基础 | common scanner/validator/exporter 与 topic API/UI 均场景无关 | 两种 foundation probe + common 双场景 fixture + 静态扫描 | 只有一套公共实现；两个独立 topic 无交叉引用；通用代码无任一 DYINT topic ID | 统一 foundation 或 `BLOCKED_CONFIRM` |

### 6.1 验证样本选择

- 正例：`UKMTO 062-26`、5 月 26 日 AIS/ADS-B 主 AOI 摘要。
- 时间负例：JMIC 后验确认、5 月 28 日媒体主张尝试进入 5 月 26 日前评分，必须失败。
- 授权负例：`display_allowed=false` 的样例数据尝试进入 customer bundle 和页面，必须失败。
- AOI 负例：`rough_bbox` 尝试通过客户 Gate，必须失败。
- 脏数据样本：缺时间、无效坐标、负速度、重复 ID、身份缺失各至少 1 条；使用合成 fixture，不复制敏感原始记录。
- 空数据样本：5 月 27/28 日主 AOI ADS-B 为 0，页面必须显示“无匹配/覆盖不足”，不能报错或填充假数据。

---

## 7. 脏数据与历史数据处理协议

### 7.1 默认原则

1. 所有外部输入只读，不在外接盘执行覆盖、重命名、删除或格式转换。
2. 不执行任何 `UPDATE/DELETE/ALTER/DROP`；本计划没有数据库写入。
3. 不自动纠正身份、时间、速度和坐标；只做标准化副本、质量标记和隔离。
4. 内部样例与真实历史遥测必须用 `data_class=sample_internal` / `historical_telemetry` 区分。
5. 客户构建默认不消费 `sample_internal`。

### 7.2 质量码

| 数据 | 质量码 | 处理 |
| --- | --- | --- |
| AIS/ADS-B | `TIME_MISSING` | 进入覆盖质量统计，不进入事前评分 |
| AIS/ADS-B | `TIME_OUT_OF_WINDOW` | 不进入 5 月 20-28 派生表，计入隔离统计 |
| AIS/ADS-B | `SOURCE_MONTH_MISMATCH` | 以解析时间为准分区，记录文件名不一致 |
| AIS/ADS-B | `COORD_MISSING` / `COORD_INVALID` | 不做 AOI 命中，原始值只留工作区 |
| AIS/ADS-B | `SPEED_NEGATIVE` / `SPEED_NON_NUMERIC` | 派生速度置空，禁止取绝对值 |
| AIS | `MMSI_MISSING` / `IMO_UNVERIFIED` | 只做匿名观测计数，不做身份结论 |
| ADS-B | `ICAO_MISSING` / `IDENTITY_UNVERIFIED` | 只做活动量和质量提示 |
| AIS | `HKEY_NOT_UNIQUE` | `IR_HKEY` 仅作源摘要，不参与唯一去重 |
| AIS/ADS-B | `DEDUPE_KEY_INCOMPLETE` | 不与其他不完整行折叠，raw/deduped 均保留并单列数量 |
| AIS/ADS-B | `DUPLICATE_COMPOSITE` | 原始口径保留，复合键完整时 deduped 只保留一条并记录数量 |
| 样例 | `SAMPLE_IDENTITY_UNVERIFIED` | 仅内部方法演示，客户 Gate 强制拒绝 |
| 来源 | `VISIBLE_AT_UNKNOWN` | 不参与历史时点评分 |

### 7.3 隔离记录

异常明细写入外部磁盘的 `QUARANTINE_ROOT`，只保留：

- 输入文件 ID 和行号/稳定 hash；
- 质量码；
- 脱敏字段摘要；
- 处理结果；
- 是否影响统计。

不得把 token、cookie、完整个人绝对路径、原始 MMSI/IMO/ICAO、未授权全文或完整原始行复制到计划、Git 或最终回复。

### 7.4 需要人工确认的处理

以下情况不得自动处理：

- 推断或覆盖目标船身份。
- 用其他时间字段改写原始事件时间。
- 删除大比例重复数据且去重键不唯一。
- 将粗 AOI 升级为正式 AOI。
- 将未授权素材设为客户可见。
- 清理原始文件所在目录、`DYINT_SCRATCH_ROOT` 或外接盘上的临时文件。

---

## 8. 执行记录表和续跑协议

### 8.1 状态定义

- `NOT_STARTED`：未开始。
- `IN_PROGRESS`：正在执行，尚未形成可恢复 commit。
- `DONE_LOCAL`：阶段验证通过并已本地 commit。
- `BLOCKED_CONFIRM`：需要用户/责任人确认、授权或外部材料。
- `FAILED`：验证失败且已记录原因，尚未形成可安全提交的结果。

### 8.2 当前执行记录

| 阶段 | 状态 | 起点 commit | 阶段 commit | 验证摘要 | 产物/剩余项 | 更新时间 |
| --- | --- | --- | --- | --- | --- | --- |
| T0 | `NOT_STARTED` | - | - | - | 重新检查分支、输入、空间、两种 foundation mode 和 Mock hash | - |
| T0.5 | `NOT_STARTED` | - | - | - | 双专题 HTML Mock 人工评审；当前 `DRAFT_REVIEW_REQUIRED` | - |
| T1 | `NOT_STARTED` | - | - | - | 来源与契约 | - |
| T2 | `NOT_STARTED` | - | - | - | 自动校验门禁 | - |
| T3 | `NOT_STARTED` | - | - | - | 事件与来源表 | - |
| T4 | `NOT_STARTED` | - | - | - | AOI 与客户 Gate | - |
| T5 | `NOT_STARTED` | - | - | - | AIS 派生表 | - |
| T6 | `NOT_STARTED` | - | - | - | ADS-B 派生表 | - |
| T7 | `NOT_STARTED` | - | - | - | 证据矩阵与时间线 | - |
| T8 | `NOT_STARTED` | - | - | - | 小型脱敏专题 bundle、两仓 commit | - |
| T9 | `NOT_STARTED` | - | - | - | 通用专题后端与兼容 API | - |
| T10 | `NOT_STARTED` | - | - | - | 通用专题地图、详情与专题回放 | - |
| T11 | `NOT_STARTED` | - | - | - | 跨仓本地总验证、6 张真实系统截图 | - |
| T12 | `NOT_STARTED` | - | - | - | 分支 push 与 MR Gate；需当轮授权 | - |
| T13 | `NOT_STARTED` | - | - | - | Jenkins 与目标环境回归；需当轮授权 | - |
| T14 | `NOT_STARTED` | - | - | - | 状态、hash、两仓和环境收口 | - |

### 8.3 必须继续条件

只要总目标未完成，且没有以下停止条件，完成当前小批后必须立即更新记录并继续下一阶段，不得因“已生成一个 CSV”“已跑一次脚本”或“内部页面能打开”就输出最终答复停止：

- `BLOCKED_CONFIRM`；
- `PROTOTYPE_GATE` 尚未批准、结论为 `REVISE`，或审批 hash 与当前 Mock 不一致；
- 测试、构建或数据对账失败且无法在当前阶段定位；
- Git 冲突、无关脏文件或暂存范围无法隔离；
- 需要客户授权、正式 AOI 审批，或即将进入尚未获得当轮授权的 T12/T13 外部写操作；
- 输入 hash 变化或外接盘断开。

### 8.4 断点恢复

1. 先读本表，定位最后一个 `DONE_LOCAL`。
2. 验证阶段 commit 存在且 `git status` 可解释。
3. 运行该阶段的最小 smoke 验证，不重新执行早期大文件处理。
4. 从下一阶段继续；若 smoke 失败，将原阶段改为 `FAILED`，回到该阶段修复。
5. 不使用 `reset --hard`、`clean`、amend 或 rebase 恢复断点；需要撤销已提交阶段时使用新的 `git revert`，并由用户确认撤销范围。

---

## 9. Git、发布和记录要求

本计划执行会在 `dy-inta` 产生 Python、测试、CSV/GeoJSON/JSON 和文档，在 `gintbroker` 产生 Python/TypeScript、测试、专题配置和小型脱敏 bundle，属于非纯文档变更。每个阶段必须完成直接相关验证后才能本地提交。

每次提交前：

```bash
git status --short
git diff --check
git diff --cached --check
git diff --cached --stat
git -C "$GINTBROKER_ROOT" status --short
git -C "$GINTBROKER_ROOT" diff --check
```

规则：

- 只暂存本阶段文件，不混入用户或其他任务改动。
- 每个 commit 单一职责，记录短 hash 到第 8 节。
- 测试未运行、失败或输入对账未完成时不自动 commit。
- T0-T11 默认不 push；只有执行轮明确授权后才进入 T12 push/MR 和 T13 Jenkins/目标环境回归。
- 本计划不修改 Jenkins job、远端 `.env`、数据库、K8S 或 JIRA；T13 只使用既有 `Shadowbroker` 发布链路。
- 不提交 `.work/`、原始数据、未脱敏映射、访问凭据、cookie、下载缓存或未授权素材。
- 若当前 `main` 的 ahead/behind 在执行期间变化，先停止并重新判断，不自动 pull/rebase。

---

## 10. 暂不处理事项、未验证假设与后续建议

### 10.1 暂不处理

- 商业 AIS/船舶登记、SAR/光学影像、天气海况、港口 ETA、污染和保险数据采购。
- 生产级数据中台接入、动态本体入图、规则 DSL、流式告警和自动报告分发。
- `gintbroker` 登录权限体系改造、全局 Time Machine 数据模型改造，以及非本专题的 UI 重构。
- 2 月基线、4 月过渡、6 月风险窗口的完整复用和联动评分。
- 面向特定攻击方、武器、军事部署或行动路线的分析。

### 10.2 未验证假设

- UKMTO/JMIC URL 在执行时仍可访问，且原文元数据足以支持 `visible_at`。
- 海贝 AIS/ADS-B 的内部处理、衍生统计和客户截图许可可以分别获得明确判断。
- 三个粗 AOI 能满足内部方法演示，但不能自动满足客户地图要求。
- bundled Python 3.12 和当前 `pandas/openpyxl` 在执行期间仍可用。
- 目标船保持匿名不会削弱客户故事的核心价值。
- `gintbroker` 通用专题 bundle 能在保留 HIMARS 旧 API/slow 键的前提下完成，不需要迁移全局实时 store。
- HTML Mock 的双专题信息架构、客户降级和共享边界仍需用户/产品责任人明确批准；当前不推断为已定型。
- 5 月先执行时可以 `bootstrap` common/foundation；6 月先执行时本计划能按两种探针切换 `reuse/resume`，不依赖固定执行顺序。
- 目标环境继续使用 `Shadowbroker` 既有 Jenkins + Docker Compose 链路；执行 T13 前必须按当时文档和流水线现场复核。

### 10.3 后续建议

1. 先完成 T0/T0.5 并取得双专题 Mock 明确批准；再完成 T1-T8 数据与小型 bundle、T9-T11 本地真实系统集成，只有 6 画面和 HIMARS/已安装 6 月专题回归都通过才判 `INTERNAL_READY`。
2. 客户 Gate 缺少正式 AOI 或授权时，仍可完成内部系统集成，但页面、截图和报告必须固定为 `INTERNAL_ONLY`，不得对外演示。
3. T12/T13 保持独立授权点；本地验证通过不等于允许 push、合并或部署。
4. 若客户明确要求实时能力，再按 `moye-v4-product` 数据接入、`doops-dev` 规则/证据治理、`gintbroker` 运行面分别拆计划，不能把三个系统合成一个大改造任务。

---

## 11. 后续执行入口

后续执行时直接使用：

[$checkpointed-plan-executor](/Users/liushen/Documents/cursorDevs/trsdevops/devops_console/.agents/skills/checkpointed-plan-executor/SKILL.md) `/Users/liushen/Documents/githubDevs/dy-inta/devdoc/DYINT场景2-5月商船攻击候选目标分析与数据补强方案-实现计划.md`

执行器必须先停在 T0.5 获取 `PROTOTYPE_GATE=APPROVED`；本轮创建 Mock 不等于用户已批准。
