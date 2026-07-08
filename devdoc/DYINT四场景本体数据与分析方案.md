# DYINT 四场景多源情报演示：场景微调、本体、数据与分析方案

> 来源文档：钉钉文档 `DYINT-Demo`，节点 `b9Y4gmKWrdgOmQNdC43lQN6dJGXn6lpz`
>
> 关联材料：`/Users/liushen/Documents/githubDevs/dy-inta/PRD-v6.md`
>
> 关联分析：`/Users/liushen/Documents/githubDevs/dy-inta/devdoc/PRD-v6-当前项目适配分析与UAE场景.md`
>
> 被评估项目：`/Users/liushen/Documents/cursorDevs/gintbroker`
>
> 分析日期：2026-07-07

## 1. 总体判断

钉钉文档提出的 4 个演示事件包方向是合适的，尤其适合面向阿联酋或海湾地区客户展示。它们共同避开了“进攻型军事打击系统”的敏感叙事，转向“海上交通保护、关键基础设施韧性、开源情报（Open Source Intelligence，简称 OSINT）降噪、多源交叉验证、误判降级”的防御型价值。这一点非常重要。

但这 4 个场景不能简单并列成 4 条互不相干的演示。它们之间有明显重叠：

- 场景 1“霍尔木兹/阿曼湾商船安全”天然会用到场景 4 的全球导航卫星系统（Global Navigation Satellite System，简称 GNSS）和船舶自动识别系统（Automatic Identification System，简称 AIS）干扰证据。
- 场景 2“商船袭击预警与区域防卫准备”与场景 3“能源关键设施损伤/恢复监测”会共享同一批设施关注区（Area of Interest，简称 AOI）、火点、影像、官方通告和开源情报。
- 四个场景都需要同一套一级异常预警（L1）、二级验证确认（L2）、三级融合报告（L3）、证据链、置信度、关注区、资产对象和关系本体。

因此推荐的工程策略是：保留 4 个场景包用于销售和叙事，但底层只建设一套统一的“事件、资产、组织、服务、证据、影像、验证、报告”本体。演示编排上优先做两条主线：

1. **主线 A：海上通道安全**，把场景 1 和场景 4 合并演示。
2. **主线 B：袭击预警与能源设施防护**，把场景 2 的商船/区域袭击预警和场景 3 的能源关键设施损伤/恢复监测串起来演示。

这样既能覆盖钉钉文档中的 4 个主题，又不会把工程团队拖进 4 套重复的数据管道和 4 套重复页面。

### 1.1 术语使用约定

本文后续尽量使用中文名。第一次出现关键英文术语时给出中英文对照；后续如果不是代码字段、官方数据源名、接口路径或对象标识符，原则上只使用中文名。

| 中文名 | 英文名或缩写 | 说明 |
| --- | --- | --- |
| 演示 | Demo | 面向客户的可控场景包，不等于生产系统全量能力 |
| 开源情报 | Open Source Intelligence, OSINT | 新闻、通告、社媒、公开数据库、公开遥感等公开来源情报 |
| 关注区 | Area of Interest, AOI | 需要监测或分析的空间区域，可以是海域、航道、港口、设施或机场 |
| 一级异常预警 | L1 anomaly warning | 从多源数据中发现异常并形成线索卡 |
| 二级验证确认 | L2 verification | 用遥感、权威通告、历史基线或其他来源验证一级线索 |
| 三级融合报告 | L3 fusion report | 汇总多源证据、置信度、判断和建议的决策报告 |
| 线索卡 | Lead card | 一级异常预警的结构化工作对象 |
| 证据链 | Evidence chain | 从原始来源、观测、异常、验证到结论的可追溯链路 |
| 验证矩阵 | Verification matrix | 对每条主张逐项标注支持、反驳、矛盾、待确认的表格 |
| 船舶自动识别系统 | Automatic Identification System, AIS | 船舶广播位置、航向、航速、身份等信息的系统 |
| 广播式自动相关监视 | Automatic Dependent Surveillance-Broadcast, ADS-B | 航空器广播位置和导航质量等信息的系统 |
| 全球导航卫星系统 | Global Navigation Satellite System, GNSS | GPS、GLONASS、Galileo、北斗等导航卫星系统统称 |
| 射频 | Radio Frequency, RF | 与无线电、导航干扰、信号环境相关的数据域 |
| 合成孔径雷达 | Synthetic Aperture Radar, SAR | 可穿透云雨和夜间成像的雷达卫星传感器 |
| 交通分离制 | Traffic Separation Scheme, TSS | 海上分道通航制度 |
| 火灾信息资源管理系统 | Fire Information for Resource Management System, FIRMS | NASA 火点与热异常数据服务 |
| 可见光红外成像辐射仪套件 | Visible Infrared Imaging Radiometer Suite, VIIRS | 常用于火点/热异常检测的卫星载荷 |
| 英国海上贸易行动办公室 | United Kingdom Maritime Trade Operations, UKMTO | 海上安全通告来源 |
| 联合海事信息中心 | Joint Maritime Information Center, JMIC | 海事安全态势与通告来源 |
| 航行警告区 | NAVAREA | 国际航行警告区域体系 |
| 武装冲突地点与事件数据项目 | Armed Conflict Location & Event Data Project, ACLED | 结构化冲突事件数据源 |
| 全球事件语言与语调数据库 | Global Database of Events, Language, and Tone, GDELT | 全球新闻事件数据库 |
| 航行通告 | Notice to Air Missions, NOTAM | 航空运行限制、机场状态、空域变化等通告 |

## 2. 四个场景是否合适，以及建议微调

### 2.1 场景适配总表

| 场景 | 原始定位 | 是否合适 | 主要价值 | 主要问题 | 建议微调 |
| --- | --- | --- | --- | --- | --- |
| 1. 霍尔木兹海峡 / 阿曼湾商船安全事件包 | 商船异常、航线偏离、船舶识别静默、近失事件、通行风险报告 | 很合适，应作为第一主场景 | 阿联酋高度依赖海上能源和贸易通道；非进攻型；数据可得性相对好；地图表现力强 | 与场景 4 重叠；如果只讲“商船遇袭”，容易变成新闻回放 | 改成“海上通道安全与风险降级”：突出通航安全、保险/港口/民防联动、误判降级 |
| 2. 5-6 月商船被袭/海峡摩擦预警包 | AIS 信号静默、坐标异常、快艇接近、航母/战机/无人机动向、新闻报道、风险评分 | 合适，但必须收边界 | 能展示“新闻结果反推预警模型”：用历史已知事件验证系统能否在袭击前形成防卫准备信号 | 容易被误解为精确预测或进攻性军事研判；实时采集不稳定 | 改成“商船袭击预警与区域防卫准备”：只输出风险上升、防卫准备、二次确认任务和非进攻建议 |
| 3. 能源关键设施损伤 / 恢复监测包 | 能源设施受损、恢复进度、供应链影响、连续监测 | 很合适，应作为第二主线的补充演示 | 最贴近阿联酋真实安全利益：炼厂、油库、LNG、港口能源码头、电力/海水淡化综合体 | 需要高质量设施边界和多时相影像；当前样例影像不是能源设施损伤样例 | 改成“能源关键设施监测”：从战损叙事转为损伤、恢复、替代能力和服务连续性 |
| 4. 导航/船舶识别干扰与航运安全包 | 船舶识别位置跳变、航空监视质量下降、GPSJam、雷达卫星核验真实船位 | 合适，但不宜作为完全独立主线 | 很能体现多源融合和射频/导航能力；防御叙事强 | 与场景 1 高度重合；公开导航干扰数据多来自航空侧，对海上船舶识别干扰需要补充证据 | 改成“导航完整性诊断能力包”：作为场景 1 的关键证据链，也可单独给技术评审演示 |

### 2.2 是否有必要微调

有必要。原因不是原场景错，而是演示面向阿联酋客户时需要更精确地控制价值叙事、敏感边界和工程可实现性。

第一，阿联酋客户更容易被“民用基础设施韧性、海上通道安全、误判降级、连续监测”打动，而不是被“某次袭击复盘”本身打动。演示应该回答决策者的实际问题：

- 海峡或港口现在还能不能安全通行？
- 哪些传闻是真的，哪些还没有证据？
- 哪些能源、港口、机场、海水淡化设施受影响？
- 损伤有没有扩大？恢复是否真实发生？
- 是否需要发布航行安全提示、调整港口调度、提高民防准备或继续监测？

第二，四个场景的技术底座高度复用。若不微调，会出现工程重复：

- 场景 1 和 4 都要船舶自动识别、导航干扰、雷达卫星、航道和船舶异常本体。
- 场景 2 和 3 都要开源情报、结构化事件/新闻、火点、卫星影像、设施关注区和损伤评估本体；其中场景 2 的主目标是袭击预警，信息降噪只是避免误报的支撑能力。
- 四个场景都要证据链、置信度、验证矩阵和报告模板。

