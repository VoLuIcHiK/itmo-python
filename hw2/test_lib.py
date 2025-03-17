import os
# ссылка на установку библиотеки https://pypi.org/project/itmo-latex-generator/
from latex_generator import generate_latex_table, generate_latex_image


data = [
    ["Column №1", "Column №2", "Column №3"],
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

latex_table = generate_latex_table(data)

# Генерация LaTeX кода для изображения
image_path = "hw2/artifacts/test.png" 
latex_image = generate_latex_image(image_path, width="4cm")

# Создание полного LaTeX документа
latex_document = f"""
\\documentclass{{article}}
\\usepackage{{graphicx}}
\\begin{{document}}

\\section{{Table}}
{latex_table}

\\section{{Image}}
{latex_image}

\\end{{document}}
"""

# Сохранение в .tex файл
with open("hw2/artifacts/res_doc.tex", "w+") as file:
    file.write(latex_document)

print("LaTeX код сохранен: res_doc.tex")

try:
    os.system("pdflatex -output-directory=hw2/artifacts/ hw2/artifacts/res_doc.tex")
    print("PDF успешно сгенерирован: res_doc.pdf")
except Exception as e:
    print(f"Ошибка при компиляции LaTeX: {e}")