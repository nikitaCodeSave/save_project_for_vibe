import os


def collect_py_files(root_dir, output_md="project.md"):
    """
    Рекурсивно обходит root_dir и собирает все .py файлы в единый Markdown-файл output_md.
    В итоговом файле указывается путь к каждому файлу и его содержимое,
    исключая директории, начинающиеся с '.'.
    """

    with open(output_md, "w", encoding="utf-8") as md_file:
        for current_path, dirs, files in os.walk(root_dir):
            # Исключаем скрытые директории (начинающиеся с ".")
            dirs[:] = [d for d in dirs if not d.startswith(".")]

            # Обходим файлы
            for filename in files:
                # Игнорируем всё, кроме .py
                if not filename.endswith(".py"):
                    continue

                # Полный путь к файлу
                full_path = os.path.join(current_path, filename)

                # Пропускаем сам выходной файл, чтобы не включать его содержимое внутрь себя
                if os.path.abspath(full_path) == os.path.abspath(output_md):
                    continue

                # Пытаемся прочитать содержимое файла
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception as e:
                    print(f"Не удалось прочитать файл {full_path}. Ошибка: {e}")
                    continue

                # Определяем относительный путь
                relative_path = os.path.relpath(full_path, root_dir)

                # Записываем данные о файле в Markdown
                md_file.write(f"## Файл: `{relative_path}`\n\n")
                md_file.write("```python\n")
                md_file.write(content)
                md_file.write("\n```\n\n")

    print(f"Все .py-файлы из директории '{root_dir}' собраны в '{output_md}'.")


if __name__ == "__main__":
    # Пример использования
    project_directory = "./"
    output_file_name = "project.md"

    collect_py_files(project_directory, output_file_name)