第三，场景 2 最容易产生合规风险。必须明确做“历史已知事件回放下的风险上升验证和防卫准备”，不能承诺精确预测或展示：

- 精确军事部署坐标。
- 武器发射点推断。
- 实时打击目标识别。
- 进攻性行动建议。

### 2.3 推荐后的四个演示包

| 推荐演示包 | 对应原场景 | 面向客户的说法 | 工程上的主线 |
| --- | --- | --- | --- |
| A. 海上通道安全与航运风险降级 | 场景 1 | 保护霍尔木兹、阿曼湾和阿拉伯湾通航安全，降低商船误判和事故风险 | 海事本体、船舶自动识别历史基线、英国海上贸易行动办公室/联合海事信息中心通告、合成孔径雷达验证 |
| B. 导航完整性诊断与真实位置核验 | 场景 4 | 识别导航干扰对航运和航空安全的影响 | 射频/导航异常本体、船舶和航空位置质量、雷达卫星真实位置核验 |
| C. 商船袭击预警与区域防卫准备 | 场景 2 | 基于 5-6 月历史已知事件回放，从 AIS/ADS-B、航母/战机动向和新闻主张中识别袭击风险上升 | 事件本体、威胁信号、AIS/ADS-B 异常、航母/战机动态、新闻主张、预警评分 |
| D. 能源关键设施损伤与恢复监测 | 场景 3 | 持续监测炼厂、油库、LNG、港口能源码头、电力/海水淡化综合体的损伤与恢复 | 设施本体、组件边界、多时相影像、火点/热异常、运营活动指标 |

## 3. 四个场景共同需要的本体

这里的“本体”不是简单的对象表或标签表。面向情报分析，它至少应包含 5 层内容：

1. **对象层**：有哪些船舶、航空器、设施、组织、航线、事件、观测、影像、报告、任务。
2. **关系层**：对象之间如何关联，例如位于、邻近、影响、依赖、支持、反驳、触发、生成。
3. **规则层**：什么情况下构成异常、什么证据能提高或降低置信度、什么条件触发二级验证或三级报告。
4. **动作层**：系统或分析师可以做什么，例如创建线索卡、请求影像、合并事件、降级传闻、生成报告、转持续监测。
5. **推理层**：基于对象、关系、规则和动作，自动生成候选事件、影响范围、证据状态、置信度变化和下一步建议。

所以，本体要支撑的是“情报生产语义图谱”，而不是“数据库表名清单”。它至少要回答 8 个问题：

1. 发生了什么事件？
2. 涉及哪些船舶、航空器、设施、组织、航线和关注区？
3. 哪些观测或证据支持这个事件？
4. 哪些证据互相印证、互相矛盾或还无法判断？
5. 置信度为什么上升或下降？
6. 事件影响了哪些航道、港口、机场、设施或服务？
7. 系统下一步应该自动做什么，哪些动作必须交给分析师确认？
8. 最终能生成什么报告和持续监测任务？

### 3.1 基于本体能不能自动推理

能，但要讲清楚边界。

如果本体、关系和规则设计得足够完整，系统可以自动推理出很多“候选判断”和“工作流动作”，例如：

- 从“船舶自动识别静默 + 海事通告 + 航道关注区重合”推理出“可能的海上通道风险线索”。
- 从“火点/热异常 + 设施关注区重合 + 新闻声称爆炸”推理出“某设施可能受影响，需要二级影像验证”。
- 从“同一时间窗内航空位置质量下降 + 船舶位置跳点 + 公开导航干扰图重合”推理出“导航完整性异常事件”。
- 从“多条开源情报主张同一地点，但影像和官方通告均不支持”推理出“传闻待确认或降级”。
- 从“受损设施与港口/机场/电力/海水淡化依赖关系”推理出“潜在民用服务影响范围”。
- 从“一级线索达到阈值，但缺遥感证据”推理出“建议请求二级验证”。
- 从“三级报告完成且风险仍高”推理出“建议转持续监测任务”。

但本体推理不是“自动知道真相”。它有 4 个硬边界：

- **缺数据不能硬推理**：没有历史基线，就不能严肃判断“异常”；没有遥感或权威来源，就不能把单源传闻升级成确认事件。
- **证据冲突不能自动裁决为事实**：系统可以标出“支持/反驳/矛盾”，但高风险结论应保留分析师确认环节。
- **规则只能表达已知模式**：不在规则库、训练样本或对象关系中的新型行为，只能先生成低置信线索，不能直接生成高置信结论。
- **合规边界必须编码进动作规则**：系统可以建议“继续监测、发布航行安全提示、通知民防”，不应自动生成进攻性处置建议。

因此，正确定位是：本体让系统自动完成“候选发现、证据组织、置信度更新、影响传播、动作推荐”，但最终高风险情报判断仍要有人工审核和审计。

### 3.2 核心对象层

这里不再设置统一的 `Entity` 对象。原因是“实体”过于宽泛，会把可移动目标、固定设施、组织主体、航线服务和地理对象混在一起，导致关系和规则只能写成泛泛的“关联/影响”，难以自动推理。核心对象应按业务语义和可观测性拆开；底层再用“身份解析记录”处理别名、编号和跨源 ID 映射。

| 本体对象 | 作用 | 关键字段 | 适用场景 |
| --- | --- | --- | --- |
| 地理关注区（`GeoAOI`） | 统一表达海域、港口、设施、机场、航道、城市、锚地、事件区域 | `aoi_id`、`name`、`type`、`geometry`、`country`、`admin_area`、`importance`、`sensitivity_level`、`source`、`valid_from` | 全部 |
| 船舶（`Vessel`） | 商船、油轮、液化天然气船、服务船等可移动海上目标 | `vessel_id`、`mmsi`、`imo`、`name`、`callsign`、`ship_type`、`flag`、`owner_operator_id`、`current_voyage_id`、`risk_tags` | 场景 1/4 |
| 航空器（`Aircraft`） | 民航、货机、公务机、无人机或其他公开可观测航空目标 | `aircraft_id`、`icao24`、`registration`、`callsign`、`aircraft_type`、`operator_id`、`route_id`、`position_quality`、`risk_tags` | 场景 2/3/4 |
| 关键设施（`CriticalFacility`） | 港口、机场、炼厂、电站、海水淡化厂、液化天然气设施、数据中心等固定资产 | `facility_id`、`facility_type`、`name`、`operator_id`、`geometry`、`country`、`criticality`、`service_tags`、`status` | 场景 2/3 |
| 组织与运营主体（`Organization`） | 港口运营方、航运公司、能源公司、机场管理方、政府部门、通告发布方 | `organization_id`、`name`、`organization_type`、`country`、`operates_assets`、`issues_sources`、`contact_policy` | 全部 |
| 航线与服务（`RouteService`） | 海上航道、空中航路、港口服务、电力/供水/网络服务等被事件影响的业务对象 | `route_service_id`、`service_type`、`geometry_or_scope`、`normal_baseline`、`dependent_facilities`、`status` | 全部 |
| 身份解析记录（`IdentityResolution`） | 处理同名、别名、编号、呼号和跨源 ID 映射；它是底层解析对象，不作为业务对象本体 | `identity_id`、`canonical_object_type`、`canonical_object_id`、`aliases`、`identifiers`、`source_refs`、`confidence` | 全部 |
| 情报事件（`Event`） | 多源线索聚合后的标准事件 | `event_id`、`event_type`、`time_window`、`location`、`affected_objects`、`status`、`severity`、`confidence`、`summary` | 全部 |
| 观测记录（`Observation`） | 来自单一源的一条观测事实，不直接等于结论 | `observation_id`、`source_id`、`source_type`、`observed_at`、`collected_at`、`location`、`raw_ref`、`claim`、`confidence`、`extraction_method` | 全部 |
| 异常记录（`Anomaly`） | 从规则或模型中发现的异常 | `anomaly_id`、`anomaly_type`、`target_object_type`、`target_object_id`、`aoi_id`、`start_time`、`end_time`、`score`、`baseline_ref`、`features` | 全部 |
| 影像资产（`ImageryAsset`） | 卫星影像或遥感产品资产 | `asset_id`、`provider`、`sensor`、`mode`、`capture_time`、`resolution`、`cloud_cover`、`geometry`、`storage_uri`、`license` | 全部 |
| 检测对象（`DetectionObject`） | 影像或遥感中的检测结果 | `object_id`、`asset_id`、`object_type`、`geometry`、`confidence`、`model_version`、`attributes` | 场景 1/3/4 |
| 证据关系（`EvidenceLink`） | 将观测、异常、影像检测与事件连接起来 | `event_id`、`evidence_id`、`relation`、`supports_or_refutes`、`weight`、`rationale` | 全部 |
| 验证矩阵（`VerificationMatrix`） | 一级线索与二级/三级验证的交叉验证结果 | `event_id`、`claim`、`source_rows`、`status`、`confidence_delta`、`analyst_notes` | 全部 |
| 风险评估（`RiskAssessment`） | 面向决策的风险评估 | `event_id`、`risk_type`、`risk_level`、`affected_routes`、`affected_facilities`、`time_horizon`、`recommended_actions` | 全部 |
| 情报报告（`IntelReport`） | 三级融合报告对象 | `report_id`、`report_type`、`event_ids`、`executive_summary`、`key_judgments`、`evidence_chain`、`confidence`、`version`、`export_uri` | 全部 |
| 持续监测任务（`MonitoringTask`） | 把一次事件转成持续监测任务 | `task_id`、`aoi_id`、`trigger_event_id`、`cadence`、`sensors`、`rules`、`owner`、`status`、`next_run_at` | 场景 1/3/4 |
| 审计轨迹（`AuditTrail`） | 审计和可追溯 | `actor`、`action`、`object_type`、`object_id`、`timestamp`、`before_after`、`reason` | 全部 |

