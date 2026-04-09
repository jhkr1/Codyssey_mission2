from quiz_app.colors import Color


class ConsoleUI:
    """
    콘솔 출력 전담 클래스.

    화면 출력 코드를 한곳에 모아두면 게임 로직은 "무엇을 할지"에 집중하고,
    UI 코드는 "어떻게 보여줄지"만 담당하게 된다.
    """

    def show_message(self, message):
        """저장 불러오기처럼 단순 안내 문구를 출력한다."""
        print(message)

    def show_save_error(self, error):
        """저장 실패 메시지를 강조해서 출력한다."""
        print(Color.RED + f"\n⚠️ 데이터를 저장하는 중 오류가 발생했습니다: {error}" + Color.END)

    def show_menu(self):
        """메인 메뉴를 출력한다."""
        print("\n\n")
        print(Color.CYAN + "========================================" + Color.END)
        print(Color.BOLD + "    🧠   나만의 퀴즈 게임  Ver 1.0   🧠" + Color.END)
        print(Color.CYAN + "========================================" + Color.END)
        print("  " + Color.BLUE + "1." + Color.END + " 퀴즈 풀기   " + Color.GREEN + "(Challenge)" + Color.END)
        print("  " + Color.BLUE + "2." + Color.END + " 퀴즈 추가   " + Color.GREEN + "(Add)" + Color.END)
        print("  " + Color.BLUE + "3." + Color.END + " 퀴즈 목록   " + Color.GREEN + "(List)" + Color.END)
        print("  " + Color.BLUE + "4." + Color.END + " 점수 확인   " + Color.GREEN + "(History)" + Color.END)
        print("  " + Color.BLUE + "5." + Color.END + " 퀴즈 삭제   " + Color.GREEN + "(Delete)" + Color.END)
        print("  " + Color.RED + "6." + Color.END + " 종료        " + Color.RED + "(Exit)" + Color.END)
        print(Color.CYAN + "========================================" + Color.END)
        print("\n" + Color.BOLD + Color.YELLOW + "  👉 원하는 메뉴 번호를 입력하세요." + Color.END + "\n")

    def show_no_quizzes_to_play(self):
        """플레이 가능한 퀴즈가 없을 때 출력한다."""
        print("\n📭 등록된 퀴즈가 없어 게임을 시작할 수 없습니다.")

    def show_quiz_start(self, total_count):
        """퀴즈 시작 전 문제 수를 알려준다."""
        print(f"\n📝 퀴즈를 시작합니다! (총 {total_count}문제)")

    def show_quiz_separator(self):
        """문제 사이 구분선을 출력한다."""
        print("\n----------------------------------------")

    def show_correct_answer(self):
        """정답 메시지를 출력한다."""
        print(Color.GREEN + "✅ 정답입니다!" + Color.END)

    def show_wrong_answer(self, answer_number, answer_text):
        """오답일 때 정답 정보를 함께 알려준다."""
        print(Color.RED + "❌ 오답입니다." + Color.END)
        print(f"정답은 {answer_number}번: {answer_text}")

    def show_quiz_result(self, total_count, correct_count, score, best_score_updated, best_score):
        """한 판이 끝난 뒤 결과와 최고 점수 관련 메시지를 출력한다."""
        print("\n========================================")
        print(f"🏆 결과: {total_count}문제 중 {correct_count}문제 정답! ({score}점)")
        if best_score_updated:
            print(Color.GREEN + "🎉 새로운 최고 점수입니다!" + Color.END)
        else:
            print(f"현재 최고 점수는 {best_score}점입니다.")
        print("========================================")

    def show_add_quiz_intro(self):
        """퀴즈 추가 시작 안내 문구를 출력한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.")
        print("입력 중 언제든지 `esc`를 입력하면 퀴즈 추가를 취소할 수 있습니다.")

    def show_quiz_added(self):
        """퀴즈가 정상 추가되었을 때 출력한다."""
        print(Color.GREEN + "\n✅ 퀴즈가 추가되었습니다!" + Color.END)

    def show_add_quiz_cancelled(self):
        """퀴즈 추가가 취소되었을 때 출력한다."""
        print(Color.YELLOW + "\n↩️ 퀴즈 추가를 취소하고 메뉴로 돌아갑니다." + Color.END)

    def show_empty_quiz_list(self):
        """퀴즈 목록이 비어 있을 때 출력한다."""
        print("\n📭 등록된 퀴즈가 없습니다.")

    def show_quiz_list(self, quizzes):
        """등록된 퀴즈 문제 제목을 목록 형태로 출력한다."""
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(quizzes)}개)")
        print("----------------------------------------")
        for index, quiz in enumerate(quizzes, start=1):
            print(f"[{index}] {quiz.question}")
        print("----------------------------------------")

    def show_delete_quiz_intro(self):
        """퀴즈 삭제 시작 안내 문구를 출력한다."""
        print("\n🗑️ 삭제할 퀴즈를 선택합니다.")
        print("입력 중 언제든지 `esc`를 입력하면 삭제를 취소할 수 있습니다.")

    def show_quiz_deleted(self, deleted_question):
        """퀴즈가 삭제되었을 때 삭제된 문제를 함께 알려준다."""
        print(Color.GREEN + f"\n✅ 퀴즈가 삭제되었습니다: {deleted_question}" + Color.END)

    def show_delete_quiz_cancelled(self):
        """퀴즈 삭제가 취소되었을 때 출력한다."""
        print(Color.YELLOW + "\n↩️ 퀴즈 삭제를 취소하고 메뉴로 돌아갑니다." + Color.END)

    def show_no_score(self):
        """플레이 기록이 없을 때 출력한다."""
        print("\n🏆 아직 퀴즈를 푼 기록이 없습니다.")

    def show_best_score_only(self, best_score):
        """최고 점수 숫자만 있을 때 간단히 출력한다."""
        print(f"\n🏆 최고 점수: {best_score}점")

    def show_best_score_detail(self, best_score, best_total_count, best_correct_count):
        """최고 점수와 정답 개수까지 자세히 출력한다."""
        print(
            f"\n🏆 최고 점수: {best_score}점 "
            f"({best_total_count}문제 중 {best_correct_count}문제 정답)"
        )

    def show_exit(self):
        """정상 종료 문구를 출력한다."""
        print("\n👋 프로그램을 종료합니다. 감사합니다!")

    def show_safe_exit(self, reason):
        """예외 상황에서도 저장 후 안전 종료 메시지를 출력한다."""
        print("\n\n" + Color.RED + f"⚠️ {reason}" + Color.END)

    def show_unknown_error(self, error):
        """예상하지 못한 오류를 화면에 보여 준다."""
        print(Color.RED + f"\n⚠️ 알 수 없는 오류가 발생했습니다: {error}" + Color.END)
