# ★☆☆☆☆
# 宇宙中最浪漫的事情，就是为喜欢的动画送上一颗星星
from RealScore import RealScore


def percentage_difference(a: float, b: float) -> float:
    diff = a - b
    percentage = (diff / b) * 100
    return percentage


def closest_number(n: float) -> int:
    closest = 2
    for i in [4, 6, 8, 10]:
        if abs(i - n) < abs(closest - n):
            closest = i
    return closest


def score(x: int) -> str:
    match x:
        case 2:
            return "★☆☆☆☆"
        case 4:
            return "★★☆☆☆"
        case 6:
            return "★★★☆☆"
        case 8:
            return "★★★★☆"
        case 10:
            return "★★★★★"
    return "☆☆☆☆☆"


media_id = input("请输入要查询的剧集的mdid(media_id):")
real_score = RealScore(media_id)
print(f"[{real_score.type_name}]{real_score.anime_title}的B站评分为{real_score.display_score}")
comments_average_score, short_comments_average_score, long_comments_average_score, score_distribution = real_score.calculate_scores()
compress_or_expand = ["缩水", "膨胀"]
real_and_display_percentage = percentage_difference(real_score.display_score, comments_average_score)
print(
    f"{real_score.anime_title}的真实评分为:{comments_average_score:.2f} {score(closest_number(comments_average_score))} ，显示的评分{real_score.display_score}相比真实评分{compress_or_expand[real_and_display_percentage >= 0]}了{abs(real_and_display_percentage):.3f}%，其中短评评分{short_comments_average_score:.3f}，长评评分{long_comments_average_score:.3f}")
print(f"得分分布：{score_distribution}")
