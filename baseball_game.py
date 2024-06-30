# 라이브러리 불러오기
import random

# 랜덤으로 4자리수 생성하기
def generate_number():
    digits = list(range(10))                    # 0~9까지 숫자를 포함하는 리스트 생성
    first_digit = random.choice(digits[1:])     # 첫번째 자리는 0이 안되므로 1부터 시작
    digits.remove(first_digit)                  # 리스트에서 first_digit에 선택된 숫자 삭제
    number = [first_digit]                      # number에 first_digit에 선택된 숫자 추가
    while len(number) < 4:                      # 리스트의 길이가 4가 될때까지 반복
        digit = random.choice(digits)
        digits.remove(digit)
        number.append(digit)
    return number                               # 4자리 숫자 리스트를 반환

def get_strikes_and_balls(guess, answer):                           # 스트라이크, 볼 개수를 산정하는 함수 만들기
    strikes = sum(1 for g, a in zip(guess, answer) if g == a)       # 숫자의 위치가 같으면 스트라이크 개수의 합 / zip 함수는 여러개의 리스트를 병렬로 처리하는 함수
    balls = sum(1 for g in guess if g in answer) - strikes          # 정답안의 숫자만 일치하는 경우의 수를 계산, 스트라이크 개수는 제외
    return strikes, balls                                           # 스트라이크와 볼의 개수를 반환

def give_hint(answer, guess):                                                           # hint를 제공하는 함수 만들기
    strikes = [g for g, a in zip(guess, answer) if g == a]
    balls = [g for g in guess if g in answer and g not in strikes]
    if strikes:                                                                         # 스트라이크가 있다면 스트라이크의 숫자를 하나 알려줌
        return f"hint: 스트라이크 숫자 중 하나는 {random.choice(strikes)}입니다."
    elif balls:                                                                         # 볼만 있다면 볼의 숫자 중 하나를 알려줌
        return f"hint: 볼 숫자 중 하나는 {random.choice(balls)}입니다."
    else:
        return "hint를 제공할 수 없습니다."

def play_game():                                                # 게임 만들기
    answer = generate_number()                                  # 정답은 랜덤으로 만든 4자리수
    print("야구 게임을 시작합니다!")
    name = input("이름을 입력해주세요: ")                        # 이름 입력하기                   
    print(f"{name}님, 4자리 숫자를 맞춰보세요.")

# 점수 산정하기 100점부터 시작
    score = 100
    attempts = 0
    hint_used = False
    last_guess = None

    while True:                                                                         # 게임 시작하기
        guess = input("숫자를 입력하세요 (힌트를 원하면 'hint'라고 입력하세요): ")
        if guess.lower() == 'hint':                                                      # hint 요청하기
            if hint_used:                                                                # hint 횟수 확인
                print("힌트는 이미 사용하셨습니다.")
            else:                                                                        # hint 가능 여부 확인
                if last_guess:                                                           # hint 제공
                    hint = give_hint(answer, last_guess)
                    print(hint)
                    if hint != "hint를 제공할 수 없습니다.":
                        hint_used = True
                else:                                                                    # hint 제공 불가능
                    print("힌트를 제공할 수 없습니다.")
            continue

# 입력값 확인하기
        if not guess.isdigit() or len(guess) != 4:
            print("유효한 4자리 숫자를 입력하세요.")
            continue

# 입력값을 리스트로 변환
        guess_list = [int(d) for d in guess]

        if guess_list[0] == 0: # 숫자 첫자리 및 4자리수 검증
            print("잘못된 숫자입니다. 다시 입력해주세요.")
            continue

        if len(set(guess_list)) != 4: # 중복된 숫자 검증
            print("중복된 숫자가 있습니다. 다시 입력해주세요.")
            continue

# 마지막 입력값 없데이트
        last_guess = guess_list
        strikes, balls = get_strikes_and_balls(guess_list, answer)  # 스트라이크와 볼 계산
        attempts += 1                                               # 시도 횟수 증가

# 정답확인
        if strikes == 4:
            print(f"정답입니다! {name}님의 점수는 {score}점입니다.")
            print(f"총 {attempts - 1}번 틀려서 {5 * (attempts - 1)}점이 감점되었습니다.")
            break
        elif strikes == 0 and balls == 0: # 아웃확인
            print("아웃!")
        else: # 결과 출력하기
            print(f"{strikes} 스트라이크, {balls} 볼")

# 점수 감소
        score -= 5
        if score == 0: # 점수확인
            print(f"점수가 0점이 되었습니다. 정답은 {''.join(map(str, answer))}입니다.")
            break

# 함수 반환
    return score, attempts, name

# 함수 정의
def main():
    while True:
        play_game()
        again = input("다시하려면 '다시하기'를 입력하고, 게임을 종료하려면 엔터를 누르세요: ") # 사용자 입력 받기
        if again.lower() != '다시하기': # 게임 종료 조건
            break

if __name__ == "__main__":
    main()