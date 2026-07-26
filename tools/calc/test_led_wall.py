#!/usr/bin/env python3
"""
Testes de valor-ouro da calculadora de parede de LED — stdlib, sem pytest.

    python3 tools/calc/test_led_wall.py

Todos os valores foram conferidos à mão e a conta está escrita no docstring
de cada teste. Se um quebrar, o comportamento mudou e algum orçamento pode
ter virado mentira.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import led_wall


class TestComposicao(unittest.TestCase):

    def test_caso_ouro_6x3_p26(self):
        """Parede 6 × 3 m, gabinete 500 × 500 mm, pitch 2.6 mm.
        Gabinetes: 6000/500 = 12 na horizontal, 3000/500 = 6 na vertical = 72.
        Pixels por gabinete: int(500/2.6) = 192 por lado.
        Resolução: 12×192 = 2304 por 6×192 = 1152.
        """
        r = led_wall.calcular(6, 3, 2.6)
        self.assertEqual(r["cabinetes"], 72)
        self.assertEqual((r["cab_x"], r["cab_y"]), (12, 6))
        self.assertEqual(r["resolucao"], (2304, 1152))
        self.assertEqual(r["pixels"], 2304 * 1152)
        self.assertAlmostEqual(r["area_m2"], 18.0, places=4)

    def test_medida_nao_multipla_arredonda_para_cima(self):
        """5,2 m com gabinete de 500 mm = 10,4 -> 11 gabinetes (12 não cabem
        na medida pedida, mas 10 deixariam a parede menor que o pedido)."""
        r = led_wall.calcular(5.2, 3, 2.6)
        self.assertEqual(r["cab_x"], 11)
        self.assertAlmostEqual(r["largura_real_m"], 5.5, places=4)

    def test_pitch_menor_gera_mais_pixels(self):
        grosso = led_wall.calcular(6, 3, 3.9)
        fino = led_wall.calcular(6, 3, 1.5)
        self.assertGreater(fino["pixels"], grosso["pixels"])
        self.assertEqual(fino["cabinetes"], grosso["cabinetes"])  # física igual

    def test_gabinete_retangular(self):
        """Gabinete 500 × 1000 mm numa parede 6 × 3 m:
        12 na horizontal, 3 na vertical = 36 gabinetes."""
        r = led_wall.calcular(6, 3, 2.6, gab_l_mm=500, gab_a_mm=1000)
        self.assertEqual((r["cab_x"], r["cab_y"]), (12, 3))
        self.assertEqual(r["cabinetes"], 36)


class TestDados(unittest.TestCase):

    def test_portas_arredondam_para_cima(self):
        """2.654.208 px ÷ 650.000 = 4,08 -> 5 portas."""
        r = led_wall.calcular(6, 3, 2.6)
        self.assertEqual(r["portas"], 5)

    def test_porta_mais_capaz_reduz_contagem(self):
        r = led_wall.calcular(6, 3, 2.6, pixels_por_porta=1_300_000)
        self.assertEqual(r["portas"], 3)


class TestEnergia(unittest.TestCase):

    def test_consumo_e_corrente_220v(self):
        """18 m² × 250 W/m² = 4,5 kW médio; a 220 V = 20,45 A.
        Pico: 18 × 800 = 14,4 kW; a 220 V = 65,45 A."""
        r = led_wall.calcular(6, 3, 2.6, tensao=220)
        self.assertAlmostEqual(r["w_medio"], 4500.0, places=2)
        self.assertAlmostEqual(r["a_medio"], 4500 / 220, places=4)
        self.assertAlmostEqual(r["w_pico"], 14400.0, places=2)
        self.assertAlmostEqual(r["a_pico"], 14400 / 220, places=4)

    def test_127v_puxa_quase_o_dobro_de_corrente(self):
        r220 = led_wall.calcular(6, 3, 2.6, tensao=220)
        r127 = led_wall.calcular(6, 3, 2.6, tensao=127)
        self.assertGreater(r127["a_pico"], r220["a_pico"] * 1.7)
        self.assertGreater(r127["circuitos"], r220["circuitos"])

    def test_circuitos_usam_folga_de_80_por_cento(self):
        """65,45 A de pico ÷ (32 × 0,8 = 25,6) = 2,56 -> 3 circuitos."""
        r = led_wall.calcular(6, 3, 2.6, tensao=220, disjuntor_a=32)
        self.assertEqual(r["circuitos"], 3)

    def test_brilho_reduz_consumo_linearmente(self):
        cheio = led_wall.calcular(6, 3, 2.6)
        metade = led_wall.calcular(6, 3, 2.6, brilho_pct=50)
        self.assertAlmostEqual(metade["w_pico"], cheio["w_pico"] / 2, places=2)


class TestEstrutura(unittest.TestCase):

    def test_peso(self):
        """18 m² × 32 kg/m² = 576 kg — carga que exige rigging calculado."""
        r = led_wall.calcular(6, 3, 2.6)
        self.assertAlmostEqual(r["peso_kg"], 576.0, places=2)


class TestSincronia(unittest.TestCase):

    def test_obturador_180_por_frame_rate(self):
        self.assertEqual(led_wall.refresh_seguro(24)["shutter_180"], "1/48")
        self.assertEqual(led_wall.refresh_seguro(25)["shutter_180"], "1/50")
        self.assertEqual(led_wall.refresh_seguro(30)["shutter_180"], "1/60")

    def test_refresh_minimo_declarado(self):
        self.assertEqual(led_wall.refresh_seguro(25)["refresh_minimo_hz"], 3840)

    def test_fps_invalido_falha(self):
        with self.assertRaises(ValueError):
            led_wall.refresh_seguro(0)


class TestEntradasInvalidas(unittest.TestCase):

    def test_dimensoes_e_pitch(self):
        for args in [(0, 3, 2.6), (6, 0, 2.6), (6, 3, 0), (-6, 3, 2.6)]:
            with self.assertRaises(ValueError):
                led_wall.calcular(*args)

    def test_brilho_fora_da_faixa(self):
        for b in (0, 101, -5):
            with self.assertRaises(ValueError):
                led_wall.calcular(6, 3, 2.6, brilho_pct=b)


class TestCLI(unittest.TestCase):

    def test_listar(self):
        self.assertEqual(led_wall.main(["--listar"]), 0)

    def test_execucao_completa(self):
        self.assertEqual(led_wall.main(
            ["--largura", "6", "--altura", "3", "--pitch", "2.6", "--fps", "24"]), 0)

    def test_gabinete_invalido(self):
        self.assertEqual(led_wall.main(
            ["--largura", "6", "--altura", "3", "--pitch", "2.6",
             "--gabinete", "nao-existe"]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
