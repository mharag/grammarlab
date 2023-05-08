from glab.export.export import Export, formatter


class A:
    pass


class B(A):
    pass


class C(A):
    pass


class ExportTest(Export):
    @formatter(A)
    def A(self, a):
        return "A"

    @formatter(B)
    def B(self, b):
        return "B"


def test_export():
    assert ExportTest().export(A()) == "A"
    assert ExportTest().export(B()) == "B"
    assert ExportTest().export(C()) == "A"
