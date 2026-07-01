# Bilibili热门视频数据分析

基于B站公开API采集热门视频数据，进行探索性数据分析（EDA）和可视化，挖掘不同分区视频的互动特征和传播规律。

## 项目结构

```
bilibili_analysis/
├── crawler.py          # 数据采集脚本
├── analysis.py         # 数据分析与可视化
├── requirements.txt    # 依赖包
├── data/
│   └── bilibili_videos.csv  # 采集的原始数据
├── output/
│   ├── 01_category_distribution.png
│   ├── 02_engagement_correlation.png
│   ├── 03_like_rate_by_category.png
│   ├── 04_upload_hour_distribution.png
│   ├── 05_top_up_engagement.png
│   ├── 06_duration_vs_views.png
│   └── 07_followers_vs_views.png
└── README.md
```

## 数据说明

通过 Bilibili 公开 API 采集了以下数据：

- **热门榜单**：综合热门推荐页，覆盖多个页码
- **分区排行**：动画、音乐、游戏、知识、美食、科技等12个分区
- **视频信息**：标题、描述、时长、发布时间
- **互动指标**：播放量、弹幕数、点赞、投币、收藏、分享、评论
- **UP主信息**：昵称、粉丝数

## 分析内容

1. **分区分布**：热门视频在各分区的数量分布
2. **互动相关性**：各指标之间的相关关系
3. **点赞率分析**：不同分区的平均点赞率差异
4. **发布时间规律**：视频发布时间与热度的关系
5. **UP主影响力**：高产UP主的互动表现
6. **视频时长**：时长与播放量的关系
7. **粉丝效应**：UP主粉丝数与播放量的关联

## 运行方式

```bash
# 安装依赖
pip install -r requirements.txt

# 采集数据（需联网）
python crawler.py

# 分析并生成图表
python analysis.py
```

## 结果示例

项目生成7张图表，涵盖分区分布、互动相关性、点赞率对比、发布时间规律和UP主影响力分析。

## 数据来源

数据通过 Bilibili 公开 REST API (`api.bilibili.com`) 采集，仅用于学习研究。