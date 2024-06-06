import pandas as pd


class SimpleChatBot:
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    def load_data(self, filepath):
        # pandas 라이브러리의 read_csv 함수를 사용해서 DataFrame 형태로 변환해줍니다. 결과는 다음의 예시와 같습니다.
        data = pd.read_csv(filepath)

        # 학습데이터(DataFrame)에서 Q(column)을 추출하여 리스트로 변환해줍니다. questions는 학습데이터 Q(column)에 있는 모든 값을 포함하는 리스트가 됩니다.
        questions = data["Q"].tolist()

        # 동일하게 학습데이터(DataFrame)에서 A(column)을 추출하여 리스트로 변환해줍니다. answers는 학습데이터 A(column)에 있는 모든 값을 포함하는 리스트가 됩니다.
        answers = data["A"].tolist()
        return questions, answers

    def calc_distance(self, a, b):
        """레벤슈타인 거리 계산하기"""
        # calc_distance 함수가 인수로 받는 문자열 a, b가 같다면, 레벤슈타인 거리는 0으로, 두 문자열을 동일하기 만들기 위해 필요한 편집 비용은 0을 의미합니다.
        if a == b:
            return 0

        # 문자열 a, b의 길이를 변수에 저장합니다.
        a_len = len(a)
        b_len = len(b)

        # 이 때 문자열 a가 빈 문자열이라면, b의 모든 문자를 삽입해야 하기 때문에
        # 레벤슈타인 거리는 b의 길이와 동일하고,
        # 마찬가지로 문자열 b가 빈 문자열이라면, a의 모든 문자를 삭제해야 하기 때문에 레벤슈타인 거리는 a의 길이와 동일합니다.
        if a == "":
            return b_len
        if b == "":
            return a_len

        # a_len + 1개의 빈 리스트를 포함하는 1차원 리스트를 만들어 줍니다.
        matrix = [[] for i in range(a_len + 1)]

        #  이 후 루프를 통해 각 빈 리스트를 b_len + 1개의 0으로 채운 리스트로 초기화하여 a_len+1 x b_len+1 크기의 2차원 매트릭스를 만듭니다.
        for i in range(a_len + 1):
            matrix[i] = [0 for j in range(b_len + 1)]

        # 각각의 행과 열의 값이 0인 지점, 즉 빈 분자열일 경우 특정 문자열로 변환할 경우 편집하고자 하는 문자열의 길이만큼의 편집 비용이 소요됩니다.
        # 때문에 첫 번째 행과 첫 번째 열은 각각 0부터 a_len까지, 그리고 0부터 b_len까지의 값을 가지도록 초기값을 설정해줍니다.
        for i in range(a_len + 1):
            matrix[i][0] = i
        for j in range(b_len + 1):
            matrix[0][j] = j

        # 2차원 매트릭스를 채우기 위해 이중 루프를 활용해 i는 1부터 a_len까지, j는 1부터 b_len까지 순회합니다.
        # 이 때, ac는 문자열 a의 i-1번째 문자를, bc는 문자열 b의 j-1번째 문자를 가집니다.
        # 만약 두 문자가 같다면(ac == bc), 편집 비용(cost)은 0이 되고, 다르면 1이 됩니다.
        for i in range(1, a_len + 1):
            ac = a[i - 1]
            for j in range(1, b_len + 1):
                bc = b[j - 1]
                cost = 0 if (ac == bc) else 1

                # 레벤슈타인 거리의 편집 비용 계산은 다음과 같습니다.
                # 글자가 서로 동일하면 대각선의 레벤슈타인 거리 수치를 가져옵니다.
                # 변경이 필요하면 대각선의 레벤슈타인 거리 수치의 +1을 합니다.
                # 삽입이 필요하면 왼쪽 레벤슈타인 거리 수치의 +1을 합니다.
                # 삭제가 필요하면 위쪽 레벤슈타인 거리 수치의 +1을 합니다.

                # 이를 다음과 같이 구현해줍니다.
                # matrix[i - 1][j] + 1 : 위쪽 값에서 1을 더한 값. (삭제)
                # matrix[i][j - 1] + 1 : 왼쪽 값에서 1을 더한 값. (삽입)
                # matrix[i - 1][j - 1] + cost : 대각선 값에서 cost를 더한 값. 이는 문자가 다르면 교체를 의미하고, 같으면 대각선 값을 그대로 가져옴 (변경 | 동일)
                matrix[i][j] = min(
                    [
                        matrix[i - 1][j] + 1,
                        matrix[i][j - 1] + 1,
                        matrix[i - 1][j - 1] + cost,
                    ]
                )

        # 최종적으로 매트릭스의 마지막 원소인 matrix[a_len][b_len] 값을 반환합니다. 이 값은 문자열 a와 b 사이의 레벤슈타인 거리입니다.
        return matrix[a_len][b_len]

    def find_best_answer(self, input_sentence):
        # 리스트 컴프리헨션을 사용하여 input_sentence(새로 들어온 질문)와 학습데이터의 질문 사이의 레벤슈타인 거리를 계산합니다.
        # 결과적으로 distances는 새로 들어온 질문과 각 질문 사이의 거리를 포함하는 리스트가 됩니다.
        distances = [
            self.calc_distance(input_sentence, question) for question in self.questions
        ]

        # distances 리스트에서 가장 작은 값을 찾아 해당 인덱스를 반환합니다
        best_match_index = distances.index(min(distances))

        # 최종적으로 best_match_index에 해당하는 답변을 반환합니다
        return self.answers[best_match_index]


filepath = "ChatbotData.csv"


chatbot = SimpleChatBot(filepath)


while True:
    input_sentence = input("You: ")
    if input_sentence.lower() == "종료":
        break
    response = chatbot.find_best_answer(input_sentence)
    print("Chatbot:", response)
