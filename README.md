import sys

# 터미널 색상을 정의하는 클래스 (문자열 앞에 붙여서 사용)
class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'  # 색상 적용 끝 (반드시 필수!)

class QuizGame:
    def __init__(self):
        # ... (생략) ...
        pass

    def display_menu(self):
        print("\n\n")  # 상단 여백
        print(Color.CYAN + "========================================" + Color.END)
        print(Color.BOLD + "    🧠   나만의 퀴즈 게임  Ver 1.0   🧠" + Color.END)
        print(Color.CYAN + "========================================" + Color.END)
        print("  " + Color.BLUE + "1." + Color.END + " 퀴즈 풀기   " + Color.GREEN + "(Challenge)" + Color.END)
        print("  " + Color.BLUE + "2." + Color.END + " 퀴즈 추가   " + Color.GREEN + "(Add)" + Color.END)
        print("  " + Color.BLUE + "3." + Color.END + " 퀴즈 목록   " + Color.GREEN + "(List)" + Color.END)
        print("  " + Color.BLUE + "4." + Color.END + " 점수 확인   " + Color.GREEN + "(History)" + Color.END)
        print("  " + Color.RED + "5." + Color.END + " 종료        " + Color.RED + "(Exit)" + Color.END)
        print(Color.CYAN + "========================================" + Color.END)
        print("\n" + Color.BOLD + Color.YELLOW + "  👉 원하는 메뉴 번호를 입력하세요." + Color.END + "\n")

    # ... (생략) ...