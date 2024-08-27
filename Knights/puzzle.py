from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."

general_knowledge = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave))
)

sentence0 = And(AKnight, AKnave)
knowledge0 = And(
    Or(AKnight,AKnave),
    Implication(AKnave, Not(sentence0)),
    Implication(AKnight, sentence0)
    )

# Puzzle 1
# A says "We are both knaves."
# B says nothing.

sentence1 = And(AKnave, BKnave)
knowledge1 = And(
    Or(AKnight,AKnave),
    Or(BKnave, BKnight),
    Implication(AKnave, Not(sentence1)),
    Implication(AKnight, sentence1)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

sentence2A1 = And(AKnave, BKnave)
sentence2A2 = And(AKnight,BKnight)
sentence2A = Or(sentence2A1, sentence2A2)

sentence2B1 = And(AKnave, BKnight)
sentence2B2 = And(AKnight, BKnave)
sentence2B = Or(sentence2B1, sentence2B2)
knowledge2 = And(
    Or(AKnight,AKnave),
    Or(BKnave, BKnight),
    Implication(AKnave, Not(sentence2A)),
    Implication(AKnight, sentence2A),
    Implication(BKnave, Not(sentence2B)),
    Implication(BKnight, sentence2B)    
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

knowledge3 = And(
    general_knowledge,
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave))),
    Implication(BKnight, Implication(AKnight, BKnave)),
    Implication(BKnave, Implication(AKnave, Not(BKnave))),
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
