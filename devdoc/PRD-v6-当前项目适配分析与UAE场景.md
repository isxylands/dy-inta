# PRD v6.0 当前项目适配分析与 UAE 场景建议

> 需求来源：`/Users/liushen/Documents/非Coding工作/DYINT/O多源情报系统/多源情报分析平台PRD_v6.0.pdf`
>
> PRD 整理稿：`/Users/liushen/Documents/githubDevs/dy-inta/PRD-v6.md`
>
> 被分析项目：`/Users/liushen/Documents/cursorDevs/gintbroker`
>
> 分析日期：2026-07-06

## 1. 结论摘要

当前项目更像一个已经具备较强可视化能力的“多源 OSINT/遥测地图底座 + AI 操作面 + SAR 异常图层”，不是 PRD v6.0 要求的“L1 → L2 → L3 情报生产系统”。

这意味着两类 PRD 场景都能复用项目的一部分底座能力，但还不能按 PRD 验收闭环跑通：

| PRD 场景 | 当前适配度 | 判断 |
| --- | --- | --- |
| 场景一：多源触发 → 情报验证链路 | 中低 | 数据层和地图层较强；有粗粒度相关性、AI pin、卫星图像查询、近邻新闻检索。但缺少正式 L1 事件、线索卡片、分析师审核、卫星任务联动、L2 识别、验证矩阵和 L3 报告闭环。 |
| 场景二：连续影像变化检测 → 情报生成 | 中低 | 已有 AOI、SAR catalog、预处理 SAR anomaly 和 Time Machine 概念；但不是 PRD 所需的监测任务、T0/Tn 多时相影像资产、像素级变化检测、L2 精识别、L3 变化报告和推送闭环。 |

从建设策略看，不建议把当前项目直接包装成“已经满足 PRD”。更合理的说法是：当前项目可以作为 PRD 平台的可视化、实时遥测、OSINT 聚合、SAR 外部异常接入和 AI 操作入口的基础；要真正支持好 PRD，需要补一层“情报生产工作流与证据链系统”，并把现有地图能力收编为 L1/L2/L3 的证据展示和操作界面。

## 2. PRD 要求的核心不是地图，而是情报生产闭环

PRD v6.0 的核心骨架是三级情报链：

| 层级 | PRD 定义 | 关键产物 |
| --- | --- | --- |
| L1 异常预警 | 从 OSINT、AIS、ADS-B、RF 或影像变化中发现异常 | 标准化异常事件、线索卡片、触发源、初始置信度 |
| L2 目标确认 | 通过卫星影像采集与 AI 目标识别确认 L1 线索 | 影像任务、影像切片、目标清单、坐标、验证状态 |
| L3 融合报告 | 多源交叉验证、意图推断、结构化报告生成 | 验证矩阵、证据链、意图推断、综合置信度、PDF/归档 |

两个场景的差异主要在 L1 触发方式：

| 场景 | L1 触发 | L2 处理 | L3 输出 |
| --- | --- | --- | --- |
| 场景一 | OSINT 热点、AIS/ADS-B/RF 异常 | 分析师确认后触发卫星影像验证 | 单事件融合情报报告 |
| 场景二 | AOI 持续影像变化检测 | 达阈值后自动触发目标精识别或高分辨率补采 | 变化情报报告与推送 |

所以评估当前项目时，不能只看是否有 AIS、ADS-B、SAR、地图、AI 接口，还要看是否有标准化生产对象和状态机：`L1Event`、`LeadCard`、`ImageryTask`、`DetectionResult`、`VerificationMatrix`、`IntelReport`、`AuditTrail`、`Notification`。

## 3. 当前项目可复用能力

### 3.1 多源地图与实时遥测底座

当前项目 README 描述其聚合 60+ live intelligence feeds，并提供 35+ 可切换图层，覆盖 aircraft、ships、satellites、GPS jamming、conflict zones、SAR ground-change 等。数据源清单包含 OpenSky、adsb.lol、aisstream.io、CelesTrak、GDELT、NASA FIRMS、IODA、Sentinel-2、Copernicus CDSE 等。

