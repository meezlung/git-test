# pyright: strict

from lab05c import TippyMemory

def test_TippyMemory():
    tippy_memory = TippyMemory()

    tippy_memory.entered_line(10, "Aoyama")
    tippy_memory.entered_line(20, "Syaro")
    assert tippy_memory.front(30) == "Aoyama"
    tippy_memory.entered_line(40, "Mocha")
    tippy_memory.front_served(50)
    assert tippy_memory.front(60) == "Syaro"
    tippy_memory.slept(35)
    assert tippy_memory.front(40) == "Aoyama"

    # TODO add more tests here
