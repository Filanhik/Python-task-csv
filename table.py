import argparse
import csv
import sys
from tabulate import tabulate

def read_csv(path):
    try:
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except Exception:
        sys.exit("Ошибка при чтении файла")

def apply_filter(rows, where):
    if not where:
        return rows

    if ">>" in where or "<<" in where or "==" in where:
        sys.exit("Неверный формат фильтрации")

    if ">" in where:
        col, val = where.split(">", 1)
        op = ">"
    elif "<" in where:
        col, val = where.split("<", 1)
        op = "<"
    elif "=" in where:
        col, val = where.split("=", 1)
        op = "="
    else:
        sys.exit("Неверный формат фильтрации")

    col, val = col.strip(), val.strip()
    if not rows or col not in rows[0]:
        sys.exit(f"Нет колонки: {col}")

    result = []
    for row in rows:
        cell = row.get(col, "")
        try:
            a = float(cell)
            b = float(val)
        except ValueError:
            a, b = cell, val

        if (op == ">" and a > b) or (op == "<" and a < b) or (op == "=" and a == b):
            result.append(row)
    return result

def aggregate(rows, agg):
    if not agg:
        return ""

    if "=" not in agg:
        sys.exit("Неверный формат агрегации")

    func, col = agg.split("=", 1)
    func, col = func.strip(), col.strip()

    if not rows or col not in rows[0]:
        sys.exit(f"Нет колонки: {col}")

    try:
        nums = [float(r[col]) for r in rows]
    except ValueError:
        sys.exit("Нельзя агрегировать нечисловые данные")

    if func == "avg":
        return f"AVG({col}) = {sum(nums)/len(nums):.2f}"
    elif func == "min":
        return f"MIN({col}) = {min(nums)}"
    elif func == "max":
        return f"MAX({col}) = {max(nums)}"
    else:
        sys.exit(f"Неизвестная агрегат-функция: {func}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath")
    parser.add_argument("--where")
    parser.add_argument("--aggregate")
    args = parser.parse_args()

    data = read_csv(args.filepath)
    data = apply_filter(data, args.where)

    if args.aggregate:
        print(aggregate(data, args.aggregate))
    else:
        print(tabulate(data, headers="keys", tablefmt="grid"))

if __name__ == "__main__":
    main()