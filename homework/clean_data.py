"""Limpieza de texto y generación de n-gramas."""

import re

import pandas as pd


def make_key(text: str) -> str:
    """
    Genera una clave (key) para un texto usando bigrams únicos + último caracter.

    El proceso:
    1. Elimina todo lo que no sea letra y convierte a minúsculas.
    2. Obtiene el conjunto único de bigrams (n-gramas de tamaño 2).
    3. Agrega el último caracter como pieza individual.
    4. Retorna todas las piezas concatenadas en orden alfabético.
    """
    cleaned = re.sub(r"[^a-zA-Z]", "", text).lower()
    if not cleaned:
        return ""
    unique_bigrams = list(set(cleaned[i : i + 2] for i in range(len(cleaned) - 1)))
    all_pieces = unique_bigrams + [cleaned[-1]]
    return "".join(sorted(all_pieces))


def clean_text(text: str) -> str:
    """
    Normaliza un texto: elimina puntuación (excepto guiones),
    colapsa espacios múltiples y convierte a mayúsculas.
    """
    t = re.sub(r"[^\w\s-]", "", text)
    t = re.sub(r"\s+", " ", t).strip()
    return t.upper()


def main(input_path: str, output_path: str) -> None:
    """
    Lee el archivo de entrada, agrupa textos similares por su key de bigrams
    y escribe los archivos de salida (output.txt y test.csv).

    Args:
        input_path: ruta al archivo CSV con columna 'raw_text'.
        output_path: ruta donde se guardará el archivo de salida con 'cleaned_text'.
    """
    df = pd.read_csv(input_path)

    df["key"] = df["raw_text"].apply(make_key)

    df["cleaned_text_individual"] = df["raw_text"].apply(clean_text)

    group_repr = (
        df.groupby("key")["cleaned_text_individual"]
        .apply(lambda texts: max(texts, key=len))
        .to_dict()
    )

    df["cleaned_text"] = df["key"].map(group_repr)

    test_df = df[["raw_text", "key"]].copy()
    test_df.to_csv("files/test.csv", index=False)

    output_df = df[["cleaned_text"]].copy()
    output_df.to_csv(output_path, index=False)
