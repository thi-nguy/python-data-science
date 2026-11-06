"""
Test suite so sánh ft_filter với filter built-in của Python.

Cách dùng:
    1. Đặt file này cùng thư mục với ft_filter.py (có hàm ft_filter)
    2. python3 test_ft_filter.py          (hoặc: pytest test_ft_filter.py)

Ý tưởng: mỗi test chạy CẢ HAI implementation trên cùng dữ liệu rồi so sánh
kết quả (hoặc loại exception). Không hard-code kết quả mong đợi, nên test
đúng với mọi phiên bản Python.
"""
import itertools
import sys
import traceback

from ft_filter import ft_filter


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def outcome(impl, make):
    """Chạy impl với args mới sinh từ make(); trả về ('ok', list) hoặc ('err', type)."""
    args, kwargs = make()
    try:
        return ("ok", list(impl(*args, **kwargs)))
    except Exception as e:  # noqa
        return ("err", type(e))


def check(make):
    """So sánh ft_filter vs filter. make() phải trả về (args, kwargs) MỚI mỗi lần gọi
    (để generator/iterator không bị dùng lại)."""
    real = outcome(filter, make)
    mine = outcome(ft_filter, make)
    assert mine == real, f"\n  filter    -> {real}\n  ft_filter -> {mine}"


def same(func, iterable_factory):
    """Shortcut: check(func, iterable) với iterable sinh mới mỗi lần."""
    check(lambda: ((func, iterable_factory()), {}))


class Recorder:
    """Callable ghi lại mọi lần được gọi, để so sánh thứ tự/số lần gọi."""
    def __init__(self, fn=None):
        self.fn = fn
        self.calls = []

    def __call__(self, x):
        self.calls.append(x)
        return self.fn(x) if self.fn else x


# --------------------------------------------------------------------------
# 1. GENERAL CASES
# --------------------------------------------------------------------------
def test_even_numbers():
    '''Ơr đây lambda: [1, 2, 3, 4, 5, 6] là một iterable_factory để tạo mới mỗi lần gọi lại, do nếu truyền thẳng iterator thì sẽ bị dùng hết. Ở đây truyền list nên không thấy rõ'''
    same(lambda x: x % 2 == 0, lambda: [1, 2, 3, 4, 5, 6]) 

def test_all_pass():
    same(lambda x: True, lambda: [1, 2, 3])

def test_none_pass():
    same(lambda x: False, lambda: [1, 2, 3])

def test_strings():
    same(lambda s: len(s) > 2, lambda: ["a", "abc", "ab", "abcd"])

def test_isdigit_method():
    same(str.isdigit, lambda: ["1", "a", "22", "", "3b"])

def test_builtin_function_as_func():
    same(callable, lambda: [len, 1, "x", print, int])

def test_bool_as_func():
    same(bool, lambda: [0, 1, "", "a", [], [0], None])

def test_order_preserved():
    same(lambda x: x > 0, lambda: [5, -1, 3, 9, -7, 1])

def test_duplicates_kept():
    same(lambda x: x == 1, lambda: [1, 1, 2, 1, 3, 1])

def test_filter_on_tuples_of_mixed_types():
    same(lambda x: isinstance(x, int), lambda: (1, "a", 2.0, 3, None, True))

def test_nested_lists():
    same(lambda x: len(x) > 1, lambda: [[1], [1, 2], [], [3, 4, 5]])

def test_function_is_method_bound():
    class A:
        def keep(self, x):
            return x > 2
    same(A().keep, lambda: range(6))

def test_function_is_callable_object():
    class Pred:
        def __call__(self, x):
            return x % 3 == 0
    same(Pred(), lambda: range(20))

def test_function_is_class():
    same(bool, lambda: [0, 1, 2])
    same(type, lambda: [0, 1])  # type(x) luôn truthy


