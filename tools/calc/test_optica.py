#!/usr/bin/env python3
"""
Testes de valor-ouro da calculadora de óptica — stdlib, sem pytest.

    python3 tools/calc/test_optica.py

As contas estão nos docstrings. Onde o valor confere com tabela conhecida do
mercado, está dito qual.
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import optica as op


class TestCoC(unittest.TestCase):

    def test_full_frame(self):
        """Diagonal FF = √(36² + 24²) = 43,267 mm; ÷ 1500 = 0,0288 mm —
        bate com o 0,029 usado nas tabelas clássicas de foto."""
        self.assertAlmostEqual(op.coc(36, 24), 43.267 / 1500, places=4)
        self.assertAlmostEqual(op.coc(36, 24), 0.0288, places=3)

    def test_formato_menor_tem_coc_menor(self):
        self.assertLess(op.coc(*op.FORMATOS["s16"][:2]), op.coc(36, 24))

    def test_divisor_maior_e_mais_exigente(self):
        self.assertLess(op.coc(36, 24, 2000), op.coc(36, 24, 1500))

    def test_dimensao_invalida(self):
        with self.assertRaises(ValueError):
            op.coc(0, 24)


class TestCampoDeVisao(unittest.TestCase):

    def test_50mm_full_frame(self):
        """2 × arctan(36 / (2×50)) = 2 × arctan(0,36) = 39,6° horizontal.
        É o valor de catálogo da 50 mm em full frame."""
        f = op.campo_de_visao(36, 24, 50)
        self.assertAlmostEqual(f["horizontal"], 39.60, places=1)
        self.assertAlmostEqual(f["vertical"], 26.99, places=1)
        self.assertAlmostEqual(f["diagonal"], 46.79, places=1)

    def test_grande_angular_abre_mais(self):
        self.assertGreater(op.campo_de_visao(36, 24, 18)["horizontal"],
                           op.campo_de_visao(36, 24, 85)["horizontal"])

    def test_sensor_menor_fecha_o_angulo(self):
        """Mesma lente, sensor menor = enquadramento mais fechado."""
        ff = op.campo_de_visao(36, 24, 50)["horizontal"]
        s16 = op.campo_de_visao(12.52, 7.41, 50)["horizontal"]
        self.assertGreater(ff, s16 * 2.5)

    def test_focal_invalida(self):
        with self.assertRaises(ValueError):
            op.campo_de_visao(36, 24, 0)


class TestEnquadramento(unittest.TestCase):

    def test_quanto_cabe_no_quadro(self):
        """50 mm em FF a 3 m: 36 × (3000/50) = 2160 mm = 2,16 m de largura."""
        e = op.enquadramento(36, 24, 50, 3)
        self.assertAlmostEqual(e["largura_m"], 2.16, places=3)
        self.assertAlmostEqual(e["altura_m"], 1.44, places=3)

    def test_dobrar_distancia_dobra_o_quadro(self):
        perto = op.enquadramento(36, 24, 50, 2)["largura_m"]
        longe = op.enquadramento(36, 24, 50, 4)["largura_m"]
        self.assertAlmostEqual(longe, perto * 2, places=6)


class TestHiperfocal(unittest.TestCase):

    def test_50mm_f28_full_frame(self):
        """H = 50² ÷ (2,8 × 0,02884) + 50 = 30.940 mm ≈ 30,99 m."""
        c = op.coc(36, 24)
        h = op.hiperfocal(50, 2.8, c)
        self.assertAlmostEqual(h, (2500 / (2.8 * c) + 50) / 1000, places=6)
        self.assertAlmostEqual(h, 30.99, places=1)

    def test_fechar_diafragma_aproxima_a_hiperfocal(self):
        c = op.coc(36, 24)
        self.assertLess(op.hiperfocal(50, 11, c), op.hiperfocal(50, 2.8, c))

    def test_grande_angular_tem_hiperfocal_curta(self):
        c = op.coc(36, 24)
        self.assertLess(op.hiperfocal(18, 4, c), op.hiperfocal(85, 4, c))


class TestProfundidade(unittest.TestCase):

    def test_50mm_f28_a_3m_full_frame(self):
        """Com H = 30,99 m e s = 3 m:
        perto = 3000 × (30940−50) ÷ (30940+3000−100) = 2737 mm
        longe = 3000 × (30940−50) ÷ (30940−3000)     = 3317 mm
        Faixa de foco ≈ 2,74 m a 3,32 m — cerca de 58 cm."""
        c = op.coc(36, 24)
        d = op.profundidade(50, 2.8, 3, c)
        self.assertAlmostEqual(d["perto_m"], 2.74, places=1)
        self.assertAlmostEqual(d["longe_m"], 3.32, places=1)
        self.assertAlmostEqual(d["total_m"], 0.58, places=1)
        self.assertFalse(d["infinito_em_foco"])

    def test_na_hiperfocal_o_infinito_entra_em_foco(self):
        c = op.coc(36, 24)
        h = op.hiperfocal(50, 2.8, c)
        d = op.profundidade(50, 2.8, h + 1, c)
        self.assertTrue(d["infinito_em_foco"])
        self.assertIsNone(d["longe_m"])

    def test_abrir_diafragma_reduz_a_faixa(self):
        c = op.coc(36, 24)
        aberto = op.profundidade(50, 1.4, 3, c)["total_m"]
        fechado = op.profundidade(50, 8, 3, c)["total_m"]
        self.assertLess(aberto, fechado)

    def test_sensor_menor_da_mais_profundidade_na_mesma_focal(self):
        """Mesma lente e abertura: formato menor tem CoC menor... mas o que
        o operador sente é mais profundidade, porque usa focal mais curta
        para o mesmo enquadramento. Aqui isolamos: mesma focal, o CoC menor
        do S16 REDUZ a faixa. É a distinção que confunde no set."""
        d_ff = op.profundidade(50, 2.8, 3, op.coc(36, 24))["total_m"]
        d_s16 = op.profundidade(50, 2.8, 3, op.coc(12.52, 7.41))["total_m"]
        self.assertLess(d_s16, d_ff)

    def test_distancia_invalida(self):
        with self.assertRaises(ValueError):
            op.profundidade(50, 2.8, 0, 0.03)


class TestEquivalencia(unittest.TestCase):

    def test_crop_s35_vs_ff(self):
        """Diagonal FF 43,27 ÷ diagonal S35 31,11 = 1,39× —
        o fator de crop clássico de Super 35."""
        self.assertAlmostEqual(op.crop("ff", "s35"), 1.39, places=2)

    def test_50mm_ff_equivale_a_36mm_s35(self):
        e = op.equivalencia(50, "ff", "s35")
        self.assertAlmostEqual(e["focal_equivalente_mm"], 35.95, places=1)

    def test_ida_e_volta_fecha(self):
        ida = op.equivalencia(50, "ff", "mft")["focal_equivalente_mm"]
        volta = op.equivalencia(ida, "mft", "ff")["focal_equivalente_mm"]
        self.assertAlmostEqual(volta, 50, places=6)

    def test_mesmo_formato_nao_muda_nada(self):
        self.assertAlmostEqual(op.crop("ff", "ff"), 1.0, places=9)

    def test_focal_invalida(self):
        with self.assertRaises(ValueError):
            op.equivalencia(0, "ff", "s35")


class TestFormatos(unittest.TestCase):

    def test_tabela_coerente(self):
        for chave, (l, h, d) in op.FORMATOS.items():
            self.assertGreater(l, 0, chave)
            self.assertGreater(h, 0, chave)
            self.assertGreater(l, h, f"{chave}: largura deve exceder a altura")
            self.assertTrue(d.strip(), chave)


class TestCLI(unittest.TestCase):

    def test_listar(self):
        self.assertEqual(op.main(["--listar"]), 0)

    def test_completo(self):
        self.assertEqual(op.main(
            ["--formato", "ff", "--focal", "50", "--tstop", "2.8", "--distancia", "3"]), 0)

    def test_equivalencia_cli(self):
        self.assertEqual(op.main(
            ["--equivalencia", "--de", "ff", "--para", "s35", "--focal", "50"]), 0)

    def test_medida_direta(self):
        self.assertEqual(op.main(
            ["--largura", "27.99", "--altura", "19.22", "--focal", "40"]), 0)

    def test_formato_invalido(self):
        self.assertEqual(op.main(["--formato", "nao-existe", "--focal", "50"]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
