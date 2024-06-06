# levenshtein distance를 이용한 챗봇 구현

## 설치 및 실행

### 설치

```bash
> git clone https://github.com/nicehyun/Chatbot-levenshtein_distance.git
> pip install -r requirements.txt
```

### 실행

```bash
> source myenv/bin/activate
> python chatbot.py
```

---

## 학습 데이터 Q, A 리스트로 변환하기

```python
    data = pd.read_csv(filepath)
```

`pandas` 라이브러리의 `read_csv` 함수를 사용해서 DataFrame 형태로 변환해줍니다.
결과는 다음의 예시와 같습니다.

</br>

```python
    questions = data["Q"].tolist()
```

학습데이터(DataFrame)에서 `Q`(column)을 추출하여 리스트로 변환해줍니다.
`questions`는 학습데이터 `Q`(column)에 있는 모든 값을 포함하는 리스트가 됩니다.
</br>

```python
    answers = data["A"].tolist()
```

동일하게 학습데이터(DataFrame)에서 `A`(column)을 추출하여 리스트로 변환해줍니다.
`answers`는 학습데이터 `A`(column)에 있는 모든 값을 포함하는 리스트가 됩니다.
</br>

load_data 함수의 최종 결과는 다음과 csv 파일을 리스트로 변환해줍니다.

- 학습데이터.csv

  | Q            | A                |
  | ------------ | ---------------- |
  | 안녕하세요   | 안녕하세요!      |
  | 날씨 어때?   | 맑아요.          |
  | 이름이 뭐야? | 저는 챗봇입니다. |

- 리스트
  `questions` : ["안녕하세요", "날씨 어때?", "이름이 뭐야?"]
  `answers` : ["안녕하세요!", "맑아요.", "저는 챗봇입니다."]

## levenshtein distance 거리 구하기

```python
    if a == b:
        return 0
```

`calc_distance` 함수가 인수로 받는 문자열 `a`, `b`가 같다면, 레벤슈타인 거리는 0으로, 두 문자열을 동일하기 만들기 위해 필요한 편집 비용은 0을 의미합니다.
</br>

```python
    a_len = len(a)
    b_len = len(b)
```

문자열 `a`, `b`의 길이를 변수에 저장합니다.
</br>

```python
    if a == "":
        return b_len
    if b == "":
        return a_len
```

이 때 문자열 `a`가 빈 문자열이라면, `b`의 모든 문자를 삽입해야 하기 때문에 레벤슈타인 거리는 `b`의 길이와 동일하고, 만찬가지로 문자열 `b`가 빈 문자열이라면, `a`의 모든 문자를 삭제해야 하기 때문에 레벤슈타인 거리는 `a`의 길이와 동일합니다.
</br>

```python
    matrix = [
        [] for i in range(a_len + 1)
    ]

    for i in range(a_len + 1):
        matrix[i] = [
            0 for j in range(b_len + 1)
        ]
```

`a_len + 1`개의 빈 리스트를 포함하는 1차원 리스트를 만들어 줍니다. 이 후 루프를 통해 각 빈 리스트를 `b_len + 1`개의 0으로 채운 리스트로 초기화하여 `a_len+1` x `b_len+1` 크기의 2차원 매트릭스를 만듭니다.

다음과 같은 0으로 초기화된 2차원 매트릭스를 생성하게 됩니다.

```plain
    [0, 0, 0, ..., 0],  # 첫 번째 행
    [0, 0, 0, ..., 0],  # 두 번째 행
    ...,
    [0, 0, 0, ..., 0]   # 마지막 행
```

</br>

```python
    for i in range(a_len + 1):
        matrix[i][0] = i
    for j in range(b_len + 1):
        matrix[0][j] = j
```

각각의 행과 열의 값이 0인 지점, 즉 빈 분자열일 경우 특정 문자열로 변환할 경우 편집하고자 하는 문자열의 길이만큼의 편집 비용이 소요됩니다.
때문에 첫 번째 행과 첫 번째 열은 각각 0부터 `a_len`까지, 그리고 0부터 `b_len`까지의 값을 가지도록 초기값을 설정해줍니다.
</br>

```python
    for i in range(1, a_len + 1):
        ac = a[i - 1]
        for j in range(1, b_len + 1):
            bc = b[j - 1]
            cost = 0 if (ac == bc) else 1
```

2차원 매트릭스를 채우기 위해 이중 루프를 활용해 `i`는 1부터 `a_len`까지, `j`는 1부터 `b_len`까지 순회합니다.
이 때, `ac`는 문자열 `a`의 `i-1`번째 문자를, `bc`는 문자열 `b`의 `j-1`번째 문자를 가집니다.
만약 두 문자가 같다면(`ac` == `bc`), 편집 비용(`cost`)은 0이 되고, 다르면 1이 됩니다.
</br>

```python
            matrix[i][j] = min(
                [
                    matrix[i - 1][j] + 1,
                    matrix[i][j - 1] + 1,
                    matrix[i - 1][j - 1]
                    + cost,
                ]
            )
```

레벤슈타인 거리의 편집 비용 계산은 다음과 같습니다.

- 글자가 서로 동일하면 대각선의 레벤슈타인 거리 수치를 가져옵니다.
- `변경`이 필요하면 대각선의 레벤슈타인 거리 수치의 +1을 합니다.
- `삽입`이 필요하면 왼쪽 레벤슈타인 거리 수치의 +1을 합니다.
- `삭제`가 필요하면 위쪽 레벤슈타인 거리 수치의 +1을 합니다.

이를 다음과 같이 구현해줍니다.

- `matrix[i - 1][j] + 1` : 위쪽 값에서 1을 더한 값. (삭제)
- `matrix[i][j - 1] + 1` : 왼쪽 값에서 1을 더한 값. (삽입)
- `matrix[i - 1][j - 1] + cost` : 대각선 값에서 `cost`를 더한 값. 이는 문자가 다르면 교체를 의미하고, 같으면 대각선 값을 그대로 가져옴 (변경 | 동일)

`matrix[i][j]`는 위의 세 가지 값 중 최소값을 가지게 됩니다.
</br>

```python
        return matrix[a_len][b_len]
```

최종적으로 매트릭스의 마지막 원소인 `matrix[a_len][b_len]` 값을 반환합니다. 이 값은 문자열 `a`와 `b` 사이의 레벤슈타인 거리입니다.

## 레벤슈타인 거리를 활용한 가장 유사한 질문의 답변 반환

```python
    distances = [
        self.calc_distance(input_sentence, question) for question in self.questions
    ]
```

리스트 컴프리헨션을 사용하여 `input_sentence`(새로 들어온 질문)와 학습데이터의 질문 사이의 레벤슈타인 거리를 계산합니다.

결과적으로 `distances`는 새로 들어온 질문과 각 질문 사이의 거리를 포함하는 리스트가 됩니다.

예를 들어, `questions`가 ["안녕하세요", "날씨 어때?", "이름이 뭐야?"]이고, `input_sentence`가 "안녕"이라면, `distances`는 `input_sentence`와 각 질문 사이의 레벤슈타인 거리를 계산한 값 [3, 5, 6]이 됩니다.
</br>

```python
    best_match_index = distances.index(min(distances))
```

`distances` 리스트에서 가장 작은 값을 찾아 해당 인덱스를 반환합니다
</br>

```python
    return self.answers[best_match_index]
```

최종적으로 `best_match_index`에 해당하는 답변을 반환합니다
</br>

---

## 실행

```python
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Chatbot:', response)
```

'종료'라는 입력이 나올 때까지 사용자의 입력에 따라 챗봇의 응답을 출력하는 무한 루프를 실행합니다.
