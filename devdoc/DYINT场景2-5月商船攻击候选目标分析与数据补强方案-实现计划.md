# DYINT 场景 2：2026 年 5 月商船安全事件数据包实现计划

计划日期：2026-07-10

计划状态：`READY_INTERNAL_WITH_CUSTOMER_GATES`

源文档：`devdoc/DYINT场景2-5月商船攻击候选目标分析与数据补强方案.md`

源文档类型：候选事件分析、推荐方案与数据补强路径的混合材料

源文档更新时间：2026-07-09 21:51:04 +0800

源文档所在目录：`devdoc/`

关联材料：

- `devdoc/DYINT场景2-3Demo数据规则与补强方案.md`
- `devdoc/DYINT场景2-3Demo数据规则与补强方案-售前演示方案评审报告.md`
- `devdoc/DYINT场景2-3Demo客户版演示脚本.md`
- `devdoc/DYINT场景2-6月10至12日霍尔木兹风险窗口目标包.md`

本计划只负责把已选定的 `UKMTO 062-26` 商船安全事件整理为可复现、可校验、可脱敏的离线 Demo 数据包和 6 张低保真演示画面。不修改 `gintbroker`、`doops-dev`、`moye-v4-product`，不接入生产数据，不输出攻击方判断、精确军事目标、武器推断或进攻性行动建议。

---

## 1. 背景、目标与完成口径

### 1.1 已确认目标

主事件固定为：

- 事件 ID：`SC2-20260526-MUSCAT-TANKER-ATTACK`
- 客户版名称：阿曼外海油轮安全事件后的航运风险验证
- 权威触发源：`UKMTO Warning 062-26`
- 后验汇总源：`JMIC Update 050`、`JMIC Update 058`
- 主时间：2026-05-26 09:45 UTC，以最终归档的 UKMTO 原文为准
- 主数据窗：2026-05-20 至 2026-05-28
- 客户动作：提升监测、二次确认、通知相关方、持续观察、报告归档

### 1.2 两级完成口径

本计划分为两个 Gate，不得把内部可用误报为客户可用：

| Gate | 完成条件 | 允许用途 |
| --- | --- | --- |
| `INTERNAL_READY` | 数据包可重复构建；验证矩阵通过；不确定性、样例数据和未授权素材均有明确标签；6 张低保真画面可离线走查 | 内部评审、产品/数据/售前彩排 |
| `CUSTOMER_READY` | `INTERNAL_READY` 已通过；正式 AOI 已审批；客户可见素材均有展示/截图许可；目标船和遥测已按规则匿名；主持人口径复审通过 | 客户现场演示、截图、录屏和报告样例 |

只完成 `INTERNAL_READY` 不等于整体完成。若客户 Gate 仍缺授权、正式 AOI 或外部核验，执行记录必须标记 `BLOCKED_CONFIRM`，不能写“已完成客户版”。

### 1.3 可交付成果

计划执行后应形成以下仓库内产物：

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
    index.html
    styles.css
    app.js
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

tools/sc2_20260526/
  README.md
  constants.py
  io_utils.py
  build_manifest.py
  build_aoi.py
  build_events.py
  build_ais.py
  build_adsb.py
  build_fusion.py
  render_storyboard.py
  validate_package.py

tests/sc2_20260526/
  test_manifest.py
  test_temporal_integrity.py
  test_telemetry_quality.py
  test_referential_integrity.py
  test_customer_gate.py
