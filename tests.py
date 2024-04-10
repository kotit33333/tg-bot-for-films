def rests(number):
    answer = []
    for i in lst:
        answer.append(i % number)
    return answer
lst = [42, 17, 34, 100501]
print(*rests(3))
print(*lst)
