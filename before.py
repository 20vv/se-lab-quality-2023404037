# after.py — 重构后的代码（消除坏味道）
# 重构手法：提取方法、消除重复、改善命名、去除魔法数字、单一职责

import math

# ===== 常量：消除魔法数字 =====
PASS_THRESHOLD = 60
GRADE_THRESHOLDS = [
    (90, "A"),
    (80, "B"),
    (70, "C"),
    (60, "D"),
]
DEFAULT_GRADE = "F"
NUM_SUBJECTS = 2


# ===== 重构 1：提取公共函数，消除重复代码 =====
# 原来 calculate_student_math_score / calculate_student_english_score 高度重复
# → 提取为通用的 calculate_subject_score，通过参数区分科目

def compute_average(scores: list[float]) -> float:
    """计算一组分数的平均值。"""
    return sum(scores) / len(scores)


def get_grade(average: float) -> str:
    """根据平均分返回等级。"""
    for threshold, grade in GRADE_THRESHOLDS:
        if average >= threshold:
            return grade
    return DEFAULT_GRADE


def get_pass_status(average: float) -> str:
    """根据平均分返回及格状态。"""
    return "Pass" if average >= PASS_THRESHOLD else "Fail"


def calculate_subject_score(name: str, subject: str, scores: list[float]) -> tuple[float, str]:
    """
    计算并打印某学生某科目的成绩信息。
    消除了重复的 Math / English 两个函数。
    """
    avg = compute_average(scores)
    grade = get_grade(avg)
    status = get_pass_status(avg)

    print(f"Student: {name}")
    print(f"Subject: {subject}")
    print(f"Average Score: {avg:.1f}")
    print(f"Grade: {grade}")
    print(f"Status: {status}")

    return avg, grade


# ===== 重构 2：拆解过长函数，遵循单一职责原则 =====
# 原 generate_full_report 函数承担了验证、计算、排序、打印、统计五项职责
# → 拆分为独立的小函数

def validate_students_data(students_data: list) -> bool:
    """验证学生数据是否合法。"""
    if not students_data:
        print("No data or empty data provided.")
        return False
    return True


def compute_student_result(student: dict) -> dict:
    """计算单个学生的各科平均分与综合平均分。"""
    math_avg = compute_average(student["math"])
    eng_avg = compute_average(student["english"])
    overall = (math_avg + eng_avg) / NUM_SUBJECTS
    return {
        "name": student["name"],
        "math_avg": math_avg,
        "eng_avg": eng_avg,
        "overall": overall,
    }


def sort_results_by_overall(results: list[dict]) -> list[dict]:
    """按综合成绩从高到低排序（使用内置 sorted，更 Pythonic）。"""
    return sorted(results, key=lambda r: r["overall"], reverse=True)


def print_student_result(rank: int, result: dict) -> None:
    """打印单个学生的成绩报告行。"""
    grade = get_grade(result["overall"])
    print(f"Rank #{rank}  Name: {result['name']}")
    print(f"  Math Avg   : {result['math_avg']:.1f}")
    print(f"  English Avg: {result['eng_avg']:.1f}")
    print(f"  Overall    : {result['overall']:.1f}")
    print(f"  Grade      : {grade}")
    print("-" * 40)


def print_class_summary(results: list[dict]) -> None:
    """打印班级统计摘要。"""
    class_avg = compute_average([r["overall"] for r in results])
    pass_count = sum(1 for r in results if r["overall"] >= PASS_THRESHOLD)
    fail_count = len(results) - pass_count
    print(f"Class Average: {class_avg:.1f}")
    print(f"Pass: {pass_count}  Fail: {fail_count}")


def generate_full_report(students_data: list) -> None:
    """
    生成完整成绩报告。
    职责：协调各子函数，完成验证→计算→排序→打印的流程。
    """
    if not validate_students_data(students_data):
        return

    results = [compute_student_result(s) for s in students_data]
    ranked = sort_results_by_overall(results)

    print("=" * 40)
    print("       STUDENT REPORT CARD        ")
    print("=" * 40)
    for rank, result in enumerate(ranked, start=1):
        print_student_result(rank, result)

    print_class_summary(ranked)
    print("=" * 40)


# ===== 重构 3：改善命名，去除无意义的参数名 =====
# 原函数 calc(a, b, c) 完全无法理解含义
# → 重命名为 compute_cylinder_geometry，参数改为语义清晰的名称

def compute_cylinder_geometry(lateral_height: float, radius: float, vertical_height: float) -> tuple[float, float]:
    """
    计算圆柱体的侧面积与体积。

    Args:
        lateral_height: 母线长度（斜高）
        radius: 底面半径
        vertical_height: 圆柱高度

    Returns:
        (lateral_surface_area, volume)
    """
    lateral_surface_area = math.pi * radius * lateral_height
    volume = (1 / 3) * math.pi * radius ** 2 * vertical_height
    return lateral_surface_area, volume


# ===== 主程序 =====
if __name__ == "__main__":
    # 使用统一的 calculate_subject_score 替代两个重复函数
    calculate_subject_score("Alice", "Math", [85, 90, 78, 92])
    calculate_subject_score("Alice", "English", [88, 76, 95, 83])

    students = [
        {"name": "Alice", "math": [85, 90, 78], "english": [88, 76, 95]},
        {"name": "Bob",   "math": [70, 65, 80], "english": [60, 72, 68]},
        {"name": "Carol", "math": [95, 98, 92], "english": [90, 85, 93]},
    ]
    generate_full_report(students)

    lateral_surface, volume = compute_cylinder_geometry(
        lateral_height=5, radius=3, vertical_height=10
    )
    print(f"Lateral Surface Area: {lateral_surface:.2f}")
    print(f"Volume: {volume:.2f}")