```

原始 CSV、Excel、PDF、商业数据、临时下载、未脱敏对象表和隔离记录不得提交到仓库，统一写入仓库根目录下未跟踪的 `.work/sc2_20260526/`。

### 1.4 非目标

- 不实现生产级采集、流处理、动态本体入图或规则下发。
- 不修改 `gintbroker` 页面或接口；运行系统集成需另立计划并现场核验代码。
- 不采购商业 AIS、SAR、天气或船舶登记数据。
- 不补全攻击方、武器类型、攻击路径或行动建议。
- 不把 5 月 22/23 日异地小型船只接近事件包装成 5 月 26 日主事件的已证实前兆。
- 不把样例 Excel 中的强身份名或演示轨迹当作客户事实。
- 不扩展到 2 月基线、4 月过渡或 6 月风险窗口的全量数据包；它们继续由相邻方案管理。

---

## 2. 当前事实、旧语义与材料缺口

### 2.1 计划编写时的仓库快照

| 项 | 当前事实 |
| --- | --- |
| 仓库 | `/Users/liushen/Documents/githubDevs/dy-inta` |
| 分支 | `main` |
| upstream | `origin/main` |
| ahead/behind | `ahead 4`，计划执行前必须重新确认 |
| 工作区 | 计划编写前干净；执行时以 T0 重新检查为准 |
| 现有代码 | 无 `demo_packages/`、无数据构建脚本、无自动校验器 |
| Python | Codex bundled Python 3.12.13；已探测 `pandas 2.2.3`、`openpyxl 3.1.5` |
| 外部盘 | 计划编写时可读；不能假设后续执行时仍挂载 |

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

### 2.4 材料缺口和 Gate

| 缺口 | 是否阻断 `INTERNAL_READY` | 是否阻断 `CUSTOMER_READY` | 处理方式 |
| --- | --- | --- | --- |
| UKMTO/JMIC 原文未归档、未记录 hash/`visible_at` | 是 | 是 | T1 重新获取；获取失败则 `BLOCKED_CONFIRM` |
| 正式事件 AOI 和港口进近区未审批 | 否，可用明确标注的粗 AOI 内部彩排 | 是 | T4 生成内部粗 AOI；正式 AOI 缺失时客户 Gate 必须失败 |
| 目标船 IMO/MMSI 未核验 | 否，使用“油轮 A” | 否，只要保持匿名且不声称已识别 | 候选身份与事实身份分栏，客户包强制匿名 |
| AIS/ADS-B 展示和截图许可未确认 | 否，只能内部 | 是 | `data_manifest.csv` 中默认 `display_allowed=false` |
| SAR/光学影像和天气海况缺失 | 否 | 否，前提是明确展示为二次确认任务而非已有证据 | 不生成伪影像，不把任务占位当事实 |
| 商业 AIS/船舶登记源缺失 | 否 | 否，前提是客户版不展示具体身份 | 列为 P1，不阻塞匿名版 |
| 客户版视觉风格或正式 UI 未提供 | 否 | 否 | 本计划仅交付无品牌、离线低保真 storyboard；正式 UI 另立计划 |

---

## 3. 推荐方案和数据契约

### 3.1 实现策略

采用“只读源数据、可重复派生、客户资产单独过 Gate”的离线方案：

1. 源数据只读，先生成文件清单、大小、修改时间和 SHA-256。
2. 公共事件、授权状态、AOI、遥测派生和融合结果分层落表，禁止一张 CSV 混合所有语义。
3. AIS/ADS-B 仅处理 5 月 20-28 日和三个粗 AOI；用分块读取控制资源，不扫描完整 2-6 月数据。
4. 同时输出 `raw_compatible` 与 `deduped` 统计，解释清洗对结果的影响。
5. 所有评分先过时间可见性检查；不能证明的“前兆”不强行制造上升曲线。
6. 客户资产仅消费 `display_allowed=true` 且已脱敏的数据；内部样例和原始标识不进入浏览器数据文件。
7. 低保真页面使用本地 HTML/CSS/JS，不依赖 CDN、远端字体、远程 API 或运行系统。

### 3.2 运行参数和路径约定

工具统一接受显式参数，不把个人绝对路径写死在提交文件中：

```bash
export PYTHON=/Users/liushen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
export AIS_FILE=/Volumes/exFAT466/海贝数据_2月1到6月15_AIS和ADS-B/AIS/event_vessel_route_202605.csv
export ADSB_ROOT=/Volumes/exFAT466/海贝数据_2月1到6月15_AIS和ADS-B/ADS-B/event_trajectory1_source_date_20260501_20260531
export SAMPLE_ROOT=/Users/liushen/Documents/非Coding工作/DYINT/O多源情报系统/样例数据
export OUTPUT_ROOT=demo_packages/sc2_20260526_muscat_tanker_attack
export WORK_ROOT=.work/sc2_20260526
```

每个新 shell 在执行阶段命令前都必须先执行上述变量块。若 bundled Python 路径不存在，停止为 `BLOCKED_CONFIRM`，不要未经验证切换到系统 Python 3.9。P0 只使用 Python 标准库、`pandas` 和 `openpyxl`，不在计划中引入 DuckDB、PyArrow、GeoPandas 或远端服务。

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
- 主去重键：非空 `IR_HKEY`；若缺失，候选键为 `IR_MMSI + IR_LASTTIME + IR_LAT + IR_LON + IR_SPEED`。
- 经纬度必须满足 `-90 <= lat <= 90`、`-180 <= lon <= 180`。
- 负速度、非数值速度不纠正为绝对值，改为空并打质量码。
- `IR_MMSI`、`IR_IMO`、船名只留在内部工作区；客户输出使用稳定匿名 ID。

ADS-B：

- 主时间字段：`source_date`；不得因为 `IR_LASTTIME` 为空而丢弃整日数据。
- 主去重键：非空 `id`；若重复或缺失，候选键为 `icao + source_date + lat + lon + alt + spd`。
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
| `score_timeline.csv` | `event_id`、`timestamp`、`score`、`level`、`evidence_refs`、`visible_at_max`、`quality_notes`、`not_yet_known`、`customer_action` |

`level` 枚举固定为 `background`、`elevated`、`event_response`、`monitoring`；若未来引入 `prepare_protective_action`，必须满足第 3.6 节的两类独立事前证据门槛并新增测试。禁止沿用客户敏感度更高的 `prepare_defense`。

---

## 4. 风险、防护和回滚

| 风险 | 影响 | 防护 | 验证 | 回滚/关闭方式 |
| --- | --- | --- | --- | --- |
| 事后信息泄露到事前评分 | Demo 被质疑为事后解释 | 时间字段分层、自动 temporal gate | `test_temporal_integrity.py` 必须全过 | 回退评分产物，修正证据分类后重建 |
| 脏数据被解释为异常行为 | 错误风险结论 | 原始值不改写，异常值隔离，质量码随记录输出 | 原始/清洗计数对账 | `git revert` 对应派生阶段 commit；原始文件不受影响 |
| 粗 AOI 被当成精确位置 | 客户误解、合规风险 | `geometry_status=rough_bbox`，客户 Gate 禁止 | `test_customer_gate.py` | 降级为内部画面，等待正式 polygon |
| 未核验船名/MMSI 泄露 | 错误归因、敏感信息泄露 | 客户表只用匿名 ID；身份候选独立分栏 | 客户产物字段白名单 | 删除客户构建产物并重建；不改原始数据 |
| 未授权素材进入截图 | 许可风险 | manifest 默认拒绝，截图前逐项 Gate | `display_allowed` 与 `screenshot_allowed` 校验 | 停止客户演示，替换为自生成低保真素材 |
| 大文件处理耗尽资源 | 长任务中断 | 按 200,000 行分块，只读所需列，只处理 9 天 | 记录 elapsed/RSS/chunk 数 | 降低 chunk；从阶段断点重跑，不重复前序 commit |
| 外部盘中途断开 | 结果不完整 | 构建前/后校验输入 hash 和文件大小 | inventory 对账 | 标记 `BLOCKED_CONFIRM`，重新挂载后从当前阶段继续 |
| 低保真页面误导为已上线能力 | 过度承诺 | 页面固定“离线 Demo/数据包版本/能力边界” | 彩排逐页检查 | 关闭客户 Gate，修订主持稿和水印 |
| 安全叙事越界 | 方案被理解为行动辅助 | 禁止词检查 + 人工售前复审 | 客户文案扫描与彩排 | 移除越界内容，重新评审，不带病演示 |

本计划无数据库写入、生产环境写入、push、CI/Jenkins/K8S、JIRA 状态变更。若后续新增这些动作，必须另立阶段并由用户当前轮明确授权。

---

## 5. 具体实施计划

### T0：执行准备、断点恢复和输入盘点

目标：

- 确认当前分支、工作区、upstream、未推送提交和输入可读性。
- 创建执行记录，但不修改原始数据。
- 判断从 T0 开始还是从已完成阶段继续。

输入：

- 本计划。
- 源文档及第 2.2 节列出的本地输入。

修改范围：

- 只允许更新本计划第 8.2 节执行记录；若只是盘点且无状态变化，不提交。

步骤：

1. 完整读取本计划和执行记录，找出最后一个 `DONE_LOCAL` 阶段及其 commit。
2. 运行 Git 检查；如果有无关改动、已有暂存内容或无法隔离的用户文件，停止，不得覆盖。
3. 检查 bundled Python、AIS、ADS-B 5 月 20-28 日文件、3 个 Excel 和地理知识库。
4. 检查磁盘剩余空间；`.work/` 和输出目录合计预留至少 2GB。若后续选择保留公共源 PDF，再额外预留 500MB。
5. 确认 `.gitignore` 已排除 `.work/`、`.env.local`、原始下载和未脱敏临时文件；若缺失，在 T1 作为本计划的非纯文档变更处理。
6. 记录输入文件大小、mtime、SHA-256；对 ADS-B 只记录 5 月 20-28 日 9 个有效文件，忽略 `._*`。
7. 若执行记录已有阶段，验证对应 commit 仍在当前分支且工作区与记录一致；一致则从下一阶段继续，不重复生成已完成阶段。

验证：

```bash
git status --short --branch
git branch --show-current
git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}'
git log --oneline '@{upstream}..HEAD'
test -x /Users/liushen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
test -r /Volumes/exFAT466/海贝数据_2月1到6月15_AIS和ADS-B/AIS/event_vessel_route_202605.csv
find /Volumes/exFAT466/海贝数据_2月1到6月15_AIS和ADS-B/ADS-B/event_trajectory1_source_date_20260501_20260531 \
  -maxdepth 1 -type f -name 'system_event_trajectory1_2026052[0-8].csv' | sort
