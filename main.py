import ezdxf
import pandas as pd
import os
from glob import glob

print("--- BIM Automator Milano v2 ---")

# Acha automaticamente qualquer DWG na pasta
dwgs = glob("*.dwg")
print(f"Encontrei {len(dwgs)} DWGs: {dwgs}")

if not dwgs:
    print("Nenhum DWG encontrado!")
    exit()

# Pega o primeiro DWG
arquivo = dwgs[0] # vai pegar a Capela ou o Sessa
print(f"Lendo: {arquivo}...")

try:
    doc = ezdxf.readfile(arquivo)
    msp = doc.modelspace()

    dados = []
    total_comprimento = 0

    for e in msp:
        try:
            if e.dxftype() == 'LINE':
                comp = e.dxf.length if hasattr(e.dxf, 'length') else 0
                dados.append({"Elemento": "LINE", "Layer": e.dxf.layer, "Comprimento": round(float(e.length),2)})
            elif e.dxftype() == 'LWPOLYLINE':
                dados.append({"Elemento": "POLYLINE", "Layer": e.dxf.layer, "Comprimento": round(float(e.length),2)})
            elif e.dxftype() == 'CIRCLE':
                dados.append({"Elemento": "CIRCLE", "Layer": e.dxf.layer, "Comprimento": round(float(e.dxf.radius*2*3.14),2)})
        except:
            pass

    df = pd.DataFrame(dados)

    # Resumo por Layer (isso é o QTO de verdade!)
    resumo = df.groupby("Layer")["Comprimento"].agg(["count", "sum"]).reset_index()
    resumo.columns = ["Layer", "Qtd_Elementos", "Comprimento_Total_m"]

    with pd.ExcelWriter("computo_metrico.xlsx") as writer:
        df.to_excel(writer, sheet_name="Detalhe", index=False)
        resumo.to_excel(writer, sheet_name="Resumo_por_Layer", index=False)

    print(f"✅ SUCESSO! {len(df)} elementos lidos!")
    print(resumo.head(10))
    print("📁 Gerado: computo_metrico.xlsx com 2 abas!")

except Exception as err:
    print(f"❌ Erro ao ler {arquivo}: {err}")
    print("Dica: Abra no AutoCAD e salve como 'AutoCAD 2013 DXF' e tente de novo.")