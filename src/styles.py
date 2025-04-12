import os
import random
import sys
import time
from colorama import init
from colorama import Fore, Style as ColoramaStyle


GREEN = "\033[92m"
RESET = "\033[0m"
BOLD = "\033[1m"

matrix_chars = (
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()"
)

init()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def typewriter(text, delay=0.02):
    for char in text:
        sys.stdout.write(GREEN + char + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def glitch_text(text, glitch_prob=0.1):
    result = ""
    for char in text:
        if random.random() < glitch_prob:

            effect = random.choice(
                [
                    lambda c: f"{Fore.LIGHTGREEN_EX}{c}{ColoramaStyle.RESET_ALL}",
                    lambda c: f"{Fore.GREEN}{c}{ColoramaStyle.RESET_ALL}",
                    lambda c: f"{Fore.WHITE}{c}{ColoramaStyle.RESET_ALL}",
                    lambda c: f"\033[38;2;0;{int(200*random.random())+55};0m{c}{ColoramaStyle.RESET_ALL}",
                    lambda c: "".join(
                        f"{Fore.GREEN}{random.choice(matrix_chars)}{ColoramaStyle.RESET_ALL}"
                        for _ in range(1, 3)
                    ),
                    lambda c: c.upper() if c.islower() else c.lower(),
                    lambda c: f"{c}{Fore.GREEN}{random.choice(matrix_chars)}{ColoramaStyle.RESET_ALL}",
                ]
            )
            result += effect(char)
        else:
            result += char
    return result


def typewriter_with_glitch(text, delay=0.02, glitch_prob=0.05):
    glitched_text = glitch_text(text, glitch_prob)
    for char in glitched_text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay * (0.5 + random.random() * 1.0))
    print()


def show_matrix_intro():
    clear_screen()
    typewriter_with_glitch("Booting up Matrix CLI...\n", 0.03, 0.07)
    time.sleep(0.5)

    progress_bar_length = 20
    for i in range(progress_bar_length + 1):
        bar = "[-" + "|" * i + " " * (progress_bar_length - i) + "-]"
        percentage = int((i / progress_bar_length) * 100)
        sys.stdout.write(
            f"\r{Fore.GREEN}Loading modules... {bar} {percentage}%{ColoramaStyle.RESET_ALL}"
        )
        sys.stdout.flush()
        time.sleep(0.1)
    print()

    time.sleep(0.5)
    typewriter_with_glitch("System initialization...", 0.05, 0.1)
    time.sleep(0.3)
    typewriter_with_glitch("Matrix connection established.", 0.05)
    time.sleep(0.5)
    typewriter_with_glitch(
        f"{Fore.WHITE}{ColoramaStyle.BRIGHT}Welcome, operator.{ColoramaStyle.RESET_ALL}\n",
        0.05,
    )
    time.sleep(0.5)


def matrix_rain(columns=100, lines=50, speed=0.05):
    try:

        streams = [
            {"pos": i, "speed": random.random() * 0.1 + 0.02, "length": int(random.random() * 5) + 3}
            for i in range(0, columns, 3)
        ]

        for _ in range(lines):
            line = [" "] * columns

            for stream in streams:

                pos = int(stream["pos"]) % columns
                line[pos] = (
                    f"{Fore.WHITE}{random.choice(matrix_chars)}{ColoramaStyle.RESET_ALL}"
                )

                for i in range(1, stream["length"]):
                    trail_pos = (pos - i) % columns
                    intensity = int(255 * (1 - i / stream["length"]))
                    line[trail_pos] = (
                        f"\033[38;2;0;{intensity};0m{random.choice(matrix_chars)}{ColoramaStyle.RESET_ALL}"
                    )

                stream["pos"] = (stream["pos"] + stream["speed"]) % columns

            print("".join(line))
            time.sleep(speed)
    except KeyboardInterrupt:
        pass


def floating_message(messages, width=80, height=15):
    positions = [
        (int(random.random() * width), int(random.random() * height)) for _ in range(len(messages))
    ]
    vectors = [(random.random() * 2 - 1, random.random() * 2 - 1) for _ in range(len(messages))]

    try:
        for frame in range(100):

            matrix = [
                [random.choice(matrix_chars) if random.random() < 0.05 else " " for _ in range(width)]
                for _ in range(height)
            ]

            for i, message in enumerate(messages):
                x, y = int(positions[i][0]), int(positions[i][1])
                if 0 <= y < height:
                    for j, char in enumerate(message):
                        if 0 <= x + j < width:
                            matrix[y][
                                x + j
                            ] = f"{Fore.WHITE}{ColoramaStyle.BRIGHT}{char}{ColoramaStyle.RESET_ALL}"

                positions[i] = (
                    (positions[i][0] + vectors[i][0]) % width,
                    (positions[i][1] + vectors[i][1]) % height,
                )

            clear_screen()
            for row in matrix:
                print(f"{Fore.GREEN}" + "".join(row) + f"{ColoramaStyle.RESET_ALL}")

            time.sleep(0.1)
    except KeyboardInterrupt:
        clear_screen()


def show_access_granted():
    clear_screen()

    typewriter_with_glitch("MATRIX: SECURITY SYSTEM", 0.03)
    typewriter_with_glitch("........................", 0.05)
    time.sleep(0.5)

    typewriter_with_glitch("Scanning in progress...", 0.03)
    time.sleep(1)

    print(f"{Fore.CYAN}Biometric authentication: {ColoramaStyle.RESET_ALL}", end="")
    for _ in range(20):
        sys.stdout.write(random.choice(["▓", "▒", "░"]))
        sys.stdout.flush()
        time.sleep(0.1)
    print(f" {Fore.GREEN}[SUCCESS]{ColoramaStyle.RESET_ALL}")
    time.sleep(0.3)

    print(f"{Fore.CYAN}Access decryption: {ColoramaStyle.RESET_ALL}", end="")
    for i in range(10):
        progress = i * 10
        sys.stdout.write(
            f"\r{Fore.CYAN}Access decryption: {Fore.GREEN}{progress}%{ColoramaStyle.RESET_ALL}"
        )
        sys.stdout.flush()
        time.sleep(0.2)
    print(f"\r{Fore.CYAN}Access decryption: {Fore.GREEN}100%{ColoramaStyle.RESET_ALL}")

    time.sleep(0.5)
    print("\n" + "=" * 40)
    print(f"{Fore.GREEN}{ColoramaStyle.BRIGHT}ACCESS GRANTED{ColoramaStyle.RESET_ALL}")
    print(
        f"{Fore.GREEN}Welcome to project {Fore.WHITE}PRJCT_HLPR{ColoramaStyle.RESET_ALL}"
    )
    print("=" * 40)
    time.sleep(1.5)
