from io import BytesIO
import pandas as pd

def to_excel(data: list[dict], sheet_name: str):
    df=pd.DataFrame(data)
    output=BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer,index=False,sheet_name=sheet_name[:31])
    output.seek(0)
    return output

def to_csv(data: list[dict]):
    df=pd.DataFrame(data)
    return BytesIO(df.to_csv(index=False).encode('utf-8'))