### 3.3 核心关系层

关系层决定系统能否推理。如果只存对象，不存关系，系统只能展示数据；有了关系，系统才能判断“这个异常影响了谁”“这条证据支持还是反驳某个判断”“下一步应该做什么”。

| 关系 | 英文关系名 | 主体 → 客体 | 推理价值 |
| --- | --- | --- | --- |
| 位于 | `located_in` | 船舶/航空器/设施/事件/观测 → 关注区 | 自动归属国家、海域、港口、机场、设施 |
| 包含 | `contains` | 关注区 → 设施/航道/锚地/事件 | 从大范围事件下钻到受影响资产 |
| 邻近 | `near` | 事件/观测 → 设施/航道/机场 | 判断潜在影响范围和需要核验的目标 |
| 穿越 | `crosses` | 航线/航迹 → 关注区/风险区 | 识别受影响航线和船舶 |
| 运营/拥有 | `operates` / `owns` | 公司/政府部门 → 设施/船舶/港口 | 生成通知对象和责任主体 |
| 依赖 | `depends_on` | 设施/服务 → 电力/港口/机场/网络 | 推理二级影响和供应链影响 |
| 观测到 | `observes` | 数据源/传感器 → 观测记录 | 追溯证据来源和采集方式 |
| 主张 | `claims` | 新闻/通告/社媒 → 事件主张 | 保留“来源说了什么”，避免把主张直接当事实 |
| 支持 | `supports` | 观测/异常/影像检测 → 事件主张 | 提升置信度 |
| 反驳 | `refutes` | 观测/异常/影像检测 → 事件主张 | 降低置信度或标为矛盾 |
| 同一事件 | `same_as` | 事件主张 → 事件主张 | 合并重复报道或多源线索 |
| 属于波次 | `part_of` | 事件 → 攻击波次/风险事件包 | 形成区域态势 |
| 前后变化 | `changed_from` | 影像/状态 → 历史基线 | 做损伤、恢复、拥堵、活动变化判断 |
| 触发 | `triggers` | 异常/规则 → 动作/任务 | 自动创建线索卡、验证任务或持续监测 |
| 生成 | `produces` | 事件/验证矩阵 → 报告 | 保证报告可追溯 |

### 3.4 核心规则层

规则层建议分成 6 类。第一版可以用显式规则，不必一开始引入复杂模型。

| 规则类型 | 示例规则 | 自动推理结果 | 人工确认点 |
| --- | --- | --- | --- |
| 空间规则 | 观测位置落入霍尔木兹交通分离制关注区，且距离主航道小于阈值 | 归属到海上通道安全事件包 | 关注区边界是否准确 |
| 时间规则 | 多条观测在同一 6 小时窗口内指向同一设施 | 合并为同一候选事件 | 是否确为同一事件 |
| 异常规则 | 船舶在高风险海域超过阈值时间无位置更新 | 生成“可能船舶识别静默”异常 | 是否是接收盲区或设备故障 |
| 交叉验证规则 | 火点/热异常与设施关注区、新闻主张同窗重合 | 将事件从单源主张提升为部分验证 | 火点是否来自工业常态燃烧 |
| 置信度规则 | 权威通告 + 遥感证据 + 历史基线异常同时成立 | 提高置信度和风险等级 | 权威通告与遥感是否指向同一对象 |
| 安全边界规则 | 报告建议不得包含进攻目标选择、发射点推断或攻击建议 | 自动过滤不合规动作 | 高敏内容需审核 |

### 3.5 核心动作层

动作层让本体从“知识库”变成“工作流”。建议把动作分成系统自动动作和分析师动作。

| 动作 | 英文动作名 | 触发条件 | 输出 |
| --- | --- | --- | --- |
| 创建线索卡 | `create_lead_card` | 一级异常规则命中 | 线索卡、初始置信度、推荐核验项 |
| 合并事件 | `merge_events` | 多条事件主张同地同窗且语义相近 | 统一事件、去重后的证据链 |
| 降级传闻 | `downgrade_rumor` | 来源弱、无遥感/官方支持、存在旧视频或反证 | 降低置信度、标记待确认或反驳 |
| 请求影像验证 | `request_imagery_check` | 一级线索达到阈值但缺二级证据 | 影像任务、目标关注区、时间窗 |
| 运行火点核验 | `run_fire_check` | 事件主张包含爆炸、火灾、设施受损 | 火点匹配结果、热异常证据 |
| 运行真实位置核验 | `run_true_position_check` | 船舶位置异常或导航干扰线索 | 雷达卫星船位核验任务 |
| 分配分析师复核 | `assign_review` | 高风险、证据冲突、置信度临界 | 人工审核任务 |
| 生成融合报告 | `generate_fusion_report` | 验证矩阵完成或达到报告阈值 | 三级融合报告 |
| 转持续监测 | `create_monitoring_task` | 事件已验证且仍有后续风险 | 关注区监测任务、传感器组合、阈值 |
| 发布非进攻性建议 | `publish_safety_recommendation` | 风险等级达到阈值且建议通过安全规则 | 航行安全、民防、港口调度或继续监测建议 |

### 3.6 观测记录的建议形态

观测记录是整个系统最关键的基础对象。它要保留“来源说了什么”，而不是过早变成“系统认定事实”。下面示例保留英文程序字段，便于后续落库和接口设计；阅读时以中文释义为准。

```json
{
  "observation_id": "obs_20260707_ukmto_001",
  "source_id": "ukmto_advisory_061",
  "source_type": "maritime_advisory",
  "observed_at": "2026-06-21T00:00:00Z",
  "collected_at": "2026-07-07T12:00:00Z",
  "location": {
    "type": "aoi_ref",
    "aoi_id": "aoi_strait_of_hormuz_tss"
  },
  "claim": {
    "claim_type": "gnss_interference_reported",
    "text": "通告称该区域持续存在导航干扰。",
    "affected_domain": ["maritime", "aviation"]
  },
  "raw_ref": {
    "url": "https://www.ukmto.org/",
    "title": "英国海上贸易行动办公室/联合海事信息中心通告",
    "language": "en"
  },
  "confidence": {
    "source_reliability": 0.85,
    "extraction_confidence": 0.95,
    "initial_fact_confidence": 0.7
  },
  "extraction_method": "manual_or_rule_v1"
}
```

### 3.7 情报事件的建议形态

情报事件是多个观测记录、异常记录、检测对象聚合后的工作对象。它有状态机，不能只是一条地图标记。

```json
{
  "event_id": "evt_hormuz_nav_integrity_20260707_001",
  "event_type": "navigation_integrity_incident",
  "status": "l2_partially_verified",
  "time_window": {
    "start": "2026-06-20T00:00:00Z",
    "end": "2026-06-22T23:59:59Z"
  },
  "location": {
    "aoi_id": "aoi_strait_of_hormuz_tss",
    "geometry": "polygon_ref"
  },
  "affected_objects": [
    {"object_type": "route_service", "object_id": "route_hormuz_eastbound_tss", "role": "affected_route"},
    {"object_type": "facility", "object_id": "port_fujairah", "role": "nearby_port"}
  ],
  "evidence": [
    {"evidence_id": "obs_ukmto_001", "relation": "supports"},
    {"evidence_id": "anom_ais_jump_cluster_001", "relation": "supports"},
    {"evidence_id": "asset_s1_20260621_001", "relation": "needs_review"}
  ],
  "confidence": {
    "l1": 0.72,
    "l2": 0.83,
    "l3": 0.0,
    "rationale": "多条海事通告和遥测信号互相支持；雷达卫星真实位置核验仍待复核。"
  },
  "decision_relevance": {
    "civilian_impact": ["航运安全", "港口调度"],
    "recommended_actions": ["继续监测", "发布航行安全提示"]
  }
}
```