# --------------------------------------------------------------------------
# 2. function = None  (lọc theo độ truthy của chính phần tử)
# --------------------------------------------------------------------------
def test_none_function_basic():
    same(None, lambda: [0, 1, "", "a", [], [0], None, False, True, 0.0, 0.1])

def test_none_function_all_falsy():
    same(None, lambda: [0, "", [], {}, set(), None, False, 0.0, 0j, ()])

def test_none_function_all_truthy():
    nan = float("nan")  # tạo 1 lần vì nan != nan
    same(None, lambda: [1, "a", [0], {0: 0}, (0,), True, -1, nan])

def test_none_function_empty():
    same(None, lambda: [])

def test_none_function_custom_bool():
    class B:
        def __init__(self, v): self.v = v
        def __bool__(self): return self.v
    items = [B(True), B(False), B(True)]
    check(lambda: ((None, iter(items)), {}))

def test_none_function_custom_len():
    class L:
        def __init__(self, n): self.n = n
        def __len__(self): return self.n
    items = [L(0), L(2), L(0), L(5)]
    check(lambda: ((None, iter(items)), {}))

def test_none_function_bool_raises():
    class Bad:
        def __bool__(self):
            raise ValueError("boom")
    check(lambda: ((None, [1, Bad(), 2]), {}))


# --------------------------------------------------------------------------
# 3. Truthiness của giá trị TRẢ VỀ bởi function (không nhất thiết là bool)
# --------------------------------------------------------------------------
def test_func_returns_truthy_non_bool():
    same(lambda x: x, lambda: [0, 1, 2, "", "a", None])

def test_func_returns_list():
    same(lambda x: [x] if x else [], lambda: [0, 1, 2])

def test_func_returns_none():
    same(lambda x: None, lambda: [1, 2, 3])

def test_func_returns_nan_is_truthy():
    nan = float("nan")
    same(lambda x: nan, lambda: [1, 2])

def test_func_returns_object_with_bool():
    class B:
        def __init__(self, v): self.v = v
        def __bool__(self): return self.v
    same(lambda x: B(x > 1), lambda: [0, 1, 2, 3])

def test_func_result_bool_raises():
    class Bad:
        def __bool__(self): raise RuntimeError("x")
    same(lambda x: Bad(), lambda: [1])


# --------------------------------------------------------------------------
# 4. EDGE CASES: iterable
# --------------------------------------------------------------------------
def test_empty_list():
    same(lambda x: True, lambda: [])

def test_empty_everything():
    for empty in ([], (), "", {}, set(), range(0), iter([]), (x for x in [])):
        check(lambda e=empty: ((lambda x: True, iter(e) if hasattr(e, "__next__") else e), {}))

def test_single_element():
    same(lambda x: True, lambda: [42])
    same(lambda x: False, lambda: [42])

def test_string_iterable():
    same(str.isalpha, lambda: "ab1c2 d")

def test_unicode_string():
    same(lambda c: c.isalpha(), lambda: "Tiếng Việt 123 ✓ 日本語")

def test_tuple_iterable():
    same(lambda x: x > 1, lambda: (1, 2, 3))

def test_range_iterable():
    same(lambda x: x % 7 == 0, lambda: range(100))
    same(lambda x: True, lambda: range(10, 0, -3))

def test_dict_iterates_keys():
    same(lambda k: k > 1, lambda: {1: "a", 2: "b", 3: "c"})

def test_dict_items_and_values():
    same(lambda kv: kv[1] != "b", lambda: {1: "a", 2: "b"}.items())
    same(lambda v: v != "b", lambda: {1: "a", 2: "b"}.values())

def test_set_iterable():
    a = sorted(filter(lambda x: x > 2, {1, 2, 3, 4}))
    b = sorted(ft_filter(lambda x: x > 2, {1, 2, 3, 4}))
    assert a == b

def test_frozenset_and_bytes():
    same(lambda x: x > 100, lambda: bytes([1, 200, 50, 255]))
    same(lambda x: x > 100, lambda: bytearray([1, 200, 50, 255]))

