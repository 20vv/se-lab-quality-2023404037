# before.py — 包含多种"代码坏味道"的示例代码
# 坏味道包括：重复代码、过长函数、未使用变量、魔法数字、命名不规范

import math

# ===== 坏味道 0：硬编码密码（Hard-coded credentials） =====
# SonarCloud 会将此识别为 High 严重性的 Security Hotspot / Code Smell
DB_PASSWORD = "admin123"        # 坏味道：硬编码密码
API_KEY = "sk-abc123secret"     # 坏味道：硬编码密钥

# ===== 坏味道 1：重复代码（Duplicated blocks of code） =====
# 两个函数逻辑几乎完全相同，仅目标科目不同

def calculate_student_math_score(name, scores):
    total = 0
    count = 0
    unused_flag = True          # 坏味道：未使用的变量
    for s in scores:
        total = total + s
        count = count + 1
    avg = total / count
    if avg >= 90:
        grade = "A"
    elif avg >= 80:
        grade = "B"
    elif avg >= 70:
        grade = "C"
    elif avg >= 60:
        grade = "D"
    else:
        grade = "F"
    print("Student: " + name)
    print("Subject: Math")
    print("Average Score: " + str(avg))
    print("Grade: " + grade)
    if avg >= 60:
        print("Status: Pass")
    else:
        print("Status: Fail")
    return avg, grade


def calculate_student_english_score(name, scores):
    total = 0
    count = 0
    unused_var = []             # 坏味道：未使用的变量
    for s in scores:
        total = total + s
        count = count + 1
    avg = total / count
    if avg >= 90:
        grade = "A"
    elif avg >= 80:
        grade = "B"
    elif avg >= 70:
        grade = "C"
    elif avg >= 60:
        grade = "D"
    else:
        grade = "F"
    print("Student: " + name)
    print("Subject: English")
    print("Average Score: " + str(avg))
    print("Grade: " + grade)
    if avg >= 60:
        print("Status: Pass")
    else:
        print("Status: Fail")
    return avg, grade


# ===== 坏味道 2：过长函数（Method has too many lines） =====
# 一个函数承担了过多职责：读取数据、计算、格式化、输出报告

def generate_full_report(students_data):
    # 步骤1：验证数据
    if students_data is None:
        print("No data")
        return
    if len(students_data) == 0:
        print("Empty data")
        return

    # 步骤2：计算每位学生各科平均分
    results = []
    for student in students_data:
        name = student["name"]
        math_scores = student["math"]
        english_scores = student["english"]

        math_total = 0
        for s in math_scores:
            math_total += s
        math_avg = math_total / len(math_scores)

        eng_total = 0
        for s in english_scores:
            eng_total += s
        eng_avg = eng_total / len(english_scores)

        overall = (math_avg + eng_avg) / 2   # 坏味道：魔法数字 2（科目数硬编码）

        results.append({
            "name": name,
            "math_avg": math_avg,
            "eng_avg": eng_avg,
            "overall": overall
        })

    # 步骤3：排序
    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            if results[j]["overall"] > results[i]["overall"]:
                results[i], results[j] = results[j], results[i]

    # 步骤4：打印报告
    print("=" * 40)
    print("       STUDENT REPORT CARD        ")
    print("=" * 40)
    rank = 1
    for r in results:
        print(f"Rank #{rank}  Name: {r['name']}")
        print(f"  Math Avg   : {r['math_avg']:.1f}")
        print(f"  English Avg: {r['eng_avg']:.1f}")
        print(f"  Overall    : {r['overall']:.1f}")
        if r["overall"] >= 90:
            print("  Grade: A")
        elif r["overall"] >= 80:
            print("  Grade: B")
        elif r["overall"] >= 70:
            print("  Grade: C")
        elif r["overall"] >= 60:
            print("  Grade: D")
        else:
            print("  Grade: F")
        print("-" * 40)
        rank += 1

    # 步骤5：统计班级情况
    total_overall = 0
    pass_count = 0
    fail_count = 0
    for r in results:
        total_overall += r["overall"]
        if r["overall"] >= 60:                # 坏味道：魔法数字 60 多次重复
            pass_count += 1
        else:
            fail_count += 1
    class_avg = total_overall / len(results)
    print(f"Class Average: {class_avg:.1f}")
    print(f"Pass: {pass_count}  Fail: {fail_count}")
    print("=" * 40)


# ===== 坏味道 3：命名不规范（Poor naming） =====

def calc(a, b, c):              # 函数名和参数名毫无语义
    x = a * b * b               # 不知道 x 代表什么
    y = (1/3) * math.pi * b * b * c   # 魔法数字 1/3、以及含义不清的字母
    return x, y


# ===== 主程序 =====
if __name__ == "__main__":
    calculate_student_math_score("Alice", [85, 90, 78, 92])
    calculate_student_english_score("Alice", [88, 76, 95, 83])

    students = [
        {"name": "Alice", "math": [85, 90, 78], "english": [88, 76, 95]},
        {"name": "Bob",   "math": [70, 65, 80], "english": [60, 72, 68]},
        {"name": "Carol", "math": [95, 98, 92], "english": [90, 85, 93]},
    ]
    generate_full_report(students)

    lateral_surface, volume = calc(5, 3, 10)
    print(f"Result: {lateral_surface}, {volume}")