这部分对 PRD 有价值：

- 可作为 M11 情报展示层的起点。
- 可作为 M0/M1 的外部数据接入雏形。
- 可作为演示阶段的多源实时态势背景。
- 可为 UAE 海域、港口、机场、边境 AOI 提供一屏式态势展示。

主要不足：

- 当前多源数据大多作为地图图层展示，不天然沉淀为 PRD 的 L1 事件对象。
- 图层数据的来源、处理状态、置信度、审核状态、证据链没有统一标准。
- 多源只是“同屏可见”，还不是“同一条情报链上的证据”。

相关证据：

- `/Users/liushen/Documents/cursorDevs/gintbroker/README.md:20`
- `/Users/liushen/Documents/cursorDevs/gintbroker/README.md:41`
- `/Users/liushen/Documents/cursorDevs/gintbroker/README.md:536`

### 3.2 粗粒度跨层相关性引擎

项目已有 `correlation_engine.py`，支持几类跨层组合信号：

- RF Anomaly：GPS jamming + internet outage。
- Military Buildup：military flights + naval vessels + GDELT conflict events。
- Infrastructure Cascade：internet outage + KiwiSDR offline。
- Possible Contradiction：official statement + infrastructure disruption。

这对 PRD 场景一有启发意义，因为它已经从“单图层展示”迈出一步，开始生成复合 alert。

主要不足：

- 这些 alert 仍是固定规则的态势提示，不是 PRD 的 L1 线索卡片。
- 没有分析师确认、任务流转、L1→L2 卫星任务联动。
- 没有每条信号的验证状态、权重、置信度跃迁。
- 没有能直接进入 L3 报告的交叉验证矩阵。

相关证据：

- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/services/correlation_engine.py:1`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/services/correlation_engine.py:70`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/services/correlation_engine.py:165`

### 3.3 SAR AOI、SAR catalog 与预处理异常图层

项目已经有 SAR 相关接口：

- `/api/sar/status`
- `/api/sar/anomalies`
- `/api/sar/scenes`
- `/api/sar/coverage`
- `/api/sar/aois`
- `/api/sar/near`

SAR catalog fetcher 使用 ASF Search 拉取 Sentinel-1 scene metadata，不下载原始影像。SAR products fetcher 拉取 NASA OPERA、Copernicus EGMS、GFM、EMS、UNOSAT 等已经计算好的异常产品，不做本地 DSP。

这对 PRD 场景二很有价值：

- AOI 管理可以作为持续监测任务的空间入口。
- SAR scene catalog 可以作为“覆盖情况/最近过境/下一次过境”能力雏形。
- 外部预处理 anomaly 可以作为 L1 变化预警的一个输入源。

主要不足：

- 当前 SAR catalog 是 metadata 级，不是 PRD 要求的影像资产管理。
- 当前 SAR anomaly 是外部预处理产品，不是平台自身基于 T0/Tn 影像做变化检测。
- 没有监测任务模型、采集频率、阈值、运行状态、失败重试、补采策略。
- 没有变化区域的 L2 精识别、变化前后对比图和 L3 变化报告。

相关证据：

- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/routers/sar.py:1`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/services/fetchers/sar_catalog.py:1`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/services/fetchers/sar_products.py:1`
- `/Users/liushen/Documents/cursorDevs/gintbroker/frontend/src/components/SarAoiEditorModal.tsx:52`

### 3.4 AI 操作面、pin 与 agent channel

项目已有 AI Intel pin、agent tool manifest、HMAC-signed command channel、batch command 等能力。AI 可以创建 pin、查询图层、拉取近邻新闻、调用卫星图像查询、生成当前态势报告。

这对 PRD 的 M10 和部分 M11 有价值：

- 可作为自然语言操作入口。
- 可让 AI 将分析结果落成地图 pin。
- 可作为后续 L1 事件、L2 结果、L3 报告的操作通道。
- 可用于演示“AI co-analyst”体验。

主要不足：

