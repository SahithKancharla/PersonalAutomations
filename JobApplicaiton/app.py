import pandas as pd
import webbrowser
import time


excel_file = 'link.xlsx'

sheets = pd.read_excel(excel_file, sheet_name=None)

urls = []
for sheet_name, df in sheets.items():
    if df.empty or df.shape[1] < 2:
        print(f"Skipping empty or single-column sheet: '{sheet_name}'")
        continue

    sheet_urls = (
        df.iloc[:, 1]          # second column
          .dropna()            # remove NaNs
          .astype(str)         # ensure strings
          .tolist()
    )

    if sheet_urls:
        urls.extend(sheet_urls)
    else:
        print(f"No URLs found in sheet: '{sheet_name}'")

if not urls:
    print("No URLs found in any sheet. Exiting.")
    exit()

batch_size = 15

for url in urls[:batch_size]:
    webbrowser.open(url)
    time.sleep(0.5)

index = batch_size
# Loop until we've opened all URLs
while index < len(urls):
    input(f"Press Enter to open links {index+1}–{min(index+batch_size, len(urls))}...")
    for url in urls[index:index + batch_size]:
        webbrowser.open(url)
        time.sleep(0.5)
    index += batch_size
