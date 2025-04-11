import colorama 

def format_table(data, headers, colors=None):
    colorama.init(autoreset=True)
    # Ширина колонок
    col_widths = [
        max(len(str(row[i])) for row in ([headers] + data))
        for i in range(len(headers))
    ]
    def fmt_row(row, sep=f"{colorama.Fore.LIGHTGREEN_EX}║", row_colors=None):
        result = sep
        for i, cell in enumerate(row):
            color = row_colors[i] if row_colors else ""
            reset = colorama.Style.RESET_ALL if row_colors else ""
            result += f" {color}{str(cell):<{col_widths[i]}}{reset} " + sep
        return result
    def line(left, mid, right, fill):
        return left + mid.join(fill * (w + 2) for w in col_widths) + right
    table = []
    table.append(colorama.Fore.LIGHTGREEN_EX + line("╔", "╦", "╗", "═") + colorama.Style.RESET_ALL)
    table.append(fmt_row(headers, row_colors=[colorama.Fore.GREEN] * len(headers)))
    table.append(colorama.Fore.LIGHTGREEN_EX + line("╠", "╬", "╣", "═") + colorama.Style.RESET_ALL)
    for row in data:
        table.append(fmt_row(row, row_colors=colors))
    table.append(colorama.Fore.LIGHTGREEN_EX + line("╚", "╩", "╝", "═") + colorama.Style.RESET_ALL)
    return "\n".join(table)
