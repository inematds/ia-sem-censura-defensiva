#!/usr/bin/env python3
"""Gera a imagem sintética do teste de visão (kit/exemplos/teste-visao.png). Precisa do Pillow.

  python3 kit/scripts/gera_imagem_teste.py
A imagem já vem pronta no repositório; rode só se quiser recriar.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CODIGO = "4826"  # o mesmo de checa_endpoint.CODIGO_DA_IMAGEM
DESTINO = Path(__file__).resolve().parents[1] / "exemplos" / "teste-visao.png"


def fonte(tamanho: int):
    for nome in ("DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "Arial Bold.ttf"):
        try:
            return ImageFont.truetype(nome, tamanho)
        except OSError:
            continue
    return ImageFont.load_default()


def main() -> None:
    img = Image.new("RGB", (800, 450), (246, 244, 238))
    d = ImageDraw.Draw(img)
    d.rectangle([20, 20, 780, 430], outline=(30, 30, 40), width=4)
    d.text((48, 44), "Teste de visão — imagem sintética", fill=(40, 40, 50), font=fonte(30))
    d.text((48, 96), "Leia o número grande:", fill=(70, 70, 80), font=fonte(26))
    d.text((210, 160), CODIGO, fill=(12, 12, 16), font=fonte(170))
    d.text((48, 390), "INEMA.CLUB · nenhum dado real", fill=(110, 110, 120), font=fonte(20))
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    img.save(DESTINO, optimize=True)
    print(DESTINO, DESTINO.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