- pin 是调查标记，不是标准情报对象。
- `/api/ai/report` 当前更像当前 telemetry 的摘要，不是 PRD L3 报告。
- agent command 是操作协议，不等于情报生产状态机。
- 缺少报告模板、版本、审核、归档、PDF 和证据链。

相关证据：

- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/routers/ai_intel.py:161`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/routers/ai_intel.py:404`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/routers/ai_intel.py:669`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/routers/ai_intel.py:1576`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/routers/ai_intel.py:2916`

### 3.5 Topic、feed ingester 与 OSINT 轻量聚合

项目已有 topic service，支持根据关键词从 news、GDELT、LiveUAMap 等来源提取相关条目。Feed ingester 支持从 GeoJSON 或 JSON feed 自动转换为 pin layer。

这对场景一的 OSINT 热点路径有价值：

- 可以快速配置面向某地区、某事件类型的监控 topic。
- 可以接入客户已有 feed，落到地图图层。
- 可以作为线索发现的输入源。

主要不足：

- 当前是关键词匹配和图层入库，不是 PRD 要求的 OSINT 结构化提取。
- 没有时间、地点、实体、行为的标准抽取结果。
- 没有来源可信度评级、跨源印证度、时效评分。
- 没有将多条 OSINT 聚合成一条 L1 LeadCard 的能力。

相关证据：

- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/services/topics/service.py:115`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/services/topics/service.py:233`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/routers/topics.py:18`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/services/feed_ingester.py:1`

### 3.6 权限与持久化现状

项目已有 admin key、scoped token、HMAC channel 等安全控制，也有 JSON 文件持久化 pin/layer。

这对原型有帮助，但距离 PRD 的生产级 M6 数据治理还远：

- 权限模型不是 PRD 的数据工程师、情报分析师、决策者分级 RBAC。
- pin/layer JSON 持久化不适合承载情报链、影像资产、审计轨迹和报告版本。
- 缺少 PostGIS、对象存储、时序数据、不可篡改审计、统一实体库。

相关证据：

- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/auth.py:94`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/services/ai_pin_store.py:54`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/services/ai_pin_store.py:75`

## 4. 场景一适配分析：多源触发 → 情报验证链路

### 4.1 PRD 要求

场景一要求从 AIS、ADS-B、RF 或 OSINT 中发现异常，形成 L1 线索；分析师确认后触发卫星影像获取；AI 做 L2 目标识别；系统把 L1 和 L2 交叉验证，生成 L3 融合报告。

端到端关键产物应包括：

- L1 异常事件。
- L1 结构化线索卡片。
- 分析师确认记录。
- 卫星影像任务单。
- 影像资产与 AI 标注切片。
- L1/L2 交叉验证矩阵。
- L3 情报报告。
- 报告 PDF、版本、归档、审计。

### 4.2 当前能满足的部分

| PRD 能力 | 当前项目情况 | 适配判断 |
| --- | --- | --- |
| 多源数据接入 | 已有 ADS-B、AIS、GDELT、GPS jamming、internet outage、SAR、Sentinel-2 等图层或查询 | 可复用为数据输入，但要标准化 |
| OSINT 热点输入 | topic service 可按关键词从 news/GDELT/LiveUAMap 抽取条目 | 可作为 MVP 输入，不满足结构化质量 |
| 传感器异常提示 | correlation engine 有 GPS jamming、military buildup 等组合 alert | 可改造成 L1 rule engine 的一部分 |
| 地图展示 | MapLibre 多图层和 AI pin 能展示事件点位 | 可作为 M11 起点 |
| 卫星图像查询 | `/api/ai/satellite-images` 可按坐标查 Sentinel-2 近 60 天低云量影像 | 可用于演示，不是任务订购 |
| AI 操作 | agent channel 可读写 pin、查询数据、生成摘要报告 | 可作为操作入口，不是 PRD 工作流 |

### 4.3 关键缺口

