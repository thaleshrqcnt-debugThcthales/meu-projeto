#!/usr/bin/env python3
"""
Fatia uma imagem em folhas A4 para montar um lambe-lambe numa tela 90x120 cm.

Grade: 5 colunas x 5 linhas = 25 folhas A4 (retrato).
Cada folha leva um pedaço de 18 x 24 cm da imagem (mesma proporção 3:4 da tela)
mais 1 cm de "aba" à direita e embaixo, que fica escondida sob a folha vizinha.

Uso:
    python3 fatiar_a4.py --esboco                 # gera esboco.png (layout de referência)
    python3 fatiar_a4.py arte_final.png           # gera lambe_lambe_A4.pdf + mapa_montagem.png
    python3 fatiar_a4.py arte_final.png --dpi 300 --saida meu.pdf

Imprima o PDF em "Tamanho real / 100%" (NUNCA "Ajustar à página").
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

# --- medidas em centímetros -------------------------------------------------
TELA_L, TELA_A = 90.0, 120.0     # tela (largura x altura)
COLS, LINHAS = 5, 5
PECA_L, PECA_A = TELA_L / COLS, TELA_A / LINHAS   # 18 x 24 cm
ABA = 1.0                        # sobreposição para colagem
A4_L, A4_A = 21.0, 29.7
MARGEM_ESQ, MARGEM_TOPO = 1.0, 1.2  # cabe nas margens não imprimíveis (~0,5 cm)
NOMES_LINHA = "ABCDE"

FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def fonte(tam):
    try:
        return ImageFont.truetype(FONTE, tam)
    except OSError:
        return ImageFont.load_default()


def cm(v, dpi):
    return round(v / 2.54 * dpi)


def preparar_imagem(caminho, dpi):
    """Abre a arte e ajusta (recorte central) para exatamente 90x120 cm no DPI pedido."""
    img = Image.open(caminho).convert("RGB")
    alvo = (cm(TELA_L, dpi), cm(TELA_A, dpi))
    prop_img, prop_tela = img.width / img.height, TELA_L / TELA_A
    if abs(prop_img - prop_tela) > 0.01:
        print(f"Aviso: a imagem tem proporção {prop_img:.3f}, a tela é 3:4 ({prop_tela:.3f}). "
              "As bordas serão recortadas pelo centro.")
    dpi_real = min(img.width / (TELA_L / 2.54), img.height / (TELA_A / 2.54))
    if dpi_real < 100:
        print(f"Aviso: resolução original equivale a ~{dpi_real:.0f} dpi na tela; "
              "o ideal é 150 dpi ou mais (≈ 5315 x 7087 px).")
    return ImageOps.fit(img, alvo, Image.LANCZOS)


def marcas(draw, x0, y0, x1, y1, dpi):
    """Marcas de corte nos cantos, só na margem branca (não invadem a imagem)."""
    t, g = cm(0.6, dpi), cm(0.1, dpi)
    w = max(1, dpi // 100)
    for x in (x0, x1):
        draw.line([(x, y0 - g - t), (x, y0 - g)], fill="black", width=w)
        draw.line([(x, y1 + g), (x, y1 + g + t)], fill="black", width=w)
    for y in (y0, y1):
        draw.line([(x0 - g - t, y), (x0 - g, y)], fill="black", width=w)
        draw.line([(x1 + g, y), (x1 + g + t, y)], fill="black", width=w)


def gerar_folhas(img, dpi):
    folhas = []
    pl, pa, aba = cm(PECA_L, dpi), cm(PECA_A, dpi), cm(ABA, dpi)
    for li in range(LINHAS):
        for co in range(COLS):
            ult_col, ult_lin = co == COLS - 1, li == LINHAS - 1
            x, y = co * pl, li * pa
            w = pl if ult_col else pl + aba
            h = pa if ult_lin else pa + aba
            peca = img.crop((x, y, x + w, y + h))

            pag = Image.new("RGB", (cm(A4_L, dpi), cm(A4_A, dpi)), "white")
            ox, oy = cm(MARGEM_ESQ, dpi), cm(MARGEM_TOPO, dpi)
            pag.paste(peca, (ox, oy))
            d = ImageDraw.Draw(pag)

            # marcas pretas = linha de CORTE (borda real da impressão, aba incluída)
            marcas(d, ox, oy, ox + w, oy + h, dpi)
            # risquinhos cinza na margem = onde começa a aba (encaixe da folha vizinha)
            cinza, f = (150, 150, 150), fonte(cm(0.25, dpi))
            lw = max(1, dpi // 100)
            if not ult_col:
                d.line([(ox + pl, oy - cm(0.7, dpi)), (ox + pl, oy - cm(0.1, dpi))], fill=cinza, width=lw)
                d.text((ox + pl + aba // 2, oy - cm(0.4, dpi)), "aba", fill=cinza, font=f, anchor="mm")
            if not ult_lin:
                d.line([(ox - cm(0.7, dpi), oy + pa), (ox - cm(0.1, dpi), oy + pa)], fill=cinza, width=lw)
                d.text((ox - cm(0.45, dpi), oy + pa + aba // 2), "aba", fill=cinza, font=f, anchor="mm")

            # etiqueta e mini-mapa no rodapé
            nome = f"{NOMES_LINHA[li]}{co + 1}"
            base = oy + h + cm(1.2, dpi)
            d.text((ox, base), nome, fill="black", font=fonte(cm(1.2, dpi)))
            txt = (f"linha {NOMES_LINHA[li]} (de cima p/ baixo), coluna {co + 1} (da esq. p/ dir.)\n"
                   f"Folha {li * COLS + co + 1} de {COLS * LINHAS}. Corte nas marcas pretas (rente à imagem).\n"
                   "Abas à direita/embaixo ficam por baixo da folha vizinha.")
            d.multiline_text((ox + cm(2.6, dpi), base), txt, fill="black",
                             font=fonte(cm(0.32, dpi)), spacing=cm(0.12, dpi))
            q = cm(0.35, dpi)
            mx = cm(A4_L, dpi) - cm(1.0, dpi) - COLS * q
            for i in range(LINHAS):
                for j in range(COLS):
                    r = (mx + j * q, base + i * q, mx + (j + 1) * q - 2, base + (i + 1) * q - 2)
                    d.rectangle(r, fill="black" if (i, j) == (li, co) else None, outline="black")
            folhas.append(pag)
    return folhas


def mapa(img, dpi_mapa=20):
    """PNG pequeno com a arte e a grade de montagem."""
    m = img.resize((cm(TELA_L, dpi_mapa), cm(TELA_A, dpi_mapa)), Image.LANCZOS)
    d = ImageDraw.Draw(m)
    pl, pa = cm(PECA_L, dpi_mapa), cm(PECA_A, dpi_mapa)
    f = fonte(cm(2.0, dpi_mapa))
    for li in range(LINHAS):
        for co in range(COLS):
            x, y = co * pl, li * pa
            d.rectangle((x, y, x + pl, y + pa), outline=(255, 0, 0), width=2)
            d.text((x + pl // 2, y + pa // 2), f"{NOMES_LINHA[li]}{co + 1}",
                   fill=(255, 0, 0), font=f, anchor="mm", stroke_width=2, stroke_fill="white")
    return m


def esboco(dpi=40):
    """Esboço esquemático da composição (não é a arte final)."""
    W, H = cm(TELA_L, dpi), cm(TELA_A, dpi)
    amarelo, preto, vermelho, verde = (247, 196, 0), (20, 20, 20), (196, 40, 28), (0, 110, 70)
    img = Image.new("RGB", (W, H), amarelo)
    d = ImageDraw.Draw(img)
    y = lambda v: cm(v, dpi)  # noqa: E731
    # faixa do título (linha A)
    d.rectangle((0, 0, W, y(24)), fill=preto)
    d.text((W // 2, y(9)), "LÉLIA", fill=amarelo, font=fonte(y(11)), anchor="mm")
    d.text((W // 2, y(19.5)), "GONZALEZ", fill=amarelo, font=fonte(y(7.5)), anchor="mm")
    # retrato (linhas B–D)
    d.ellipse((y(14), y(28), y(76), y(94)), fill=vermelho)
    d.ellipse((y(22), y(33), y(68), y(91)), fill=preto)
    d.text((W // 2, y(60)), "RETRATO\nem retícula\n(meio-tom)", fill=amarelo,
           font=fonte(y(4)), anchor="mm", align="center")
    d.text((y(2.5), y(46)), "AMEFRICANIDADE", fill=preto, font=fonte(y(2.2)))
    d.text((W - y(2.5), y(84)), "PRETUGUÊS", fill=preto, font=fonte(y(2.6)), anchor="ra")
    # frase (linha E)
    d.rectangle((0, y(96), W, H), fill=verde)
    d.multiline_text((W // 2, y(105.5)), "“A GENTE NÃO NASCE NEGRO,\nA GENTE SE TORNA NEGRO.”",
                     fill="white", font=fonte(y(4.3)), anchor="mm", align="center")
    d.text((W // 2, y(116)), "LÉLIA GONZALEZ · 1935–1994 · MNU · Racismo e sexismo na cultura brasileira",
           fill=amarelo, font=fonte(y(1.6)), anchor="mm")
    return img


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("imagem", nargs="?", help="arte final (ideal: 3:4, ≥ 5315x7087 px)")
    ap.add_argument("--dpi", type=int, default=200, help="resolução de impressão (padrão 200)")
    ap.add_argument("--saida", default="lambe_lambe_A4.pdf")
    ap.add_argument("--esboco", action="store_true", help="gera esboco.png com o layout proposto")
    a = ap.parse_args()

    if a.esboco:
        esboco().save("esboco.png")
        print("esboco.png gerado.")
        if not a.imagem:
            return
    if not a.imagem:
        ap.error("informe a imagem da arte final (ou use --esboco)")

    img = preparar_imagem(a.imagem, a.dpi)
    folhas = gerar_folhas(img, a.dpi)
    folhas[0].save(a.saida, save_all=True, append_images=folhas[1:], resolution=a.dpi)
    saida_mapa = Path(a.saida).with_name("mapa_montagem.png")
    mapa(img).save(saida_mapa)
    print(f"{a.saida}: {len(folhas)} páginas A4 · {saida_mapa} gerado.")


if __name__ == "__main__":
    main()
