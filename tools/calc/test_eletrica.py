#!/usr/bin/env python3
"""
Testes de valor-ouro da calculadora elétrica — stdlib, sem pytest.

    python3 tools/calc/test_eletrica.py

Domínio de risco: aqui o teste não protege só o orçamento, protege decisão que
vira instalação em set. Toda conta está escrita no docstring.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import eletrica as el


class TestCorrente(unittest.TestCase):

    def test_monofasico_220v(self):
        """14.400 W ÷ (220 × 0,92) = 71,15 A — a parede de LED de 6×3 m
        no pico, que é o caso que originou esta calculadora."""
        self.assertAlmostEqual(el.corrente(14400, 220, 0.92), 14400 / (220 * 0.92), places=4)
        self.assertAlmostEqual(el.corrente(14400, 220, 0.92), 71.15, places=1)

    def test_127v_puxa_mais_corrente(self):
        i220 = el.corrente(5000, 220)
        i127 = el.corrente(5000, 127)
        self.assertGreater(i127, i220 * 1.7)

    def test_trifasico_reduz_corrente_por_fase(self):
        """Trifásico divide por √3: mesma potência, corrente por fase menor."""
        mono = el.corrente(14400, 220, 0.92, trifasico=False)
        tri = el.corrente(14400, 220, 0.92, trifasico=True)
        self.assertAlmostEqual(tri, mono / (3 ** 0.5), places=4)

    def test_fator_de_potencia_pior_puxa_mais(self):
        self.assertGreater(el.corrente(5000, 220, fp=0.7), el.corrente(5000, 220, fp=0.95))

    def test_entradas_invalidas(self):
        with self.assertRaises(ValueError):
            el.corrente(-100)
        with self.assertRaises(ValueError):
            el.corrente(1000, tensao=0)
        for fp in (0, 1.5, -0.5):
            with self.assertRaises(ValueError):
                el.corrente(1000, fp=fp)


class TestCircuitos(unittest.TestCase):

    def test_folga_de_80_por_cento(self):
        """71,15 A ÷ (32 × 0,8 = 25,6) = 2,78 -> 3 circuitos."""
        self.assertEqual(el.circuitos(71.15, 32), 3)

    def test_carga_zero_nao_precisa_circuito(self):
        self.assertEqual(el.circuitos(0), 0)

    def test_limite_exato_nao_arredonda_para_cima(self):
        """25,6 A é exatamente 80% de 32 A — cabe em 1 circuito."""
        self.assertEqual(el.circuitos(25.6, 32), 1)
        self.assertEqual(el.circuitos(25.7, 32), 2)


class TestQuedaTensao(unittest.TestCase):

    def test_queda_cresce_com_distancia(self):
        curta = el.queda_tensao(30, 20, 6)
        longa = el.queda_tensao(30, 80, 6)
        self.assertAlmostEqual(longa, curta * 4, places=4)

    def test_queda_cai_com_bitola_maior(self):
        fina = el.queda_tensao(30, 50, 4)
        grossa = el.queda_tensao(30, 50, 16)
        self.assertAlmostEqual(fina / grossa, 4.0, places=4)

    def test_formula_monofasica(self):
        """ΔV = 2 × 0,0225 × 50 m × 30 A ÷ 6 mm² = 11,25 V
        Em 220 V = 5,11%."""
        self.assertAlmostEqual(el.queda_tensao(30, 50, 6, 220), 100 * 11.25 / 220, places=3)

    def test_entradas_invalidas(self):
        for args in [(30, 0, 6), (30, 50, 0), (30, -10, 6)]:
            with self.assertRaises(ValueError):
                el.queda_tensao(*args)


class TestBitola(unittest.TestCase):

    def test_tirada_longa_exige_cabo_mais_grosso_que_a_conducao(self):
        """30 A conduzem em 4 mm², mas a 80 m a queda estoura o limite —
        o cabo precisa engrossar por causa da tirada, não da corrente.
        É o erro clássico de gerador longe do set."""
        curta = el.bitola_minima(30, 10)
        longa = el.bitola_minima(30, 80)
        self.assertLess(curta, longa)

    def test_bitola_atende_os_dois_criterios(self):
        b = el.bitola_minima(50, 40)
        self.assertGreaterEqual(el.CAPACIDADE_A[b], 50)
        self.assertLessEqual(el.queda_tensao(50, 40, b), el.QUEDA_MAX_PCT)

    def test_carga_absurda_nao_tem_bitola(self):
        self.assertIsNone(el.bitola_minima(400, 200))


class TestDisjuntor(unittest.TestCase):

    def test_recomendacao_respeita_folga(self):
        """20 A precisa de disjuntor cujo 80% seja >= 20 -> 25 A (25×0,8=20)."""
        self.assertEqual(el.disjuntor_recomendado(20), 25)

    def test_acima_da_tabela(self):
        self.assertIsNone(el.disjuntor_recomendado(500))


class TestGerador(unittest.TestCase):

    def test_kva_util(self):
        """20 kW ÷ 0,92 = 21,74 kVA."""
        g = el.gerador(20000, 0.92)
        self.assertAlmostEqual(g["kva_util"], 20 / 0.92, places=4)

    def test_margem_padrao_25_por_cento(self):
        g = el.gerador(20000, 0.92)
        self.assertAlmostEqual(g["kva_recomendado"], (20 / 0.92) * 1.25, places=4)

    def test_partida_indutiva_amplia_reserva(self):
        sem = el.gerador(20000, partida=False)
        com = el.gerador(20000, partida=True)
        self.assertGreater(com["kva_recomendado"], sem["kva_recomendado"] * 1.3)


class TestBalanceamento(unittest.TestCase):

    def test_cargas_iguais_ficam_equilibradas(self):
        b = el.balancear([1000] * 6)
        self.assertEqual(b["totais_w"], [2000, 2000, 2000])
        self.assertAlmostEqual(b["desequilibrio_pct"], 0.0, places=6)

    def test_carga_unica_grande_torna_equilibrio_impossivel(self):
        """2400,1200,1200,600,600,600 = 6600 W; ideal seria 2200 por fase.
        Mas a maior carga (2400 W) sozinha JÁ excede esse ideal, e carga não
        se divide entre fases. Logo 27,3% é o mínimo matemático, não falha do
        algoritmo — o guloso acerta. Esta asserção nasceu errada e o teste a
        corrigiu: a expectativa é que estava mal calibrada."""
        b = el.balancear([2400, 1200, 1200, 600, 600, 600])
        self.assertEqual(sum(b["totais_w"]), 6600)
        self.assertAlmostEqual(b["desequilibrio_pct"], 100 * 600 / 2200, places=1)
        self.assertTrue(b["inevitavel"], "deve sinalizar desequilíbrio forçado")

    def test_equilibrio_possivel_nao_e_sinalizado(self):
        b = el.balancear([1000] * 6)
        self.assertFalse(b["inevitavel"])

    def test_carga_unica_desequilibra_tudo(self):
        b = el.balancear([5000])
        self.assertEqual(b["totais_w"], [5000, 0, 0])
        self.assertGreater(b["desequilibrio_pct"], 100)


class TestCLI(unittest.TestCase):

    def test_potencia(self):
        self.assertEqual(el.main(["--potencia", "14400"]), 0)

    def test_com_distancia(self):
        self.assertEqual(el.main(["--potencia", "5000", "--distancia", "60"]), 0)

    def test_gerador(self):
        self.assertEqual(el.main(["--gerador", "20000", "--partida"]), 0)

    def test_fases(self):
        self.assertEqual(el.main(["--fases", "2400,1200,1200,600"]), 0)

    def test_fases_invalidas(self):
        self.assertEqual(el.main(["--fases", "abc,def"]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