| 缺口 | 为什么重要 | 不补的后果 |
| --- | --- | --- |
| L1 标准事件模型 | PRD 验收要求 L1 事件有类型、坐标、来源、置信度、状态 | 当前 alert/pin/topic 无法统一流转 |
| LeadCard 线索卡片 | 分析师确认 L1→L2 需要结构化对象 | 无法把 OSINT 和传感器异常合并成可审核线索 |
| 信源评级与跨源聚合 | PRD 要求来源权威性、多源印证度、时效性 | 置信度没有依据，L1 质量不可控 |
| 影像任务联动 | PRD 要求确认后 1 分钟内生成并下发影像任务 | 当前只能查公开 Sentinel-2 图像，无法表达 task id、状态、补采 |
| L2 目标识别 | PRD 要求舰船、飞机、车辆、设施识别与坐标 | 当前没有模型推理接口和检测结果对象 |
| 交叉验证矩阵 | PRD 的 L2→L3 核心证据 | 无法说明每条 L1 线索是已确认、部分确认、矛盾还是未确认 |
| L3 报告系统 | PRD 要求 7 项必填、PDF、归档、置信度 90-99% | 当前 `/api/ai/report` 只是态势摘要 |

### 4.4 建议的场景一 MVP

建议先做一个可演示、可验收、但不一开始承诺真实卫星订购和高精度识别的 MVP：

1. 新增 `L1Event` 和 `LeadCard`。
   - 输入来自 topic、correlation、AIS/ADS-B/GPS jamming、手工导入 fixture。
   - 字段包括 `event_id`、`aoi`、`entity_type`、`time_window`、`trigger_sources`、`confidence`、`status`。

2. 新增分析师审核队列。
   - 状态：`new`、`triaged`、`approved_for_l2`、`rejected`。
   - 操作必须写审计日志。

3. 新增 `ImageryTask` 抽象。
   - 先接 mock provider 或公开 STAC provider。
   - 接口预留真实影像订购平台：`create_task`、`get_status`、`ingest_scene`。
   - 必须支持 `task_id`、`provider`、`aoi`、`time_window`、`status`、`failure_reason`。

4. 新增 L2 detection result 抽象。
   - MVP 可以先接预置标注 fixture 或人工上传 GeoJSON。
   - 后续再接目标识别模型。

5. 新增 verification matrix。
   - 比对目标类型、数量、坐标距离、时间窗。
   - 输出 `confirmed`、`partially_confirmed`、`unconfirmed`、`contradicted`。

6. 新增 L3 report template。
   - 先生成 Markdown/HTML/PDF。
   - 报告必须引用 L1、L2、verification matrix 和信源列表。

## 5. 场景二适配分析：连续影像变化检测 → 情报生成

### 5.1 PRD 要求

场景二要求分析师配置 AOI、采集频率、影像类型、变化类型和阈值；系统持续获取 T0/T1/Tn 影像；新影像入库后自动执行变化检测；达阈值后触发 L2 精识别；最后生成 L3 变化情报报告并推送。

端到端关键产物应包括：

- 监测任务。
- AOI 与采集计划。
- T0/Tn 多时相影像资产。
- 变化检测结果。
- L1 变化预警。
- L2 精识别结果。
- 变化前后对比图。
- 变化时序链。
- L3 变化报告。
- 推送记录。

### 5.2 当前能满足的部分

| PRD 能力 | 当前项目情况 | 适配判断 |
| --- | --- | --- |
| AOI 配置 | SAR AOI editor 支持创建、删除 AOI，含中心点、半径、类别 | 可作为空间配置起点 |
| SAR 覆盖查询 | ASF Sentinel-1 scene metadata 和 coverage summary | 可用于判断过境和覆盖 |
| 外部变化异常 | OPERA、EGMS、GFM、EMS、UNOSAT 预处理 anomaly | 可作为变化预警输入之一 |
| 地图展示 | SAR anomaly pins 和 AOI 边界可视化 | 可作为变化预警展示 |
| Time Machine | 支持 snapshot diff，但目前是 count diff | 概念可复用，能力不足 |

### 5.3 关键缺口

