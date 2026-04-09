import sys
from pathlib import Path

from quiz_app.input_handler import InputHandler, QuizAddCancelled
from quiz_app.models import Quiz
from quiz_app.storage import StateStore
from quiz_app.ui import ConsoleUI


class QuizGame:
    """
    콘솔 퀴즈 게임 전체 흐름을 관리하는 중심 클래스.

    실행 중 상태는 이 클래스가 가지고 있고, 저장 같은 세부 책임은
    별도 모듈에 맡겨서 각 메서드가 너무 길어지지 않도록 구성했다.
    """

    def __init__(self, state_path="state.json"):
        self.state_path = Path(state_path)
        self.store = StateStore(self.state_path)
        self.input_handler = InputHandler()
        self.ui = ConsoleUI()
        self.quizzes = []
        self.best_score = None
        self.best_correct_count = None
        self.best_total_count = None
        self.load_state()

    def load_state(self):
        """프로그램 시작 시 저장 데이터를 한 번 불러오고 안내 문구를 출력한다."""
        (
            self.quizzes,
            self.best_score,
            self.best_correct_count,
            self.best_total_count,
            message,
        ) = self.store.load()
        self.ui.show_message(message)

    def save_state(self):
        """메모리에 있는 현재 상태를 저장하고, 저장 실패는 메시지로만 알린다."""
        try:
            self.store.save(
                self.quizzes,
                self.best_score,
                self.best_correct_count,
                self.best_total_count,
            )
        except OSError as error:
            self.ui.show_save_error(error)

    def play_quiz(self):
        """퀴즈 한 판을 진행하고 필요하면 최고 점수를 갱신한다."""
        if not self.quizzes:
            self.ui.show_no_quizzes_to_play()
            return

        correct_count = 0
        total_count = len(self.quizzes)

        self.ui.show_quiz_start(total_count)

        for index, quiz in enumerate(self.quizzes, start=1):
            self.ui.show_quiz_separator()
            quiz.display(index)
            user_answer = self.input_handler.prompt_number("\n정답 입력 (1-4): ", 1, 4)

            if quiz.is_correct(user_answer):
                correct_count += 1
                self.ui.show_correct_answer()
            else:
                correct_choice = quiz.choices[quiz.answer - 1]
                self.ui.show_wrong_answer(quiz.answer, correct_choice)

        score = int((correct_count / total_count) * 100)
        best_score_updated = False

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.best_correct_count = correct_count
            self.best_total_count = total_count
            best_score_updated = True

        self.ui.show_quiz_result(
            total_count,
            correct_count,
            score,
            best_score_updated,
            self.best_score,
        )
        self.save_state()

    def add_quiz(self):
        """사용자 입력으로 새 퀴즈를 만들고 바로 저장한다."""
        self.ui.show_add_quiz_intro()

        try:
            question = self.input_handler.prompt_text("문제를 입력하세요: ", allow_cancel=True)
            choices = []

            for index in range(1, 5):
                choice = self.input_handler.prompt_text(f"선택지 {index}: ", allow_cancel=True)
                choices.append(choice)

            answer = self.input_handler.prompt_number("정답 번호 (1-4): ", 1, 4, allow_cancel=True)
            self.quizzes.append(Quiz(question, choices, answer))
            self.save_state()
            self.ui.show_quiz_added()
        except QuizAddCancelled:
            self.ui.show_add_quiz_cancelled()

    def show_quizzes(self):
        """선택지 전체 대신 문제 제목만 모아 간단한 목록으로 보여 준다."""
        if not self.quizzes:
            self.ui.show_empty_quiz_list()
            return

        self.ui.show_quiz_list(self.quizzes)

    def delete_quiz(self):
        """사용자가 고른 번호의 퀴즈를 삭제하고 즉시 저장한다."""
        if not self.quizzes:
            self.ui.show_empty_quiz_list()
            return

        self.ui.show_delete_quiz_intro()
        self.ui.show_quiz_list(self.quizzes)

        try:
            delete_index = self.input_handler.prompt_number(
                "삭제할 퀴즈 번호를 입력하세요: ",
                1,
                len(self.quizzes),
                allow_cancel=True,
            )
            deleted_quiz = self.quizzes.pop(delete_index - 1)
            self.save_state()
            self.ui.show_quiz_deleted(deleted_quiz.question)
        except QuizAddCancelled:
            self.ui.show_delete_quiz_cancelled()

    def show_best_score(self):
        """저장된 최고 점수를 사람이 읽기 쉬운 형식으로 보여 준다."""
        if self.best_score is None:
            self.ui.show_no_score()
            return

        if self.best_correct_count is None or self.best_total_count is None:
            self.ui.show_best_score_only(self.best_score)
            return

        self.ui.show_best_score_detail(
            self.best_score,
            self.best_total_count,
            self.best_correct_count,
        )

    def display_menu(self):
        """매 반복마다 메인 메뉴를 다시 출력해 사용자가 현재 선택지를 바로 보게 한다."""
        self.ui.show_menu()

    def handle_menu_choice(self, choice):
        """메뉴 번호에 맞는 기능 메서드를 호출한다."""
        if choice == 1:
            self.play_quiz()
        elif choice == 2:
            self.add_quiz()
        elif choice == 3:
            self.show_quizzes()
        elif choice == 4:
            self.show_best_score()
        elif choice == 5:
            self.delete_quiz()
        elif choice == 6:
            self.save_state()
            self.ui.show_exit()
            return False
        return True

    def run(self):
        """
        프로그램의 최상위 반복 루프를 실행한다.

        이 메서드는 일부러 짧게 유지했다. 세부 기능을 별도 메서드로
        분리해 두면 전체 흐름을 처음 읽는 사람도 더 쉽게 이해할 수 있다.
        """
        while True:
            self.display_menu()
            try:
                choice = self.input_handler.prompt_number("선택: ", 1, 6)
                should_continue = self.handle_menu_choice(choice)
                if not should_continue:
                    break
            except KeyboardInterrupt:
                self.save_state()
                self.ui.show_safe_exit("프로그램이 중단되어 저장 후 안전하게 종료합니다.")
                sys.exit(0)
            except EOFError:
                self.save_state()
                self.ui.show_safe_exit("입력 스트림이 끊어져 저장 후 안전하게 종료합니다.")
                sys.exit(0)
            except Exception as error:
                self.ui.show_unknown_error(error)
