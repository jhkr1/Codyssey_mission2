class Quiz:
    """문제 1개, 선택지 4개, 정답 번호 1개로 구성된 퀴즈 객체."""

    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, number=None):
        """사용자가 보기 쉬운 형식으로 문제와 선택지를 출력한다."""
        if number is not None:
            print(f"\n[문제 {number}]")
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def is_correct(self, user_answer):
        """입력한 번호가 정답 번호와 같으면 True를 반환한다."""
        return user_answer == self.answer

    def to_dict(self):
        """객체를 JSON으로 저장할 수 있는 딕셔너리 형태로 바꾼다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        """저장된 딕셔너리 데이터를 다시 Quiz 객체로 복원한다."""
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
        )