| 缺口 | 为什么重要 | 不补的后果 |
| --- | --- | --- |
| MonitoringTask 模型 | PRD 场景二从“一次性 AOI”升级为“持续任务” | 无法表达频率、阈值、负责人、运行状态 |
| 影像资产管理 | PRD 要求 T0/T1/Tn 多时相影像 | 只有 scene metadata，不能做平台内变化检测 |
| 影像订购/调度 | PRD 要求历史档案与编程影像 | 不能保证持续覆盖和任务状态可追踪 |
| 本地变化检测 | PRD 要求设施、装备、活动痕迹分类 | 只接外部 anomaly，无法满足客户自定义 AOI 与模型验收 |
| L2 精识别 | PRD 要求变化区域目标类型、数量、坐标、状态 | 无法把变化从“异常”升级为“情报确认” |
| 时序链 | PRD 要求跨期变化聚合和趋势识别 | 无法支撑渐进式部署、扩建、修复等研判 |
| L3 报告和推送 | PRD 要求自动报告、通知、报告链接 | 当前缺少报告生命周期和通知闭环 |

### 5.4 建议的场景二 MVP

场景二建议不要从“训练高精度变化检测模型”开始。更稳的 MVP 是先做任务编排和资产闭环，用预置样本或外部变化结果打通流程：

1. 新增 `MonitoringTask`。
   - 字段包括 `aoi`、`frequency`、`sensor_type`、`change_types`、`threshold`、`owner`、`status`、`next_run_at`。

2. 新增 `ImageryAsset`。
   - 字段包括 `asset_id`、`task_id`、`timestamp`、`sensor`、`resolution`、`cloud_cover`、`bbox`、`storage_uri`、`source`。
   - 支持 T0/T1/Tn 标记。

3. 新增 `ChangeDetectionRun`。
   - 记录 `baseline_asset_id`、`current_asset_id`、`model_version`、`status`、`duration_ms`、`quality_flags`。

4. 新增 `ChangeObject`。
   - 字段包括 geometry、area、change_type、sub_type、confidence、trend_group_id。

5. 先支持三类检测来源。
   - 外部预处理 SAR anomaly。
   - 人工/fixture 标注的变化 GeoJSON。
   - 后续接入真实变化检测模型。

6. 新增 L3 变化报告。
   - 必须包含 T0/Tn 对比图、变化列表、时序图、意图推断、OSINT 佐证和置信度。

## 6. 横向基础能力缺口

### 6.1 数据治理底座 M6 是最优先短板

PRD 的 M6 是所有 L1/L2/L3 的基础。当前项目如果继续依赖内存、JSON 文件和图层对象，很难支撑验收。

建议最小建设：

| 能力 | 建议 |
| --- | --- |
| 结构化与地理存储 | PostgreSQL + PostGIS |
| 影像与报告文件 | 对象存储，开发期可用本地 S3-compatible/MinIO |
| 时序与轨迹 | 先用 PostGIS + 分区表，数据量上来再拆时序库 |
| 事件溯源 | 所有 L1/L2/L3 对象保留 source、operator、timestamp、status transition |
| 审计 | 审核、任务下发、报告修改、导出都写 audit log |
| 实体库 | 船舶、飞机、港口、机场、基地、AOI、任务、报告统一关联 |

### 6.2 PRD 指标需要重新定标

PRD 写了若干较强指标，例如：

- 舰船识别 ≥90%。
- 飞机识别 ≥85%。
- 坐标误差 <3m。
- 设施变化 ≥90%。
- 装备变化 ≥95%。
- L3 报告 ≤30 秒。

这些指标不能靠当前项目自然满足，必须绑定：

- 明确的数据集。
- 标注口径。
- AOI 类型。
- 影像分辨率。
- 模型版本。
- 统计样本量。
- 误报/漏报定义。

否则验收时会出现“演示可跑，但指标无法证明”的风险。

### 6.3 安全、权限和合规需要产品化

面向 UAE 这类政府、港口、边境、关键基础设施客户时，安全和合规不是附加项。

建议至少补齐：

