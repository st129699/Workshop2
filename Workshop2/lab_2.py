import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ========== 1. ЗАГРУЗКА ДАННЫХ (ДЛЯ ВАШЕГО ФОРМАТА) ==========
U_eb = []
ln_I = []

with open('lab7_measurements.csv', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()
    
    # Пропускаем первую строку (заголовок)
    for line in lines[1:]:
        line = line.strip()
        if line:
            # Убираем кавычки, если есть
            line = line.replace('"', '')
            parts = line.split(',')
            if len(parts) >= 3:
                try:
                    u_val = float(parts[0].replace(',', '.'))
                    # Пропускаем I_k_ma (второй столбец)
                    ln_val = float(parts[2].replace(',', '.'))
                    U_eb.append(u_val)
                    ln_I.append(ln_val)
                except Exception as e:
                    print(f"Ошибка в строке: {line} - {e}")

n = len(U_eb)
print(f"Загружено {n} измерений")

if n == 0:
    print("\nОШИБКА: Данные не загружены!")
    print("Проверьте файл lab7_measurements.csv")
    exit(1)

print(f"U_эб: {U_eb}")
print(f"ln I_к: {ln_I}")

# ========== 2. МЕТОД НАИМЕНЬШИХ КВАДРАТОВ ==========
slope, intercept, r_value, p_value, std_err = stats.linregress(U_eb, ln_I)

print("\n" + "="*60)
print("РЕЗУЛЬТАТЫ МЕТОДА НАИМЕНЬШИХ КВАДРАТОВ")
print("="*60)
print(f"Уравнение: ln I_к = {intercept:.6f} + {slope:.6f} * U_эб")
print(f"Коэффициент корреляции: r = {r_value:.6f}")
print(f"Коэффициент детерминации: R² = {r_value**2:.6f}")
print(f"Стандартная ошибка наклона: Δb = {std_err:.6f}")

# ========== 3. РАСЧЕТ e/k ==========
T = 299.18  # абсолютная температура, К
e_k = slope * T
delta_e_k = std_err * T

print("\n" + "="*60)
print("РАСЧЕТ ОТНОШЕНИЯ e/k")
print("="*60)
print(f"Температура: T = {T:.2f} K")
print(f"Наклон (b) = {slope:.6f} В⁻¹")
print(f"e/k = b * T = {e_k:.2f} Кл/К")
print(f"Погрешность Δ(e/k) = {delta_e_k:.2f} Кл/К")

# Теоретическое значение
e = 1.602e-19
k = 1.381e-23
e_k_theory = e / k

print(f"\nТеоретическое значение: {e_k_theory:.2f} Кл/К")
print(f"Относительная погрешность: {abs(e_k - e_k_theory)/e_k_theory*100:.2f}%")

# ========== 4. ПОСТРОЕНИЕ ГРАФИКА ==========
plt.figure(figsize=(10, 6))
plt.scatter(U_eb, ln_I, color='blue', s=50, label='Экспериментальные точки')

U_fit = np.linspace(min(U_eb)-0.01, max(U_eb)+0.01, 100)
ln_I_fit = slope * U_fit + intercept
plt.plot(U_fit, ln_I_fit, 'r-', linewidth=2, 
         label=f'МНК: ln I_к = {slope:.4f}·U_эб + {intercept:.4f}')

plt.xlabel('U_эб, В', fontsize=12)
plt.ylabel('ln I_к', fontsize=12)
plt.title('Зависимость ln I_к от напряжения эмиттер-база', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('lnI_vs_U.png', dpi=150)
print("\n✓ Сохранен: lnI_vs_U.png")
plt.close()

# ========== 5. СОХРАНЕНИЕ РЕЗУЛЬТАТОВ ==========
with open('results_lab7.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(['Параметр', 'Значение', 'Единица измерения'])
    writer.writerow(['Количество измерений', n, ''])
    writer.writerow(['Наклон (b)', f"{slope:.6f}", 'В⁻¹'])
    writer.writerow(['Свободный член (a)', f"{intercept:.6f}", ''])
    writer.writerow(['Коэффициент корреляции', f"{r_value:.6f}", ''])
    writer.writerow(['R²', f"{r_value**2:.6f}", ''])
    writer.writerow(['Температура', T, 'K'])
    writer.writerow(['e/k (эксперимент)', f"{e_k:.2f}", 'Кл/К'])
    writer.writerow(['Δ(e/k)', f"{delta_e_k:.2f}", 'Кл/К'])
    writer.writerow(['e/k (теория)', f"{e_k_theory:.2f}", 'Кл/К'])

print("\n✓ Сохранен: results_lab7.csv")
print("\n" + "="*60)
print(f"ИТОГОВЫЙ РЕЗУЛЬТАТ: e/k = {e_k:.0f} ± {delta_e_k:.0f} Кл/К")
print("="*60)