### 3.8 验证矩阵的建议形态

验证矩阵是演示中最能体现“多源情报分析”的产物。它让客户看到系统如何从传闻、单源异常，逐步升级为多源确认，或者把错误消息降级。

| 主张 | 开源情报 | 船舶/航空/射频证据 | 卫星/火点/雷达证据 | 官方/通告 | 结果 |
| --- | --- | --- | --- | --- | --- |
| 某海域存在导航干扰 | 多条航运/新闻提及 | 航空监视位置质量降低，船舶识别跳点增多 | 合成孔径雷达需要验证真实船位 | 英国海上贸易行动办公室/联合海事信息中心提及 | `partially_verified` |
| 某港口发生爆炸 | 社媒热度高但来源混杂 | 航班/船舶活动变化待核验 | 热异常或光学影像确认 | 港口/政府通告待确认 | `pending_or_disputed` |
| 某设施已恢复运营 | 企业公告声称恢复 | 船舶靠泊量回升 | 新影像显示车辆/船舶活动恢复 | 官方通告确认 | `verified` |

## 4. 场景 1：海上通道安全与航运风险降级本体

### 4.1 需要的本体

| 本体 | 说明 | 关键字段 |
| --- | --- | --- |
| 海事区域（`MaritimeArea`） | 海峡、海湾、专属经济区、领海、风险区 | `geometry`、`jurisdiction`、`risk_level`、`source` |
| 航道（`SeaLane`） | 主航道、交通分离制、推荐通行走廊 | `geometry`、`direction`、`normal_speed_range`、`normal_density_baseline` |
| 锚地（`Anchorage`） | 锚地、等待区、避险区 | `geometry`、`capacity_baseline`、`normal_wait_time` |
| 港口（`Port`） | 港口、码头、泊位 | `unlocode`、`berths`、`handled_cargo`、`operator`、`status` |
| 船舶（`Vessel`） | 船舶对象 | `mmsi`、`imo`、`name`、`callsign`、`ship_type`、`flag`、`owner_operator` |
| 航次（`Voyage`） | 一次航次或港口调用 | `vessel_id`、`origin`、`destination`、`eta`、`route_geometry`、`port_call_status` |
| 海事通告（`MaritimeAdvisory`） | 英国海上贸易行动办公室、联合海事信息中心、航行警告区、港口通告 | `issuer`、`advisory_id`、`valid_time`、`aoi`、`hazard_type`、`recommended_action` |
| 船舶识别观测（`AISObservation`） | 单个船舶自动识别点或消息 | `mmsi`、`timestamp`、`lat`、`lng`、`sog`、`cog`、`heading`、`nav_status`、`receiver` |
| 船舶识别异常（`AISAnomaly`） | 航迹异常 | `anomaly_type`、`baseline_ref`、`score`、`duration`、`affected_route` |
| 海事风险评估（`MaritimeRiskAssessment`） | 通航风险评估 | `risk_level`、`affected_routes`、`affected_vessel_classes`、`confidence`、`recommendation` |

### 4.2 需要哪些数据构建

| 数据 | 用途 | 当前项目覆盖 | 主要缺口 | 可获取来源 |
| --- | --- | --- | --- | --- |
| 船舶自动识别当前点位 | 展示船舶位置、航速、航向、船型 | 已有 AISStream 网络套接字和 AISHub 备用拉取；`fetch_ships` 会合并航母和船舶自动识别船舶 | 缺历史航迹、接收站质量、长窗口基线、船舶识别静默事件 | AISStream、AISHub、Spire/MarineTraffic exactEarth 等商业源、客户自有船舶识别数据 |
| 船舶自动识别历史基线 | 识别航线偏离、拥堵、异常锚泊、船舶识别静默 | 当前基本没有可追溯历史库 | 缺 7 天、90 天、180 天基线；缺航道正常密度模型 | 商业船舶识别历史、客户船舶识别站、归档现有船舶识别流 |
| 航道/交通分离制/锚地/港口 | 判断偏航、拥堵和通行风险 | 当前缺专门海事关注区 | 缺霍尔木兹交通分离制、富查伊拉锚地、杰贝阿里/哈利法/富查伊拉港区和泊位边界 | 开放街图/Overpass、ADMIRALTY 或电子海图授权数据、联合国地点代码、港口官网、客户海事部门 |
| 海事通告 | 一级事件来源 | 当前新闻、RSS、全球事件语言与语调数据库可间接覆盖，但没有专用连接器 | 缺英国海上贸易行动办公室、联合海事信息中心、航行警告区 IX、港口通告结构化接入 | 英国海上贸易行动办公室通告、联合海事信息中心说明、航行警告区 IX 警告、港口/航运公司通告 |
| 雷达/光学卫星影像 | 核验拥堵、锚泊、大型船舶真实位置 | 已有哨兵-2查询、ASF 哨兵-1目录、外部雷达异常产品 | 缺哨兵-1原始影像下载、船舶检测、真实位置核验、T0/Tn 管理 | ASF 搜索接口、哥白尼数据空间生态、微软行星计算机、商业雷达/光学影像 |
| 航运影响 | 评估客户关心的实际影响 | 当前没有 | 缺港口吞吐、排队时长、保险风险、船期延误 | 港口公告、船舶自动识别推导、航运公司通告、保险/海事风险报告 |

### 4.3 当前项目能支撑到什么程度

当前项目可以支撑“地图上展示实时船舶 + 新闻/全球事件语言与语调数据库背景 + 哨兵-2快照 + 人工智能查询”的浅层演示，但还不能支撑一个真正的“商船安全一级预警→二级验证→三级报告事件包”。主要原因是缺：

- 航运对象本体：航道、锚地、港口调用、海事通告。
- 船舶自动识别历史库和异常规则：船舶识别静默、航线偏离、异常速度、异常锚泊、拥堵。
- 雷达卫星船舶检测：当前雷达卫星目录是元数据，不是船位核验。
- 一级线索卡、二级验证矩阵、三级通行风险报告。

## 5. 场景 4：导航完整性诊断与真实位置核验本体

### 5.1 为什么建议和场景 1 绑定

场景 4 独立展示时，容易变成“看 GPSJam 热力图”或“看船舶识别跳点”，客户会问：这和我的航运、港口、能源通道有什么关系？

把它嵌入场景 1，价值会更清楚：

1. 英国海上贸易行动办公室/联合海事信息中心或公开通告提示某片海域存在导航/船舶识别干扰。
2. 系统发现船舶识别航迹异常或航空监视位置质量下降。
3. 系统用合成孔径雷达检查船舶真实位置，判断船舶识别声称位置是否可信。
4. 三级报告输出“导航完整性风险”和“通航安全建议”。

这样它不是单独的技术秀，而是海上安全决策链中的关键证据。

### 5.2 需要的本体

| 本体 | 说明 | 关键字段 |
| --- | --- | --- |
| 导航干扰格网（`GNSSGridCell`） | 全球导航卫星系统干扰格网 | `cell_id`、`geometry`、`score`、`severity`、`source`、`time_window` |
| 航空位置质量观测（`ADSBQualityObservation`） | 广播式自动相关监视的位置质量观测 | `icao24`、`timestamp`、`lat`、`lng`、`nacp`、`nic`、`source` |
| 船舶位置质量（`AISPositionQuality`） | 船舶自动识别位置质量与一致性 | `mmsi`、`timestamp`、`position_quality`、`receiver_count`、`jump_score` |
| 欺骗/漂移聚类（`SpoofingCluster`） | 群体位置异常 | `cluster_id`、`objects`、`aoi`、`start_time`、`end_time`、`pattern` |
| 真实位置证据（`TruePositionEvidence`） | 雷达/光学影像核验的真实位置证据 | `asset_id`、`detected_object_id`、`target_match_confidence`、`position_delta_m` |
| 导航完整性事件（`NavigationIntegrityIncident`） | 导航完整性事件 | `event_id`、`affected_domain`、`affected_routes`、`severity`、`confidence` |

### 5.3 需要哪些数据构建

