from django import template

register = template.Library()


@register.filter(name="kelas_normalized")
def kelas_normalized(value):
    """Normalisasi string kelas untuk mencegah card dobel.

    Contoh: "XII IPA  A" -> "XII IPA A"
    "XII IPA A " -> "XII IPA A"
    "  XII   IPA   A  " -> "XII IPA A"
    """
    if value is None:
        return ""
    # Pastikan menjadi string
    s = str(value)
    # Trim & collapse whitespace
    return " ".join(s.split())


@register.filter(name="split")
def split(value, delimiter=","):
    """Split string berdasarkan delimiter.

    Django default tidak menyediakan filter `split`, jadi kita buatkan sendiri
    agar template bisa menulis: {{ "a,b"|split:"," }}.
    """
    if value is None:
        return []

    s = str(value)
    d = delimiter if delimiter is not None else ","
    return s.split(d)

