from quiz_app.colors import Color


class QuizAddCancelled(Exception):
    """사용자가 입력 도중 `esc`로 현재 작업을 취소했을 때 사용하는 예외."""


class InputHandler:
    """
    사용자 입력 검증만 전담하는 클래스.

    입력 처리 규칙을 한곳에 모아두면 메뉴 입력, 정답 입력, 퀴즈 생성 입력이
    모두 같은 기준으로 동작하게 되어 유지보수가 쉬워진다.
    """

    def show_warning(self, message):
        """입력 검증 실패 메시지를 같은 형식으로 출력한다."""
        print(Color.YELLOW + message + Color.END)

    def is_cancel_input(self, value):
        """문자열 `esc`와 실제 ESC 입력을 모두 취소 신호로 판단한다."""
        return value.lower() == "esc" or value == "\x1b"

    def handle_cancel(self, value, allow_cancel):
        """
        취소 입력을 허용하는 상황이라면 `esc` 입력 시 예외를 발생시킨다.

        입력 함수 바깥에서는 이 예외를 잡아서
        "추가 취소", "삭제 취소"처럼 기능별 문구를 출력한다.
        """
        if allow_cancel and self.is_cancel_input(value):
            raise QuizAddCancelled

    def prompt_text(self, message, allow_cancel=False):
        """
        비어 있지 않은 문자열을 입력받을 때까지 반복해서 묻는다.

        흐름은 다음 순서로 고정되어 있다.
        1. 입력받기
        2. 취소 여부 확인
        3. 빈 입력 여부 확인
        4. 통과하면 그대로 반환
        """
        while True:
            value = input(message).strip()
            self.handle_cancel(value, allow_cancel)

            # 문자열 입력은 내용이 비어 있지 않은지만 확인하면 된다.
            if not value:
                self.show_warning("⚠️ 입력이 비어있습니다. 다시 입력하세요.")
                continue

            # 검증을 통과한 입력만 호출한 곳으로 돌려준다.
            return value

    def prompt_number(self, message, minimum, maximum, allow_cancel=False):
        """
        허용 범위 안의 숫자를 입력할 때까지 반복해서 묻는다.

        숫자 입력은 문자열 입력보다 확인할 것이 많다.
        1. 입력받기
        2. 취소 여부 확인
        3. 빈 입력 여부 확인
        4. 숫자 형태인지 확인
        5. 허용 범위 안인지 확인
        6. 모두 통과하면 정수로 반환
        """
        while True:
            value = input(message).strip()
            self.handle_cancel(value, allow_cancel)

            # 아무 값도 입력하지 않은 경우에는 다음 단계로 넘어가지 않는다.
            if not value:
                self.show_warning(
                    f"⚠️ 입력이 비어있습니다. {minimum}-{maximum} 사이의 숫자를 입력하세요."
                )
                continue

            # 숫자로 바꿀 수 없는 값은 여기서 걸러낸다.
            if not value.isdigit():
                self.show_warning(
                    f"⚠️ 잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요."
                )
                continue

            number = int(value)

            # 숫자이더라도 메뉴 범위나 정답 범위를 벗어나면 다시 입력받는다.
            if number < minimum or number > maximum:
                self.show_warning(
                    f"⚠️ 잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요."
                )
                continue

            # 여기까지 오면 호출한 기능이 신뢰할 수 있는 정수 입력이 된다.
            return number