| 数据 | 用途 | 当前项目覆盖 | 主要缺口 | 可获取来源 |
| --- | --- | --- | --- | --- |
| 航空监视位置质量字段 | 从航空侧推断导航干扰区域 | 当前有 `detect_gps_jamming_zones`，基于航空位置精度降级聚合成 1 度格网 | 缺长期历史、机场/航路基线、不同质量字段的数据源差异、真实干扰标注 | adsb.lol、airplanes.live、ADS-B Exchange、Flightradar24 导航干扰、客户航空监视数据 |
| GPSJam/Flightradar24 干扰图 | 公共导航干扰参考层 | 当前没有专门连接器，但现有模型可接入 | 缺接口/抓取/授权策略、时间序列入库 | GPSJam、Flightradar24 导航干扰 |
| 船舶自动识别原始点和质量 | 检测海上跳点、群体漂移、船舶识别静默 | 有实时船舶识别点，但缺历史和质量字段 | 缺原始消息保留、接收站信息、异常标签 | AISStream、AISHub、商业船舶识别、客户船舶识别 |
| 雷达卫星船舶检测 | 核对船舶识别位置是否真实 | 有 ASF 哨兵-1目录，没有船舶检测 | 缺雷达影像下载、船舶检测器、船舶识别与雷达匹配 | ASF/哥白尼哨兵-1、ICEYE/Capella 等商业雷达 |
| 地理约束 | 判断船舶是否跳到陆地、机场或不可能区域 | 有基础底图，但缺航运语义层 | 缺海岸线、港区、交通分离制、锚地、不可航行区域 | Natural Earth、开放街图、电子海图授权数据 |

### 5.4 当前项目能支撑到什么程度

当前项目已经有一个很有价值的起点：航空监视位置质量降级检测可以生成导航干扰区域，且有船舶自动识别实时点位和雷达卫星目录。这个组合很适合演示。

但要让客户相信结果，需要补三件事：

- 建立历史基线，证明“今天异常”不是系统噪声。
- 用雷达/光学影像进行真实位置核验，不能只靠船舶自动识别自证。
- 将导航/船舶识别干扰结果表达为航线、港口、船型、时间窗的业务影响，而不是单纯热区。

## 6. 场景 2：商船袭击预警与区域防卫准备本体

### 6.1 需要的本体

| 本体 | 说明 | 关键字段 |
| --- | --- | --- |
| 历史结果事件（`HistoricalAttackEvent`） | 5-6 月已知商船被袭、拦截、海峡摩擦或封锁结果，用于回放验证 | `event_id`、`event_time`、`event_type`、`aoi_id`、`result_summary`、`known_after_time` |
| 威胁信号（`ThreatSignal`） | 结果发生前可见的新闻、AIS、ADS-B、航母/战机动向信号 | `signal_id`、`signal_type`、`observed_at`、`aoi_id`、`target_ref`、`score_delta`、`evidence_ref` |
| 商船/油轮对象（`MerchantVessel`） | 被保护和被评估的商船、油轮、LNG 船等 | `vessel_id`、`mmsi`、`imo`、`ship_type`、`flag`、`operator`、`voyage_ref` |
| 快艇/巡逻艇活动（`FastBoatActivity`） | 近距离接近、集群出现、高速穿越等威胁候选 | `activity_id`、`vessel_refs`、`time_window`、`aoi_id`、`speed_features`、`distance_to_target` |
| 航空支撑活动（`AirSupportActivity`） | 侦察机、加油机、战机、无人机、预警机等同窗活动 | `activity_id`、`aircraft_refs`、`time_window`、`aoi_id`、`activity_type`、`identity_confidence` |
| 新闻主张（`SecurityIncidentClaim`） | 单条新闻、社媒、官方声明中的事件主张，不直接等于事实 | `claim_id`、`claim_type`、`actor_claimed`、`target_claimed`、`time_claimed`、`location_claimed`、`source_id`、`visible_at` |
| 预警事件（`AttackWarningEvent`） | 多源信号融合后的袭击风险上升事件 | `warning_id`、`aoi_id`、`time_window`、`risk_score`、`risk_level`、`supported_by`、`uncertainties` |
| 卫星二次确认任务（`ImageryVerificationTask`） | 证据不足但风险较高时，对特定区域请求影像核验 | `task_id`、`trigger_warning_id`、`aoi_id`、`sensor_request`、`time_window`、`status` |
| 防卫准备建议（`DefensivePreparednessAdvice`） | 面向海事、港口、能源运营方的非进攻性建议 | `advice_id`、`warning_id`、`affected_routes`、`affected_assets`、`recommended_actions`、`confidence` |

### 6.2 需要哪些数据构建

| 数据 | 用途 | 当前项目覆盖 | 主要缺口 | 可获取来源 |
| --- | --- | --- | --- | --- |
| 历史结果事件表 | 训练和验证“结果反推预警模型”，防止只做事后解释 | 样例新闻已有 5-6 月油轮拦截、海峡冲突、无人机/空袭等结果线索 | 缺结构化 `event_results.csv`、结果确认时间、事件边界 | 样例新闻人工标注、英国海上贸易行动办公室、联合海事信息中心、航行警告、官方通告 |
| 新闻/开源情报 | 提取报复警告、无人机、封锁、油轮拦截、攻击声明等前兆信号 | 有样例新闻、RSS、全球事件语言与语调数据库、LiveUAMap | 缺 `visible_at`、原文归档、多语言抽取、同源转载识别 | Reuters/AP/Al Jazeera/本地媒体、Telegram/X/公开视频平台、客户开源情报工具 |
| AIS 历史轨迹 | 识别商船 AIS 静默、坐标异常、快艇接近、异常减速/停船 | 有样例 AIS；海贝 5-6 月 AIS 可做更真实底座 | 缺去重派生层、商船/快艇身份补全、正式 AOI、历史基线 | 海贝 AIS、商业 AIS、客户 AIS、港口船舶数据 |
| ADS-B/航空活动 | 识别侦察、加油、战机、无人机、预警支撑活动 | 有样例 ADS-B；海贝 ADS-B 可做背景 | 大文件身份字段缺失，缺航空器 enrichment、质量字段 | ADS-B Exchange、OpenSky、adsb.lol、airplanes.live、客户航空监视数据 |
| 航母/战机动向 | 验证战略部署、空中支撑与商船风险之间的关联 | 样例 AIS/ADS-B/新闻已有航母、补给舰、F-35、KC-135、RC-135、MQ-9 | 缺身份标准化、部署事件表、同窗关联规则 | 样例数据、海贝数据、新闻、公开航迹源 |
| 卫星影像 | 风险高但证据不足时，对特定海域或设施 AOI 二次确认 | 已有 4 张多时相影像样例、哨兵-2查询、雷达卫星目录 | 当前样例不是商船被袭现场；缺任务化影像和船舶/设施检测 | 哨兵-1/2、Landsat、Planet/Maxar/Vantor、SAR 商业源 |
| 海事/官方通告 | 提升或校正预警置信度 | 当前没有专门接入 | 缺 UKMTO/JMIC/NAVAREA/港口通告结构化源 | UKMTO、JMIC、NAVAREA IX、港口和航运公司公告 |

### 6.3 场景 2 的边界要求

场景 2 必须明确做“袭击风险上升预警和防卫准备”，不要做“精确预测”或“进攻性军事研判”。建议在演示中强制这些边界：

- 只展示粗粒度关注区，不展示可用于打击的精确军事坐标。
- 使用历史已知事件回放验证模型，不承诺未来真实事件的确定性预测。
- 预警评分只能使用当时已可见证据，不能把结果发生后的新闻用于提前评分。
- 把输出分成“背景关注（`background`）”、“风险上升（`elevated`）”、“建议防卫准备（`prepare_defense`）”、“需要二次确认（`verify_now`）”。
- 对 AIS 静默、坐标异常、快艇接近、ADS-B 异常都使用“候选信号”表述，必须保留数据质量解释。
- 报告建议使用“提升监测、护航/避险准备、通知海事/港口/能源运营方、调取卫星二次确认”等非进攻性行动。

### 6.4 当前项目能支撑到什么程度

当前材料和样例数据可以支撑一个固定历史回放 demo：用 5 月 25-28 日、6 月 8-11 日样例窗口，展示新闻威胁、AIS 快艇/商船异常、ADS-B 战机/无人机/加油/侦察活动如何共同推高预警分，并在证据不足时触发卫星二次确认任务。

但要做成客户可信的一级预警→二级验证→三级报告演示，还缺：

- 结构化历史结果事件表，明确哪些新闻是结果，哪些是结果前信号。
- 海贝 AIS/ADS-B 去重派生层和身份 enrichment。
- 正式 AOI：霍尔木兹、阿曼湾、商船航道、锚地、港口进近区。
- UKMTO/JMIC/NAVAREA 等海事权威通告。
- 动态本体中的威胁信号、预警事件、证据关系和评分时间线。
- 防止未来信息泄露的 `visible_at` 字段和回放评估规则。

## 7. 场景 3：能源关键设施损伤与恢复监测本体

### 7.1 需要的本体

