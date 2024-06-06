import pandas as pd


class SimpleChatBot:
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data["Q"].tolist()
        answers = data["A"].tolist()
        return questions, answers

    def calc_distance(self, a, b):
        """레벤슈타인 거리 계산하기"""
        if a == b:
            return 0
        a_len = len(a)
        b_len = len(b)
        if a == "":
            return b_len
        if b == "":
            return a_len

        matrix = [[] for i in range(a_len + 1)]
        for i in range(a_len + 1):
            matrix[i] = [0 for j in range(b_len + 1)]

        for i in range(a_len + 1):
            matrix[i][0] = i
        for j in range(b_len + 1):
            matrix[0][j] = j

        for i in range(1, a_len + 1):
            ac = a[i - 1]
            for j in range(1, b_len + 1):
                bc = b[j - 1]
                cost = 0 if (ac == bc) else 1
                matrix[i][j] = min(
                    [
                        matrix[i - 1][j] + 1,
                        matrix[i][j - 1] + 1,
                        matrix[i - 1][j - 1] + cost,
                    ]
                )
        return matrix[a_len][b_len]

    def find_best_answer(self, input_sentence):
        distances = [
            self.calc_distance(input_sentence, question) for question in self.questions
        ]

        best_match_index = distances.index(min(distances))
        return self.answers[best_match_index]


filepath = "ChatbotData.csv"


chatbot = SimpleChatBot(filepath)


while True:
    input_sentence = input("You: ")
    if input_sentence.lower() == "종료":
        break
    response = chatbot.find_best_answer(input_sentence)
    print("Chatbot:", response)
