# DigiTwin LIDAR Vehicle Profile Processing

This project processes 3D LIDAR data to analyze the profiles of vehicles passing under a scanning gantry, simulating a real-world highway detection system.

![image](https://github.com/user-attachments/assets/2562be4a-e587-486a-ae5c-545a5a2b9800)

![image](https://github.com/user-attachments/assets/e9657a62-faea-4dd0-b2cc-4e23b72e48b9)

---

## 📚 Project Overview

- **Goal:** Load and merge LIDAR scan data, generate 3D point clouds, and automatically measure the width, height, and length of each detected vehicle.
- **Context:** Vehicles are scanned in real time. Those exceeding height or width limits are detected, and warnings are triggered for alternative routing.

---

## 🗂️ Repository Structure

project-root/
│
├── src/                    # Source code
│   └── main.py
├── input_data/             # Raw data
│   ├── measurements/
│   │   ├── LIDAR0_01.txt
│   │   └── LIDAR1_01.txt
│   └── vehicle_info.txt
├── python_helper/          # Output point clouds & results
│   └── Cloud_01.txt
├── requirements.txt        # Python dependencies
├── README.md
├── .gitignore
└── LICENSE

---

## 🚀 How to Run

1. **Clone the repository**

   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name

2. **Install dependencies**

   pip install -r requirements.txt

3. **Prepare input data**
   - Place LIDAR and vehicle info files inside `input_data/measurements/` and `input_data/`.

4. **Run the main script**

   python src/main.py

   Output point clouds and vehicle dimensions will appear in `python_helper/`.

---

## 📊 Results

- **Point clouds**: Saved in `python_helper/Cloud_xx.txt` (one per vehicle)
- **Dimensions**: Printed in console and saved in `python_helper/dimensions.txt`

---

## 📦 Dependencies

See `requirements.txt`. Main dependencies:
- numpy
- pyqt5, pyqtgraph, pyopengl (for 3D visualization)

---

## 🙋‍♂️ Authors

- ANge-Morija KOUAMENAN [University of BME Budapest]
- 2025

---

## 📝 License

MIT License (or as specified)

---

## 📷 Example Visualization
![image](https://github.com/user-attachments/assets/ea327959-3f62-427f-b89b-9d87434df042)
---

## 📣 Contact

For questions, please contact [kouamenanangemorija@gmail.com].