| 本体 | 说明 | 关键字段 |
| --- | --- | --- |
| 关键设施（`CriticalFacility`） | 港口、机场、炼厂、电站、海水淡化厂、液化天然气/天然气制液、数据中心 | `facility_id`、`facility_type`、`name`、`operator`、`geometry`、`country`、`criticality` |
| 设施组件（`FacilityComponent`） | 泊位、储罐、跑道、变电站、冷却设施、泵站、取水口等组件 | `component_id`、`facility_id`、`component_type`、`geometry`、`function` |
| 运行状态（`OperationalStatus`） | 设施运行状态 | `facility_id`、`status`、`reported_by`、`observed_at`、`confidence` |
| 损伤评估（`DamageAssessment`） | 损伤评估 | `facility_id`、`damage_type`、`damage_extent`、`affected_components`、`confidence` |
| 恢复证据（`RecoveryEvidence`） | 恢复证据 | `indicator_type`、`baseline_value`、`current_value`、`trend`、`source` |
| 供应链影响（`SupplyChainImpact`） | 供应链或服务影响 | `affected_service`、`duration`、`scope`、`severity`、`downstream_entities` |
| 设施监测基线（`FacilityMonitoringBaseline`） | 正常活动基线 | `facility_id`、`metric`、`baseline_window`、`seasonality`、`thresholds` |

### 7.2 设施本体建议细分

阿联酋场景下，设施不应只做“点”。至少要分成三层：

| 层级 | 示例 | 为什么需要 |
| --- | --- | --- |
| 设施级 | 富查伊拉港、杰贝阿里港、哈利法港、Al Dhafra 太阳能电站、杰贝阿里电力/海水淡化综合体 | 面向高层报告和地图总览 |
| 组件级 | 泊位、油罐区、液化天然气码头、跑道、变电站、海水取水口、泵站、冷却塔、数据中心楼宇 | 做损伤定位和恢复判断 |
| 指标级 | 靠泊船数、排队船数、火点、车辆密度、夜光、航班取消、吞吐公告、网络中断 | 做运营影响和恢复趋势 |

### 7.3 需要哪些数据构建

| 数据 | 用途 | 当前项目覆盖 | 主要缺口 | 可获取来源 |
| --- | --- | --- | --- | --- |
| 设施清单和边界 | 建立关键设施和设施组件 | 有电站数据 34,936 条，其中阿联酋约 30 条；有数据中心数据；有 OurAirports 大机场；有 IODA/RIPE 网络中断和探针 | 缺港口、炼厂、液化天然气/天然气制液、海水淡化厂、机场组件、设施多边形；电站多为点位 | 开放街图/Overpass、世界资源研究所全球电站数据库、OurAirports、联合国地点代码、港口/机场/能源公司官网、客户内部资产台账 |
| 多时相影像 | 判断损伤和恢复 | 有哨兵-2按需查询、雷达卫星目录、火点数据 | 缺 T0/T1/T2/Tn 影像资产库、云量/天气解释、商业高分影像、变化检测结果 | 哨兵-1/2、Landsat、NASA 火灾信息资源管理系统、商业影像 |
| 运营状态 | 判断“是否真的恢复” | 当前没有结构化接入 | 缺港口公告、机场延误/取消、能源公司公告、生产/吞吐数据 | 官方通告、港口/机场网站、航班数据、船舶自动识别推导、公司公告 |
| 船舶和航班活动 | 判断港口/机场活动变化 | 有船舶自动识别和航空监视当前层 | 缺历史基线、港口调用、航班取消/改航 | 船舶自动识别历史、OpenSky 航班历史、航班数据供应商、港口船舶识别推导 |
| 网络/服务中断 | 评估数据中心/通信影响 | 有 IODA、RIPE Atlas、数据中心 | 缺设施级归因、客户网络指标 | IODA、RIPE Atlas、Cloudflare Radar、客户网络运营中心 |

### 7.4 当前项目能支撑到什么程度

当前项目在设施类演示上有两个优势：

- 已经有电站、数据中心、机场、火点、IODA/RIPE、哨兵-2、雷达卫星目录这些可视化基础。
- 人工智能工具可以做坐标附近上下文汇总，把某个坐标附近的设施、新闻、火点和遥感信息拉到一起。

但它还没有“关键基础设施韧性监测”的核心：

- 没有关键设施/设施组件的统一本体。
- 没有阿联酋关键设施的完整公开/客户资产清单。
- 没有设施级正常活动基线。
- 没有损伤与恢复指标的标准化规则。
- 没有连续监测任务和报告版本。

## 8. 当前项目数据覆盖与缺口总表

### 8.1 已经具备或部分具备

| 能力 | 当前项目证据 | 可复用方式 |
| --- | --- | --- |
| 多源地图底座 | `README` 描述 Next.js、MapLibre、FastAPI、Python 等技术栈，35+ 图层，包含航空器、船舶、导航干扰、雷达地表变化、火点、哨兵-2 | 作为 M11 展示层和演示工作台 |
| 船舶自动识别当前船舶 | `backend/services/ais_stream.py`、`backend/services/fetchers/aishub_fallback.py`、`backend/services/fetchers/geo.py` | 支撑船舶点位、初步船型、实时态势 |
| 航空监视 | `backend/services/fetchers/flights.py`、OpenSky、adsb.lol、airplanes.live | 支撑航迹、机场周边活动、导航干扰检测 |
| 导航干扰粗检测 | `detect_gps_jamming_zones` 使用航空位置质量降级 | 可作为场景 4 的一级异常源 |
| 新闻/RSS/全球事件语言与语调数据库/LiveUAMap | `backend/services/fetchers/news.py`、`backend/services/fetchers/geo.py`、`backend/services/liveuamap_scraper.py` | 可作为开源情报热点输入 |
| 主题服务 | `backend/services/topics/service.py`，当前有 HIMARS 示例主题 | 可扩展成霍尔木兹、海湾、阿联酋基础设施主题 |
| 哨兵-2查询 | `backend/services/sentinel_search.py`、`/api/ai/satellite-images` | 可作为二级影像展示原型 |
| 哨兵-1/雷达卫星目录 | `backend/services/fetchers/sar_catalog.py` | 可查询雷达卫星覆盖和场景元数据 |
| 外部雷达异常产品 | `backend/services/fetchers/sar_products.py` | 可作为外部变化异常参考 |
| 火点 | `backend/services/fetchers/earth_observation.py` | 可做爆炸/火灾热异常验证 |
| 电站/数据中心/机场/网络中断 | `backend/data/power_plants.json`、`datacenters*.json`、`fetch_airports`、`infrastructure.py` | 可作为设施演示的起点 |
| 人工智能工具面 | `backend/routers/ai_intel.py`、`backend/services/telemetry.py` | 可复用为查询、证据汇总、地图标记、报告草稿入口 |

### 8.2 关键缺口

| 缺口 | 影响 | 优先级 |
| --- | --- | --- |
| 统一一级/二级/三级情报对象模型 | 多源数据只能同屏展示，无法形成生产闭环 | P0 |
| 观测记录、证据关系、验证矩阵、情报报告 | 不能解释结论从何而来、为何可信 | P0 |
| 历史船舶识别/航空监视数据和基线 | 无法稳定识别异常、拥堵、偏航、静默、恢复 | P0 |
| 海事通告、航行警告、结构化事件连接器 | 缺少海事和冲突事件的权威一级输入 | P0 |
| 港口/航道/锚地/设施多边形 | 无法把异常绑定到客户关心的资产 | P0 |
| 哨兵-1/雷达卫星船舶检测和影像资产库 | 无法做真实位置核验和多时相变化检测 | P0/P1 |
| 关键基础设施组件级本体 | 不能从“某设施受影响”下钻到“哪个组件受损/恢复” | P1 |
| 社媒原文、传播链、地理定位、反查 | 场景 2 无法可靠控制误报，历史回放也难以证明哪些信号在袭击前已可见 | P1 |
| 航行通告、机场状态、航班取消/改航 | 航空/机场影响评估不足 | P1 |
| 报告模板、PDF、版本、审计 | 无法交付 PRD 的三级成果物 | P0 |
| 阿拉伯语/波斯语/希伯来语处理 | 海湾区域开源情报覆盖不足 | P1 |

## 9. 缺失数据从哪里获取

### 9.1 P0 数据源

