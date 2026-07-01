# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os, warnings
warnings.filterwarnings("ignore")

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DengXian"]
plt.rcParams["axes.unicode_minus"] = False

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE, "data", "bilibili_videos.csv")
OUTPUT_DIR = os.path.join(BASE, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_and_prep():
    df = pd.read_csv(DATA_PATH)
    df = df[df["views"] > 0].copy()
    # compute derived metrics
    df["like_rate"] = df["likes"] / df["views"]
    df["danmaku_rate"] = df["danmaku"] / df["views"]
    df["coin_rate"] = df["coins"] / df["views"]
    df["fav_rate"] = df["favorites"] / df["views"]
    df["duration_min"] = df["duration"] / 60
    return df

def plot_1_category(df):
    cats = df["category_name"].value_counts().head(12)
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = plt.cm.Set2(np.linspace(0, 1, len(cats)))
    ax.barh(range(len(cats)), cats.values, color=colors, edgecolor="white", height=0.7)
    ax.set_yticks(range(len(cats)))
    ax.set_yticklabels(cats.index, fontsize=10)
    ax.set_xlabel("视频数量", fontsize=11)
    ax.set_title("B站热门视频 · 分区分布 (Top 12)", fontsize=13, fontweight="bold")
    for i, v in enumerate(cats.values):
        ax.text(v + 2, i, str(v), va="center", fontsize=9)
    ax.invert_yaxis()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "01_category_distribution.png"), dpi=150, bbox_inches="tight")
    plt.close()

def plot_2_corr(df):
    cols = ["views","likes","coins","favorites","shares","danmaku","reply"]
    corr = df[cols].corr()
    labels = ["播放","点赞","投币","收藏","分享","弹幕","评论"]
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(corr, cmap="RdYlBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(cols)))
    ax.set_yticks(range(len(cols)))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_yticklabels(labels, fontsize=9)
    for i in range(len(cols)):
        for j in range(len(cols)):
            v = corr.iloc[i, j]
            c = "white" if abs(v) > 0.6 else "black"
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=8, color=c)
    ax.set_title("互动指标相关性矩阵", fontsize=13, fontweight="bold")
    plt.colorbar(im, ax=ax, shrink=0.8)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "02_engagement_correlation.png"), dpi=150, bbox_inches="tight")
    plt.close()

def plot_3_like_rate(df):
    d = df[df["views"] > 100].copy()
    stats = d.groupby("category_name").agg(
        avg_like_rate=("like_rate", "mean"),
        count=("bvid", "count")
    ).query("count >= 5").sort_values("avg_like_rate", ascending=False).head(15)
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(stats)))
    vals = stats["avg_like_rate"].values * 100
    ax.barh(range(len(stats)), vals, color=colors, edgecolor="white", height=0.7)
    ax.set_yticks(range(len(stats)))
    ax.set_yticklabels(stats.index, fontsize=9)
    ax.set_xlabel("平均点赞率 (%)", fontsize=11)
    ax.set_title("各分区视频 · 平均点赞率 (Top 15)", fontsize=13, fontweight="bold")
    for i, v in enumerate(vals):
        ax.text(v + 0.2, i, f"{v:.1f}%", va="center", fontsize=8)
    ax.invert_yaxis()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "03_like_rate_by_category.png"), dpi=150, bbox_inches="tight")
    plt.close()

def plot_4_hour(df):
    hours = df["upload_hour"].value_counts().sort_index()
    hours_pct = hours / hours.sum() * 100
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ["#e74c3c" if v > hours_pct.median() else "#3498db" for v in hours_pct.values]
    ax.bar(hours_pct.index, hours_pct.values, color=colors, edgecolor="white", width=0.8)
    ax.set_xlabel("发布小时 (0-23)", fontsize=11)
    ax.set_ylabel("占比 (%)", fontsize=11)
    ax.set_title("B站热门视频 · 发布时间分布", fontsize=13, fontweight="bold")
    ax.set_xticks(range(0, 24))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for i, v in enumerate(hours_pct.values):
        if v > 3:
            ax.text(i, v + 0.3, f"{v:.1f}%", ha="center", fontsize=7)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "04_upload_hour_distribution.png"), dpi=150, bbox_inches="tight")
    plt.close()

