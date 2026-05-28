# run_all.py
# 一键顺序运行：main.py → analyze.py → plot.py
import os
import sys
import subprocess

def run_script(script_name):
    """运行指定的 Python 脚本"""
    print(f"\n========================================")
    print(f" 正在运行：{script_name} ...")
    print(f"========================================\n")
    
    # 运行脚本
    result = subprocess.run([sys.executable, script_name])
    
    # 如果出错，停止整个流程
    if result.returncode != 0:
        print(f"\n❌ {script_name} 运行失败！程序停止。")
        sys.exit(1)
    else:
        print(f"\n✅ {script_name} 运行成功！")

if __name__ == "__main__":
    print("🚀 豆瓣TOP250项目 一键启动")
    print("将按顺序执行：爬虫 → 数据分析 → 绘图\n")

    # 按顺序运行
    run_script("main.py")       # 1. 爬取数据 + 导出Excel
    run_script("analyze.py")    # 2. 清洗数据 + 生成报告
    run_script("plot.py")       # 3. 绘制三张图表

    print("\n🎉 全部执行完成！")
    print("📁 结果保存在：../数据文件夹/")