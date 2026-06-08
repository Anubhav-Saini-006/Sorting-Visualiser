
import pygame
import random
import sys

WIDTH, HEIGHT = 1100, 600
PANELS = 4
ARRAY_SIZE = 50
FPS = 60

BG = (18, 18, 24)
BAR = (100, 149, 237)
COMPARE = (255, 180, 50)
SWAP = (220, 60, 60)
DONE = (72, 199, 142)
TEXT = (220, 220, 220)
DIVIDER = (50, 50, 60)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Algorithm Visualizer")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 28)
small_font = pygame.font.SysFont(None, 22)

speed = 1


def make_array():
    arr = list(range(1, ARRAY_SIZE + 1))
    random.shuffle(arr)
    return arr


def bubble_sort(arr):
    a = arr[:]
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            yield a[:], j, j + 1, "compare"
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
                yield a[:], j, j + 1, "swap"
        if not swapped:
            break
    yield a[:], -1, -1, "done"


def selection_sort(arr):
    a = arr[:]
    n = len(a)
    for i in range(n):
        m = i
        for j in range(i + 1, n):
            yield a[:], m, j, "compare"
            if a[j] < a[m]:
                m = j
        if m != i:
            a[i], a[m] = a[m], a[i]
            yield a[:], i, m, "swap"
    yield a[:], -1, -1, "done"


def insertion_sort(arr):
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            yield a[:], j, j + 1, "compare"
            a[j + 1] = a[j]
            yield a[:], j, j + 1, "swap"
            j -= 1
        a[j + 1] = key
    yield a[:], -1, -1, "done"


def merge_sort(arr):
    a = arr[:]
    n = len(a)
    width = 1
    while width < n:
        for left in range(0, n, 2 * width):
            mid = min(left + width, n)
            right = min(left + 2 * width, n)

            L = a[left:mid]
            R = a[mid:right]

            i = j = 0
            k = left

            while i < len(L) and j < len(R):
                yield a[:], left + i, mid + j, "compare"
                if L[i] <= R[j]:
                    a[k] = L[i]
                    i += 1
                else:
                    a[k] = R[j]
                    j += 1
                yield a[:], k, -1, "swap"
                k += 1

            while i < len(L):
                a[k] = L[i]
                i += 1
                k += 1

            while j < len(R):
                a[k] = R[j]
                j += 1
                k += 1

        width *= 2

    yield a[:], -1, -1, "done"


class Panel:
    def __init__(self, name):
        self.name = name
        self.comparisons = 0
        self.swaps = 0
        self.finished = False
        self.arr = []
        self.a = -1
        self.b = -1
        self.action = None


def setup():
    base = make_array()

    panels = [
        Panel("Bubble Sort"),
        Panel("Selection Sort"),
        Panel("Insertion Sort"),
        Panel("Merge Sort"),
    ]

    gens = [
        bubble_sort(base),
        selection_sort(base),
        insertion_sort(base),
        merge_sort(base),
    ]

    for p in panels:
        p.arr = base[:]

    return panels, gens


def draw_panel(panel, idx):
    panel_width = WIDTH // PANELS
    x_offset = idx * panel_width

    chart_height = HEIGHT - 100

    pygame.draw.line(
        screen, DIVIDER,
        (x_offset, 0),
        (x_offset, HEIGHT),
        2
    )

    n = len(panel.arr)
    if n == 0:
        return

    bar_width = panel_width / n

    for i, value in enumerate(panel.arr):
        h = (value / ARRAY_SIZE) * chart_height

        color = BAR

        if panel.finished:
            color = DONE
        elif panel.action == "compare" and i in (panel.a, panel.b):
            color = COMPARE
        elif panel.action == "swap" and i in (panel.a, panel.b):
            color = SWAP

        x = x_offset + i * bar_width
        y = HEIGHT - 80 - h

        pygame.draw.rect(
            screen,
            color,
            (x + 1, y, max(bar_width - 2, 1), h)
        )

    title = font.render(panel.name, True, TEXT)
    stats = small_font.render(
        f"cmp:{panel.comparisons} swp:{panel.swaps}",
        True,
        TEXT
    )

    screen.blit(title, (x_offset + 10, HEIGHT - 65))
    screen.blit(stats, (x_offset + 10, HEIGHT - 35))


panels, generators = setup()

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                panels, generators = setup()

            elif event.key == pygame.K_UP:
                speed = min(speed + 1, 20)

            elif event.key == pygame.K_DOWN:
                speed = max(speed - 1, 1)

    for _ in range(speed):
        for i, gen in enumerate(generators):
            panel = panels[i]

            if panel.finished:
                continue

            try:
                arr, a, b, action = next(gen)

                panel.arr = arr
                panel.a = a
                panel.b = b
                panel.action = action

                if action == "compare":
                    panel.comparisons += 1
                elif action == "swap":
                    panel.swaps += 1
                elif action == "done":
                    panel.finished = True

            except StopIteration:
                panel.finished = True

    screen.fill(BG)

    for i, panel in enumerate(panels):
        draw_panel(panel, i)

    info = small_font.render(
        f"UP/DOWN = Speed ({speed})   R = Restart",
        True,
        TEXT
    )
    screen.blit(info, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
