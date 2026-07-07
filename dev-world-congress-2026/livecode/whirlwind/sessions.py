"""
session types.

types describe communication protocols. each endpoint has a session
type, and the two endpoints must be duals of each other: one sends where
the other receives, and vice versa.

real systems (scribble, links, sessionkotlin, sepi) enforce linear
channel usage and support delegation. this toy covers send, receive,
internal and external choice, and end, plus duality and a runtime check
that a sequence of operations conforms to a declared session. choice is
the move that makes protocols expressive, so we keep it.
"""

from dataclasses import dataclass
from typing import Union


# payload types

@dataclass(frozen=True)
class TInt:
    pass


@dataclass(frozen=True)
class TStr:
    pass


Ty = Union[TInt, TStr]


def type_of(v) -> Ty:
    if isinstance(v, int):
        return TInt()
    if isinstance(v, str):
        return TStr()
    raise TypeError(f"unsupported payload: {v!r}")


# session types

@dataclass(frozen=True)
class End:
    pass


@dataclass(frozen=True)
class Send: # !T . S
    ty: Ty
    cont: "Session"


@dataclass(frozen=True)
class Recv: # ?T . S
    ty: Ty
    cont: "Session"


@dataclass(frozen=True)
class Choose: # ⊕{l: S, ...} internal choice
    branches: tuple


@dataclass(frozen=True)
class Offer: # &{l: S, ...} external choice
    branches: tuple


Session = Union[End, Send, Recv, Choose, Offer]


def branches(d: dict) -> tuple:
    return tuple(sorted(d.items()))


def dual(s: Session) -> Session:
    match s:
        case End():
            return End()
        case Send(t, c):
            return Recv(t, dual(c))
        case Recv(t, c):
            return Send(t, dual(c))
        case Choose(bs):
            return Offer(tuple((k, dual(v)) for k, v in bs))
        case Offer(bs):
            return Choose(tuple((k, dual(v)) for k, v in bs))


# process: a linear sequence of operations on a channel

@dataclass(frozen=True)
class OSend:
    val: object


@dataclass(frozen=True)
class ORecv:
    pass


@dataclass(frozen=True)
class OPick: # internal choice
    label: str
    then: tuple


@dataclass(frozen=True)
class OCase: # external choice: ((label, ops), ...)
    cases: tuple


def check(ops: tuple, sess: Session) -> None:
    for op in ops:
        match (op, sess):
            case (OSend(v), Send(ty, cont)):
                if type_of(v) != ty:
                    raise TypeError(f"send {v!r}: expected {ty}, got {type_of(v)}")
                sess = cont
            case (ORecv(), Recv(_, cont)):
                sess = cont
            case (OPick(lbl, then), Choose(bs)):
                bmap = dict(bs)
                if lbl not in bmap:
                    raise TypeError(f"choose {lbl!r} not in {list(bmap)}")
                check(then, bmap[lbl])
                return
            case (OCase(cs), Offer(bs)):
                bmap = dict(bs)
                for lbl, then in cs:
                    if lbl not in bmap:
                        raise TypeError(f"offer {lbl!r} not in protocol")
                    check(then, bmap[lbl])
                if set(dict(cs)) != set(bmap):
                    raise TypeError(f"offer: uncovered labels {set(bmap) - set(dict(cs))}")
                return
            case _:
                raise TypeError(f"step {op} does not match session {sess}")
    if not isinstance(sess, End):
        raise TypeError(f"session unfinished: {sess}")


# demo

if __name__ == "__main__":
    # client: send a query, receive a reply, end.   !Str . ?Int . end
    client = Send(TStr(), Recv(TInt(), End()))
    print("client:", client)
    print("server:", dual(client))

    good = (OSend("status?"), ORecv())
    check(good, client)
    print("good client: OK")

    bad = (OSend(42), ORecv()) # wrong payload type
    try:
        check(bad, client)
    except TypeError as e:
        print("rejected:", e)

    # a protocol with choice: client picks 'quit' or sends one query.
    chatty = Choose(branches({
        "quit": End(),
        "ask":  Send(TStr(), Recv(TInt(), End())),
    }))
    check((OPick("quit", ()),), chatty)
    print("quit branch: OK")
    check((OPick("ask", (OSend("ping"), ORecv())),), chatty)
    print("ask branch: OK")
