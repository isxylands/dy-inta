# DYINT 四场景多源情报 demo：场景微调、本体、数据与分析方案

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

钉钉文档提出的 4 个 demo 事件包方向是合适的，尤其适合面向阿联酋或海湾地区客户展示。它们共同避开了“进攻型军事打击系统”的敏感叙事，转向“海上交通保护、关键基础设施韧性、OSINT 降噪、多源交叉验证、误判降级”的防御型价值。这一点非常重要。

但这 4 个场景不能简单并列成 4 条互不相干的 demo。它们之间有明显重叠：

- 场景 1“霍尔木兹/阿曼湾商船安全”天然会用到场景 4 的 GNSS/AIS 干扰证据。
- 场景 2“区域导弹/无人机袭击态势”与场景 3“关键基础设施损伤/恢复”会共享同一批设施 AOI、火点、影像、官方通告和 OSINT。
- 四个场景都需要同一套 L1 线索、L2 验证、L3 报告、证据链、置信度、AOI 和实体本体。

因此推荐的工程策略是：保留 4 个场景包用于销售和叙事，但底层只建设一套统一的“事件、实体、证据、影像、验证、报告”本体。demo 编排上优先做两条主线：

1. **主线 A：海上通道安全**，把场景 1 和场景 4 合并演示。
2. **主线 B：关键基础设施影响评估**，把场景 2 的袭击态势和场景 3 的损伤/恢复串起来演示。

这样既能覆盖钉钉文档中的 4 个主题，又不会把工程团队拖进 4 套重复的数据管道和 4 套重复页面。

## 2. 四个场景是否合适，以及建议微调

### 2.1 场景适配总表

| 场景 | 原始定位 | 是否合适 | 主要价值 | 主要问题 | 建议微调 |
| --- | --- | --- | --- | --- | --- |
| 1. 霍尔木兹海峡 / 阿曼湾商船安全事件包 | 商船异常、航线偏离、AIS 静默、近失事件、通行风险报告 | 很合适，应作为第一主场景 | 阿联酋高度依赖海上能源和贸易通道；非进攻型；数据可得性相对好；地图表现力强 | 与场景 4 重叠；如果只讲“商船遇袭”，容易变成新闻回放 | 改成“海上通道安全与风险降级”：突出通航安全、保险/港口/民防联动、误判降级 |
| 2. 2 月 28 日后海湾地区导弹/无人机袭击态势包 | OSINT 热点、袭击波次、机场/炼厂/港口影响、谣言降噪 | 合适，但必须收边界 | 能展示 OSINT 信息洪水中的事实核验；适合高层态势简报 | 事件时效和事实会持续变化；容易触碰军事归因、打击路径和实时目标敏感边界 | 改成“区域安全事件信息降噪与民用影响评估”：只做事后/近实时验证、粗粒度 AOI、民用影响 |
| 3. 能源与关键基础设施损伤 / 恢复监测包 | 设施受损、恢复进度、供应链影响、连续监测 | 很合适，应作为第二主场景 | 最贴近阿联酋真实安全利益：港口、机场、电力、海水淡化、能源、数据中心 | 需要高质量设施边界和多时相影像；开源数据只够做部分确认 | 改成“关键基础设施韧性监测”：从战损叙事转为损伤、恢复、替代能力和服务连续性 |
| 4. GNSS / AIS 干扰与航运安全包 | AIS 位置跳变、ADS-B 质量下降、GPSJam、SAR 核验真实船位 | 合适，但不宜作为完全独立主线 | 很能体现多源融合和 RF/GNSS 能力；防御叙事强 | 与场景 1 高度重合；公开 GNSS 数据多来自航空侧，对海上 AIS 干扰需要补充证据 | 改成“导航完整性诊断能力包”：作为场景 1 的关键证据链，也可单独给技术评审演示 |

### 2.2 是否有必要微调

有必要。原因不是原场景错，而是 demo 面向阿联酋客户时需要更精确地控制价值叙事、敏感边界和工程可实现性。

第一，阿联酋客户更容易被“民用基础设施韧性、海上通道安全、误判降级、连续监测”打动，而不是被“某次袭击复盘”本身打动。demo 应该回答决策者的实际问题：

- 海峡或港口现在还能不能安全通行？
- 哪些传闻是真的，哪些还没有证据？
- 哪些能源、港口、机场、海水淡化设施受影响？
- 损伤有没有扩大？恢复是否真实发生？
- 是否需要发布航行安全提示、调整港口调度、提高民防准备或继续监测？

第二，四个场景的技术底座高度复用。若不微调，会出现工程重复：

- 场景 1 和 4 都要 AIS、GNSS、SAR、航道和船舶异常本体。
- 场景 2 和 3 都要 OSINT、ACLED/新闻、FIRMS、卫星影像、设施 AOI 和损伤评估本体。
- 四个场景都要证据链、置信度、验证矩阵和报告模板。

第三，场景 2 最容易产生合规风险。必须明确做“事后或延迟态势验证”，不能展示：

- 精确军事部署坐标。
- 武器发射点推断。
- 实时打击目标识别。
- 进攻性行动建议。

### 2.3 推荐后的四个 demo 包

| 推荐 demo 包 | 对应原场景 | 面向客户的说法 | 工程上的主线 |
| --- | --- | --- | --- |
| A. 海上通道安全与航运风险降级 | 场景 1 | 保护霍尔木兹、阿曼湾和阿拉伯湾通航安全，降低商船误判和事故风险 | Maritime ontology + AIS baseline + UKMTO/JMIC + SAR verification |
| B. 导航完整性诊断与真实位置核验 | 场景 4 | 识别 GNSS/AIS 干扰对航运和航空安全的影响 | RF/GNSS anomaly ontology + AIS/ADS-B quality + SAR true-position |
| C. 区域安全事件信息降噪 | 场景 2 | 在 OSINT 信息洪水中区分传闻、误报、拦截和已确认影响 | Event ontology + source reliability + VIIRS/FIRMS + imagery + official statements |
| D. 关键基础设施韧性监测 | 场景 3 | 持续监测能源、港口、机场、海水淡化、电力、数据中心的损伤与恢复 | Facility ontology + AOI baseline + multi-temporal imagery + activity indicators |

