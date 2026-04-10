import json
import sys
from pathlib import Path

from quiz_app.models import Quiz


class Color:
    """콘솔 출력을 보기 쉽게 만드는 ANSI 색상 코드 모음."""

    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"


class QuizGame:
    """퀴즈 목록, 점수, 메뉴 흐름을 한곳에서 관리하는 메인 클래스."""

    def __init__(self, state_path="state.json"):
        self.state_path = Path(state_path)
        self.quizzes = []
        self.best_score = None
        self.best_correct_count = None
        self.best_total_count = None
        self.startup_message = ""
        self.load_state()

    def run(self):
        """메인 메뉴를 반복해서 보여 주고 선택한 기능을 실행한다."""
        if self.startup_message:
            print(self.startup_message)

        while True:
            try:
                self.show_menu()
                choice = self.prompt_number("선택: ", 1, 6)

                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_quiz_list()
                elif choice == 4:
                    self.show_best_score()
                elif choice == 5:
                    self.delete_quiz()
                else:
                    self.save_state()
                    print("\n프로그램을 종료합니다.")
                    break
            except (KeyboardInterrupt, EOFError):
                self.safe_exit()

    def show_menu(self):
        """메인 메뉴 화면을 출력한다."""
        line = f"{Color.CYAN}========================================{Color.END}"
        print(f"\n{line}")
        print(f"{Color.BOLD}        나만의 퀴즈 게임{Color.END}")
        print(line)
        print(f"{Color.BLUE}1.{Color.END} 퀴즈 풀기")
        print(f"{Color.BLUE}2.{Color.END} 퀴즈 추가")
        print(f"{Color.BLUE}3.{Color.END} 퀴즈 목록")
        print(f"{Color.BLUE}4.{Color.END} 점수 확인")
        print(f"{Color.BLUE}5.{Color.END} 퀴즈 삭제")
        print(f"{Color.RED}6.{Color.END} 종료")
        print(line)

    def play_quiz(self):
        """저장된 퀴즈를 순서대로 출제하고 점수를 계산한다."""
        if not self.quizzes:
            print(f"\n{Color.YELLOW}등록된 퀴즈가 없어 게임을 시작할 수 없습니다.{Color.END}")
            return

        total_count = len(self.quizzes)
        correct_count = 0

        print(f"\n퀴즈를 시작합니다. 총 {total_count}문제입니다.")

        for index, quiz in enumerate(self.quizzes, start=1):
            quiz.display(index)
            user_answer = self.prompt_number("정답 입력 (1-4): ", 1, 4)

            if quiz.is_correct(user_answer):
                correct_count += 1
                print(f"{Color.GREEN}정답입니다.{Color.END}")
            else:
                print(
                    f"{Color.RED}오답입니다.{Color.END} "
                    f"정답은 {quiz.answer}번: {quiz.correct_choice_text()}"
                )

        score = int((correct_count / total_count) * 100)
        is_new_best = self.update_best_score(score, correct_count, total_count)

        print(f"\n{Color.CYAN}========================================{Color.END}")
        print(f"결과: {total_count}문제 중 {correct_count}문제 정답! ({score}점)")
        if is_new_best:
            print(f"{Color.GREEN}새로운 최고 점수입니다.{Color.END}")
        elif self.best_score is not None:
            print(f"현재 최고 점수는 {self.best_score}점입니다.")
        print(f"{Color.CYAN}========================================{Color.END}")

        self.save_state()

    def add_quiz(self):
        """문제, 선택지, 정답 번호를 입력받아 새 퀴즈를 추가한다."""
        print("\n새로운 퀴즈를 추가합니다.")
        print("입력 중 `esc`를 입력하면 취소할 수 있습니다.")

        question = self.prompt_text("문제를 입력하세요: ", allow_cancel=True)
        if question is None:
            print(f"\n{Color.YELLOW}퀴즈 추가를 취소하고 메뉴로 돌아갑니다.{Color.END}")
            return

        choices = []
        for index in range(1, 5):
            choice = self.prompt_text(f"선택지 {index}: ", allow_cancel=True)
            if choice is None:
                print(f"\n{Color.YELLOW}퀴즈 추가를 취소하고 메뉴로 돌아갑니다.{Color.END}")
                return
            choices.append(choice)

        answer = self.prompt_number("정답 번호 (1-4): ", 1, 4, allow_cancel=True)
        if answer is None:
            print(f"\n{Color.YELLOW}퀴즈 추가를 취소하고 메뉴로 돌아갑니다.{Color.END}")
            return

        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()
        print(f"\n{Color.GREEN}퀴즈가 추가되었습니다.{Color.END}")

    def show_quiz_list(self):
        """저장된 퀴즈 제목 목록을 출력한다."""
        if not self.quizzes:
            print(f"\n{Color.YELLOW}등록된 퀴즈가 없습니다.{Color.END}")
            return

        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("----------------------------------------")
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"[{index}] {quiz.question}")
        print("----------------------------------------")

    def show_best_score(self):
        """현재 저장된 최고 점수를 보여 준다."""
        if self.best_score is None:
            print(f"\n{Color.YELLOW}아직 퀴즈를 푼 기록이 없습니다.{Color.END}")
            return

        if self.best_correct_count is None or self.best_total_count is None:
            print(f"\n{Color.GREEN}최고 점수: {self.best_score}점{Color.END}")
            return

        print(
            f"\n{Color.GREEN}최고 점수: {self.best_score}점{Color.END} "
            f"({self.best_total_count}문제 중 {self.best_correct_count}문제 정답)"
        )

    def delete_quiz(self):
        """선택한 번호의 퀴즈를 삭제한다."""
        if not self.quizzes:
            print(f"\n{Color.YELLOW}등록된 퀴즈가 없습니다.{Color.END}")
            return

        print("\n삭제할 퀴즈 번호를 선택하세요.")
        print("입력 중 `esc`를 입력하면 취소할 수 있습니다.")
        self.show_quiz_list()

        delete_index = self.prompt_number(
            "삭제할 퀴즈 번호: ",
            1,
            len(self.quizzes),
            allow_cancel=True,
        )
        if delete_index is None:
            print(f"\n{Color.YELLOW}퀴즈 삭제를 취소하고 메뉴로 돌아갑니다.{Color.END}")
            return

        deleted_quiz = self.quizzes.pop(delete_index - 1)
        self.save_state()
        print(f"\n{Color.GREEN}퀴즈가 삭제되었습니다:{Color.END} {deleted_quiz.question}")

    def prompt_text(self, message, allow_cancel=False):
        """비어 있지 않은 문자열을 입력받는다."""
        while True:
            value = input(message).strip()

            if allow_cancel and self.is_cancel_input(value):
                return None
            if not value:
                print(f"{Color.YELLOW}입력이 비어 있습니다. 다시 입력하세요.{Color.END}")
                continue

            return value

    def prompt_number(self, message, minimum, maximum, allow_cancel=False):
        """허용 범위 안의 숫자를 입력받는다."""
        while True:
            value = input(message).strip()

            if allow_cancel and self.is_cancel_input(value):
                return None
            if not value:
                print(
                    f"{Color.YELLOW}입력이 비어 있습니다. "
                    f"{minimum}-{maximum} 사이의 숫자를 입력하세요.{Color.END}"
                )
                continue
            if not value.isdigit():
                print(
                    f"{Color.YELLOW}잘못된 입력입니다. "
                    f"{minimum}-{maximum} 사이의 숫자를 입력하세요.{Color.END}"
                )
                continue

            number = int(value)
            if minimum <= number <= maximum:
                return number

            print(
                f"{Color.YELLOW}잘못된 입력입니다. "
                f"{minimum}-{maximum} 사이의 숫자를 입력하세요.{Color.END}"
            )

    def is_cancel_input(self, value):
        """입력값이 취소 명령인지 확인한다."""
        return value.lower() == "esc" or value == "\x1b"

    def update_best_score(self, score, correct_count, total_count):
        """최고 점수를 갱신했으면 True를 반환한다."""
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.best_correct_count = correct_count
            self.best_total_count = total_count
            return True

        return False

    def load_state(self):
        """state.json을 읽고, 없거나 손상되었으면 기본 데이터로 복구한다."""
        default_quizzes = self.create_default_quizzes()

        if not self.state_path.exists():
            self.quizzes = default_quizzes
            self.save_state()
            self.startup_message = "\n저장 파일이 없어 기본 퀴즈 데이터를 사용합니다."
            return

        try:
            with self.state_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            quizzes_data = data.get("quizzes", [])
            if not isinstance(quizzes_data, list):
                raise ValueError("quizzes 데이터는 리스트여야 합니다.")

            self.quizzes = [Quiz.from_dict(item) for item in quizzes_data]
            if not self.quizzes:
                self.quizzes = default_quizzes

            self.best_score = self.read_optional_int(data.get("best_score"))
            self.best_correct_count = self.read_optional_int(data.get("best_correct_count"))
            self.best_total_count = self.read_optional_int(data.get("best_total_count"))

            loaded_best_score = (
                f"{self.best_score}점" if self.best_score is not None else "없음"
            )
            self.startup_message = (
                f"\n{Color.CYAN}저장된 데이터를 불러왔습니다.{Color.END} "
                f"(퀴즈 {len(self.quizzes)}개, 최고 점수 {loaded_best_score})"
            )
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            self.reset_to_default(default_quizzes)

    def save_state(self):
        """현재 퀴즈와 점수를 state.json에 저장한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct_count": self.best_correct_count,
            "best_total_count": self.best_total_count,
        }

        try:
            with self.state_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError as error:
            print(f"\n{Color.RED}데이터를 저장하는 중 오류가 발생했습니다: {error}{Color.END}")

    def reset_to_default(self, default_quizzes):
        """손상된 저장 데이터를 기본 퀴즈와 초기 점수로 복구한다."""
        self.quizzes = default_quizzes
        self.best_score = None
        self.best_correct_count = None
        self.best_total_count = None
        self.save_state()
        self.startup_message = (
            f"\n{Color.YELLOW}state.json 파일이 손상되어 기본 퀴즈 데이터로 복구합니다.{Color.END}"
        )

    def read_optional_int(self, value):
        """정수 또는 None만 허용하고, 그 외 값은 오류로 처리한다."""
        if value is None:
            return None
        if not isinstance(value, int):
            raise ValueError("점수 데이터는 정수여야 합니다.")
        return value

    def create_default_quizzes(self):
        """첫 실행 또는 복구 시 사용할 기본 퀴즈를 만든다."""
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

    def safe_exit(self):
        """Ctrl+C 또는 EOF 상황에서 저장 후 안전하게 종료한다."""
        self.save_state()
        print(f"\n{Color.RED}입력이 중단되어 저장 후 안전하게 종료합니다.{Color.END}")
        sys.exit(0)
