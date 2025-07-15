# wbgenplus

A **WishBone³** bus device generator for VHDL, written in Python. Automatically produces VHDL interfaces to WishBone buses, saving manual boilerplate coding time.

---

## 🔧 Features

- Generates **VHDL entity/architecture/package/stub** files for custom WishBone³ bus peripherals.
- Also generates matching register layouts as C header files for firmware/software use
- Python-based—no manual VHDL template editing required
- interfaces are described as XML structures
- Ideal for FPGA/ASIC projects using WishBone interconnects

---

## 🛠️ Requirements

- Python 3.7+
- No external dependencies (pure Python tool)

---

## 🚀 Installation

Clone the repo:
```bash
git clone https://github.com/mkreider/wbgenplus.git
cd wbgenplus
```

Run wbgenplus on the included example XMLs to get started
