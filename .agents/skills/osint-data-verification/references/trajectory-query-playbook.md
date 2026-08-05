# 195 环境航迹数据高效查询手册

## 1. 查询范围和边界

本 skill 查询内部 AIS/ADS-B 时，唯一数据源是 195 环境航迹工作台已经采集并标准化的 SQLite 数据。优先通过工作台只读管理 API 访问该 SQLite；API 只是访问入口，不构成第二数据源。不得自动改查其他内网接口、外接存储或历史原始文件。

工作台适合查询：

- 指定时间窗和区域内的记录数、对象数、类型或国家分布；
- 指定 ICAO、MMSI、registration 或 IMO 的历史观测；
- 事件窗、前序窗和基线窗的结构差异；
- 字段质量、身份冲突、入库延迟和数据知识截止时间。

工作台不适合证明上游采集或现实世界绝对完整。不要在查证任务中启动采集、回填、备份、索引、DDL 或历史处理；用户明确要求改变运行态时，另行按实施或运维流程处理。

## 2. 入口与现场确认

当前部署、schema 和 API 可能变化，先从 `dy-track-explorer` 当前代码与 195 目标环境现场确认，不照抄历史合同。历史管理入口为：

```text
http://192.168.211.195:8080/admin/observations
```

优先使用只读 API：

- `GET /api/v1/observations`
- `GET /api/v1/observation-distributions?dimension=category|country`
- `GET /api/v1/observation-trends`
- `GET /api/v1/observations/{id}/explorer-preset`

`/api/v1/observations` 常用参数：

```text
dataset=adsb|ais
objectId=<ICAO-or-MMSI>
nameOrModel=<text>
registryId=<registration-or-IMO>
category=<category>
country=<country>
startTime=<RFC3339-with-timezone>
endTime=<RFC3339-with-timezone>
minLon=<number>&minLat=<number>&maxLon=<number>&maxLat=<number>
minCollectionDelaySeconds=<integer>
maxCollectionDelaySeconds=<integer>
orderBy=observedAt|collectionDelay
order=asc|desc
limit=10|20|30|50
offset=<integer>
```

时间窗统一使用 UTC 半开区间 `[start, end)`。四个 bbox 参数必须同时出现。不要在文档、命令或日志中保存凭据、会话信息或完整敏感点位。

## 3. 高效查询顺序

1. 冻结命题、时间窗、AOI、数据集和判定条件。
2. 先调用 distributions/trends，确认数据新鲜度、覆盖和高价值窗口。
3. 再调用 observations，以小 `limit` 验证字段、排序、过滤和对象标识。
4. 先统计 `record_count`、`object_count`、`valid_object_count` 和多点对象数，再下钻具体对象。
5. 对异常对象查询事件前记录，区分“此前已存在”和“事件窗新出现”。
6. API 无法完成复杂聚合时，才使用明确只读的 SQLite 连接或一致性只读副本。
7. 保存脱敏后的查询参数、采集时间、响应摘要、知识截止时间和必要的校验值。

事件查证至少比较事件窗与前一日同钟点；判断异常时补 14—28 天同星期同时段基线。bbox 只适合初筛，正式地理结论应使用项目已定义的 AOI polygon 或说明矩形近似误差。

## 4. SQLite 只读查询

直接查询 SQLite 前确认数据库路径、表名、字段和运行模式。不要在 live WAL 数据库执行写操作、DDL、备份或深度完整性检查。能够使用一致性只读副本时优先使用副本。

窗口聚合模板：

```sql
SELECT
  dataset,
  count(*) AS records,
  count(DISTINCT object_id) AS objects,
  min(observed_at) AS min_observed_at,
  max(observed_at) AS max_observed_at,
  max(loaded_at) AS max_loaded_at
FROM track_observation
WHERE observed_at >= :start_utc
  AND observed_at <  :end_utc
  AND lon >= :min_lon AND lon <= :max_lon
  AND lat >= :min_lat AND lat <= :max_lat
GROUP BY dataset;
```

对象点数分布模板：

```sql
WITH object_points AS (
  SELECT object_id, count(*) AS points
  FROM track_observation
  WHERE dataset = :dataset
    AND observed_at >= :start_utc
    AND observed_at <  :end_utc
    AND lon >= :min_lon AND lon <= :max_lon
    AND lat >= :min_lat AND lat <= :max_lat
  GROUP BY object_id
)
SELECT points, count(*) AS objects
FROM object_points
GROUP BY points
ORDER BY points;
```

必须同时检查：

- `observed_at` 与 `loaded_at`，并计算 `collection_delay_seconds`；
- 记录数、对象数、有效对象数和多点对象数；
- 同一 MMSI 多 IMO、类别或尺寸突变等 identity conflict；
- AIS `heading/cog`、`rot/sog` 的映射与单位；
- ADS-B `speed`、`altitude` 的单位、异常编码和高值；
- `processing_version`、pending 状态和数据知识截止时间。

## 5. 证据解释门禁

| 观测 | 可以说 | 不能说 |
| --- | --- | --- |
| 单点 | 对象在该时刻被工作台数据看见 | 连续路线、停留、改道、任务 |
| 稀疏多点 | 历史位置序列、方向候选 | 完整航迹或精确穿越 |
| 事件窗对象数高 | 当时可见活动背景较强 | 事件导致活动暴增 |
| 前后等长窗结构变化 | 支援或船型结构与事件窗重合 | 具体对象参战或因冲突改道 |
| 入库延迟大 | 适合历史回溯 | 系统当时已实时发现 |
| 空结果 | 当前工作台和查询条件未返回 | 现实世界无活动 |

军用航空只展示历史、区域、国家和机型聚合，不输出单机实时精确坐标或可用于持续跟踪的逐点航迹。商业船舶对象级历史点位仅用于航运安全、民用基础设施保护和供应链复盘。