def test_generator_iterable():
    same(lambda x: x % 2, lambda: (i for i in range(10)))

def test_iterator_iterable():
    same(lambda x: x % 2, lambda: iter(range(10)))

def test_map_zip_enumerate_reversed():
    same(lambda x: x > 3, lambda: map(lambda y: y * 2, range(5)))
    same(lambda p: p[0] != p[1], lambda: zip([1, 2, 3], [1, 0, 3]))
    same(lambda p: p[0] % 2, lambda: enumerate("abcdef"))
    same(lambda x: x > 1, lambda: reversed([1, 2, 3]))

def test_filter_of_filter():
    check(lambda: ((lambda x: x > 2, filter(lambda x: x % 2, range(10))), {}))
    check(lambda: ((lambda x: x > 2, ft_filter(lambda x: x % 2, range(10))), {}))

def test_unhashable_and_none_items():
    same(lambda x: x is not None, lambda: [None, [], {}, set(), 1])

def test_custom_iterable_with_iter():
    class It:
        def __iter__(self):
            return iter([1, 2, 3, 4])
    same(lambda x: x % 2 == 0, lambda: It())

def test_legacy_getitem_sequence_protocol():
    class Seq:
        def __getitem__(self, i):
            if i >= 5:
                raise IndexError
            return i * 10
    same(lambda x: x > 15, lambda: Seq())

def test_large_input():
    same(lambda x: x % 3 == 0, lambda: range(200_000))

def test_tuple_not_modified_original_list_not_modified():
    data = [1, 2, 3, 4]
    copy = list(data)
    list(ft_filter(lambda x: x > 2, data))
    assert data == copy


# --------------------------------------------------------------------------
# 5. EDGE CASES: kiểu trả về & hành vi iterator / lazy
# --------------------------------------------------------------------------
def test_does_not_return_list_or_tuple():
    r = ft_filter(None, [1, 2])
    assert not isinstance(r, (list, tuple, set, str)), f"returned {type(r)}"

def test_returns_iterator():
    r = ft_filter(lambda x: x, [1, 2, 3])
    assert iter(r) is r, "iter(r) phải trả về chính r"
    assert hasattr(r, "__next__")
    assert hasattr(r, "__iter__")

def test_next_and_stopiteration():
    for impl in (filter, ft_filter):
        r = impl(lambda x: x > 1, [1, 2, 3])
        assert next(r) == 2
        assert next(r) == 3
        for _ in range(3):  # vẫn StopIteration khi gọi lại
            try:
                next(r)
            except StopIteration:
                pass
            else:
                raise AssertionError(f"{impl} không raise StopIteration")

def test_next_default():
    for impl in (filter, ft_filter):
        assert next(impl(lambda x: False, [1, 2]), "dflt") == "dflt"

def test_single_use_exhausted_after_list():
    for impl in (filter, ft_filter):
        r = impl(None, [1, 2, 3])
        assert list(r) == [1, 2, 3]
        assert list(r) == []

def test_for_loop_and_unpack():
    a = [x for x in filter(lambda x: x, [0, 1, 2])]
    b = [x for x in ft_filter(lambda x: x, [0, 1, 2])]
    assert a == b
    x, y = ft_filter(lambda v: v, [0, 5, 0, 6])
    assert (x, y) == (5, 6)

def test_works_with_other_consumers():
    mk = lambda impl: impl(lambda x: x % 2, range(10))
    assert sum(mk(filter)) == sum(mk(ft_filter))
    assert tuple(mk(filter)) == tuple(mk(ft_filter))
    assert set(mk(filter)) == set(mk(ft_filter))
    assert sorted(mk(filter), reverse=True) == sorted(mk(ft_filter), reverse=True)
    assert max(mk(filter)) == max(mk(ft_filter))
    assert list(zip(mk(filter), "abc")) == list(zip(mk(ft_filter), "abc"))
    assert " ".join(map(str, mk(filter))) == " ".join(map(str, mk(ft_filter)))

