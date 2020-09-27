from chosun import ChosunHandler
from hani import HaniHandler


# TODO async io 적용하기
def main():
    # 조선일보
    chosun = ChosunHandler()
    chosun.paper_route()
    # 한계레
    hani = HaniHandler()
    hani.paper_route()


if __name__ == "__main__":
    main()