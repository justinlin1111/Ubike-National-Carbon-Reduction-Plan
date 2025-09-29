# 🚲 Ubike-National-Carbon-Reduction-Plan

本專案旨在透過 **深度學習 (Deep Learning)** 與 **基因演算法 (Genetic Algorithm, GA)**，實現 **公共自行車（YouBike）調度最佳化**，以協助城市降低碳排放、提升運輸效率。  
系統會預測各站點在未來一段時間內的「最佳需求量」，並據此自動生成一組調度策略，協助車輛再分配。

---

## 📊 系統流程概述

```mermaid
graph TD
    A[📂 歷史資料收集] --> B[🔍 特徵選擇]
    B --> C[🧠 深度學習模型訓練]
    C --> D[📈 預測未來需求量]
    D --> E[🔁 轉換為 GA 輸入格式]
    E --> F[🧬 基因演算法最佳化]
    F --> G[🚚 輸出車輛調度策略]