def test_lazy_function_not_called_on_creation():
    for impl in (filter, ft_filter):
        rec = Recorder(lambda x: True)
        r = impl(rec, [1, 2, 3])
        assert rec.calls == [], f"{impl.__name__}: gọi function quá sớm"
        next(r)
        assert rec.calls == [1]

def test_lazy_does_not_consume_source_on_creation():
    for impl in (filter, ft_filter):
        consumed = []
        def src():
            for i in range(5):
                consumed.append(i)
                yield i
        r = impl(lambda x: True, src())
        assert consumed == [], f"{impl.__name__}: tiêu thụ iterable quá sớm"
        next(r)
        assert consumed == [0]

def test_infinite_iterable():
    for impl in (filter, ft_filter):
        r = impl(lambda x: x % 5 == 0, itertools.count())
        assert [next(r) for _ in range(5)] == [0, 5, 10, 15, 20]
        assert list(itertools.islice(impl(None, itertools.cycle([0, 1])), 4)) == [1, 1, 1, 1]

def test_calls_order_and_count_identical():
    logs = []
    for impl in (filter, ft_filter):
        rec = Recorder(lambda x: x % 2)
        list(impl(rec, [5, 2, 8, 3, 3, 0]))
        logs.append(rec.calls)
    assert logs[0] == logs[1], f"\n  filter    -> {logs[0]}\n  ft_filter -> {logs[1]}"

def test_function_called_exactly_once_per_item():
    for impl in (filter, ft_filter):
        rec = Recorder(lambda x: True)
        list(impl(rec, range(10)))
        assert len(rec.calls) == 10

def test_none_function_does_not_call_anything():
    # filter(None, ...) không gọi function nào cả
    check(lambda: ((None, [0, 1, 2]), {}))

def test_returns_same_objects_identity():
    objs = [object(), [1], {"a": 1}, "str", 3.14]
    for impl in (filter, ft_filter):
        out = list(impl(lambda x: True, objs))
        assert len(out) == len(objs)
        for a, b in zip(out, objs):
            assert a is b, f"{impl.__name__} đã tạo bản sao thay vì trả về chính object"

def test_lazy_sees_mutations_to_list():
    for impl in (filter, ft_filter):
        data = [1, 2, 3]
        r = impl(lambda x: True, data)
        assert next(r) == 1
        data.append(4)
        assert list(r) == [2, 3, 4]

def test_independent_iterators():
    data = [1, 2, 3, 4]
    for impl in (filter, ft_filter):
        a = impl(lambda x: x > 1, data)
        b = impl(lambda x: x > 1, data)
        assert next(a) == 2
        assert next(b) == 2
        assert next(a) == 3
        assert next(b) == 3

def test_works_when_iterating_manually_same_as_builtin():
    def trace(impl):
        r = impl(lambda x: x != 2, [1, 2, 3, 2, 4])
        out = []
        while True:
            try:
                out.append(next(r))
            except StopIteration:
                break
        return out
    assert trace(filter) == trace(ft_filter)


# --------------------------------------------------------------------------
# 6. EDGE CASES: lỗi / exception
# --------------------------------------------------------------------------
def test_no_args():
    check(lambda: ((), {}))

def test_one_arg():
    check(lambda: ((lambda x: x,), {}))
    check(lambda: ((None,), {}))

def test_too_many_args():
    check(lambda: ((lambda x: x, [1], [2]), {}))

def test_keyword_args():
    check(lambda: ((), {"function": lambda x: x, "iterable": [1, 2]}))
    check(lambda: ((lambda x: x,), {"iterable": [1, 2]}))

def test_non_iterable():
    for bad in (5, 3.14, None, object(), True):
        check(lambda b=bad: ((lambda x: x, b), {}))

