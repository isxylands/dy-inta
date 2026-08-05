# 项目航迹数据高效查询手册

## 1. 三种查询面如何选择

| 查询面 | 适合 | 不适合 | 首选动作 |
| --- | --- | --- | --- |
| 外接盘海贝 CSV | 2—6 月长历史基线、字段画像、离线派生 | 反复交互扫描、近期新增数据 | 先读已有盘点和 `_derived`，只为缺口局部扫描 |
| `dh.trs.cn` API | 探测上游历史数据、按对象/AOI/时间补查、验证当前接口合同 | 稳定快照式大分页 | 小窗实测；超 1000 条按时间二分 |
| 航迹工作台 SQLite/API | 查询已经采集并标准化的快照、趋势、分布、延迟和质量 | 证明上游或现实世界绝对完整 | 先管理 API 聚合，再按需只读 SQL 下钻 |

不要在查证任务中启动采集、回填、备份、索引或历史处理。用户明确要求改变运行态时，另行按实施/运维流程处理。

## 2. 外接盘海贝 AIS/ADS-B

历史路径：

```text
/Volumes/exFAT466/海贝数据_2月1到6月15_AIS和ADS-B
```

已知规模和风险：

- AIS：5 个按月命名 CSV，约 642.8 万行；文件内存在跨月和少量异常时间。
- ADS-B：135 个逐日 CSV，约 1.662 亿行。
- 合计约 16GB、1.7267 亿遥测数据行。
- 原始 CSV 和大派生数据不进入 Git。

高效顺序：

1. 先读 `devdoc/海贝AIS-ADSB数据盘点与场景1-4Demo可用性分析.md`，不要重复已做的全量字段画像。
2. 用 `rg --files`/`find` 生成 manifest，记录路径、大小、mtime、行数和 `header_hash`；排除 `.done`、`.DS_Store`、`._*`、`~$*`。
3. 只抽表头、首尾小样本和目标日期/AOI，验证 schema、时间和字段质量。
4. 需要多轮查询时先生成 Parquet/DuckDB 派生层，按日期分区并预计算 AOI；不要继续直接扫 CSV。
5. AIS 必须按 `IR_LASTTIME` 重新分区，不按文件名月份统计。
6. AIS 暂用 `(MMSI, observed_time, lat, lon, speed, course)` 粗去重；有稳定 source event id 后改用源 ID。
7. ADS-B 保留 `source_date`、`IR_LASTTIME`、原始 `spd/alt/trak`，单位和异常编码未确认前不做速度或机动结论。

推荐派生目录：

```text
_derived/
  manifest/files.csv
  manifest/field_profile.csv
  parquet/ais_points/
  parquet/adsb_points/
  duckdb/haibei_ais_adsb.duckdb
  summary/daily_region_counts.csv
  summary/demo_window_inventory.csv
```

查询先聚合 `unique_targets` 和对象点数分布，再下钻 MMSI/ICAO。bbox 只适合初筛，正式结论使用 AOI polygon。

## 3. `dh.trs.cn` 航迹数据服务

基础地址和认证合同见 `devdoc/飞机与船舶航迹数据服务API实测与高效接入指南-20260731.md`。不要把用户名、密码、digest 或 token 写入命令、文档和日志。

端点：

```text
POST /base/osint/aircraft/adsb/list
POST /base/osint/ship/ais/list
```

共同参数：

- `startPubTime`、`endPubTime`：观测时间。
- `startLoadTime`、`endLoadTime`：入库时间；`endLoadTime` 已实测有效，旧文档重复写 `startLoadTime` 是笔误。
- `minLon`、`minLat`、`maxLon`、`maxLat`：矩形范围。
- `pageNum` 从 0 开始，`pageSize` 实测上限 1000。
- `sorts` 支持 `pubTime`、`loadTime`；`-` 前缀表示倒序。
- ADS-B 对象字段为 `icao`，AIS 为 `mmsi`。

必须同时检查 HTTP 状态与业务 `code`。无 token 时可能仍返回 HTTP 200、业务 `code=604`。

### 小样本探测

每次接口行为可能变化，先用 5—30 分钟、小 AOI、`pageSize=1000,pageNum=0` 验证：

1. 时间和空间过滤是否生效；
2. 结果是否支持 gzip；
3. 总量、字段和最大时间；
4. `receiveTime/lastdyn` 与 `loadTime` 的延迟；
5. 对照区有无数据；
6. 同一查询重复调用时总数是否变化。

### 避免不稳定分页

历史分页曾出现相邻请求总数变化和页间重复。不要用普通 `pageNum++` 追完整：

1. 取第 0 页、`pageSize=1000`。
2. `totalPages <= 1` 时保存并按 `id` 去重。
3. `totalPages > 1` 时丢弃不完整片，按时间中点二分。
4. 单秒仍超过一页时停止并告警。
5. 对最近片段做第二轮复扫，吸收补录和重整。

任何“完整”都只能写 `best_effort_complete` 或“采集侧闭合”，并附 `verified_at`、扫描轮次和上游可能修订说明。

### 增量和迟到数据

若用户另行授权采集方案设计：

- 仅在成功持久化后推进最大 `loadTime` 水位线；
- 重叠回看 30—60 分钟并按 `id` 幂等覆盖；
- 每日回看 24—48 小时；
- 保存请求参数、HTTP/业务码、`requestid`、记录数、最大观测时间、最大 `loadTime` 和响应 SHA-256。

## 4. 航迹工作台 SQLite 和管理 API

当前运行入口和版本可能变化，先从 `dy-track-explorer` 当前代码与目标环境现场确认。历史入口为：

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

时间窗必须半开 `[start, end)`；查询和比较使用 UTC。四个 bbox 参数必须同时出现。先用 distributions/trends 找高价值窗口，再用 observations 下钻，不要把全量明细拉到客户端统计。

### 直接 SQL 的使用边界

只有管理 API 不足以回答字段质量或复杂聚合，且已取得一致性只读副本或明确只读连接时，才直接查询 SQLite。不要在 live WAL 数据库上执行写操作、DDL、备份或深度完整性检查。

查询模板：

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

对象点数分布：

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
- `record_count`、`object_count`、`valid_object_count` 和多点对象数；
- 同一 MMSI 多 IMO、类别/尺寸突变等 identity conflict；
- AIS `heading/cog`、`rot/sog` 疑似映射错误；
- ADS-B `speed` 单位或高值异常；
- `processing_version`、pending 状态和数据知识截止时间。

## 5. 航迹证据解释门禁

| 观测 | 可以说 | 不能说 |
| --- | --- | --- |
| 单点 | 对象在该时刻被此数据源看见 | 连续路线、停留、改道、任务 |
| 稀疏多点 | 历史位置序列、方向候选 | 完整航迹或精确穿越 |
| 事件窗对象数高 | 当时可见活动背景较强 | 事件导致活动暴增 |
| 前后等长窗结构变化 | 支援或船型结构与事件窗重合 | 具体对象参战或因冲突改道 |
| 入库延迟大 | 适合历史回溯 | 系统当时已实时发现 |
| 空结果 | 当前查询面未返回 | 现实世界无活动 |

军用航空只展示区域、国家和机型聚合，不输出单机精确坐标或可用于实时跟踪的逐点航迹。商业船舶对象级历史点位仅用于航运安全和供应链复盘。
