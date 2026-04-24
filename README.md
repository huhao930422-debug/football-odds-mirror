# Football Odds Mirror

完整镜像 [football-data.co.uk](https://www.football-data.co.uk) 的足球比赛数据，包含完整的博彩赔率和统计信息。

## 数据来源

数据来自 Joseph Buchdahl 的 Football-Data.co.uk 网站，该网站自 2001 年起提供欧洲主流联赛的历史数据，每周更新两次（周日和周三晚上）。

## 覆盖联赛

- **英超** (Premier League) - 1993/94 至今
- **西甲** (La Liga) - 1993/94 至今
- **意甲** (Serie A) - 1993/94 至今
- **德甲** (Bundesliga) - 1993/94 至今
- **法甲** (Ligue 1) - 1993/94 至今

## 数据字段

每个 CSV 文件包含 100+ 列数据，包括：

- 比赛基本信息（日期、主客队、比分）
- 裁判信息和犯规统计
- 多家博彩公司的赔率数据：
  - Bet365, Pinnacle, William Hill, Interwetten 等
  - 1X2 赔率（主胜/平局/客胜）
  - 亚洲盘口（Asian Handicap）
  - 大小球盘口（Over/Under）
  - 收盘赔率（Closing odds）

## 目录结构

```
data/
├── premier-league/
│   ├── season-9394.csv
│   ├── season-9495.csv
│   └── ...
├── la-liga/
├── serie-a/
├── bundesliga/
└── ligue-1/
```

## 更新频率

GitHub Actions 每天 UTC 05:00 自动运行，检查并下载最新数据。

## 使用方法

直接克隆仓库或下载所需的 CSV 文件：

```bash
git clone https://github.com/huhao930422-debug/football-odds-mirror.git
```

## 许可声明

数据版权归 football-data.co.uk 所有。本仓库仅作为数据镜像，方便自动化访问和版本控制。请遵守原网站的使用条款。
