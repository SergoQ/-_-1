import random
import numpy as np
import matplotlib.pyplot as plt

class CityGrid:
    def __init__(self, n, m, budget, порог_покрытия=0.3):
        self.n = n
        self.m = m
        self.budget = budget
        self.grid = np.zeros((n, m), dtype=bool)  # Сетка города
        self.coverage = np.zeros((n, m), dtype=bool)  # Зона покрытия вышек
        self.tower_types = []  # Типы вышек с различными радиусами и стоимостями
        
        # Размещение заблокированных блоков случайным образом
        for i in range(n):
            for j in range(m):
                if random.random() > порог_покрытия:
                    self.grid[i, j] = True
    
    def add_tower_type(self, r, cost):
        # Добавление типа вышки с заданным радиусом и стоимостью
        self.tower_types.append((r, cost))
    
    def place_tower(self, x, y, r):
        # Определение зоны покрытия вышки
        for i in range(max(0, x - r), min(self.n, x + r + 1)):
            for j in range(max(0, y - r), min(self.m, y + r + 1)):
                if (i - x) ** 2 + (j - y) ** 2 <= r ** 2:
                    self.coverage[i, j] = True
    
    def optimize_towers(self):
        # Размещение вышек, чтобы максимизировать покрытие при ограниченном бюджете
        вышки = []
        budget_left = self.budget
        
        while budget_left > 0:
            best_tower = None
            best_coverage = np.copy(self.coverage)
            best_cost = float('inf')
            
            for x in range(self.n):
                for y in range(self.m):
                    if self.grid[x, y] or self.coverage[x, y]:
                        continue
                    
                    for r, cost in self.tower_types:
                        new_coverage = np.copy(self.coverage)
                        self.place_tower(x, y, r)
                        
                        # Вычисление дополнительного покрытия и стоимости
                        additional_coverage = np.sum(self.coverage) - np.sum(new_coverage)
                        total_cost = cost + additional_coverage
                        
                        if total_cost < best_cost:
                            best_tower = (x, y, r)
                            best_coverage = new_coverage
                            best_cost = total_cost
            
            if best_tower is None:
                break
            
            x, y, r = best_tower
            self.place_tower(x, y, r)
            вышки.append((x, y, r))
            budget_left -= best_cost
        
        return вышки
    
    def plot_grid(self):
        # Визуализация сетки города с заблокированными блоками и зонами покрытия вышек
        plt.figure(figsize=(10, 10))
        plt.imshow(self.grid, cmap='gray')
        plt.imshow(self.coverage, cmap='cool', alpha=0.3)
        plt.title('Сетка города')
        plt.show()

