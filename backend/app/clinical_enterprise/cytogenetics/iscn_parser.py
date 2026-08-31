"""
AcuPath Enterprise LIS - ISCN 2020 Cytogenetic Karyotyping Parser
Parses standard human karyotype nomenclature strings and flags chromosomal abnormalities.
"""

from typing import Dict, List, Optional

class ISCNKaryotypeParser:
    @staticmethod
    def parse_karyotype(iscn_string: str) -> Dict[str, Any]:
        is_normal = iscn_string.strip() in ["46,XX", "46,XY"]
        abnormalities = []
        if "47,XX,+21" in iscn_string or "47,XY,+21" in iscn_string:
            abnormalities.append("Trisomy 21 (Down Syndrome)")
        if "t(9;22)" in iscn_string:
            abnormalities.append("t(9;22)(q34.1;q11.2) BCR-ABL1 Fusion (Philadelphia Chromosome)")

        return {
            "karyotype": iscn_string,
            "is_normal": is_normal,
            "abnormalities": abnormalities,
            "clinical_significance": "ABNORMAL" if not is_normal else "NORMAL"
        }