- RBAC：数据工程师、情报分析师、决策者、管理员。
- 审计日志：所有敏感操作可追溯。
- 密钥管理：影像平台、OSINT API、通知渠道密钥集中管理。
- 数据分级：公开 OSINT、客户私有数据、敏感报告分级。
- 脱敏导出：报告导出前可隐藏来源 URL、内部任务 ID、人员信息。
- 离线/内网部署选项：对政府客户尤其重要。

## 7. 建议实施路线

### 阶段 0：产品口径收敛

目标：不要把当前项目直接承诺成完整 PRD 平台，而是明确“现有底座 + 新增情报生产工作流”。

产物：

- 当前能力与 PRD mapping。
- L1/L2/L3 对象模型草案。
- 两个端到端 demo script。
- 验收指标的可测口径。

### 阶段 1：L1 事件与线索卡片

目标：把现有 topic、correlation、feed、pin 输入统一成标准 L1。

产物：

- `L1Event`。
- `LeadCard`。
- 分析师审核队列。
- 初始置信度计算。
- 地图与列表联动。

验收：

- OSINT 三条同 AOI 输入能聚合为一条线索。
- AIS/ADS-B/GPS jamming fixture 能生成 L1 事件。
- 分析师能确认或驳回线索。

### 阶段 2：影像任务与 L2 抽象

目标：不依赖真实供应商先打通 L1→L2。

产物：

- `ImageryTask`。
- STAC/mock provider。
- `ImageryAsset`。
- `DetectionResult`。
- AI 标注图层或 GeoJSON overlay。

验收：

- 分析师确认 L1 后 1 分钟内生成任务。
- 任务完成后生成 L2 result。
- 地图能显示影像和目标标注。

### 阶段 3：验证矩阵与 L3 报告

目标：把“地图上看到东西”变成“可审计情报产品”。

产物：

- `VerificationMatrix`。
- `IntelReport`。
- Markdown/HTML/PDF 导出。
- 报告版本和归档。

验收：

- 每条 L1 线索都有验证状态。
- 报告包含 PRD 7 项必填字段。
- 置信度从 L1 到 L2 到 L3 有可解释变化。

### 阶段 4：场景二持续监测

目标：把 SAR AOI 升级为持续监测任务。

产物：

- `MonitoringTask`。
- T0/Tn 影像资产管理。
- `ChangeDetectionRun`。
- `ChangeObject`。
- 变化时序链。
- 变化报告与推送。

验收：

- AOI 任务配置后可自动运行。
- 预置三期影像能生成变化对象和时序图。
- 达阈值后生成 L3 变化报告。

### 阶段 5：真实模型与真实影像订购平台接入

目标：从 demo/MVP 进入客户验收。

产物：

- 影像订购平台适配器。
- 模型推理服务。
- 数据集评测报告。
- 运行监控、失败重试、成本控制。

验收：

- 使用客户认可 AOI 和样本集评估精度。
- 有失败重试、补采、降级策略。
- 有运维指标和审计报表。

## 8. 面向 UAE 用户的三个打动场景

以下场景是假设客户在阿联酋，偏向海事安全、关键基础设施、边境与大型活动保障。为了避免不必要的敏感承诺，建议对外表述为“maritime security / critical infrastructure protection / event security intelligence”，不要直接包装成进攻性军事侦察。

### 场景 A：霍尔木兹海峡与富查伊拉港海事异常闭环

目标用户：

- 海事安全部门。
- 港口运营方。
- 能源与航运风险管理团队。

业务痛点：

- 阿联酋对油气、港口和航运安全高度敏感。
- 船舶 AIS 静默、异常停泊、异常绕航、靠近敏感海域，单靠地图很难判断是否值得升级。
- 决策者需要的是“这个异常是否被卫星或其他来源证实”，不是一堆散点。

演示脚本：

