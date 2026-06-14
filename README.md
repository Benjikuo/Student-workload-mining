# Student-workload-mining

![License](https://img.shields.io/badge/License-MIT-yellow)
![Language](https://img.shields.io/badge/Language-Python-blue)

It analyzed the homework deadline data from YZU poral platform.

This repository also includes IEEE format [**report**](https://github.com/Benjikuo/Student-workload-mining/blob/main/report.pdf) about this project.  

<p>
  <img src="https://github.com/Benjikuo/Student-workload-mining/blob/main/image/showcase.gif?raw=true" width="784">
</p>

<br>

## 🛠️ Why I Built This
- This is the group project for the **Data Mining course**. I choose this topic because it is relevant and interesting.
- It is a good opportunity to learn how to use .ipynb to analized my homework data in school's platform.
- I am corious that is it possible to predict the workload in next semester with deadlines in the last.

<br>

## 🧩 Features
- 🔧 **Visualization** – Interactive visuals that help simplify and clarify data structures and algorithms.
- 📑 **Structure** – Modular architecture with four focused sections: Basic Structures, Searching, Sorting, and Trees.
- 🕑 **Interaction** – Real-time operations such as push/pop and enqueue/dequeue for hands-on learning.
- 👟 **Animation** – Step-by-step algorithm animations that reveal how each process works internally.
- ⬜ **Interface** – A clean, minimal UI designed to support intuitive, visualization-based learning.
 

<br>

## 📂 Project Structure  
```
Homework mining/
├── image/                 # Demonstration gif
├── .env                   # Place to put your YZU portal password
├── requirements.txt       # Required Python packages
├── get_hw_list.py         # Script for collecting homework data
├── homeworks.json         # Collected homework data
├── hw_analysis.ipynb      # Data analysis and machine learning notebook
├── report.pdf             # Final project report
├── LICENSE                # MIT license
└── README.md              # Project documentation
```

<br>

## ⚙️ Requirements
Install dependencies before running:
```bash
pip install selenium python-dotenv pandas numpy matplotlib scikit-learn
```

<br>

## ▶️ How to Run
1. Clone this repository:
```bash
git clone https://github.com/Benjikuo/Student-workload-mining.git
cd Student-workload-mining
```
2. Install required packages
```bash
pip install -r requirements.txt
```
3. Add your YZU portal account at .env file
```bash
YZU_ID=your_student_id
YZU_PASS=your_password
```
4. Run the data collection script
```bash
python get_hw_list.py
```
5. Open `hw_analysis.ipynb` with Jupyter Notebook or VS Code to analyze the data.

<br>

## 📜 License
Released under the **MIT License**.  
You are free to use, modify, and share it for learning or personal projects.  

**It is a assignment to analyze assignment.**
