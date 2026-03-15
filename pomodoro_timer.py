#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
番茄钟倒计时器 (Pomodoro Timer)

功能说明：
- 用户可以输入专注时间（分钟）
- 程序开始倒计时，每秒刷新显示剩余时间
- 时间结束时，播放提示音（Windows 使用 beep，其他平台使用打印字符模拟）
- 支持用户中途按 'q' 键退出

作者：Python Assistant
版本：1.0.0
"""

import time
import sys
import os
import threading
from typing import Optional


# 全局标志，用于控制倒计时是否继续运行
is_running = False
should_exit = False


def clear_screen():
    """清屏函数，兼容 Windows 和 Unix 系统"""
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception:
        # 如果清屏失败，打印空行
        print("\n" * 3)


def play_notification_sound():
    """
    播放提示音
    Windows 系统使用系统 beep 声音
    其他系统使用打印字符模拟
    """
    try:
        if os.name == 'nt':
            # Windows 系统播放 beep 音
            import winsound
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        else:
            # Unix/Linux/Mac 系统尝试播放声音
            print('\a')  # 终端响铃字符
    except Exception:
        # 如果播放失败，使用打印字符模拟
        pass


def format_time(seconds: int) -> str:
    """
    将秒数格式化为 MM:SS 格式

    参数:
        seconds: 剩余秒数

    返回:
        格式化后的时间字符串，如 "25:00"
    """
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def display_timer(remaining_seconds: int, total_seconds: int):
    """
    显示倒计时界面

    参数:
        remaining_seconds: 剩余秒数
        total_seconds: 总秒数（用于计算进度）
    """
    clear_screen()

    # 计算进度百分比
    progress = ((total_seconds - remaining_seconds) / total_seconds) * 100

    # 计算进度条长度（30 个字符宽度）
    bar_length = 30
    filled_length = int(bar_length * remaining_seconds / total_seconds)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)

    # 打印倒计时界面
    print("=" * 50)
    print("           🍅 番茄钟倒计时器 🍅")
    print("=" * 50)
    print()
    print(f"           剩余时间: {format_time(remaining_seconds)}")
    print()
    print(f"           [{bar}]")
    print(f"           进度: {100 - progress:.1f}%")
    print()
    print("-" * 50)
    print("  提示: 按 'q' 键然后回车可退出倒计时")
    print("=" * 50)


def check_exit_input():
    """
    在后台线程中检查用户是否输入 'q' 键退出
    使用非阻塞方式读取输入
    """
    global should_exit

    while is_running and not should_exit:
        try:
            # 使用非阻塞方式读取输入（仅适用于 Unix 系统）
            # Windows 系统使用另一种方式
            if os.name == 'nt':
                # Windows: 使用 msvcrt 检查按键
                import msvcrt
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8', errors='ignore').lower()
                    if key == 'q':
                        should_exit = True
                        break
            else:
                # Unix/Linux/Mac: 使用 select 检查输入
                import select
                import termios
                import tty

                # 保存当前终端设置
                old_settings = termios.tcgetattr(sys.stdin)
                try:
                    # 设置终端为原始模式
                    tty.setcbreak(sys.stdin.fileno())
                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        key = sys.stdin.read(1).lower()
                        if key == 'q':
                            should_exit = True
                            break
                finally:
                    # 恢复终端设置
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

        except Exception:
            # 如果检测输入失败，继续运行
            pass

        time.sleep(0.1)


def get_user_input():
    """
    获取用户输入的专注时间

    返回:
        用户输入的分钟数，如果输入无效则返回默认值 25
    """
    while True:
        try:
            user_input = input("请输入专注时间（分钟，默认 25 分钟，直接回车使用默认）: ").strip()

            # 如果用户直接回车，使用默认值 25
            if user_input == '':
                return 25

            # 尝试将输入转换为整数
            minutes = int(user_input)

            # 验证输入范围
            if minutes <= 0:
                print("⚠️  时间必须大于 0 分钟，请重新输入！")
                continue
            if minutes > 180:
                print("⚠️  建议专注时间不超过 3 小时（180 分钟），请重新输入！")
                continue

            return minutes

        except ValueError:
            print("⚠️  输入无效，请输入一个整数！")
        except KeyboardInterrupt:
            print("\n\n程序已被用户中断。")
            sys.exit(0)


def countdown(minutes: int):
    """
    倒计时主函数

    参数:
        minutes: 专注时间的分钟数
    """
    global is_running, should_exit

    total_seconds = minutes * 60
    remaining_seconds = total_seconds

    is_running = True
    should_exit = False

    # 启动后台线程监听退出按键
    exit_thread = threading.Thread(target=check_exit_input, daemon=True)
    exit_thread.start()

    try:
        while remaining_seconds > 0 and not should_exit:
            # 显示倒计时界面
            display_timer(remaining_seconds, total_seconds)

            # 等待 1 秒
            time.sleep(1)

            # 减少剩余时间
            remaining_seconds -= 1

        # 显示最终状态
        if should_exit:
            clear_screen()
            print("\n" + "=" * 50)
            print("           ⏹️  倒计时已被用户取消")
            print("=" * 50)
        else:
            # 倒计时结束，显示完成界面
            display_timer(0, total_seconds)
            print("\n" + "=" * 50)
            print("           ✅ 专注时间结束！")
            print("=" * 50)

            # 播放提示音
            play_notification_sound()

            # 播放多次提示音
            for _ in range(3):
                time.sleep(0.5)
                play_notification_sound()

    except KeyboardInterrupt:
        clear_screen()
        print("\n" + "=" * 50)
        print("           ⏹️  倒计时已被用户中断")
        print("=" * 50)

    finally:
        is_running = False


def main():
    """
    程序主入口函数
    """
    try:
        clear_screen()

        # 打印程序欢迎信息
        print("=" * 50)
        print("      🍅 欢迎使用番茄钟倒计时器 🍅")
        print("=" * 50)
        print()
        print("  番茄工作法：专注工作 25 分钟，然后休息 5 分钟")
        print()

        # 获取用户输入的专注时间
        minutes = get_user_input()

        print(f"\n⏱️  倒计时即将开始，专注时间: {minutes} 分钟")
        print("3 秒后开始...")
        time.sleep(3)

        # 开始倒计时
        countdown(minutes)

        print("\n感谢使用番茄钟倒计时器！")

    except Exception as e:
        print(f"\n❌ 程序发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
