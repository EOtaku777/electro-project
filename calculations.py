import math

def calc_current(power_kw, voltage=220, power_factor=0.95):
    """Расчёт тока по мощности"""
    return round((power_kw * 1000) / (voltage * power_factor), 1)

def select_circuit_breaker(current_a):
    """Выбирает автомат по току"""
    standard_ratings = [6, 10, 16, 20, 25, 32, 40, 50, 63]
    for rating in standard_ratings:
        if rating >= current_a:
            return rating
    return 63

def calculate_group_load(devices):
    """Суммарная нагрузка группы"""
    total_power = sum(d['power_kw'] for d in devices)
    total_current = sum(calc_current(d['power_kw']) for d in devices)
    # Коэффициент одновременности для жилых помещений
    if len(devices) <= 3:
        koef = 1.0
    elif len(devices) <= 6:
        koef = 0.8
    else:
        koef = 0.7
    
    return {
        'total_power': round(total_power * koef, 1),
        'total_current': round(total_current * koef, 1),
        'recommended_breaker': select_circuit_breaker(round(total_current * koef)),
        'koef_simultaneity': koef
    }

# Пример использования
if __name__ == '__main__':
    devices = [
        {'name': 'Розетки кухня', 'power_kw': 3.5},
        {'name': 'Чайник', 'power_kw': 2.0},
        {'name': 'Микроволновка', 'power_kw': 1.5},
    ]
    result = calculate_group_load(devices)
    print(f"Ток: {result['total_current']}А → Автомат: {result['recommended_breaker']}А")