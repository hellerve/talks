# whirlwind toys

five tiny typecheckers, a little bestiary to poke at after the talk.
`refinement`, `effects`, and `sessions` map onto tour rungs, and the live
build under `../refinement/` is a stripped-down `refinement.py`. `rows`
and `gradual` didn't make the cut, but they earn their keep as further
reading.

each one stands alone, leans on nothing but the standard library, and
needs python 3.10+ for the pattern matching.

they share a shape:

1. a small AST of types, as frozen dataclasses.
2. the one move that makes the system tick (consistency, duality,
   implication, row variables, effect rows), as a single function.
3. a `__main__` that shows one thing it accepts and one it rejects.

run them:

```
python refinement.py
python effects.py
python rows.py
python sessions.py
python gradual.py
```

## what each one is about

| file            | idea                          | the move                              |
| --------------- | ----------------------------- | ------------------------------------- |
| `refinement.py` | types with predicates         | subtyping by logical entailment       |
| `effects.py`    | effects in function types     | the effect row flows through a call   |
| `rows.py`       | records polymorphic in fields | a row variable soaks up the rest      |
| `sessions.py`   | types as protocols            | duality, plus send/recv/choice checks |
| `gradual.py`    | the `?` type                  | consistency, lifted through `->`      |

## note!

these are toys, and they'll probably undersell how hard the real thing is.
each one opens with a docstring listing what i skipped (smt solvers, handler
continuations, row unification, linear-usage checks, runtime casts).
these are not conceptual limitations, but they are what you’re up against if
you want to make a real system.

<hr/>

have fun!