1. 系统在富查伊拉港外或霍尔木兹海峡附近发现某船舶 AIS 长时间静默，同时附近出现 GPS jamming 或 OSINT 报道。
2. 平台生成 L1 LeadCard：船舶标识、最后位置、异常类型、时间窗、触发源和 65% 初始置信度。
3. 分析师确认后，一键触发 L2 影像任务。
4. 系统展示历史档案影像或最新 SAR/光学影像，识别目标船只或异常聚集。
5. 验证矩阵显示 AIS 异常、OSINT、影像结果的吻合/矛盾状态。
6. L3 报告输出：事件摘要、证据链、风险等级、建议动作，可导出 PDF 给值班负责人。

能打动客户的点：

- 从“看见船”升级为“解释异常并形成可交付报告”。
- 对 UAE 的港口、航道、能源出口安全直接相关。
- 可以先用公开数据和样例影像演示，后续接客户自有 AIS、港口数据和商业影像。

对应 PRD：

- 场景一主线。
- 场景一到场景二联动：确认后把该海域设为持续监测 AOI。

### 场景 B：关键能源设施与港区的连续变化监测

目标用户：

- 能源设施安保。
- 关键基础设施保护部门。
- 港口和自由区运营方。

业务痛点：

- 油气设施、港区、储罐区、码头、机场周边的施工、毁损、临时设施和异常车辆/船舶活动，需要持续监测。
- 人工定期看影像容易漏掉渐进式变化。
- 决策层希望看到趋势，而不是单期截图。

演示脚本：

1. 分析师在 Jebel Ali、Fujairah、Ruwais 或指定能源设施周边画 AOI。
2. 设置每 3 天一次的 SAR/光学监测任务，关注设施变化、装备/车辆聚集、活动痕迹。
3. 系统取 T0 基准影像，随后导入 T1/T2/T3 样例影像或外部 SAR anomaly。
4. 变化检测发现新增临时设施、车辆聚集或码头区域活动变化，生成 L1 变化预警。
5. 达阈值后触发 L2 精识别，输出变化区域、面积、目标数量和前后对比图。
6. L3 变化报告生成趋势图、证据链和可能意图，例如“常规施工”“临时扩容”“异常集结待核查”。

能打动客户的点：

- 不是等新闻或告警发生后再查，而是持续主动发现变化。
- 对关键基础设施保护、港口运营、灾害/事故恢复评估都可复用。
- SAR 能突出“夜间、云层、沙尘条件下仍可监测”的价值，但要明确当前项目现阶段是接外部预处理异常和 catalog，完整像素级检测需要后续建设。

对应 PRD：

- 场景二主线。
- 场景二到场景一联动：变化报告一键触发 OSINT 核查。

### 场景 C：大型活动与城市安全的空地海多源态势保障

目标用户：

- 城市安全运营中心。
- 大型活动安保团队。
- 应急管理与交通协调部门。

业务痛点：

- Dubai、Abu Dhabi 常有大型国际会议、展会、赛事和高规格访问。
- 活动期间需要同时关注空域、港口、道路、社交舆情、通信干扰和突发事件。
- 单独的航班、船舶、新闻、CCTV 系统割裂，值班人员难以形成统一判断。

演示脚本：

1. 以活动场馆、机场、港口和主要交通走廊建立多个 AOI。
2. 平台实时展示 ADS-B、AIS、GPS jamming、OSINT topic、CCTV/feed pin、天气和突发事件图层。
3. 若出现异常低空航迹、可疑船舶靠近、通信干扰、社交媒体热点，系统生成 L1 线索。
4. 分析师把高优先级线索升级为 L2，联动影像或外部核查。
5. 系统生成值班简报：异常清单、证据来源、处置建议、待确认事项。

能打动客户的点：

- 当前项目已有多图层实时态势优势，适合先做高冲击演示。
- 比单一情报系统更贴近城市级运营中心。
- 可把 PRD 的 L1/L2/L3 做成“值班情报生产流程”，而不是纯军事语境。

对应 PRD：

- 以场景一为主。
- 可扩展场景二：活动前后对关键区域做变化监测。

## 9. 推荐对外表达

对 UAE 用户建议这样定位：

> We already have a real-time multi-source geospatial intelligence surface. The next product step is to turn it into an auditable intelligence production workflow: L1 anomaly detection, L2 satellite-backed confirmation, and L3 evidence-based reporting.

