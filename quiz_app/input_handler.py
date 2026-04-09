from quiz_app.colors import Color
from quiz_app.exceptions import QuizAddCancelled


class InputHandler:
    """
    사용자 입력 검증만 전담하는 클래스.

    입력 처리 규칙을 한곳에 모아두면 메뉴 입력, 정답 입력, 퀴즈 생성 입력이
    모두 같은 기준으로 동작하게 되어 유지보수가 쉬워진다.
    """

    def is_cancel_input(self, value):
        """문자열 `esc`와 실제 ESC 입력을 모두 취소 신호로 판단한다."""
        return value.lower() == "esc" or value == "\x1b"

    def prompt_text(self, message, allow_cancel=False):
        """비어 있지 않은 문자열을 입력받을 때까지 반복해서 묻는다."""
        while True:
            value = input(message).strip()
            if allow_cancel and self.is_cancel_input(value):
                raise QuizAddCancelled
            if not value:
                print(Color.YELLOW + "⚠️ 입력이 비어있습니다. 다시 입력하세요." + Color.END)
                continue
            return value

    def prompt_number(self, message, minimum, maximum, allow_cancel=False):
        """허용 범위 안의 숫자를 입력할 때까지 반복해서 묻는다."""
        while True:
            value = input(message).strip()
            if allow_cancel and self.is_cancel_input(value):
                raise QuizAddCancelled
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
