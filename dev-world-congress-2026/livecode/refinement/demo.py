"""A refinement type checker."""

from dataclasses import dataclass

INF = float("inf")

# Refinement types: a base type carrying a predicate on its value v ----
# Each refinement knows the integers it admits (`values`) and how to
# render itself. Subtyping is `<=`, shared once on the base class.

class Refinement:
    def values(self):
        """The integer intervals this type admits."""
        raise NotImplementedError

    def __le__(self, other):
        """Subtyping: is every value of self also a value of other?"""
        return all(any(c <= a and b <= d for c, d in other.values())
                   for a, b in self.values())


@dataclass(frozen=True)
class Int(Refinement):             # v : Int  (any integer)
    def values(self):
        return [(-INF, INF)]

    def __str__(self):
        return "Int"


@dataclass(frozen=True)
class Eq(Refinement):              # v = n
    n: int

    def values(self):
        return [(self.n, self.n)]

    def __str__(self):
        return f"{{v = {self.n}}}"


@dataclass(frozen=True)
class Ne(Refinement):              # v ≠ n
    n: int

    def values(self):
        return [(-INF, self.n - 1), (self.n + 1, INF)]

    def __str__(self):
        return f"{{v ≠ {self.n}}}"


@dataclass(frozen=True)
class Gt(Refinement):              # v > n
    n: int

    def values(self):
        return [(self.n + 1, INF)]

    def __str__(self):
        return f"{{v > {self.n}}}"


@dataclass(frozen=True)
class Lt(Refinement):              # v < n
    n: int

    def values(self):
        return [(-INF, self.n - 1)]

    def __str__(self):
        return f"{{v < {self.n}}}"


# A tiny expression language ------------------------------------------
# Each expression infers its own refinement type and renders itself.

class Expr:
    def infer(self, ctx):
        """Infer the refinement type of this expression."""
        raise NotImplementedError


@dataclass(frozen=True)
class Lit(Expr):                   # 5
    n: int

    def infer(self, ctx):
        return Eq(self.n)          # the literal n has type {v = n}

    def __str__(self):
        return str(self.n)


@dataclass(frozen=True)
class Var(Expr):                   # x
    name: str

    def infer(self, ctx):
        return ctx[self.name]      # look the variable up

    def __str__(self):
        return self.name


@dataclass(frozen=True)
class Call(Expr):                  # div(a, b)
    fn: str
    args: tuple

    def infer(self, ctx):
        params, result = SIGS[self.fn]
        for arg, param in zip(self.args, params):
            ty = arg.infer(ctx)                 # recurse into the argument
            if not (ty <= param):               # the subtyping check
                raise TypeError(f"{self.fn}: {ty} is not {param}")
        return result

    def __str__(self):
        return f"{self.fn}({', '.join(str(a) for a in self.args)})"


SIGS = {                           # fn : (parameter types) -> result type
    "div": ((Int(), Ne(0)), Int()),
}

# Type-check a few programs -------------------------------------------
if __name__ == "__main__":
    print("div : (Int, {v ≠ 0}) → Int\n")
    ctx = {"x": Gt(0), "n": Int()}
    for e in [Call("div", (Lit(10), Lit(2))),
              Call("div", (Lit(10), Lit(0))),
              Call("div", (Lit(10), Var("x"))),
              Call("div", (Lit(10), Var("n")))]:
        try:
            print(f"  {str(e):14}  :  {e.infer(ctx)}")
        except TypeError as err:
            print(f"  {str(e):14}  :  TYPE ERROR   {err}")
