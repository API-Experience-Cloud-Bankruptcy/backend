# Backend

基於 **uv** 與 **FastAPI** 的後端專案。

---

## 🚀 建立虛擬環境

```bash
uv venv
```

> 若需指定 Python 版本：
>
> ```bash
> uv venv --python 3.12
> ```

---

## ⚙️ 安裝依賴

```bash
uv sync
```

或新增新套件：

```bash
uv add <package>
```

---

## 🧩 必要 VS Code 擴充套件

| Extension | ID                         |
| --------- | -------------------------- |
| Python    | `ms-python.python`         |
| Pylance   | `ms-python.vscode-pylance` |
| Ruff      | `charliermarsh.ruff`       |

快速安裝：

```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension charliermarsh.ruff
```

---

## ▶️ 執行伺服器

請於專案根目錄執行：

```bash
uv run uvicorn app.main:app --reload
```

瀏覽器開啟：

* [http://127.0.0.1:8000](http://127.0.0.1:8000)
* [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📖 uv 安裝文件

如尚未安裝 `uv`，請參考官方文件：

🔗 [https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_2](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_2)

---

## 🗂️ 專案結構（示例）

```
backend/
├─ app/
│  ├─ main.py
│  └─ router.py
├─ pyproject.toml
├─ uv.lock
└─ README.md
```
