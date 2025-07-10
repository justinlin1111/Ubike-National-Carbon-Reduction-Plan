from src.predict.model_predictor import predict_model
from src.utils.genetic_algorithm import genetic_algorithm

# 這邊參數也直接放到config統一管理比較好
Stations = predict_model('dnn', '2024-06-15 18:00', '捷運公館站(1號出口)')

#---GA---
solutions = genetic_algorithm(Stations)
sln_sum = 0
for station, allocation in zip(Stations, solutions):
    sln_sum += allocation
    if allocation < 0:
        print(f"{station.name}需要移走{-allocation}輛車")
    elif allocation > 0:
        print(f"{station.name}需要移入{allocation}輛車")

print("sln_sum =", sln_sum)