import json

from quiz_app.default_data import create_default_quizzes
from quiz_app.models import Quiz


class StateStore:
    """
    state.json 읽기와 쓰기를 전담하는 저장소 클래스.

    파일 입출력 책임을 게임 로직에서 분리하면 코드를 읽을 때
    "게임 진행"과 "저장 처리"를 따로 이해할 수 있어 유지보수가 쉬워진다.
    """

    def __init__(self, state_path):
        self.state_path = state_path

    def validate_quiz_data(self, item):
        """손상된 퀴즈 데이터가 게임 로직까지 들어오지 않도록 미리 검사한다."""
        if not isinstance(item, dict):
            raise ValueError("퀴즈 항목 형식이 올바르지 않습니다.")

        question = item.get("question")
        choices = item.get("choices")
        answer = item.get("answer")

        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제 데이터가 올바르지 않습니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지 데이터가 올바르지 않습니다.")
        if not all(isinstance(choice, str) and choice.strip() for choice in choices):
            raise ValueError("선택지 데이터가 올바르지 않습니다.")
        if not isinstance(answer, int) or answer < 1 or answer > 4:
            raise ValueError("정답 데이터가 올바르지 않습니다.")

    def load(self):
        """
        디스크에서 퀴즈와 점수 데이터를 읽어 온다.

        반환값은 아래 순서의 튜플이다.
        (quizzes, best_score, best_correct_count, best_total_count, message)
        """
        default_quizzes = create_default_quizzes()

        if not self.state_path.exists():
            self.save(default_quizzes, None, None, None)
            return default_quizzes, None, None, None, "\n📂 저장 파일이 없어 기본 퀴즈 데이터를 사용합니다."

        try:
            with self.state_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            quizzes_data = data.get("quizzes", [])
            for item in quizzes_data:
                self.validate_quiz_data(item)

            quizzes = [Quiz.from_dict(item) for item in quizzes_data]
            if not quizzes:
                quizzes = default_quizzes

            best_score = data.get("best_score")
            best_correct_count = data.get("best_correct_count")
            best_total_count = data.get("best_total_count")
            loaded_best_score = best_score if best_score is not None else "없음"
            message = (
                f"\n📂 저장된 데이터를 불러왔습니다. "
                f"(퀴즈 {len(quizzes)}개, 최고점수 {loaded_best_score})"
            )
            return quizzes, best_score, best_correct_count, best_total_count, message
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            self.save(default_quizzes, None, None, None)
            return (
                default_quizzes,
                None,
                None,
                None,
                "\n⚠️ state.json 파일이 손상되어 기본 퀴즈 데이터로 복구합니다.",
            )
        except OSError as error:
            message = (
                f"\n⚠️ 저장 파일을 읽는 중 오류가 발생했습니다: {error}\n"
                "기본 퀴즈 데이터로 계속 진행합니다."
            )
            return default_quizzes, None, None, None, message

    def save(self, quizzes, best_score, best_correct_count, best_total_count):
        """현재 게임 상태 전체를 UTF-8 JSON 파일로 저장한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in quizzes],
            "best_score": best_score,
            "best_correct_count": best_correct_count,
            "best_total_count": best_total_count,
        }

        with self.state_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