## 3. 四个场景共同需要的本体

这里的“本体”不是简单的标签表，而是一套能支撑 L1 → L2 → L3 情报生产的结构化对象体系。它至少要回答 6 个问题：

1. 发生了什么事件？
2. 涉及哪些实体和 AOI？
3. 哪些观测或证据支持这个事件？
4. 哪些证据互相印证、互相矛盾或还无法判断？
5. 置信度为什么上升或下降？
6. 最终能生成什么报告和持续监测任务？

### 3.1 核心对象层

| 本体对象 | 作用 | 关键字段 | 适用场景 |
| --- | --- | --- | --- |
| `GeoAOI` | 统一表达海域、港口、设施、机场、航道、城市、锚地、事件区域 | `aoi_id`、`name`、`type`、`geometry`、`country`、`admin_area`、`importance`、`sensitivity_level`、`source`、`valid_from` | 全部 |
| `Entity` | 船舶、飞机、设施、港口、机场、公司、组织、地理地物的统一实体 | `entity_id`、`entity_type`、`names`、`identifiers`、`home_country`、`geometry_or_position`、`owner_operator`、`risk_tags` | 全部 |
| `Event` | 多源线索聚合后的标准事件 | `event_id`、`event_type`、`time_window`、`location`、`affected_entities`、`status`、`severity`、`confidence`、`summary` | 全部 |
| `Observation` | 来自单一源的一条观测事实，不直接等于结论 | `observation_id`、`source_id`、`source_type`、`observed_at`、`collected_at`、`location`、`raw_ref`、`claim`、`confidence`、`extraction_method` | 全部 |
| `Anomaly` | 从规则或模型中发现的异常 | `anomaly_id`、`anomaly_type`、`entity_id`、`aoi_id`、`start_time`、`end_time`、`score`、`baseline_ref`、`features` | 全部 |
| `ImageryAsset` | 卫星影像或遥感产品资产 | `asset_id`、`provider`、`sensor`、`mode`、`capture_time`、`resolution`、`cloud_cover`、`geometry`、`storage_uri`、`license` | 全部 |
| `DetectionObject` | 影像或遥感中的检测结果 | `object_id`、`asset_id`、`object_type`、`geometry`、`confidence`、`model_version`、`attributes` | 场景 1/3/4 |
| `EvidenceLink` | 将观测、异常、影像检测与事件连接起来 | `event_id`、`evidence_id`、`relation`、`supports_or_refutes`、`weight`、`rationale` | 全部 |
| `VerificationMatrix` | L1 与 L2/L3 的交叉验证结果 | `event_id`、`claim`、`source_rows`、`status`、`confidence_delta`、`analyst_notes` | 全部 |
| `RiskAssessment` | 面向决策的风险评估 | `event_id`、`risk_type`、`risk_level`、`affected_routes`、`affected_facilities`、`time_horizon`、`recommended_actions` | 全部 |
| `IntelReport` | L3 报告对象 | `report_id`、`report_type`、`event_ids`、`executive_summary`、`key_judgments`、`evidence_chain`、`confidence`、`version`、`export_uri` | 全部 |
| `MonitoringTask` | 把一次事件转成持续监测任务 | `task_id`、`aoi_id`、`trigger_event_id`、`cadence`、`sensors`、`rules`、`owner`、`status`、`next_run_at` | 场景 1/3/4 |
| `AuditTrail` | 审计和可追溯 | `actor`、`action`、`object_type`、`object_id`、`timestamp`、`before_after`、`reason` | 全部 |

### 3.2 `Observation` 的建议形态

