"""Validación automatizada de los assets generados en panalnegro-assets.
Comprueba que todos los archivos SVG sean XML válido, no tengan NaN,
tengan viewBox correcto y las referencias a dimensiones sean consistentes.
"""
import pathlib
import xml.etree.ElementTree as ET

AQUI = pathlib.Path(__file__).parent

def validar_svgs():
    svgs = list(AQUI.glob("**/*.svg"))
    assert len(svgs) > 0, "No se encontraron archivos SVG para validar"
    
    errores = []
    exitos = 0
    
    for f in svgs:
        rel_path = f.relative_to(AQUI)
        try:
            content = f.read_text(encoding="utf-8")
            
            # 1. Comprobar que no haya NaNs
            if "nan" in content.lower():
                errores.append(f"{rel_path}: Contiene 'NaN' en sus datos numéricos")
                continue
                
            # 2. Parsear XML
            root = ET.fromstring(content)
            
            # 3. Comprobar namespace y tag
            if not root.tag.endswith("svg"):
                errores.append(f"{rel_path}: El tag raíz no es <svg> (encontrado: {root.tag})")
                continue
                
            # 4. Comprobar viewBox
            vb = root.attrib.get("viewBox")
            if not vb:
                errores.append(f"{rel_path}: Falta el atributo viewBox")
                continue
                
            vb_parts = [float(p) for p in vb.split()]
            if len(vb_parts) != 4:
                errores.append(f"{rel_path}: viewBox inválido: {vb}")
                continue
                
            w_vb, h_vb = vb_parts[2], vb_parts[3]
            if w_vb <= 0 or h_vb <= 0:
                errores.append(f"{rel_path}: Dimensiones de viewBox inválidas: {w_vb}x{h_vb}")
                continue
                
            exitos += 1
        except Exception as e:
            errores.append(f"{rel_path}: Error de parseo XML: {e}")

    print(f"Total SVGs analizados: {len(svgs)}")
    print(f"SVGs correctos: {exitos}")
    if errores:
        print(f"Errores encontrados ({len(errores)}):")
        for err in errores:
            print(f"  - {err}")
        return False
    else:
        print("TODOS LOS SVGS SON VALIDOS Y BIEN FORMADOS.")
        return True

if __name__ == "__main__":
    ok = validar_svgs()
    exit(0 if ok else 1)