df -h . /Volumes/exFAT466
```

预期结果：

- Git 状态可解释且可隔离本轮文件。
- Python 3.12.13 或经验证的同等 bundled runtime 可用。
- AIS 1 个文件和 ADS-B 9 个日文件可读。
- 没有把 `._*.csv` 算作有效输入。

暂停条件：

- 存在用户无关改动或不明暂存内容。
- 当前分支、upstream 或 ahead/behind 与执行记录冲突。
- 外部盘未挂载、输入文件缺失或 hash 在同一阶段内变化。
- 空间不足或 Python 依赖缺失。

提交与记录：

- T0 默认只读，不提交。
- 更新执行记录中的输入 hash 摘要、分支、起点 commit 和下一阶段。

### T1：冻结数据包骨架、字段契约和来源清单

目标：

- 建立目录、字段说明和来源归档规则。
- 重新核验 UKMTO/JMIC 原文，避免把源文档摘要直接当机器事实。

输入：

- T0 输入盘点和文件 hash。
- 源文档中的公开来源 URL、事件定义和客户边界。
- 相邻方案的 manifest、时间字段和客户门禁契约。

修改范围：

- `demo_packages/sc2_20260526_muscat_tanker_attack/README.md`
- `00_manifest/*`
- `tools/sc2_20260526/README.md`
- 必要时 `.gitignore`

步骤：

1. 创建第 1.3 节目录骨架，只提交允许进仓库的空模板和说明，不提交原始文件。
2. `target_definition.csv` 冻结事件 ID、时间窗、粗 AOI、客户名称、内部名称、被保护对象、允许/禁止结论和版本。
3. `source_manifest.csv` 最低字段：`source_id`、`source_type`、`source_owner`、`source_url_or_path_template`、`retrieved_at`、`sha256`、`event_time`、`visible_at`、`known_after_time`、`time_precision`、`license`、`display_allowed`、`screenshot_allowed`、`quality_note`。
4. 将源文档列出的 UKMTO/JMIC URL 重新获取到 `.work/sc2_20260526/raw_sources/`；记录 HTTP 状态、最终 URL、获取时间、文件 hash 和原文标题。
5. 人工核对 `Warning 062-26` 是否明确提供事件时间、位置精度、船型、安全状态和环境影响；只把原文明确内容写入表。
6. JMIC、gCaptain 和 5 月 28 日媒体按 `official_maritime`、`maritime_summary`、`media_enrichment`、`single_party_claim` 分类。
7. 无法证明最早公开时间时，`visible_at` 留空并说明；不得用当前下载时间回填历史可见时间。
8. `data_manifest.csv` 所有素材默认 `display_allowed=false`、`screenshot_allowed=false`，只有明确许可后逐项升级。

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

- `tools/sc2_20260526/io_utils.py`
- `tools/sc2_20260526/validate_package.py`
- `tests/sc2_20260526/test_*.py`
- `06_validation/validation_report.md` 模板

步骤：

1. 使用 Python 标准库 `unittest`，不新增 pytest 依赖。
2. 为每个 CSV 固定必需列、枚举值、日期格式、空值规则和主键唯一性。
3. 实现跨表引用校验：`source_ref`、`evidence_ref`、`aoi_id`、`asset_id` 必须能回到对应主表。
4. 实现 temporal gate：参与某一评分点的证据必须满足 `visible_at <= scoring_time`；空 `visible_at` 不得参与。
5. 实现 customer gate：客户资产只能引用 `display_allowed=true`；截图只能引用 `screenshot_allowed=true`；`rough_bbox` 不得在客户模式伪装成批准 AOI。
6. 实现客户字段白名单：客户 JSON/HTML 数据不得包含 MMSI、IMO、ICAO、呼号、未核验船名、原始绝对路径。
7. 实现安全文案检查，重点审查“推荐打击”“精确坐标”“武器发射点”“攻击路线”“拦截并反制”“目标优先级”等行动性表达；事件事实中的“攻击/外部爆炸”可存在，但不能转成行动建议。
8. 测试先使用最小 fixture，不读取 370MB 原始文件。

验证：

```bash
PYTHON=/Users/liushen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
$PYTHON -m unittest discover -s tests/sc2_20260526 -p 'test_*.py' -v
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

1. 使用 `pandas.read_csv(..., chunksize=200_000, usecols=[...])`，编码先尝试 `utf-8-sig`；禁止整表载入。
2. 只读取 `IR_LASTTIME`、`IR_LOADTIME`、`IR_NAME`、`IR_DESTINATION`、`IR_SPEED`、`IR_NAVIGATION_STATUS`、`IR_IMO`、`IR_MMSI`、`IR_LAT`、`IR_LON`、`IR_HKEY`、`SOURCE`。
3. 先生成 `raw_compatible` 统计，严格按有效 `IR_LASTTIME` 日期和 bbox 过滤，复现源文档计数。
4. 再按第 3.5 节生成 `deduped` 统计；不得用去重后的值覆盖原始口径。
5. 统计每个日期/AOI 的行数、唯一 MMSI 数、缺失身份数、缺失/越界坐标数、负速度数、去重删除数、低速/等待候选数和时间回退数。
6. `nearby_vessel_candidates.csv` 只保留匿名 ID、日期、AOI、速度区间、导航状态类别、目的港类别、质量说明；不得提交原始 MMSI/IMO/船名/精确轨迹。
7. 内部原始 ID 到匿名 ID 的映射只写 `.work/`，不得提交。
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

1. 只枚举 `system_event_trajectory1_YYYYMMDD.csv`，显式排除 `._*`。
2. 使用 `source_date` 作为主时间；读取 `id`、`icao`、`reg`、`type`、`spd`、`alt`、`lon`、`lat`、`call`、`mil`、`source_date`、`IR_LASTTIME`、`IR_LOADTIME`。
3. 分别输出 `raw_compatible` 和 `deduped` 口径。
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
3. `score_timeline.csv` 同时输出 `score`、`level`、`evidence_refs`、`visible_at_max`、`quality_notes`、`not_yet_known`。
4. 先执行 temporal gate，再计算分数；测试中要证明后验 JMIC 和 5 月 28 日主张无法进入 5 月 26 日前评分。
5. 如果同 AOI 事前证据不足，按第 3.6 节保留背景/证据不足，5 月 26 日进入“事件响应与二次确认”，不要称为提前预测。
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

### T8：生成离线低保真演示资产

目标：

- 用冻结数据包生成 6 张固定画面和保护性报告，支撑 8-12 分钟内部走查。

输入：

- T7 已通过内部 Gate 的证据、时间线、任务和报告数据。
- `devdoc/DYINT场景2-3Demo客户版演示脚本.md`。
- T1 `data_manifest.csv` 和 T4 AOI 精度状态。

修改范围：

- `tools/sc2_20260526/render_storyboard.py`
- `05_customer_assets/*`
- 前端静态资源和截图

步骤：

1. 使用原生 HTML/CSS/JS，无框架、无 CDN、无外部字体、无远程请求。
2. 6 个画面固定为：客户压力、事件定义、风险时间线、AOI 地图、证据矩阵、二次确认与保护性报告。
3. 页面顶部固定显示 `Offline Demo`、包版本、Gate 状态、数据窗和“非生产系统”。
4. AOI 地图若仍是 bbox，画面明确显示“粗筛选范围”，不得出现假精确爆炸点。
5. 客户模式只加载经过 customer gate 的匿名 JSON；内部模式允许展示质量缺口，但仍不得加载原始 ID。
6. 状态矩阵至少覆盖：正常内部演示、身份未知、来源冲突、遥测稀疏、正式 AOI 未批准、素材未授权。
7. 交互仅包括步骤导航、证据状态筛选和报告打印；键盘可操作，颜色之外再用文字/图标表达支持、反驳、待确认。
8. 生成 6 张截图并写 `screen_manifest.csv`；截图只使用自生成图形和允许展示的文字/数据。

视口矩阵：

| 视口 | 用途 | 通过标准 |
| --- | --- | --- |
| 1920x1080 | 会议室主屏 | 6 个画面无需缩放，关键信息不溢出 |
| 1440x900 | 笔记本彩排 | 主要内容首屏可读，导航和状态标签完整 |
| 390x844 | 移动 smoke | 不要求正式演示体验，但不得重叠、泄露隐藏数据或无限横向滚动 |

允许变化范围：

- 可调整布局、字号、颜色和图表形式以提高可读性。
- 不得改变事实状态、证据等级、时间可见性、授权状态和安全边界。
- 不得用素材图、军事图标或视觉特效制造未被证据支持的行动氛围。

验证：

```bash
PYTHON=/Users/liushen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
$PYTHON tools/sc2_20260526/render_storyboard.py \
  --package "$OUTPUT_ROOT" --mode internal
$PYTHON -m http.server 8765 --directory "$OUTPUT_ROOT/05_customer_assets"
```

浏览器验证必须完成：

- 逐页截图 1920x1080 和 1440x900；移动视口做 smoke。
- Console 无 error；Network 无远端请求、404 或隐式数据外传。
- HTML 源和浏览器数据中无 MMSI、IMO、ICAO、呼号、个人绝对路径和未核验船名。
- 客户模式在客户 Gate 未通过时必须显示阻断页，不能静默降级为可演示。

暂停条件：

- 需要使用未授权图片、远程地图瓦片或客户未批准的品牌素材。
- 客户模式绕过 Gate 才能显示完整内容。
- 浏览器发现原始 ID、敏感路径或远程请求。

提交与记录：

- 浏览器和自动验证通过后本地提交：`feat(sc2): 生成商船安全事件低保真演示资产`。
- 记录截图、视口、Console/Network 结果和 commit；不 push。

### T9：整体验收、确定性复跑和内部彩排

目标：

- 从干净输出目录完整重建一次，证明结果可重复，并判定两个 Gate。

输入：

- T1-T8 的本地 commit、构建脚本、数据包和阶段验证记录。
- 已取得的 AOI 审批、展示许可和截图许可；缺失项按客户 Gate 阻断处理。
- 6 张低保真画面和主持稿。

修改范围：

- `06_validation/*`
- `README.md`、`protective_report.md`、`presenter_script.md`
- 本计划执行记录

步骤：

1. 保留原始输入不动，将旧生成目录重命名到 `.work/previous_build/`；不得删除未知文件。
2. 按 T1-T8 命令完整重建。
3. 对两次构建的稳定输出计算 SHA-256；允许 `retrieved_at`、构建时间和执行日志不同，但业务 CSV、GeoJSON、HTML 数据应一致。
4. 运行全部单测、内部校验和客户校验。
5. 客户校验预期可能因正式 AOI/授权失败；失败必须列出精确 Gate，不得把它当代码失败，也不得冒进放行。
6. 由非技术同事或独立评审者按 6 张画面做一次 8-12 分钟彩排，记录是否能复述“谁承压、系统改变什么动作、输出什么任务/报告”。
7. 使用 `presales-demo-review` 对完成资产做轻量复审，重点检查客户共鸣、证据闭环、授权和高敏术语；该复审是客户 Gate 的输入，不代替自动验证。
8. 更新 `validation_report.md` 和执行记录，列出通过项、阻断项、未验证假设和后续负责人。

验证：

```bash
PYTHON=/Users/liushen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
$PYTHON -m unittest discover -s tests/sc2_20260526 -p 'test_*.py' -v
$PYTHON tools/sc2_20260526/validate_package.py --package "$OUTPUT_ROOT" --mode internal
$PYTHON tools/sc2_20260526/validate_package.py --package "$OUTPUT_ROOT" --mode customer
$PYTHON tools/sc2_20260526/validate_package.py \
  --package "$OUTPUT_ROOT" \
  --write-stable-checksums "$OUTPUT_ROOT/06_validation/output_checksums.sha256"
git diff --check
```

稳定 checksum 只覆盖业务 CSV、GeoJSON、HTML/CSS/JS 和报告正文；排除构建时间、`retrieved_at`、执行日志、验证报告和浏览器截图等环境相关产物。被排除字段仍需做 schema 和内容 Gate，不得因排除 checksum 而跳过验证。

合并策略：

- 单测、schema、引用、时间和安全文案可在同一轮 `unittest + validate_package` 中合并验证。
- 6 张画面的视口、Console、Network 和主持人口径可在同一轮浏览器彩排中合并。
- `internal` 与 `customer` Gate 不能合并：前者允许明确标注的内部素材，后者必须严格拒绝未授权和粗 AOI。
- 原始口径和去重口径不能合并成一列；两者用于不同判断，必须分别验收。

暂停条件：

- 任一自动测试失败。
- 两次构建的稳定产物不一致且无可解释的非确定字段。
- 内部 Gate 未通过。
- 客户 Gate 被绕过、误标通过或缺少责任人确认。
- 彩排出现越界表述或无法解释某次评分变化。

提交与记录：

- `INTERNAL_READY` 全部通过后本地提交：`test(sc2): 完成商船安全事件包内部验收`。
- 若客户 Gate 也通过，可追加单一职责提交：`docs(sc2): 完成商船安全Demo客户门禁`。
- 未通过客户 Gate 时只记录 `BLOCKED_CONFIRM`，不提交“客户门禁完成”信息。
- 全程不 push。

### T10：收口复核

目标：

- 确认 Git、文档、执行记录和未处理事项一致，防止长任务完成一部分就提前结束。

输入：

- T0-T9 执行记录、commit、自动验证报告和彩排结论。
- 当前 Git 分支、upstream、工作区和未推送提交。

修改范围：

- 本计划第 8.2 节执行记录。
- `06_validation/validation_report.md` 的最终 Gate 状态。
- 不默认修改源分析文档或相邻方案。

步骤：

1. 核对每个阶段的状态、commit、验证证据和剩余 Gate。
2. 核对 `git status --short` 只剩已知文件；不得提交 `.work/`、原始数据或无关改动。
3. 核对所有本地 commit 均为单一职责且未 push。
4. 更新源文档中的推进状态只在用户另有要求时进行；本计划不默认改写源分析结论。
5. 输出最终状态：`INTERNAL_READY`、`CUSTOMER_READY` 或 `BLOCKED_CONFIRM`，不得只写“脚本已完成”。

验证：

```bash
git status --short --branch
git log --oneline '@{upstream}..HEAD'
git diff --check
```

暂停条件：

- 有未解释变更、未记录 commit、失败测试或缺少 Gate 证据。

提交与记录：

- 若只更新本计划执行记录，按纯文档规则检查并本地提交：`docs(sc2): 收口5月商船安全事件包执行记录`。
- 不 push。

---

## 6. 验证矩阵

| ID | 验证层 | 覆盖点 | 样本/命令 | 通过标准 | 失败处理 |
| --- | --- | --- | --- | --- | --- |
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
| V11 | 视觉 | 6 画面、3 视口、状态矩阵 | 浏览器截图 | 不溢出、不遮挡、状态可读 | 回到 T8 |
| V12 | 浏览器 | Console、Network、远程依赖 | DevTools | 0 error、0 远程请求、0 404 | 阻断提交 |
| V13 | 安全文案 | 非进攻性叙事 | 自动扫描 + 人工复审 | 只有航运安全、复核、监测、报告动作 | 删除越界内容并复审 |
| V14 | 性能/资源 | 分块读取、耗时、峰值内存 | T5/T6 日志 | RSS < 2GB；无整表扫描 | 降低 chunk，从断点重跑 |
| V15 | 确定性 | 两次构建稳定输出 hash | T9 checksums | 业务产物一致 | 定位非确定字段后重建 |
| V16 | 演示闭环 | 8-12 分钟、非技术复述 | 内部彩排 | 能复述压力、动作、输出；每次升级可追溯 | 回到 T7/T8 |

### 6.1 验证样本选择

- 正例：`UKMTO 062-26`、5 月 26 日 AIS/ADS-B 主 AOI 摘要。
- 时间负例：JMIC 后验确认、5 月 28 日媒体主张尝试进入 5 月 26 日前评分，必须失败。
- 授权负例：`display_allowed=false` 的样例数据尝试进入客户 HTML，必须失败。
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
| AIS/ADS-B | `DUPLICATE_PRIMARY` / `DUPLICATE_FALLBACK` | 原始口径保留，去重口径只保留一条并记录数量 |
| 样例 | `SAMPLE_IDENTITY_UNVERIFIED` | 仅内部方法演示，客户 Gate 强制拒绝 |
| 来源 | `VISIBLE_AT_UNKNOWN` | 不参与历史时点评分 |

### 7.3 隔离记录

异常明细写入 `.work/sc2_20260526/quarantine/`，只保留：

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
- 清理 `.work/` 或外接盘上的原始/临时文件。

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
| T0 | `NOT_STARTED` | - | - | - | 重新检查分支、输入和空间 | - |
| T1 | `NOT_STARTED` | - | - | - | 来源与契约 | - |
| T2 | `NOT_STARTED` | - | - | - | 自动校验门禁 | - |
| T3 | `NOT_STARTED` | - | - | - | 事件与来源表 | - |
| T4 | `NOT_STARTED` | - | - | - | AOI 与客户 Gate | - |
| T5 | `NOT_STARTED` | - | - | - | AIS 派生表 | - |
| T6 | `NOT_STARTED` | - | - | - | ADS-B 派生表 | - |
| T7 | `NOT_STARTED` | - | - | - | 证据矩阵与时间线 | - |
| T8 | `NOT_STARTED` | - | - | - | 低保真画面 | - |
| T9 | `NOT_STARTED` | - | - | - | 总验收与彩排 | - |
| T10 | `NOT_STARTED` | - | - | - | 收口复核 | - |

### 8.3 必须继续条件

只要总目标未完成，且没有以下停止条件，完成当前小批后必须立即更新记录并继续下一阶段，不得因“已生成一个 CSV”“已跑一次脚本”或“内部页面能打开”就输出最终答复停止：

- `BLOCKED_CONFIRM`；
- 测试、构建或数据对账失败且无法在当前阶段定位；
- Git 冲突、无关脏文件或暂存范围无法隔离；
- 需要客户授权、正式 AOI 审批、生产/外部系统写操作；
- 输入 hash 变化或外接盘断开。

### 8.4 断点恢复

1. 先读本表，定位最后一个 `DONE_LOCAL`。
2. 验证阶段 commit 存在且 `git status` 可解释。
3. 运行该阶段的最小 smoke 验证，不重新执行早期大文件处理。
4. 从下一阶段继续；若 smoke 失败，将原阶段改为 `FAILED`，回到该阶段修复。
5. 不使用 `reset --hard`、`clean`、amend 或 rebase 恢复断点；需要撤销已提交阶段时使用新的 `git revert`，并由用户确认撤销范围。

---

## 9. Git、发布和记录要求

本计划执行会产生 Python、测试、HTML/CSS/JS、CSV/GeoJSON 和文档，属于非纯文档变更。每个阶段必须完成直接相关验证后才能本地提交。

每次提交前：

```bash
git status --short
git diff --check
git diff --cached --check
git diff --cached --stat
```

规则：

- 只暂存本阶段文件，不混入用户或其他任务改动。
- 每个 commit 单一职责，记录短 hash 到第 8 节。
- 测试未运行、失败或输入对账未完成时不自动 commit。
- 不 push；本计划不包含 CI、Jenkins、K8S、JIRA 或生产环境操作。
- 不提交 `.work/`、原始数据、未脱敏映射、访问凭据、cookie、下载缓存或未授权素材。
- 若当前 `main` 的 ahead/behind 在执行期间变化，先停止并重新判断，不自动 pull/rebase。

---

## 10. 暂不处理事项、未验证假设与后续建议

### 10.1 暂不处理

- 商业 AIS/船舶登记、SAR/光学影像、天气海况、港口 ETA、污染和保险数据采购。
- 生产级数据中台接入、动态本体入图、规则 DSL、流式告警和自动报告分发。
- `gintbroker` 真实 UI 集成、权限、接口和部署。
- 2 月基线、4 月过渡、6 月风险窗口的完整复用和联动评分。
- 面向特定攻击方、武器、军事部署或行动路线的分析。

### 10.2 未验证假设

- UKMTO/JMIC URL 在执行时仍可访问，且原文元数据足以支持 `visible_at`。
- 海贝 AIS/ADS-B 的内部处理、衍生统计和客户截图许可可以分别获得明确判断。
- 三个粗 AOI 能满足内部方法演示，但不能自动满足客户地图要求。
- bundled Python 3.12 和当前 `pandas/openpyxl` 在执行期间仍可用。
- 目标船保持匿名不会削弱客户故事的核心价值。

### 10.3 后续建议

1. 先完成 `INTERNAL_READY`，用真实数据对账决定 5 月事件是否确实比 6 月窗口更适合主 Demo。
2. 客户 Gate 缺少正式 AOI 或授权时，优先补这两项，不要先做运行系统集成。
3. 若低保真资产和数据包通过售前复审，再对 `gintbroker` 做只读能力盘点，并另写 UI/API 集成计划。
4. 若客户明确要求实时能力，再按 `moye-v4-product` 数据接入、`doops-dev` 规则/证据治理、`gintbroker` 运行面分别拆计划，不能把三个系统合成一个大改造任务。

---

## 11. 后续执行入口

后续执行时直接使用：

[$checkpointed-plan-executor](/Users/liushen/Documents/cursorDevs/trsdevops/devops_console/.agents/skills/checkpointed-plan-executor/SKILL.md) `/Users/liushen/Documents/githubDevs/dy-inta/devdoc/DYINT场景2-5月商船攻击候选目标分析与数据补强方案-实现计划.md`
