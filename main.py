import random
from custom_exceptions import SurplusEmptyError, DeficitEmptyError
import Station
import genetic_algorithm

if __name__ == "__main__":
    print("hello world")

'''
輸出
調度完的結果
調度花費

to do list:
1.意願函數 假設 100
    車子 100 + 油錢(先不考慮/3.3 * 0.7 ntd/km)
    意願 100% 費用 5
    <=20騎 相反 車載
2.意願不是100討論期望值
    def 意願函數(費用 距離)
4.預測需求:可以使用很多方法 抓真實資料比較有意義 可以抓去年下學期的Ubike使用數量
最後在使用GA或者其他方法來實現調度
5.這樣的話需求就不需要隨機，而可以直接變成一個已知數



'''