# 公开数据源最小查询手册

## 1. 通用顺序

1. 先用官方页面、RSS 或聚合搜索发现候选。
2. 回到原始 URL，保存标题、发布者、发布时间、正文摘要和采集时间。
3. 再用结构化观测回答时间、空间、数量或变化问题。
4. 对事件窗建立同口径前序窗和对照区，检查覆盖、新鲜度和零结果。
5. 命令只放占位符，不把 key、token、cookie 或内网凭据写进 Git。

所有命令仅是历史实测过的查询形态，端点和参数可能变化，使用前核对官方文档和当前服务条款。

## 2. 新闻发现与官方发布

### GDELT DOC 2.0

```bash
curl -L -G 'https://api.gdeltproject.org/api/v2/doc/doc' \
  --data-urlencode 'query="pause" Iran United States' \
  --data 'mode=artlist' \
  --data 'maxrecords=250' \
  --data 'format=json' \
  --data 'startdatetime=20260724000000' \
  --data 'enddatetime=20260729235959' \
  --data 'sort=datedesc'
```

GDELT 只用于发现。按规范标题、通讯社作者、正文相似度和原始 URL 归并转载；连续请求至少间隔数秒，并记录限流和空响应。

### 官方 RSS

```bash
curl -L 'https://www.whitehouse.gov/news/feed/'
curl -L 'https://en.irna.ir/rss'
curl -L 'https://www.fm.gov.om/en/feed/'
```

用 `guid` 或规范化 URL 去重，保存 `pubDate`、标题、摘要和正文链接。RSS 未命中只表示当前订阅结果未发现。

### 受网页防护的官方站点

先试低频 `curl -L -A 'Mozilla/5.0' <url>`。若明确遇到 Akamai/Cloudflare 等防护，不循环重试、不绕过访问控制；改用本机浏览器人工读取官方页面，保存页面 URL、标题、正文、发布时间和采集时间。仍不可访问时记录失败并寻找官方 RSS、公开频道或机构镜像。

## 3. 海事与船流

### NAVAREA IX 和 IMO

```bash
curl -L 'https://hydrography.paknavy.gov.pk/navarea-ix-warnings/'
curl -L -A 'Mozilla/5.0' \
  'https://www.imo.org/en/mediacentre/hottopics/pages/middle-east-highlighted-incidents.aspx'
```

NAVAREA 同时保存索引编号、下载文件名和 TXT 正文编号，以正文为准，并解析发布时间、位置、事件类型、有效/撤销关系。IMO 以船名与事件日期联合去重。两者未收录不等于事件未发生。

### IMF PortWatch

```bash
curl -L \
  'https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/Daily_Chokepoints_Data/FeatureServer/0/query?where=portid%3D%27chokepoint6%27&outFields=date,n_total,n_tanker,n_cargo,capacity&orderByFields=date%20DESC&resultRecordCount=100&f=json' \
  | jq '[.features[].attributes]'
```

`chokepoint6` 是霍尔木兹。分别记录观测日期与采集日期；计算最近 7 天、前 7 天和历史同期。PortWatch 是清洗后的日度通道指标，不是原始 AIS；`n_total` 也不代表所有船。

### AISStream 覆盖探测

WebSocket 建连后发送：

```json
{
  "APIKey": "<AISSTREAM_API_KEY>",
  "BoundingBoxes": [[[25.4, 55.4], [27.1, 57.5]]]
}
```

短时探测必须同时选一个已知有覆盖的对照区。记录连接是否成功、消息数、唯一 MMSI、首末时间和连接在线率。目标区为零且对照区有数据时，结论是“目标区接收覆盖不足或当时无返回”，不是“没有船”。

### Global Fishing Watch 4Wings

```bash
curl -L -X POST \
  'https://gateway.api.globalfishingwatch.org/v3/4wings/report?datasets%5B0%5D=public-global-presence%3Alatest&date-range=2026-07-01%2C2026-07-30&temporal-resolution=DAILY&spatial-resolution=LOW&group-by=VESSEL_ID&spatial-aggregation=true&format=JSON' \
  -H 'Authorization: Bearer <GFW_TOKEN>' \
  -H 'Content-Type: application/json' \
  --data '{
    "geojson": {
      "type": "Polygon",
      "coordinates": [[[55.5,25.5],[57.5,25.5],[57.5,27.2],[55.5,27.2],[55.5,25.5]]]
    }
  }'
```

先按接口返回的当前枚举验证 `group-by`；历史上 `VESSEL_TYPE` 返回过 HTTP 422，而 `VESSEL_ID` 可用。区域存在小时和唯一身份不等于固定断面穿越量。

## 4. 航空与天气

### ADSB.lol 固定口径快照

```bash
curl -L 'https://api.adsb.lol/v2/lat/26.5/lon/56.3/dist/100' \
  | jq '{
      observed_at: (now | todate),
      fresh: ([.ac[] | select((.seen // 999) <= 15)] | length),
      airborne_fresh: ([.ac[] |
        select((.seen // 999) <= 15 and
               .alt_baro != "ground" and
               .alt_baro != null)] | length)
    }'
```

