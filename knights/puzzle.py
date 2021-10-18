from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Encode information about exclusivity of Knight and Knave "classes" and that every char is either Knight or Knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),

    # Encode the knowledge that if A is Knight, what he said it's true. Else, it's false. 
    # A said: "And(AKnight, AKnave)"
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Encode information about exclusivity of Knight and Knave "classes"
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),
    
    # Encode the knowledge that if A is Knight, what he said it's true. Else, it's false. 
    # A said: "And(AKnave, BKnaves)"
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Encode information about exclusivity of Knight and Knave "classes"
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),

    # Encode the knowledge that if A is Knight, what he said it's true. Else, it's false. 
    # A said: "And(Biconditional(AKnight, BKnight), Biconditional(AKnave, BKnave))"
    Implication(AKnight, And(Biconditional(AKnight, BKnight), Biconditional(AKnave, BKnave))),
    Implication(AKnave, Not(And(Biconditional(AKnight, BKnight), Biconditional(AKnave, BKnave)))),

    # Encode the knowledge that if B is Knight, what he said it's true. Else, it's false. 
    # B said: "And(Implication(AKnight, BKnave), Implication(AKnave, BKnight))"
    Implication(BKnight, And(Implication(AKnight, BKnave), Implication(AKnave, BKnight))),
    Implication(BKnave, Not(And(Implication(AKnight, BKnave), Implication(AKnave, BKnight))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Encode information about exclusivity of Knight and Knave "classes"
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),

    # Encode the knowledge that if A is Knight, what he said it's true. Else, it's false. 
    # A said one of this statement, but not both: "Aknight", "AKnave"
    Or(
        And(
            Implication(AKnight, AKnight),
            Implication(AKnave, Not(AKnight))
        ),
        And(
            Implication(AKnight, AKnave),
            Implication(AKnave, Not(AKnave))
        ),
    ),

    # Encode the knowledge that if B is Knight, what he said it's true. Else, it's false. 
    # B said: "And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))"
    Implication(BKnight, And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))),
    Implication(BKnave, Not(And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave))))),
    # B also said: "CKnave"
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),

    # Encode the knowledge that if C is Knight, what he said it's true. Else, it's false. 
    # C said: "Aknight"
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
