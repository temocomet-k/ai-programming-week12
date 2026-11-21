# 성적 CSV 읽기와 테스트

## ① 무엇을 하나요
성적 파일에서 유효한 (이름, 점수)와 제외한 줄의 번호, 내용, 이유를 돌려줍니다.

## ② 왜 만들었나요
scores.csv에는 김하나가 88점과 91점으로 두 번 나오고 105점과 빈 점수도 섞여 있습니다. 같은 이름의 두 기록을 모두 보존하면서, 성적으로 쓸 수 없는 줄을 다시 찾으려고 만들었습니다.

## ③ 어떻게 쓰나요
Python 3.12에서 확인했습니다. 저장소를 내려받고, load_scores.py가 있는 폴더에서 실행합니다.

    git clone https://github.com/temocomet-k/ai-programming-week12.git
    cd ai-programming-week12
    python -m pip install pytest pytest-cov
    python load_scores.py scores.csv

유효한 성적 5개, 제외한 줄 5개가 출력됩니다.

## ④ 어떻게 테스트하나요

    python -m pytest -q test_load_scores.py --cov=load_scores --cov-report=term-missing

결과: 10 passed, 80%. 아래 이미지는 실행 출력입니다.

![테스트 결과](test_result.png)

AI 비교와 함정 실험은 따로 실행합니다.

    python -m pytest -q test_ai_A.py
    python -m pytest -q test_ai_B.py
    python -m pytest -q test_ai_bug.py

마지막 실험에서는 배포된 find_max의 버그로 2개가 실패합니다.

## ⑤ 파일 구성
- load_scores.py / scores.csv / empty.csv / weird.csv — 배포 함수와 성적 파일
- test_load_scores.py — 8개 기본 사례와 2개 추가 사례
- test_ai_A.py / test_ai_B.py / test_ai_bug.py — 코드·명세로 만든 비교 테스트와 함정 실험 테스트
- bug3_logic.py — 함정 실험에 사용하는 배포 코드
- test_result.png — 기본·추가 사례의 실행 출력
- LICENSE — MIT License (배포 코드의 출처는 수업 자료)

## ⑥ 작성 및 AI 사용
기계공학부 김혜성. ChatGPT를 테스트 설계·작성, 실행, 결과 비교와 문서화에 사용했습니다. 판정 기준은 배포 자료의 명세를 따랐습니다.
