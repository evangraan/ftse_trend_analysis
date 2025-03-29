import pandas as pd
from pathlib import Path

xlsx_dir = Path("../")
output_dir = xlsx_dir / "csv"
output_dir.mkdir(exist_ok=True)

for xlsx_file in xlsx_dir.glob("*.xlsx"):
    try:
        sheet_name = "Index Values"
        csv_filename = output_dir / f"{xlsx_file.stem}_{sheet_name}.csv"

        if csv_filename.exists():
            print(f"Already exists, skipping: {csv_filename.name}")
            continue

        df = pd.read_excel(xlsx_file, sheet_name=sheet_name, engine='openpyxl')
        df.to_csv(csv_filename, index=False)
        print(f"Converted: {csv_filename.name}")

    except Exception as e:
        print(f"Failed to convert {xlsx_file.name}: {e}")
