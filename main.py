import sys

# 터미널 색상을 정의하는 클래스
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
    END = '\033[0m'

class QuizGame:
    def __init__(self):
        # 나중에 파일 불러오기(state.json) 로직이 이곳에 추가될 예정입니다.
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

    def run(self):
        while True:
            self.display_menu()
            try:
                # 입력 앞뒤 공백 제거 후 처리
                choice_input = input("선택: ").strip()

                if not choice_input:
                    print(Color.YELLOW + "⚠️ 입력이 비어있습니다. 1-5 사이의 숫자를 입력하세요." + Color.END)
                    continue

                if not choice_input.isdigit():
                    print(Color.YELLOW + "⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요." + Color.END)
                    continue

                choice = int(choice_input)

                if choice < 1 or choice > 5:
                    print(Color.YELLOW + "⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요." + Color.END)
                    continue

                # 정상적인 메뉴 선택 흐름
                if choice == 1:
                    print("\n📝 [퀴즈 풀기] 기능은 곧 구현됩니다!")
                elif choice == 2:
                    print("\n📌 [퀴즈 추가] 기능은 곧 구현됩니다!")
                elif choice == 3:
                    print("\n📋 [퀴즈 목록] 기능은 곧 구현됩니다!")
                elif choice == 4:
                    print("\n🏆 [점수 확인] 기능은 곧 구현됩니다!")
                elif choice == 5:
                    print("\n👋 프로그램을 종료합니다. 감사합니다!")
                    break

            except KeyboardInterrupt:
                print("\n\n" + Color.RED + "⚠️ 프로그램이 강제 종료되었습니다. 안전하게 종료합니다." + Color.END)
                sys.exit(0)
            except EOFError:
                print("\n\n" + Color.RED + "⚠️ 입력 스트림이 끊어졌습니다. 안전하게 종료합니다." + Color.END)
                sys.exit(0)
            except Exception as e:
                print(Color.RED + f"\n⚠️ 알 수 없는 오류가 발생했습니다: {e}" + Color.END)

# 프로그램 실행 진입점
if __name__ == "__main__":
    game = QuizGame()
    game.run()