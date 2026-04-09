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

class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, number=None):
        if number is not None:
            print(f"\n[문제 {number}]")
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def is_correct(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
        )

class QuizGame:
    def __init__(self):
        self.quizzes = self.create_default_quizzes()
        self.best_score = None

    def create_default_quizzes(self):
        return [
            Quiz(
                "파이썬의 창시자는 누구인가요?",
                ["귀도 반 로섬", "리누스 토르발스", "제임스 고슬링", "브렌던 아이크"],
                1,
            ),
            Quiz(
                "파이썬에서 리스트를 만들 때 사용하는 기호는 무엇인가요?",
                ["()", "{}", "[]", "<>"],
                3,
            ),
            Quiz(
                "조건이 참일 때만 코드를 실행할 때 사용하는 키워드는 무엇인가요?",
                ["for", "while", "if", "def"],
                3,
            ),
            Quiz(
                "반복문으로 리스트의 모든 요소를 순회할 때 가장 자주 사용하는 문장은 무엇인가요?",
                ["if", "for", "class", "import"],
                2,
            ),
            Quiz(
                "파이썬에서 함수를 정의할 때 사용하는 키워드는 무엇인가요?",
                ["func", "define", "lambda", "def"],
                4,
            ),
        ]

    def prompt_text(self, message):
        while True:
            try:
                value = input(message).strip()
                if not value:
                    print(Color.YELLOW + "⚠️ 입력이 비어있습니다. 다시 입력하세요." + Color.END)
                    continue
                return value
            except KeyboardInterrupt:
                raise
            except EOFError:
                raise

    def prompt_number(self, message, minimum, maximum):
        while True:
            try:
                value = input(message).strip()
                if not value:
                    print(
                        Color.YELLOW
                        + f"⚠️ 입력이 비어있습니다. {minimum}-{maximum} 사이의 숫자를 입력하세요."
                        + Color.END
                    )
                    continue
                if not value.isdigit():
                    print(
                        Color.YELLOW
                        + f"⚠️ 잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요."
                        + Color.END
                    )
                    continue

                number = int(value)
                if number < minimum or number > maximum:
                    print(
                        Color.YELLOW
                        + f"⚠️ 잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요."
                        + Color.END
                    )
                    continue
                return number
            except KeyboardInterrupt:
                raise
            except EOFError:
                raise

    def play_quiz(self):
        if not self.quizzes:
            print("\n📭 등록된 퀴즈가 없어 게임을 시작할 수 없습니다.")
            return

        correct_count = 0
        total_count = len(self.quizzes)

        print(f"\n📝 퀴즈를 시작합니다! (총 {total_count}문제)")

        for index, quiz in enumerate(self.quizzes, start=1):
            print("\n----------------------------------------")
            quiz.display(index)
            user_answer = self.prompt_number("\n정답 입력 (1-4): ", 1, 4)

            if quiz.is_correct(user_answer):
                correct_count += 1
                print(Color.GREEN + "✅ 정답입니다!" + Color.END)
            else:
                correct_choice = quiz.choices[quiz.answer - 1]
                print(Color.RED + "❌ 오답입니다." + Color.END)
                print(f"정답은 {quiz.answer}번: {correct_choice}")

        score = int((correct_count / total_count) * 100)

        print("\n========================================")
        print(f"🏆 결과: {total_count}문제 중 {correct_count}문제 정답! ({score}점)")

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print(Color.GREEN + "🎉 새로운 최고 점수입니다!" + Color.END)
        else:
            print(f"현재 최고 점수는 {self.best_score}점입니다.")
        print("========================================")

    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.")

        question = self.prompt_text("문제를 입력하세요: ")
        choices = []

        for index in range(1, 5):
            choice = self.prompt_text(f"선택지 {index}: ")
            choices.append(choice)

        answer = self.prompt_number("정답 번호 (1-4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))

        print(Color.GREEN + "\n✅ 퀴즈가 추가되었습니다!" + Color.END)

    def show_quizzes(self):
        if not self.quizzes:
            print("\n📭 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("----------------------------------------")
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"[{index}] {quiz.question}")
        print("----------------------------------------")

    def show_best_score(self):
        if self.best_score is None:
            print("\n🏆 아직 퀴즈를 푼 기록이 없습니다.")
            return

        total_count = len(self.quizzes)
        correct_count = round((self.best_score / 100) * total_count)
        print(f"\n🏆 최고 점수: {self.best_score}점 ({total_count}문제 중 {correct_count}문제 정답)")

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
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_quizzes()
                elif choice == 4:
                    self.show_best_score()
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