def plot_5_top_up(df):
    up = df.groupby("up_name").agg(
        total_views=("views", "sum"),
        total_likes=("likes", "sum"),
        count=("bvid", "count")
    ).query("count >= 3").sort_values("total_views", ascending=False).head(12)
    fig, ax1 = plt.subplots(figsize=(10, 5.5))
    x = range(len(up))
    ax1.bar(x, up["total_views"].values / 10000, color="#3498db", alpha=0.8, width=0.5, label="总播放 (万)")
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(up.index, rotation=30, ha="right", fontsize=8)
    ax1.set_ylabel("总播放量 (万)", fontsize=11, color="#3498db")
    ax2 = ax1.twinx()
    ax2.plot(x, up["total_likes"].values / 10000, "o-", color="#e74c3c", linewidth=2, markersize=6, label="总点赞 (万)")
    ax2.set_ylabel("总点赞量 (万)", fontsize=11, color="#e74c3c")
    ax1.set_title("高产UP主 · 播放与点赞表现对比 (Top 12)", fontsize=13, fontweight="bold")
    ax1.spines["top"].set_visible(False)
    l1, lb1 = ax1.get_legend_handles_labels()
    l2, lb2 = ax2.get_legend_handles_labels()
    ax1.legend(l1 + l2, lb1 + lb2, loc="upper left", fontsize=9)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "05_top_up_engagement.png"), dpi=150, bbox_inches="tight")
    plt.close()

def plot_6_duration(df):
    d = df[(df["duration"] > 30) & (df["duration"] < 3600)].copy()
    fig, ax = plt.subplots(figsize=(10, 5))
    sc = ax.scatter(d["duration_min"], d["views"], c=np.log1p(d["likes"]),
                    cmap="viridis", alpha=0.5, s=15, edgecolors="none")
    ax.set_xlabel("视频时长 (分钟)", fontsize=11)
    ax.set_ylabel("播放量", fontsize=11)
    ax.set_title("视频时长 vs 播放量 · 颜色表示点赞数", fontsize=13, fontweight="bold")
    plt.colorbar(sc, ax=ax, label="点赞数 (log)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "06_duration_vs_views.png"), dpi=150, bbox_inches="tight")
    plt.close()

def plot_7_top_analytics(df):
    """Top 10 categories engagement comparison"""
    cats = df.groupby("category_name").agg(
        avg_views=("views", "mean"),
        avg_likes=("likes", "mean"),
        avg_coins=("coins", "mean"),
        count=("bvid", "count")
    ).query("count >= 5").sort_values("avg_views", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(cats))
    w = 0.25
    ax.bar([i - w for i in x], cats["avg_likes"].values / 10000, w, color="#e74c3c", alpha=0.8, label="平均点赞 (万)")
    ax.bar(x, cats["avg_coins"].values / 10000, w, color="#f39c12", alpha=0.8, label="平均投币 (万)")
    ax.set_xticks(list(x))
    ax.set_xticklabels(cats.index, rotation=25, ha="right", fontsize=9)
    ax.set_ylabel("互动量 (万)", fontsize=11)
    ax.set_title("高播放分区 · 点赞与投币对比 (Top 10)", fontsize=13, fontweight="bold")
    ax.legend(fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "07_top_category_engagement.png"), dpi=150, bbox_inches="tight")
    plt.close()

def main():
    print("=" * 50)
    print("B站热门视频数据分析")
    print("=" * 50)
    df = load_and_prep()
    print(f"加载数据: {len(df)} 条")
    print(f"数据日期: {df['upload_date'].min()} ~ {df['upload_date'].max()}")
    print(f"覆盖分区: {df['category_name'].nunique()} 个")
    print(f"UP主数量: {df['up_name'].nunique()}")
    print(f"\n开始生成图表...")
    plot_1_category(df)
    print("  [1/7] 分区分布")
    plot_2_corr(df)
    print("  [2/7] 相关性矩阵")
    plot_3_like_rate(df)
    print("  [3/7] 点赞率分析")
    plot_4_hour(df)
    print("  [4/7] 发布时间分布")
    plot_5_top_up(df)
    print("  [5/7] UP主表现")
    plot_6_duration(df)
    print("  [6/7] 时长 vs 播放量")
    plot_7_top_analytics(df)
    print("  [7/7] 分区互动对比")
    print(f"\n全部完成！图表已保存至: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()