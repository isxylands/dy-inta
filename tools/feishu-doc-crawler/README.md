# 飞书智能纪要抓取适配器

这是 `crawl4ai` 的飞书/豆包文档站点适配层，用于抓取公开可访问或用户已获授权访问的智能纪要文档。

它不直接信任 `result.markdown`，而是分别处理：

- 纪要：进入同源文档 iframe，滚动虚拟列表直到高度稳定，按 `data-block-id` 去重并保留原始块结构。
- 原始记录：只捕获 `/minutes/doubao/api/subtitles_v2` 响应，选择 `size == total` 的完整响应并保留原始 JSON。
- 完整性：检查滚动是否稳定到达底部、章节覆盖、逐字稿分页闭合、段落数量、ID 重复和时间范围。
- 可追溯性：输出采集时间、真实 Chrome User-Agent、统计报告及文件 SHA-256。

## 环境

本机当前 `which python` 指向 `pyenv 3.11.7`，已安装 `crawl4ai 0.9.2`。检查：

```bash
python -c "import importlib.metadata; print(importlib.metadata.version('crawl4ai'))"
```

本工具直接使用本机 Chrome，不需要运行 `crawl4ai-setup`，也不会额外下载 Chromium。

注意：只有同样解析到该 `pyenv 3.11.7` 的项目能共享这次安装。激活 venv、设置项目级 `.python-version` 或直接调用当前 Homebrew `python3` 时，需要在对应环境安装依赖。

## 使用

在项目根目录直接调用一键脚本：

```bash
./crawler_feishu_doc.sh 'https://feishu.doubao.com/docx/文档Token'
```

从其他目录调用时使用脚本的绝对路径，输出默认落在当时的当前目录：

```bash
/Users/liushen/Documents/githubDevs/dy-inta/crawler_feishu_doc.sh \
  'https://feishu.doubao.com/docx/文档Token'
```

不传 `--output` 时，结果写入调用脚本时的当前目录。绝对路径和相对路径均可：

```bash
./crawler_feishu_doc.sh \
  'https://feishu.doubao.com/docx/文档Token' \
  --output ./feishu-output

./crawler_feishu_doc.sh \
  'https://feishu.doubao.com/docx/文档Token' \
  --output /absolute/path/to/feishu-output
```

脚本自动定位项目源码，并优先使用当前 `python`；如果当前 Python 没有安装 `crawl4ai`，会尝试已配置的 `pyenv 3.11.7`。也可通过 `CRAWLER_FEISHU_PYTHON` 显式指定 Python。

默认自动读取本机 Chrome 版本并构造匹配的 User-Agent。其他参数会原样透传，例如显式 User-Agent：

```bash
./crawler_feishu_doc.sh \
  'https://feishu.doubao.com/docx/文档Token' \
  --user-agent 'Mozilla/5.0 (...) Chrome/151.0.7922.108 Safari/537.36'
```

如果文档需要登录，只能使用用户已授权导出的 Playwright storage state：

```bash
./crawler_feishu_doc.sh \
  'https://feishu.doubao.com/docx/文档Token' \
  --storage-state /absolute/path/to/storage-state.json
```

底层 Python 入口仍可直接调用，其 `--output` 同样是可选参数：

```bash
PYTHONPATH=tools/feishu-doc-crawler/src \
  python -m feishu_doc_crawler \
  'https://feishu.doubao.com/docx/文档Token'
```

工具不会尝试绕过登录、权限控制或验证码，也不会自动读取个人 Chrome profile。

## 输出

| 文件 | 用途 |
| --- | --- |
| `minutes.md` | 纪要可读文本 |
| `minutes.blocks.json` | 按块保存的纪要原始结构，是纪要文本的审计真源 |
| `transcript.md` | 按段落和时间整理的原始记录 |
| `transcript.raw.json` | 飞书逐字稿接口原始响应，是原始记录文本和时间轴的审计真源 |
| `speakers.raw.json` | 飞书说话人映射原始响应，是发言人归属的审计真源 |
| `report.json` | 抓取参数、数量、完整性检查和警告 |
| `manifest.json` | 上述文件的 SHA-256 与字节数 |

若 `report.json` 中 `complete=false`，命令退出码为 `2`，不得把结果标记为完整抓取。

`minutes.md` 只渲染标题、正文、列表、引用和图片说明等语义块，避免把页面、页签、网格等父容器再次输出造成重复；完整原始块仍保留在 `minutes.blocks.json`。

当前范围是纪要和逐字稿文本。图片、画板、音频等二进制资源只保留块内引用，不承诺离线资源包完整；如需归档这些资源，应另加下载、权限和哈希校验流程。

## 测试

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```
