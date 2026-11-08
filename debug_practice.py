# -*- coding: utf-8 -*-
"""
学生成绩统计脚本
本脚本故意包含 6 个 bug，类型各不相同：
语法错误、逻辑错误、类型错误、空值比较、除零风险、可变默认参数陷阱
练习目标：先运行，读报错信息逐个修复；全部修完后，验证输出是否正确。
"""

students = {
    "小明": [85, 92, 78],
    "小红": [90, 88, 95],
    "小刚": [60, 55, 70],
}


def average(scores):
    total = 0
    for i in range(1, len(scores)):  # 提示：平均分真的算对了吗？
        total = total + scores[i]
    return total / len(scores)


def pass_rate(all_scores):
    count = 0
    for scores in all_scores:
        if average(scores) >= 60  # 提示：运行时会先在这里报错
            count += 1
    return count / len(all_scores)


def report():
    print("各学生平均分：")
    for name, scores in students.items():
        print(name + "的平均分是" + average(scores))

    top = None
    for name in students:
        if average(students[name]) > average(top):
            top = name
    print("平均分最高的是：" + top)


def add_bonus(scores=[0]):
    scores.append(99)
    return scores


if __name__ == "__main__":
    report()
    print("及格率：", pass_rate(list(students.values())))
    print(add_bonus([]))
    print(add_bonus())
