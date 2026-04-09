# 나만의 퀴즈 게임

## 프로젝트 개요

Python 콘솔 환경에서 실행되는 퀴즈 게임입니다.  
메뉴를 통해 퀴즈 풀기, 퀴즈 추가, 퀴즈 목록 확인, 최고 점수 확인을 할 수 있으며, 프로그램 상태는 `state.json`에 저장되어 재실행 후에도 유지됩니다.

## 퀴즈 주제와 선정 이유

퀴즈 주제는 `Python 기초 문법`입니다.  
이번 미션의 핵심이 Python 문법과 클래스, 파일 저장을 직접 구현해 보는 것이기 때문에, 학습 과정 자체를 퀴즈 주제로 연결하면 복습과 구현을 함께 할 수 있다고 판단했습니다.

## 실행 방법

1. Python 3 환경에서 프로젝트 폴더로 이동합니다.
2. 아래 명령어로 프로그램을 실행합니다.

```bash
python3 main.py
```

## 기능 목록

- 메뉴 선택 기능
- 퀴즈 풀기
- 퀴즈 추가
- 퀴즈 목록 확인
- 최고 점수 확인
- `state.json` 저장 및 불러오기
- 잘못된 입력 처리
- `KeyboardInterrupt`, `EOFError` 안전 종료 처리

## 파일 구조

```text
Codyssey_mission2/
├── main.py
├── state.json
├── README.md
├── .gitignore
└── docs/
    └── screenshots/
        └── .gitkeep
```

## 데이터 파일 설명

프로그램 데이터는 프로젝트 루트의 `state.json`에 UTF-8 인코딩으로 저장됩니다.

- `quizzes`: 퀴즈 목록
- `best_score`: 최고 점수
- `best_correct_count`: 최고 점수 기록 당시 맞힌 문제 수
- `best_total_count`: 최고 점수 기록 당시 전체 문제 수

예시 스키마:

```json
{
    "quizzes": [
        {
            "question": "파이썬의 창시자는 누구인가요?",
            "choices": ["귀도 반 로섬", "리누스 토르발스", "제임스 고슬링", "브렌던 아이크"],
            "answer": 1
        }
    ],
    "best_score": 80,
    "best_correct_count": 4,
    "best_total_count": 5
}
```

## 스크린샷 정리 예시

아래 경로에 실행 결과 스크린샷을 저장해서 제출 자료로 활용할 수 있습니다.

- `docs/screenshots/menu.png`
- `docs/screenshots/play.png`
- `docs/screenshots/add_quiz.png`
- `docs/screenshots/score.png`

## Git 실습 메모

clone 후 README를 수정하고 push한 뒤, 원본 작업 디렉터리에서 pull로 반영 여부를 확인했습니다.