| 数据域 | 推荐来源 | 说明 |
| --- | --- | --- |
| 海事安全通告 | 英国海上贸易行动办公室通告、联合海事信息中心说明、航行警告区 IX 警告 | 用于场景 1/4 的权威一级触发；先做 PDF/HTML 半自动解析也可 |
| 结构化冲突事件 | 武装冲突地点与事件数据项目接口/导出、全球事件语言与语调数据库 | 用于场景 2 的事件时间线；武装冲突地点与事件数据项目需要注册和许可边界确认 |
| 航道/港口/锚地 | 开放街图/Overpass、联合国地点代码、港口官网、电子海图授权数据、客户内部数据 | 开放街图/联合国地点代码可做原型；正式客户环境建议接客户或授权海图 |
| 船舶自动识别历史 | 客户船舶识别站、AISStream/AISHub 归档、商业船舶识别 | 演示至少准备 7 天事件窗口和 90 天基线 |
| 哨兵-1/2 影像 | ASF 搜索接口、哥白尼数据空间生态、微软行星计算机 | 免费源可覆盖原型；雷达卫星船舶检测需要下载和处理 |
| 火点/热异常 | NASA 火灾信息资源管理系统接口 | 火点验证非常适合场景 2/3 |
| 设施基础库 | 世界资源研究所全球电站数据库、OurAirports、开放街图、联合国地点代码、企业官网、政府开放数据 | 当前已有电站、机场、数据中心局部基础；港口/海水淡化/炼厂需补 |

### 9.2 P1/P2 数据源

| 数据域 | 推荐来源 | 用途 |
| --- | --- | --- |
| 导航干扰公共层 | GPSJam、Flightradar24 导航干扰 | 场景 4 的外部参照层 |
| 航行通告/机场状态 | 官方航行通告、机场官网、航班数据商 | 场景 2/3 的机场影响验证 |
| 社媒和公开视频 | X、Telegram、公开视频平台、客户开源情报工具 | 场景 2 的袭击预警补充线索，但必须做来源、时间和媒体反查 |
| 商业影像 | Planet、Maxar/Vantor、Capella、ICEYE 等 | 关键关注区高分辨率确认 |
| 经济/物流影响 | 港口公告、保险风险报告、航运公司公告、油气价格和出口统计 | 只作为民用影响评估，不作为军事判断 |
| 天气/云量 | NOAA、ECMWF、Meteostat、影像元数据 | 解释光学影像不可用、选择雷达影像 |

## 10. 如果本体和数据具备，四个场景能做出的分析

### 10.1 场景 1 可产出的分析

| 分析类型 | 能回答的问题 | 输出结果 |
| --- | --- | --- |
| 航线偏离检测 | 船舶是否偏离常规航道或推荐走廊？ | 偏离距离、偏离时间、受影响航段、历史分位数 |
| 船舶识别静默检测 | 船舶是否在高风险海域突然消失？ | 静默开始/结束、最后可信点、重现点、风险评分 |
| 异常锚泊/拥堵 | 锚地或海峡是否异常拥堵？ | 船舶密度、等待时间、船型构成、与 90 天基线对比 |
| 海事通告关联 | 英国海上贸易行动办公室、联合海事信息中心、航行警告区通告是否与遥测异常重合？ | 通告关注区与船舶识别异常交集、时间差、置信度提升 |
| 雷达卫星船位核验 | 船舶识别声称位置和真实船位是否一致？ | 船舶识别与雷达影像匹配表、位置差、无法匹配船舶清单 |
| 通行风险评估 | 哪些航线、船型、港口受影响？ | 风险等级、影响范围、建议继续监测或发布航行提示 |

对阿联酋客户最有价值的结果不是“某船异常”，而是：

- 富查伊拉、杰贝阿里、哈利法港等港口外部通道的风险变化。
- 油轮、液化天然气船、集装箱船是否出现绕行或等待异常。
- 是否需要向港口、海事、能源和民防部门同步航行安全提示。

### 10.2 场景 4 可产出的分析

| 分析类型 | 能回答的问题 | 输出结果 |
| --- | --- | --- |
| 导航干扰热区 | 哪些区域导航质量持续下降？ | 时间序列热图、严重度、受影响航路/航道 |
| 船舶识别跳点/漂移 | 是否存在欺骗或压制干扰迹象？ | 跳点事件、群体同步漂移、陆地跳点、异常速度 |
| 航空监视质量降级 | 航空侧是否也显示导航异常？ | 位置质量降级比例、受影响高度层、机场附近风险 |
| 跨域印证 | 船舶异常、航空位置质量下降和公开导航干扰图是否同区同窗？ | 验证矩阵、置信度跃迁 |
| 真实位置核验 | 雷达/光学影像是否支持船舶识别位置？ | 真实位置证据、位置不一致列表 |
| 导航安全建议 | 如何降低碰撞、搁浅、误入敏感区风险？ | 受影响航线、建议监测窗口、非进攻性处置建议 |

这个场景最适合展示“多源数据不是简单叠图”：航空监视的位置质量、海上船舶识别异常、海事通告、雷达卫星真值可以互相验证或互相反驳。

### 10.3 场景 2 可产出的分析

| 分析类型 | 能回答的问题 | 输出结果 |
| --- | --- | --- |
| 历史事件回放 | 在 5-6 月已知商船被袭/拦截/海峡摩擦结果发生前，系统能否看到风险上升？ | 结果事件表、前兆窗口、当时可见证据、预警评分曲线 |
| AIS 前兆检测 | 商船、油轮、快艇是否出现静默、坐标异常、异常减速、快速接近或集群活动？ | AIS 异常候选、快艇接近事件、商船风险对象 |
| ADS-B 支撑活动识别 | 战机、侦察机、加油机、无人机是否在同一窗口增强活动？ | 航空支撑活动、风险窗口旁证、身份待核验项 |
| 新闻威胁信号抽取 | 是否出现报复警告、无人机/拦截、海峡封锁、油轮袭击等结果前信号？ | `ThreatSignal`、信号类型、可见时间、风险增量 |
| 多源预警评分 | 新闻、AIS、ADS-B、航母/战机动向是否共同推高风险？ | `AttackWarningEvent`、风险分、关键触发原因 |
| 卫星二次确认 | 风险高但证据不足时，应调取哪片区域、哪个时间窗的影像？ | `ImageryVerificationTask`、AOI、传感器需求 |
| 防卫准备报告 | 应采取哪些非进攻性防护动作？ | 提升监测、护航/避险准备、通知海事/港口/能源运营方 |

对阿联酋客户最有价值的结果是“提前形成防卫准备信号”：

- 哪些已知袭击/拦截事件在发生前有可观察前兆？
- 哪些 AIS/ADS-B 异常和新闻信号共同出现？
- 哪些信号只是数据质量问题或背景噪声，不能提高风险？
- 哪些窗口应触发卫星二次确认或人工复核？

### 10.4 场景 3 可产出的分析

| 分析类型 | 能回答的问题 | 输出结果 |
| --- | --- | --- |
| 设施损伤识别 | 哪个设施、哪个组件可能受损？ | 损伤区域、组件类型、置信度、影像证据 |
| 火点和烟羽验证 | 是否存在火灾或热异常？ | 火点/热异常匹配、热异常强度、持续时间 |
| 活动变化检测 | 港口、机场、电站周边活动是否下降或恢复？ | 船舶靠泊、车辆密度、航班活动、夜光/热异常趋势 |
| 恢复真实性评估 | 官方称恢复运营是否有外部证据？ | 恢复指标、与基线差距、矛盾证据 |
| 供应链影响 | 哪些服务或下游资产受影响？ | 港口排队、航班取消、能源/水/网络服务影响 |
| 持续监测任务 | 后续应监测什么、多久更新一次？ | 关注区监测任务、传感器组合、触发阈值 |

这个场景最适合做成“事件到持续监测”的闭环：

1. 一级预警：新闻或官方通告称某设施发生火灾或中断。
2. 二级验证：火点/热异常、哨兵、雷达或商业影像确认是否有火点、烟羽、活动变化。
3. 三级报告：生成损伤和恢复报告。
4. 自动转成持续监测任务，持续跟踪 T2/T3/Tn 是否恢复。

## 11. 建设顺序建议

### 11.1 不建议的做法

不建议为 4 个场景分别做 4 套页面、4 套数据表、4 套规则和 4 套报告。这会造成：

- 本体重复。
- 证据链不一致。
- 报告口径不一致。
- 后续无法扩展到新场景。
- 演示看起来丰富，但工程上不可维护。

### 11.2 推荐的最小可行产品路线