def test_non_callable_function():
    for bad in (5, "abc", [1], {}, 3.14, object()):
        check(lambda b=bad: ((b, [1, 2, 3]), {}))

def test_non_callable_with_empty_iterable():
    # filter thật không báo lỗi nếu iterable rỗng (function không bao giờ được gọi)
    check(lambda: ((5, []), {}))
    check(lambda: (("abc", ()), {}))

def test_function_wrong_arity():
    check(lambda: ((lambda: True, [1, 2]), {}))
    check(lambda: ((lambda a, b: True, [1, 2]), {}))

def test_function_raises():
    def f(x):
        if x == 3:
            raise ValueError("bad")
        return True
    same(f, lambda: [1, 2, 3, 4])

def test_exception_type_propagates_unchanged():
    class MyErr(Exception):
        pass
    def f(x):
        raise MyErr()
    for impl in (filter, ft_filter):
        try:
            list(impl(f, [1]))
        except MyErr:
            pass
        else:
            raise AssertionError(f"{impl.__name__} nuốt exception")

def test_iterable_raises_midway():
    def gen():
        yield 1
        yield 2
        raise KeyError("src")
    same(lambda x: True, gen)

def test_resume_after_function_exception():
    # Sau khi function raise, iterator vẫn dùng tiếp được ở phần tử kế tiếp
    def run(impl):
        def f(x):
            if x == 2:
                raise ValueError
            return True
        r = impl(f, [1, 2, 3, 4])
        out = []
        for _ in range(6):
            try:
                out.append(next(r))
            except ValueError:
                out.append("ERR")
            except StopIteration:
                out.append("STOP")
                break
        return out
    assert run(filter) == run(ft_filter), f"\n  {run(filter)}\n  {run(ft_filter)}"

def test_function_raises_stopiteration():
    def f(x):
        raise StopIteration
    check(lambda: ((f, [1, 2]), {}))

def test_next_on_non_iterator_function_arg():
    # filter() không có __len__ / __getitem__
    r1, r2 = filter(None, [1]), ft_filter(None, [1])
    for r in (r1, r2):
        for attr in ("__len__", "__getitem__"):
            assert not hasattr(r, attr), f"không được có {attr}"


# --------------------------------------------------------------------------
# 7. Các tình huống tổng hợp
# --------------------------------------------------------------------------
def test_filter_with_lambda_capturing_state():
    def run(impl):
        seen = set()
        def uniq(x):
            if x in seen:
                return False
            seen.add(x)
            return True
        return list(impl(uniq, [1, 2, 1, 3, 2, 4]))
    assert run(filter) == run(ft_filter)

def test_bool_subclass_and_numpy_like_truthiness():
    class Weird:
        def __bool__(self): return False
        def __len__(self): return 10   # __bool__ ưu tiên hơn __len__
    items = [Weird(), Weird()]
    check(lambda: ((None, iter(items)), {}))

def test_reuse_same_function_multiple_times():
    f = lambda x: x > 1
    for _ in range(3):
        same(f, lambda: [0, 1, 2, 3])

def test_isinstance_checks():
    import collections.abc as abc
    r = ft_filter(None, [])
    assert isinstance(r, abc.Iterator)
    assert isinstance(r, abc.Iterable)



# --------------------------------------------------------------------------
# Runner (không cần pytest)
# --------------------------------------------------------------------------
def main():
    tests = [(n, f) for n, f in sorted(globals().items())
        if n.startswith("test_") and callable(f)]
    passed, failed = 0, []
    for name, fn in tests:
        try:
            fn()
            print(f"  PASS  {name}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {name}: {type(e).__name__}: {e}")
            failed.append(name)
    print("-" * 60)
    print(f"{passed}/{len(tests)} tests passed")
    if failed:
        print("Failed:", ", ".join(failed))
        sys.exit(1)

if __name__ == "__main__":
    main()
