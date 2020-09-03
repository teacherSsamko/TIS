from collections import Counter

def find_top_N_recurring_words(seq, N):
    dcounter = Counter()
    for word in seq.split():
        dcounter[word] += 1
    return dcounter.most_common(N)

def test_top_N_recurring_words():
    seq = "버피 엔젤 몬스터 젠더 윌로 버피 몬스터 슈퍼 버피 엔젤"
    N = 3
    assert(find_top_N_recurring_words(seq, N) == [("버피",3), ("엔젤",2), ("몬스터",2)])
    print("pass")

if __name__ == "__main__":
    test_top_N_recurring_words()