中文口径：

> 当前系统已经具备多源实时态势与地图操作能力；下一步要补的是可审计的情报生产闭环，把异常发现、卫星确认和融合报告串成 L1→L2→L3 的标准流程。

不建议这样说：

- “当前项目已经满足 PRD v6.0。”
- “已经具备 90%+ 目标识别精度。”
- “已经能自动订购卫星并完成变化检测。”
- “已经是生产级政府情报系统。”

更稳妥的承诺：

- 演示版可以在 2-4 周内打通 L1→L2→L3 mock/fixture 闭环。
- MVP 可以在 6-10 周内打通真实数据底座、任务流转、报告闭环。
- 真实影像订购平台和模型精度验收需要另设专项，以客户数据、供应商接口和标注集为准。

## 10. 风险与控制措施

| 风险 | 影响 | 控制措施 |
| --- | --- | --- |
| 把公开图层展示误认为情报闭环 | 验收失败 | 明确当前能力与 PRD 产物差异，先补对象模型和工作流 |
| 目标识别/变化检测精度无法证明 | 客户不认可 | 提前定义测试集、标注口径、指标统计方法 |
| 影像订购平台接口不确定 | L1→L2 断链 | 先做 provider interface 和 mock provider，再接真实供应商 |
| OSINT 来源质量不稳定 | 误报和误判 | 信源评级、跨源印证、人工审核、黑白名单 |
| 地图 pin 过载 | 分析师无法处理 | L1 事件队列、优先级、聚合和降噪 |
| 敏感数据与权限不足 | 政府/企业客户不可用 | RBAC、审计、密钥管理、脱敏导出、内网部署 |
| 当前持久化不适合生产 | 数据丢失或不可追溯 | 引入 PostGIS、对象存储、审计日志和备份策略 |

## 11. 最小验收建议

### 11.1 场景一 Demo 验收

- 输入 3 条 OSINT fixture 和 1 条 AIS/ADS-B/GPS 异常 fixture。
- 系统聚合生成 1 条 L1 LeadCard。
- 分析师确认后生成 L2 ImageryTask。
- mock provider 返回影像和目标检测结果。
- 系统生成 verification matrix。
- 系统生成 L3 报告，包含 PRD 7 项字段。
- 地图能定位 L1/L2/L3 对象。

### 11.2 场景二 Demo 验收

- 创建 1 个 AOI MonitoringTask。
- 导入 T0/T1/T2 三期样例影像或变化 GeoJSON。
- 系统生成 ChangeDetectionRun 和 ChangeObject。
- 达阈值后生成 L1 变化预警。
- 生成 L2 精识别结果和 T0/Tn 对比图。
- 生成 L3 变化报告并写入报告列表。

### 11.3 平台级验收

- 每个 L1/L2/L3 对象都能追溯来源。
- 每次人工审核都有 audit log。
- 报告可导出 PDF。
- 权限能区分数据工程师、分析师和决策者。
- 任意一条报告能反查到原始 OSINT、传感器记录或影像资产。

## 12. 最终建议

当前项目的最大价值不是“已经完成 PRD”，而是它已经有了一个很适合演示和承载情报操作的地图与多源数据底座。真正要补的是产品化的情报生产层。

优先级建议如下：

1. 先做 M6 的最小数据模型和 L1/L2/L3 对象。
2. 再做场景一，因为它能最大化复用现有 AIS/ADS-B/OSINT/correlation/AI pin 能力，也最适合 UAE 海事安全演示。
3. 随后做场景二，把 SAR AOI 扩展为持续监测任务。
4. 最后接真实影像订购平台和 AI 模型，把 demo 指标升级为可验收指标。

如果面向 UAE 做售前演示，建议首选“霍尔木兹海峡与富查伊拉港海事异常闭环”，其次是“关键能源设施连续变化监测”。这两个场景最贴近阿联酋的地缘、港口、能源和关键基础设施诉求，也最能体现 PRD 的 L1→L2→L3 价值。