多区域比较使用相同半径、相近采集时间、`seen` 阈值和地面目标口径。圆形快照只说明采样时有多少新鲜目标，不说明航班恢复率。

### OpenSky 同区域复核

```bash
curl -L \
  'https://opensky-network.org/api/states/all?lamin=25&lomin=54.5&lamax=28&lomax=58' \
  | jq '.states | length'
```

ADSB.lol 的圆形范围与 OpenSky 的矩形范围不能直接比较。先裁成同一 AOI，再统一新鲜度与地面/空中定义。

### METAR 天气排除

```bash
curl -L \
  'https://aviationweather.gov/api/data/metar?ids=OOMS,OMAA,OMDB,OIKB&format=json&hours=6' \
  | jq '[.[] | {icaoId, obsTime, visib, wdir, wspd, clouds, rawOb}]'
```

METAR 用于检查天气能否解释航空变化，不用于确认空域开放、机场正常或航班恢复。实际运行状态还需 NOTAM、机场与航司公告。

## 5. 热异常与卫星影像

### NASA FIRMS

```bash
curl -L \
  'https://firms.modaps.eosdis.nasa.gov/api/area/csv/<MAP_KEY>/VIIRS_SNPP_NRT/52,23,61,28.5/5/2026-07-24'
```

按 S-NPP、NOAA-20、NOAA-21 分开拉取，单次 `DAY_RANGE` 不超过接口当前上限。保存 `latitude`、`longitude`、`acq_date`、`acq_time`、`confidence`、`frp`、卫星和处理版本。用多日前序基线排除工业火炬等持续热源。只返回表头时写“尚无可用数据”或“未返回记录”，不要直接写现实为零。

### Copernicus STAC

```bash
curl -L -X POST 'https://stac.dataspace.copernicus.eu/v1/search' \
  -H 'Content-Type: application/json' \
  --data '{
    "collections": ["sentinel-1-grd"],
    "bbox": [55.5, 25.5, 57.5, 27.2],
    "datetime": "2026-07-15T00:00:00Z/2026-07-29T23:59:59Z",
    "limit": 100
  }' \
  | jq '[.features[] | {id, datetime: .properties.datetime, bbox}]'
```

目录检索先回答“有没有场景和覆盖”，不能替代影像判读。下载前检查 footprint、轨道、极化和相近轨道对照。

### Earth Search

```bash
curl -L -X POST 'https://earth-search.aws.element84.com/v1/search' \
  -H 'Content-Type: application/json' \
  --data '{
    "collections": ["sentinel-2-l2a"],
    "bbox": [55.5, 25.5, 57.5, 27.2],
    "datetime": "2026-07-15T00:00:00Z/2026-07-29T23:59:59Z",
    "limit": 100
  }' \
  | jq '[.features[] | {
    id,
    datetime: .properties.datetime,
    cloud: .properties["eo:cloud_cover"],
    visual: .assets.visual.href
  }]'
```

先按云量、覆盖、日期和对照时相筛选；读取 COG 目标窗口，避免无目的整景下载。

## 6. 网络与市场

### IODA 国家级告警

```bash
curl -L -G 'https://api.ioda.inetintel.cc.gatech.edu/v2/outages/alerts' \
  --data-urlencode 'entityType=country' \
  --data-urlencode 'entityCode=IR' \
  --data-urlencode 'from=<UTC_EPOCH_SECONDS>' \
  --data-urlencode 'until=<UTC_EPOCH_SECONDS>' \
  | jq .
```

同时查看 `critical` 与恢复记录，再下钻地区、ASN 和原始信号。BGP 异常不能单独说明原因。

### Yahoo Finance 事件窗

```bash
curl -L -A 'Mozilla/5.0' \
  'https://query1.finance.yahoo.com/v8/finance/chart/CL%3DF?range=5d&interval=5m&includePrePost=true'
```

保存时区、时间戳、OHLC 和 `regularMarketPreviousClose`。事件时点在休市空档时使用事件前最后可交易样本。跨资产比较统一基点，接口限流或失败时不得沿用旧缓存冒充当前行情。

## 7. ACLED 权限探测

OAuth 凭据只从受控环境变量读取。先验证 token，再用极小国家/日期窗请求事件。若 token 成功但事件接口为 HTTP 403，应写“认证成功、账号缺事件访问级别或许可”，不能写成参数错误，也不能把 ACLED 列为本轮已取得证据。

## 8. 每次查询的最小留痕

至少保存：

- 原始 URL 或 endpoint；
- 完整查询参数的脱敏副本；
- 采集时间和数据覆盖时间；
- HTTP 状态、业务状态、错误体摘要；
- 最新数据时间和数据新鲜度；
- 返回记录数、唯一对象数或场景数；
- 原始响应摘要/SHA-256；
- 覆盖、许可、限流和已知解释边界。
