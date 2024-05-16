from idea.base.data import Block


def round(plain:tuple[Block], key:tuple[Block]) -> tuple[Block]:
    step1 = plain[0] * key[0]
    step2 = plain[1] + key[1]
    step3 = plain[2] + key[2]
    step4 = plain[3] + key[3]
    step5 = step1 ^ step3
    step6 = step2 ^ step4
    step7 = step5 * key[4]
    step8 = step6 + step7
    step9 = step8 * key[5]
    step10 = step7 + step9
    step11 = step1 ^ step9
    step12 = step3 ^ step9
    step13 = step2 ^ step10
    step14 = step4 ^ step10
    return step11, step12, step13, step14


def final_round(plain:tuple[Block], key:tuple[Block]) -> tuple[Block]:
    step1 = plain[0] * key[0]
    step2 = plain[1] + key[1]
    step3 = plain[2] + key[2]
    step4 = plain[3] * key[3]
    return step1, step2, step3, step4