`Observation` 是整个系统最关键的基础对象。它要保留“来源说了什么”，而不是过早变成“系统认定事实”。

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
    "text": "Advisory reports continuing navigational interference in the region.",
    "affected_domain": ["maritime", "aviation"]
  },
  "raw_ref": {
    "url": "https://www.ukmto.org/",
    "title": "UKMTO/JMIC advisory",
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

### 3.3 `Event` 的建议形态

`Event` 是多个 `Observation`、`Anomaly`、`DetectionObject` 聚合后的工作对象。它有状态机，不能只是一条地图 marker。

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
  "affected_entities": [
    {"entity_id": "route_hormuz_eastbound_tss", "role": "affected_route"},
    {"entity_id": "port_fujairah", "role": "nearby_port"}
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
    "rationale": "Multiple advisory and telemetry signals; SAR true-position review pending."
  },
  "decision_relevance": {
    "civilian_impact": ["shipping safety", "port scheduling"],
    "recommended_actions": ["continue monitoring", "issue navigation caution"]
  }
}
```

### 3.4 `VerificationMatrix` 的建议形态

`VerificationMatrix` 是 demo 中最能体现“多源情报分析”的产物。它让客户看到系统如何从传闻、单源异常，逐步升级为多源确认，或者把错误消息降级。

| Claim | OSINT | AIS/ADS-B/RF | Satellite/FIRMS/SAR | Official/advisory | Result |
| --- | --- | --- | --- | --- | --- |
| 某海域存在导航干扰 | 多条航运/新闻提及 | ADS-B NACp/NIC 降低，AIS 跳点增多 | SAR 需要验证真实船位 | UKMTO/JMIC 提及 | `partially_verified` |
| 某港口发生爆炸 | 社媒热度高但来源混杂 | 航班/船舶活动变化待核验 | VIIRS 火点或光学影像确认 | 港口/政府通告待确认 | `pending_or_disputed` |
| 某设施已恢复运营 | 企业公告声称恢复 | 船舶靠泊量回升 | 新影像显示车辆/船舶活动恢复 | 官方通告确认 | `verified` |

## 4. 场景 1：海上通道安全与航运风险降级本体

### 4.1 需要的本体

| 本体 | 说明 | 关键字段 |
| --- | --- | --- |
| `MaritimeArea` | 海峡、海湾、专属经济区、领海、风险区 | `geometry`、`jurisdiction`、`risk_level`、`source` |
| `SeaLane` | 主航道、TSS、推荐通行走廊 | `geometry`、`direction`、`normal_speed_range`、`normal_density_baseline` |
| `Anchorage` | 锚地、等待区、避险区 | `geometry`、`capacity_baseline`、`normal_wait_time` |
| `Port` | 港口、码头、泊位 | `unlocode`、`berths`、`handled_cargo`、`operator`、`status` |
| `Vessel` | 船舶实体 | `mmsi`、`imo`、`name`、`callsign`、`ship_type`、`flag`、`owner_operator` |
| `Voyage` | 一次航次或港口调用 | `vessel_id`、`origin`、`destination`、`eta`、`route_geometry`、`port_call_status` |
| `MaritimeAdvisory` | UKMTO/JMIC/NAVAREA/港口通告 | `issuer`、`advisory_id`、`valid_time`、`aoi`、`hazard_type`、`recommended_action` |
| `AISObservation` | 单个 AIS 点或消息 | `mmsi`、`timestamp`、`lat`、`lng`、`sog`、`cog`、`heading`、`nav_status`、`receiver` |
| `AISAnomaly` | 航迹异常 | `anomaly_type`、`baseline_ref`、`score`、`duration`、`affected_route` |
| `MaritimeRiskAssessment` | 通航风险评估 | `risk_level`、`affected_routes`、`affected_vessel_classes`、`confidence`、`recommendation` |

### 4.2 需要哪些数据构建

| 数据 | 用途 | 当前项目覆盖 | 主要缺口 | 可获取来源 |
| --- | --- | --- | --- | --- |
| AIS 当前点位 | 展示船舶位置、航速、航向、船型 | 已有 AISStream WebSocket 和 AISHub fallback；`fetch_ships` 会合并航母和 AIS 船舶 | 缺历史航迹、接收站质量、长窗口基线、AIS 静默事件 | AISStream、AISHub、Spire/MarineTraffic exactEarth 等商业源、客户自有 AIS |
| AIS 历史基线 | 识别航线偏离、拥堵、异常锚泊、AIS 静默 | 当前基本没有可追溯历史库 | 缺 7 天、90 天、180 天基线；缺航道正常密度模型 | 商业 AIS 历史、客户 AIS 站、归档现有 AIS 流 |
| 航道/TSS/锚地/港口 | 判断偏航、拥堵和通行风险 | 当前缺专门海事 AOI | 缺霍尔木兹 TSS、Fujairah 锚地、Jebel Ali/Khalifa/Fujairah 港区和泊位边界 | OSM/Overpass、ADMIRALTY 或 ENC 授权数据、UN/LOCODE、港口官网、客户海事部门 |
| 海事通告 | L1 事件来源 | 当前 news/RSS/GDELT 可间接覆盖，但没有专用 connector | 缺 UKMTO、JMIC、NAVAREA IX、港口通告结构化接入 | UKMTO Advisories、JMIC notes、NAVAREA IX warnings、港口/航运公司通告 |
| SAR/光学影像 | 核验拥堵、锚泊、大型船舶真实位置 | 已有 Sentinel-2 查询、ASF Sentinel-1 catalog、外部 SAR anomaly products | 缺 Sentinel-1 原始影像下载、船舶检测、SAR true-position、T0/Tn 管理 | ASF Search API、Copernicus CDSE、Microsoft Planetary Computer、商业 SAR/光学 |
| 航运影响 | 评估客户关心的实际影响 | 当前没有 | 缺港口吞吐、排队时长、保险风险、船期延误 | 港口公告、AIS 推导、航运公司通告、保险/海事风险报告 |

### 4.3 当前项目能支撑到什么程度

当前项目可以支撑“地图上展示实时船舶 + 新闻/GDELT 背景 + Sentinel-2 快照 + AI 查询”的浅层演示，但还不能支撑一个真正的“商船安全 L1→L2→L3 事件包”。主要原因是缺：

- 航运实体本体：`SeaLane`、`Anchorage`、`PortCall`、`MaritimeAdvisory`。
- AIS 历史库和异常规则：AIS 静默、航线偏离、异常速度、异常锚泊、拥堵。
- SAR 船舶检测：当前 SAR catalog 是元数据，不是船位核验。
- L1 线索卡、L2 验证矩阵、L3 通行风险报告。

## 5. 场景 4：导航完整性诊断与真实位置核验本体

### 5.1 为什么建议和场景 1 绑定

场景 4 独立展示时，容易变成“看 GPSJam 热力图”或“看 AIS 跳点”，客户会问：这和我的航运、港口、能源通道有什么关系？

把它嵌入场景 1，价值会更清楚：

1. UKMTO/JMIC 或公开通告提示某片海域存在 GNSS/AIS interference。
2. 系统发现 AIS 航迹异常或 ADS-B 位置质量下降。
3. 系统用 SAR 检查船舶真实位置，判断 AIS 声称位置是否可信。
4. L3 报告输出“导航完整性风险”和“通航安全建议”。

这样它不是单独的技术秀，而是海上安全决策链中的关键证据。

### 5.2 需要的本体

| 本体 | 说明 | 关键字段 |
| --- | --- | --- |
| `GNSSGridCell` | GNSS 干扰格网 | `cell_id`、`geometry`、`score`、`severity`、`source`、`time_window` |
| `ADSBQualityObservation` | ADS-B 位置质量观测 | `icao24`、`timestamp`、`lat`、`lng`、`nacp`、`nic`、`source` |
| `AISPositionQuality` | AIS 位置质量与一致性 | `mmsi`、`timestamp`、`position_quality`、`receiver_count`、`jump_score` |
| `SpoofingCluster` | 群体位置异常 | `cluster_id`、`entities`、`aoi`、`start_time`、`end_time`、`pattern` |
| `TruePositionEvidence` | SAR/光学核验的真实位置证据 | `asset_id`、`detected_object_id`、`entity_match_confidence`、`position_delta_m` |
| `NavigationIntegrityIncident` | 导航完整性事件 | `event_id`、`affected_domain`、`affected_routes`、`severity`、`confidence` |

### 5.3 需要哪些数据构建

| 数据 | 用途 | 当前项目覆盖 | 主要缺口 | 可获取来源 |
| --- | --- | --- | --- | --- |
| ADS-B NACp/NIC/质量字段 | 从航空侧推断 GNSS 干扰区域 | 当前有 `detect_gps_jamming_zones`，基于 ADS-B 位置精度降级聚合成 1 度格网 | 缺长期历史、机场/航路基线、NIC 数据源差异、真实干扰标注 | adsb.lol、airplanes.live、ADS-B Exchange、Flightradar24 GPS jamming、客户 ADS-B |
| GPSJam/FR24 干扰图 | 公共 GNSS 干扰参考层 | 当前没有专门 connector，但现有模型可接入 | 缺 API/抓取/授权策略、时间序列入库 | GPSJam、Flightradar24 GPS jamming |
| AIS 原始点和质量 | 检测海上跳点、群体漂移、AIS 静默 | 有实时 AIS 点，但缺历史和质量字段 | 缺原始消息保留、接收站信息、异常标签 | AISStream、AISHub、商业 AIS、客户 AIS |
| SAR 船舶检测 | 核对 AIS 位置是否真实 | 有 ASF Sentinel-1 catalog，没有船舶检测 | 缺 SAR imagery download、ship detector、AIS-SAR matching | ASF/Copernicus Sentinel-1、Iceye/Capella/Spacety 等商业 SAR |
| 地理约束 | 判断船舶是否跳到陆地、机场或不可能区域 | 有基础底图，但缺航运语义层 | 缺 coastline、港区、TSS、锚地、不可航行区域 | Natural Earth、OSM、ENC 授权数据 |

### 5.4 当前项目能支撑到什么程度

当前项目已经有一个很有价值的起点：ADS-B 位置质量降级检测可以生成 GPS jamming zones，且有 AIS 实时点位和 SAR catalog。这个组合很适合 demo。

但要让客户相信结果，需要补三件事：

- 建立历史基线，证明“今天异常”不是系统噪声。
- 用 SAR/光学进行真实位置核验，不能只靠 AIS 自证。
- 将 GNSS/AIS 干扰结果表达为航线、港口、船型、时间窗的业务影响，而不是单纯热区。

## 6. 场景 2：区域安全事件信息降噪本体

### 6.1 需要的本体

| 本体 | 说明 | 关键字段 |
| --- | --- | --- |
| `SecurityIncidentClaim` | 单条新闻、社媒、官方声明中的事件主张 | `claim_id`、`claim_type`、`actor_claimed`、`target_claimed`、`time_claimed`、`location_claimed`、`source_id` |
| `AttackWave` | 多个事件聚合成的波次，仅做粗粒度态势 | `wave_id`、`time_window`、`countries`、`incident_count`、`confirmed_count`、`uncertain_count` |
| `ImpactSite` | 可能受影响地点 | `site_id`、`aoi_id`、`facility_id`、`impact_type`、`status` |
| `InterceptionOrDebrisEvent` | 拦截、坠落碎片、远处火光等容易被误报为命中的事件 | `event_id`、`evidence`、`classification`、`confidence` |
| `RumorThread` | 同一传闻的传播链 | `thread_id`、`first_seen`、`canonical_media_hash`、`reposts`、`geolocation_status` |
| `SourceReliability` | 信源可靠性 | `source_id`、`source_type`、`historical_accuracy`、`proximity`、`bias_notes`、`license` |
| `CivilianImpactAssessment` | 民用影响评估 | `affected_facilities`、`airport_status`、`port_status`、`casualty_claims`、`service_disruption` |

### 6.2 需要哪些数据构建

| 数据 | 用途 | 当前项目覆盖 | 主要缺口 | 可获取来源 |
| --- | --- | --- | --- | --- |
| 事件数据库 | 形成事件时间线和粗粒度态势 | 有 GDELT 和 LiveUAMap，可做新闻事件背景 | 缺 ACLED 结构化事件接入、官方事件清单、统一事件去重 | ACLED API/exports、GDELT、LiveUAMap、官方声明 |
| 新闻/OSINT | 发现传闻和热点 | 有 RSS news、GDELT、部分 Reuters/AP/RSSHub 等 feed | 缺原文归档、多语言抽取、社媒传播链、图片/视频反查 | Reuters/AP/Al Jazeera/PBS/本地媒体、Telegram/X/公开视频平台、客户 OSINT |
| 官方声明 | 验证或反驳传闻 | 当前没有专门接入 | 缺政府、机场、港口、能源公司、民防、国防相关公开通告 | 官方网站、社媒认证账号、港口/机场公告 |
| FIRMS/VIIRS 火点 | 快速判断爆炸/火灾是否存在热异常 | 已有 NASA FIRMS 全球 NOAA-20 VIIRS 24h，无 key；country-scoped FIRMS 需 MAP_KEY | 缺与事件 AOI 的自动关联、历史火点基线、误报过滤 | NASA FIRMS API |
| 卫星影像 | 确认火灾、烟羽、设施损伤 | 已有 Sentinel-2 查询、SAR catalog | 缺任务化影像资产、商业高分影像、影像变化检测 | Sentinel-1/2、Landsat、Planet/Maxar/Vantor 等商业源 |
| 航空/机场数据 | 判断机场是否受影响 | 有 OpenSky/adsb.lol/airplanes.live 实时或近实时航迹 | 缺 NOTAM、机场状态、航班取消/改航历史 | OpenSky、ADS-B Exchange、OurAirports、NOTAM、机场官网、航班数据供应商 |

### 6.3 场景 2 的边界要求

场景 2 必须明确做“信息降噪和民用影响评估”，不要做“军事打击研判”。建议在 demo 中强制这些边界：

- 只展示粗粒度 AOI，不展示可用于打击的精确军事坐标。
- 把事件状态分成 `rumor`、`single_source_claim`、`partially_verified`、`verified`、`refuted`。
- 对社媒视频只展示“地理定位状态”和“媒体复用/旧视频风险”，不把单条视频直接当事实。
- 报告建议使用“继续监测、通知民防、发布公共安全提示、调度备用能力”等非进攻性行动。

### 6.4 当前项目能支撑到什么程度

当前项目的新闻/GDELT/LiveUAMap/AI 搜索能力可以做一个“热点地图”或“事件背景看板”。但要做成客户可信的 L1→L2→L3 demo，还缺：

- ACLED 或同类结构化事件源。
- 信源可靠性和传播链本体。
- 多语言原文归档与抽取。
- OSINT 与 FIRMS/影像/官方通告的验证矩阵。
- 事件版本和置信度随证据变化的轨迹。

## 7. 场景 3：关键基础设施韧性监测本体

### 7.1 需要的本体

| 本体 | 说明 | 关键字段 |
| --- | --- | --- |
| `CriticalFacility` | 港口、机场、炼厂、电站、海水淡化厂、LNG/GTL、数据中心 | `facility_id`、`facility_type`、`name`、`operator`、`geometry`、`country`、`criticality` |
| `FacilityComponent` | 泊位、储罐、跑道、变电站、冷却设施、泵站、取水口等组件 | `component_id`、`facility_id`、`component_type`、`geometry`、`function` |
| `OperationalStatus` | 设施运行状态 | `facility_id`、`status`、`reported_by`、`observed_at`、`confidence` |
| `DamageAssessment` | 损伤评估 | `facility_id`、`damage_type`、`damage_extent`、`affected_components`、`confidence` |
| `RecoveryEvidence` | 恢复证据 | `indicator_type`、`baseline_value`、`current_value`、`trend`、`source` |
| `SupplyChainImpact` | 供应链或服务影响 | `affected_service`、`duration`、`scope`、`severity`、`downstream_entities` |
| `FacilityMonitoringBaseline` | 正常活动基线 | `facility_id`、`metric`、`baseline_window`、`seasonality`、`thresholds` |

### 7.2 设施本体建议细分

阿联酋场景下，设施不应只做“点”。至少要分成三层：

| 层级 | 示例 | 为什么需要 |
| --- | --- | --- |
| 设施级 | Port of Fujairah、Jebel Ali Port、Khalifa Port、Al Dhafra Solar PV、Jebel Ali power/desalination complex | 面向高层报告和地图总览 |
| 组件级 | 泊位、油罐区、LNG 码头、跑道、变电站、海水取水口、泵站、冷却塔、数据中心楼宇 | 做损伤定位和恢复判断 |
| 指标级 | 靠泊船数、排队船数、火点、车辆密度、夜光、航班取消、吞吐公告、网络中断 | 做运营影响和恢复趋势 |

### 7.3 需要哪些数据构建

| 数据 | 用途 | 当前项目覆盖 | 主要缺口 | 可获取来源 |
| --- | --- | --- | --- | --- |
| 设施清单和边界 | 建立 `CriticalFacility` 和 `FacilityComponent` | 有 power_plants 数据 34,936 条，其中 UAE 约 30 条；有 datacenters 数据；有 OurAirports 大机场；有 IODA/RIPE internet outage/probes | 缺港口、炼厂、LNG/GTL、海水淡化厂、机场组件、设施 polygon；power plant 多为点位 | OSM/Overpass、WRI Global Power Plant Database、OurAirports、UN/LOCODE、港口/机场/能源公司官网、客户内部资产台账 |
| 多时相影像 | 判断损伤和恢复 | 有 Sentinel-2 on-demand、SAR catalog、FIRMS | 缺 T0/T1/T2/Tn 影像资产库、云量/天气解释、商业高分影像、变化检测结果 | Sentinel-1/2、Landsat、NASA FIRMS、商业影像 |
| 运营状态 | 判断“是否真的恢复” | 当前没有结构化接入 | 缺港口公告、机场延误/取消、能源公司公告、生产/吞吐数据 | 官方通告、港口/机场网站、航班数据、AIS 推导、公司公告 |
| 船舶和航班活动 | 判断港口/机场活动变化 | 有 AIS 和 ADS-B 当前层 | 缺历史基线、港口调用、航班取消/改航 | AIS 历史、OpenSky flight history、航班数据供应商、港口 AIS 推导 |
| 网络/服务中断 | 评估数据中心/通信影响 | 有 IODA、RIPE Atlas、datacenters | 缺设施级归因、客户网络指标 | IODA、RIPE Atlas、Cloudflare Radar、客户 NOC |

### 7.4 当前项目能支撑到什么程度

当前项目在设施类 demo 上有两个优势：

- 已经有电站、数据中心、机场、FIRMS、IODA/RIPE、Sentinel-2、SAR catalog 这些可视化基础。
- AI 工具可以做 near-coordinate context，把某个坐标附近的设施、新闻、火点和遥感信息拉到一起。

但它还没有“关键基础设施韧性监测”的核心：

- 没有 `CriticalFacility`/`FacilityComponent` 的统一本体。
- 没有阿联酋关键设施的完整公开/客户资产清单。
- 没有设施级正常活动基线。
- 没有损伤与恢复指标的标准化规则。
- 没有连续监测任务和报告版本。

## 8. 当前项目数据覆盖与缺口总表

### 8.1 已经具备或部分具备

| 能力 | 当前项目证据 | 可复用方式 |
| --- | --- | --- |
| 多源地图底座 | README 描述 Next.js/MapLibre/FastAPI/Python、35+ layers，包含 aircraft、ships、GPS jamming、SAR ground-change、FIRMS、Sentinel-2 | 作为 M11 展示层和 demo 工作台 |
| AIS 当前船舶 | `backend/services/ais_stream.py`、`backend/services/fetchers/aishub_fallback.py`、`backend/services/fetchers/geo.py` | 支撑船舶点位、初步船型、实时态势 |
| ADS-B/航空 | `backend/services/fetchers/flights.py`、OpenSky/adsb.lol/airplanes.live | 支撑航迹、机场周边活动、GNSS 干扰检测 |
| GNSS jamming 粗检测 | `detect_gps_jamming_zones` 使用 ADS-B 位置质量降级 | 可作为场景 4 的 L1 异常源 |
| 新闻/RSS/GDELT/LiveUAMap | `backend/services/fetchers/news.py`、`backend/services/fetchers/geo.py`、`backend/services/liveuamap_scraper.py` | 可作为 OSINT 热点输入 |
| Topic service | `backend/services/topics/service.py`，当前有 HIMARS 示例 topic | 可扩展成 Hormuz/Gulf/UAE infrastructure topics |
| Sentinel-2 查询 | `backend/services/sentinel_search.py`、`/api/ai/satellite-images` | 可作为 L2 影像展示原型 |
| Sentinel-1/SAR catalog | `backend/services/fetchers/sar_catalog.py` | 可查询 SAR 覆盖和 scene metadata |
| 外部 SAR anomaly products | `backend/services/fetchers/sar_products.py` | 可作为外部变化异常参考 |
| FIRMS 火点 | `backend/services/fetchers/earth_observation.py` | 可做爆炸/火灾热异常验证 |
| 电站/数据中心/机场/网络 outage | `backend/data/power_plants.json`、`datacenters*.json`、`fetch_airports`、`infrastructure.py` | 可作为设施 demo 的起点 |
| AI 工具面 | `backend/routers/ai_intel.py`、`backend/services/telemetry.py` | 可复用为查询、证据汇总、地图 pin、报告草稿入口 |

### 8.2 关键缺口

| 缺口 | 影响 | 优先级 |
| --- | --- | --- |
| 统一 L1/L2/L3 情报对象模型 | 多源数据只能同屏展示，无法形成生产闭环 | P0 |
| `Observation`、`EvidenceLink`、`VerificationMatrix`、`IntelReport` | 不能解释结论从何而来、为何可信 | P0 |
| 历史 AIS/ADS-B 数据和基线 | 无法稳定识别异常、拥堵、偏航、静默、恢复 | P0 |
| UKMTO/JMIC/NAVAREA/ACLED connector | 缺少海事和冲突事件的权威 L1 输入 | P0 |
| 港口/航道/锚地/设施 polygon | 无法把异常绑定到客户关心的资产 | P0 |
| Sentinel-1/SAR 船舶检测和影像资产库 | 无法做真实位置核验和多时相变化检测 | P0/P1 |
| 关键基础设施组件级本体 | 不能从“某设施受影响”下钻到“哪个组件受损/恢复” | P1 |
| 社媒原文、传播链、地理定位、反查 | 场景 2 无法可靠降噪 | P1 |
| NOTAM、机场状态、航班取消/改航 | 航空/机场影响评估不足 | P1 |
| 报告模板、PDF、版本、审计 | 无法交付 PRD 的 L3 成果物 | P0 |
| 阿拉伯语/波斯语/希伯来语处理 | 海湾区域 OSINT 覆盖不足 | P1 |

## 9. 缺失数据从哪里获取

### 9.1 P0 数据源

| 数据域 | 推荐来源 | 说明 |
| --- | --- | --- |
| 海事安全通告 | UKMTO Advisories、JMIC Advisory Notes、NAVAREA IX warnings | 用于场景 1/4 的权威 L1 触发；先做 PDF/HTML 半自动解析也可 |
| 结构化冲突事件 | ACLED API/exports、GDELT | 用于场景 2 的事件时间线；ACLED 需要注册和许可边界确认 |
| 航道/港口/锚地 | OSM/Overpass、UN/LOCODE、港口官网、ENC 授权数据、客户内部数据 | OSM/UNLOCODE 可做原型；正式客户环境建议接客户或授权海图 |
| AIS 历史 | 客户 AIS 站、AISStream/AISHub 归档、商业 AIS | demo 至少准备 7 天事件窗口和 90 天基线 |
| Sentinel-1/2 影像 | ASF Search API、Copernicus CDSE、Microsoft Planetary Computer | 免费源可覆盖原型；SAR 船舶检测需要下载和处理 |
| FIRMS/VIIRS | NASA FIRMS API | 火点验证非常适合场景 2/3 |
| 设施基础库 | WRI Global Power Plant Database、OurAirports、OSM、UN/LOCODE、企业官网、政府开放数据 | 当前已有电站、机场、数据中心局部基础；港口/海水淡化/炼厂需补 |

### 9.2 P1/P2 数据源

| 数据域 | 推荐来源 | 用途 |
| --- | --- | --- |
| GNSS 干扰公共层 | GPSJam、Flightradar24 GPS jamming | 场景 4 的外部参照层 |
| NOTAM/机场状态 | 官方 NOTAM、机场官网、航班数据商 | 场景 2/3 的机场影响验证 |
| 社媒和公开视频 | X、Telegram、公开视频平台、客户 OSINT 工具 | 场景 2 的传闻降噪，但必须做来源和媒体反查 |
| 商业影像 | Planet、Maxar/Vantor、Capella、ICEYE 等 | 关键 AOI 高分辨率确认 |
| 经济/物流影响 | 港口公告、保险风险报告、航运公司公告、油气价格和出口统计 | 只作为民用影响评估，不作为军事判断 |
| 天气/云量 | NOAA、ECMWF、Meteostat、影像元数据 | 解释光学影像不可用、选择 SAR |

## 10. 如果本体和数据具备，四个场景能做出的分析

### 10.1 场景 1 可产出的分析

| 分析类型 | 能回答的问题 | 输出结果 |
| --- | --- | --- |
| 航线偏离检测 | 船舶是否偏离常规航道或推荐走廊？ | 偏离距离、偏离时间、受影响航段、历史分位数 |
| AIS 静默检测 | 船舶是否在高风险海域突然消失？ | 静默开始/结束、最后可信点、重现点、风险评分 |
| 异常锚泊/拥堵 | 锚地或海峡是否异常拥堵？ | 船舶密度、等待时间、船型构成、与 90 天基线对比 |
| 海事通告关联 | UKMTO/JMIC/NAVAREA 通告是否与遥测异常重合？ | 通告 AOI 与 AIS 异常交集、时间差、置信度提升 |
| SAR 船位核验 | AIS 声称位置和真实船位是否一致？ | AIS-SAR 匹配表、位置差、无法匹配船舶清单 |
| 通行风险评估 | 哪些航线、船型、港口受影响？ | 风险等级、影响范围、建议继续监测或发布航行提示 |

对阿联酋客户最有价值的结果不是“某船异常”，而是：

- Fujairah、Jebel Ali、Khalifa Port 等港口外部通道的风险变化。
- 油轮、LNG 船、集装箱船是否出现绕行或等待异常。
- 是否需要向港口、海事、能源和民防部门同步航行安全提示。

### 10.2 场景 4 可产出的分析

| 分析类型 | 能回答的问题 | 输出结果 |
| --- | --- | --- |
| GNSS 干扰热区 | 哪些区域导航质量持续下降？ | 时间序列热图、严重度、受影响航路/航道 |
| AIS 跳点/漂移 | 是否存在 spoofing 或 jamming 迹象？ | 跳点事件、群体同步漂移、陆地跳点、异常速度 |
| ADS-B 质量降级 | 航空侧是否也显示 GNSS 异常？ | NACp/NIC 降级比例、受影响高度层、机场附近风险 |
| 跨域印证 | AIS 异常、ADS-B 质量下降和公开 GNSS 图是否同区同窗？ | 验证矩阵、置信度跃迁 |
| 真实位置核验 | SAR/光学是否支持 AIS 位置？ | true-position evidence、位置不一致列表 |
| 导航安全建议 | 如何降低碰撞、搁浅、误入敏感区风险？ | 受影响航线、建议监测窗口、非进攻性处置建议 |

这个场景最适合展示“多源数据不是简单叠图”：航空 ADS-B 的位置质量、海上 AIS 的异常、海事通告、SAR 真值可以互相验证或互相反驳。

### 10.3 场景 2 可产出的分析

| 分析类型 | 能回答的问题 | 输出结果 |
| --- | --- | --- |
| 传闻聚类 | 多条新闻/社媒是否指向同一事件？ | rumor thread、重复媒体、最早来源、传播路径 |
| 事件状态判定 | 是传闻、单源声称、部分确认、已确认还是反驳？ | event status、confidence timeline |
| 爆炸/火灾验证 | 是否存在热异常或影像证据？ | FIRMS 近邻匹配、Sentinel/商业影像前后对比 |
| 拦截/碎片/命中区分 | 社媒火光是否一定是设施命中？ | claim 分类、矛盾证据、待验证项 |
| 民用影响评估 | 机场、港口、能源设施是否受影响？ | 受影响 AOI、航班/港口/服务状态、影响时长 |
| 高层态势报告 | 区域风险是否上升，哪些信息还不确定？ | 攻击波次摘要、已确认/未确认事件、关键判断 |

对阿联酋客户最有价值的结果是“把噪声压下去”：

- 哪些消息只是社媒重复转发？
- 哪些事件有官方或遥感证据支撑？
- 哪些设施确实受影响，哪些只是传闻？
- 哪些判断仍不确定，需要下一轮影像或官方通告确认？

### 10.4 场景 3 可产出的分析

| 分析类型 | 能回答的问题 | 输出结果 |
| --- | --- | --- |
| 设施损伤识别 | 哪个设施、哪个组件可能受损？ | 损伤区域、组件类型、置信度、影像证据 |
| 火点和烟羽验证 | 是否存在火灾或热异常？ | FIRMS/VIIRS 匹配、热异常强度、持续时间 |
| 活动变化检测 | 港口、机场、电站周边活动是否下降或恢复？ | 船舶靠泊、车辆密度、航班活动、夜光/热异常趋势 |
| 恢复真实性评估 | 官方称恢复运营是否有外部证据？ | 恢复指标、与基线差距、矛盾证据 |
| 供应链影响 | 哪些服务或下游资产受影响？ | 港口排队、航班取消、能源/水/网络服务影响 |
| 持续监测任务 | 后续应监测什么、多久更新一次？ | AOI 监测任务、传感器组合、触发阈值 |

这个场景最适合做成“事件到持续监测”的闭环：

1. L1：新闻或官方通告称某设施发生火灾或中断。
2. L2：FIRMS/VIIRS、Sentinel、SAR 或商业影像确认是否有火点、烟羽、活动变化。
3. L3：生成损伤和恢复报告。
4. 自动转成 `MonitoringTask`，持续跟踪 T2/T3/Tn 是否恢复。

## 11. 建设顺序建议

### 11.1 不建议的做法

不建议为 4 个场景分别做 4 套页面、4 套数据表、4 套规则和 4 套报告。这会造成：

- 本体重复。
- 证据链不一致。
- 报告口径不一致。
- 后续无法扩展到新场景。
- demo 看起来丰富，但工程上不可维护。

### 11.2 推荐的 MVP 路线

| 阶段 | 目标 | 交付物 | 覆盖场景 |
| --- | --- | --- | --- |
| M0. 基础本体 | 定义统一对象和状态机 | `GeoAOI`、`Entity`、`Observation`、`Event`、`EvidenceLink`、`VerificationMatrix`、`IntelReport` schema | 全部 |
| M1. 阿联酋/Gulf 实体库 | 建立 demo 所需 AOI 和实体 | 港口、航道、锚地、机场、能源、电站、海水淡化、数据中心、行政区 | 全部 |
| M2. 权威事件源接入 | 补齐 L1 输入 | UKMTO/JMIC/NAVAREA/ACLED connector 或半自动导入 | 1/2/4 |
| M3. 历史遥测基线 | 让异常检测可信 | AIS/ADS-B 7 天事件窗口和 90 天基线，异常规则 | 1/4 |
| M4. 遥感资产和验证 | 让 L2 可演示 | Sentinel-1/2/FIRMS 资产索引、T0/T1/Tn、影像证据卡、SAR/光学人工或半自动标注 | 1/2/3/4 |
| M5. L1 线索卡和验证矩阵 | 打通多源证据链 | LeadCard、claim/evidence/status、置信度变化 | 全部 |
| M6. L3 报告模板 | 输出客户可读结果 | 海上通道风险报告、区域安全事件简报、设施韧性报告、导航完整性报告 | 全部 |
| M7. demo script 和 fixture | 保证演示稳定 | 冻结事件包、样例数据、截图/影像缓存、失败降级方案 | 全部 |

### 11.3 第一版 demo 的最小可行组合

第一版不要追求所有自动化。建议做一个“可解释、稳定、可复盘”的 fixture demo：

| 组件 | 最小要求 |
| --- | --- |
| 事件包 | 选 2 个主事件：一个海上通道安全事件，一个关键基础设施影响事件 |
| 数据 | 冻结事件窗口内的 UKMTO/JMIC/ACLED/新闻、AIS/ADS-B、FIRMS、Sentinel/SAR 元数据 |
| 本体 | 手工或半自动生成 `Observation`、`Event`、`EvidenceLink`、`VerificationMatrix` |
| UI | 地图展示 AOI、事件、证据层；点击事件显示 L1/L2/L3 |
| 报告 | 生成 Markdown/PDF 风格报告，结论先行，证据链可追溯 |
| 降级 | 外部 API 不可用时使用缓存数据，明确标识 `fixture` 或 `cached` |

## 12. 验收口径建议

### 12.1 场景级验收

每个场景都不应只验收“地图上有点”，而要验收情报链：

| 验收项 | 标准 |
| --- | --- |
| L1 线索 | 至少 2 类来源生成同一事件或同一 AOI 的线索 |
| L2 验证 | 至少 1 类遥感或权威源对 L1 claim 做支持、反驳或待确认标注 |
| L3 报告 | 报告包含结论、证据链、置信度、剩余不确定性、非进攻性建议 |
| 可追溯 | 任一结论能回到原始 source、采集时间、处理方式和分析师动作 |
| 可降级 | 外部数据源失败时 demo 不崩溃，能展示缓存和数据新鲜度 |

### 12.2 数据级验收

| 数据 | 最低验收 |
| --- | --- |
| AIS/ADS-B | 至少覆盖事件前后 7 天；关键指标有 90 天基线更好 |
| OSINT | 保留原文 URL、发布时间、抓取时间、语言、信源评分 |
| 影像 | 每个重点 AOI 至少 T0/T1；关键设施最好 T2/Tn |
| AOI | 港口、航道、设施必须是 polygon 或 route，不只是一组点 |
| 报告 | 报告中的每条关键判断至少有一条 source-backed evidence |

## 13. 主要风险与防护

| 风险 | 表现 | 防护措施 |
| --- | --- | --- |
| 实时事件事实变化 | 场景 2 的事件结论会随新闻更新变化 | demo 使用冻结事件包；live 数据仅作为“新增观察”显示 |
| 数据授权风险 | AIS、商业影像、ACLED、社媒数据可能有许可限制 | 明确 demo 数据来源、license、缓存策略和客户部署边界 |
| 误报风险 | 社媒旧视频、错误坐标、火点误匹配 | 建立 `RumorThread`、media hash、geolocation status、verification matrix |
| 敏感军事用途风险 | 被误解为进攻目标选择系统 | 产品文案和报告模板固定为民用保护、风险降级、持续监测 |
| 影像不可用 | 云、重访周期、商业影像成本 | 光学不可用时切 SAR；报告中解释数据缺口 |
| 当前项目能力被过度包装 | 现有项目更像地图底座，不是完整情报生产系统 | demo 明确区分“已具备底座”和“新增情报工作流” |

## 14. 结论

4 个场景都值得保留，但要重新组织成两条主线、四个能力包：

- 海上通道安全是第一主线，最适合阿联酋客户，也最适合展示 AIS、UKMTO/JMIC、GNSS、SAR 和 L3 通行风险报告。
- 导航完整性诊断应作为海上通道安全的关键证据能力，同时可在技术评审中单独展示。
- 区域安全事件信息降噪适合展示 OSINT 多源验证，但必须严格收边界，聚焦民用影响和传闻降级。
- 关键基础设施韧性监测是第二主线，最能打动决策层，尤其是港口、机场、能源、电力、海水淡化和数据中心。

当前项目已经有不少可复用素材：多源地图、AIS/ADS-B、GPS jamming 粗检测、新闻/GDELT/LiveUAMap、Sentinel-2、SAR catalog、FIRMS、电站/数据中心/机场和 AI 查询工具。但它还缺最关键的一层：统一本体、历史基线、证据链、验证矩阵、报告对象和持续监测任务。

所以，下一步不是先堆更多图层，而是先把 `Observation → Event → EvidenceLink → VerificationMatrix → IntelReport → MonitoringTask` 这条主干建起来。只要这条主干成立，4 个场景都可以成为同一套情报生产系统上的不同 demo 包。

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

- UKMTO: <https://www.ukmto.org/>
- ACLED conflict data: <https://acleddata.com/conflict-data>
- ACLED API documentation: <https://acleddata.com/api-documentation/getting-started>
- GPSJam: <https://gpsjam.org/>
- Flightradar24 GPS jamming: <https://www.flightradar24.com/data/gps-jamming>
- NASA FIRMS API: <https://firms.modaps.eosdis.nasa.gov/api/>
- ASF Search API: <https://docs.asf.alaska.edu/api/basics/>
- Microsoft Planetary Computer Sentinel-2 L2A: <https://planetarycomputer.microsoft.com/dataset/sentinel-2-l2a>
- AISStream documentation: <https://aisstream.io/documentation>
- OpenSky REST API: <https://openskynetwork.github.io/opensky-api/rest.html>
- GDELT: <https://www.gdeltproject.org/>
- NAVAREA IX: <https://hydrography.paknavy.gov.pk/navarea/>
- WRI Global Power Plant Database: <https://datasets.wri.org/datasets/global-power-plant-database>
- OSM Overpass API: <https://wiki.openstreetmap.org/wiki/Overpass_API>
- OurAirports data: <https://ourairports.com/data/>
- Natural Earth: <https://www.naturalearthdata.com/>
- UN/LOCODE: <https://unece.org/trade/uncefact/unlocode>