| 阶段 | 目标 | 交付物 | 覆盖场景 |
| --- | --- | --- | --- |
| M0. 基础本体 | 定义统一对象、关系、规则、动作和状态机 | 地理关注区、船舶、航空器、关键设施、组织、航线与服务、身份解析、观测记录、情报事件、证据关系、验证矩阵、情报报告等模式 | 全部 |
| M1. 阿联酋/海湾资产与关注区库 | 建立演示所需关注区、资产和运营主体 | 港口、航道、锚地、机场、能源、电站、海水淡化、数据中心、行政区、运营方 | 全部 |
| M2. 权威事件源接入 | 补齐一级输入 | 英国海上贸易行动办公室、联合海事信息中心、航行警告区、武装冲突地点与事件数据项目连接器或半自动导入 | 1/2/4 |
| M3. 历史遥测基线 | 让异常检测可信 | 船舶识别/航空监视 7 天事件窗口和 90 天基线，异常规则 | 1/4 |
| M4. 遥感资产和验证 | 让二级验证可演示 | 哨兵-1/2、火点资产索引、T0/T1/Tn、影像证据卡、雷达/光学人工或半自动标注 | 1/2/3/4 |
| M5. 一级线索卡和验证矩阵 | 打通多源证据链 | 线索卡、主张、证据、状态、置信度变化 | 全部 |
| M6. 三级报告模板 | 输出客户可读结果 | 海上通道风险报告、区域安全事件简报、设施韧性报告、导航完整性报告 | 全部 |
| M7. 演示脚本和固定样例包 | 保证演示稳定 | 冻结事件包、样例数据、截图/影像缓存、失败降级方案 | 全部 |

### 11.3 第一版演示的最小可行组合

第一版不要追求所有自动化。建议做一个“可解释、稳定、可复盘”的固定样例演示：

| 组件 | 最小要求 |
| --- | --- |
| 事件包 | 选 2 个主事件：一个海上通道安全事件，一个关键基础设施影响事件 |
| 数据 | 冻结事件窗口内的海事通告、结构化事件、新闻、船舶识别/航空监视、火点、哨兵/雷达卫星元数据 |
| 本体 | 手工或半自动生成观测记录、情报事件、证据关系、验证矩阵 |
| 界面 | 地图展示关注区、事件、证据层；点击事件显示一级/二级/三级链路 |
| 报告 | 生成 Markdown/PDF 风格报告，结论先行，证据链可追溯 |
| 降级 | 外部接口不可用时使用缓存数据，明确标识“固定样例”或“缓存” |

## 12. 验收口径建议

### 12.1 场景级验收

每个场景都不应只验收“地图上有点”，而要验收情报链：

| 验收项 | 标准 |
| --- | --- |
| 一级线索 | 至少 2 类来源生成同一事件或同一关注区的线索 |
| 二级验证 | 至少 1 类遥感或权威源对一级主张做支持、反驳或待确认标注 |
| 三级报告 | 报告包含结论、证据链、置信度、剩余不确定性、非进攻性建议 |
| 可追溯 | 任一结论能回到原始来源、采集时间、处理方式和分析师动作 |
| 可降级 | 外部数据源失败时演示不崩溃，能展示缓存和数据新鲜度 |

### 12.2 数据级验收

| 数据 | 最低验收 |
| --- | --- |
| 船舶识别/航空监视 | 至少覆盖事件前后 7 天；关键指标有 90 天基线更好 |
| 开源情报 | 保留原文链接、发布时间、抓取时间、语言、信源评分 |
| 影像 | 每个重点关注区至少 T0/T1；关键设施最好 T2/Tn |
| 关注区 | 港口、航道、设施必须是多边形或路线，不只是一组点 |
| 报告 | 报告中的每条关键判断至少有一条有来源支撑的证据 |

## 13. 主要风险与防护

| 风险 | 表现 | 防护措施 |
| --- | --- | --- |
| 实时事件事实变化 | 场景 2 的事件结论会随新闻更新变化 | 演示使用冻结事件包；实时数据仅作为“新增观察”显示 |
| 数据授权风险 | 船舶识别、商业影像、结构化冲突事件、社媒数据可能有许可限制 | 明确演示数据来源、许可、缓存策略和客户部署边界 |
| 误报风险 | 社媒旧视频、错误坐标、火点误匹配 | 建立传闻传播链、媒体哈希、地理定位状态、验证矩阵 |
| 敏感军事用途风险 | 被误解为进攻目标选择系统 | 产品文案和报告模板固定为民用保护、风险降级、持续监测 |
| 影像不可用 | 云、重访周期、商业影像成本 | 光学不可用时切雷达影像；报告中解释数据缺口 |
| 当前项目能力被过度包装 | 现有项目更像地图底座，不是完整情报生产系统 | 演示明确区分“已具备底座”和“新增情报工作流” |

## 14. 结论

4 个场景都值得保留，但要重新组织成两条主线、四个能力包：

- 海上通道安全是第一主线，最适合阿联酋客户，也最适合展示船舶自动识别、海事通告、导航干扰、雷达卫星和三级通行风险报告。
- 导航完整性诊断应作为海上通道安全的关键证据能力，同时可在技术评审中单独展示。
- 商船袭击预警与区域防卫准备是第二主线的主场景，适合用 5-6 月历史已知事件回放，展示 AIS/ADS-B、航母/战机动向和新闻主张如何共同形成风险上升信号；信息降噪只是防误报能力，不是主目标。
- 能源关键设施损伤与恢复监测是第二主线的补充演示，最能打动决策层，尤其是炼厂、油库、LNG、港口能源码头、电力/海水淡化综合体。

当前项目已经有不少可复用素材：多源地图、船舶识别/航空监视、导航干扰粗检测、新闻/全球事件语言与语调数据库/LiveUAMap、哨兵-2、雷达卫星目录、火点、电站/数据中心/机场和人工智能查询工具。但它还缺最关键的一层：统一本体、历史基线、证据链、验证矩阵、报告对象和持续监测任务。

所以，下一步不是先堆更多图层，而是先把“观测记录 → 情报事件 → 证据关系 → 验证矩阵 → 情报报告 → 持续监测任务”这条主干建起来。只要这条主干成立，4 个场景都可以成为同一套情报生产系统上的不同演示包。

## 15. 参考来源

### 15.1 钉钉文档与项目材料

- 钉钉文档：`DYINT-Demo`，节点 `b9Y4gmKWrdgOmQNdC43lQN6dJGXn6lpz`
- PRD 整理稿：`/Users/liushen/Documents/githubDevs/dy-inta/PRD-v6.md`
- 当前项目适配分析：`/Users/liushen/Documents/githubDevs/dy-inta/devdoc/PRD-v6-当前项目适配分析与UAE场景.md`
- 被评估项目：`/Users/liushen/Documents/cursorDevs/gintbroker`

### 15.2 当前项目证据索引

- `/Users/liushen/Documents/cursorDevs/gintbroker/README.md`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/services/ais_stream.py`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/services/fetchers/aishub_fallback.py`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/services/fetchers/flights.py`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/services/fetchers/news.py`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/services/fetchers/geo.py`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/services/fetchers/earth_observation.py`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/services/fetchers/sar_catalog.py`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/services/fetchers/sar_products.py`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/services/sentinel_search.py`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/services/topics/service.py`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/routers/ai_intel.py`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/services/telemetry.py`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/data/power_plants.json`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/data/datacenters.json`
- `/Users/liushen/Documents/cursorDevs/gintbroker/backend/data/datacenters_geocoded.json`

### 15.3 外部数据源

- 英国海上贸易行动办公室（UKMTO）：<https://www.ukmto.org/>
- 武装冲突地点与事件数据项目冲突数据（ACLED conflict data）：<https://acleddata.com/conflict-data>
- 武装冲突地点与事件数据项目接口文档（ACLED API documentation）：<https://acleddata.com/api-documentation/getting-started>
- GPSJam 导航干扰地图：<https://gpsjam.org/>
- Flightradar24 导航干扰数据：<https://www.flightradar24.com/data/gps-jamming>
- NASA 火灾信息资源管理系统接口（NASA FIRMS API）：<https://firms.modaps.eosdis.nasa.gov/api/>
- 阿拉斯加卫星设施搜索接口（ASF Search API）：<https://docs.asf.alaska.edu/api/basics/>
- 微软行星计算机哨兵-2 L2A 数据集（Microsoft Planetary Computer Sentinel-2 L2A）：<https://planetarycomputer.microsoft.com/dataset/sentinel-2-l2a>
- AISStream 船舶识别流文档：<https://aisstream.io/documentation>
- OpenSky 航空数据接口（OpenSky REST API）：<https://openskynetwork.github.io/opensky-api/rest.html>
- 全球事件语言与语调数据库（GDELT）：<https://www.gdeltproject.org/>
- 航行警告区 IX（NAVAREA IX）：<https://hydrography.paknavy.gov.pk/navarea/>
- 世界资源研究所全球电站数据库（WRI Global Power Plant Database）：<https://datasets.wri.org/datasets/global-power-plant-database>
- 开放街图 Overpass 接口（OSM Overpass API）：<https://wiki.openstreetmap.org/wiki/Overpass_API>
- OurAirports 机场数据：<https://ourairports.com/data/>
- Natural Earth 自然地理数据：<https://www.naturalearthdata.com/>
- 联合国地点代码（UN/LOCODE）：<https://unece.org/trade/uncefact/unlocode>
