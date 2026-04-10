class Quiz:
    """문제, 선택지 4개, 정답 번호를 담는 퀴즈 객체."""

    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, number):
        """문제 번호와 선택지를 콘솔에 출력한다."""
        print("\n----------------------------------------")
        print(f"[문제 {number}]")
        print(self.question)
        print()

        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def is_correct(self, user_answer):
        """사용자 입력이 정답 번호와 같은지 확인한다."""
        return user_answer == self.answer

    def correct_choice_text(self):
        """정답 번호에 해당하는 선택지 문구를 반환한다."""
        return self.choices[self.answer - 1]

    def to_dict(self):
        """JSON 저장용 딕셔너리로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        """딕셔너리 데이터를 검증한 뒤 Quiz 객체로 복원한다."""
        if not isinstance(data, dict):
            raise ValueError("퀴즈 항목은 딕셔너리여야 합니다.")

        question = data.get("question")
        choices = data.get("choices")
        answer = data.get("answer")

        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제 데이터가 올바르지 않습니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지 데이터가 올바르지 않습니다.")
        if not all(isinstance(choice, str) and choice.strip() for choice in choices):
            raise ValueError("선택지 데이터가 올바르지 않습니다.")
        if not isinstance(answer, int) or not 1 <= answer <= 4:
            raise ValueError("정답 데이터가 올바르지 않습니다.")

        cleaned_choices = [choice.strip() for choice in choices]
        return cls(question.strip(), cleaned_choices, answer)
