#!/usr/bin/env python3
"""
Testes de valor-ouro da calculadora de storage — stdlib (unittest), sem pytest.

    python3 tools/calc/test_storage.py

Valores conferidos à mão. Se um destes quebrar, a calculadora mudou de
comportamento e alguma nota do acervo pode ter virado mentira.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import storage


class TestCalculo(unittest.TestCase):

    def test_caso_ouro_1000mbps_1h(self):
        """1000 Mbps por 1 hora = 450 GB. Conta à mão:
        1000 Mb/s × 3600 s = 3.600.000 Mb ÷ 8 = 450.000 MB = 450 GB."""
        r = storage.calcular(1000, 1, cameras=1, copias=1)
        self.assertAlmostEqual(r["gb_por_camera"], 450.0, places=4)
        self.assertAlmostEqual(r["gb_total"], 450.0, places=4)

    def test_multiplicacao_por_cameras_e_copias(self):
        r = storage.calcular(1000, 1, cameras=2, copias=3)
        self.assertAlmostEqual(r["gb_bruto"], 900.0, places=4)
        self.assertAlmostEqual(r["gb_total"], 2700.0, places=4)

    def test_prores_422hq_6h_2cams(self):
        """880 Mbps × 6h = 2376 GB por câmera; 2 câmeras = 4752 GB."""
        r = storage.calcular(880, 6, cameras=2, copias=2)
        self.assertAlmostEqual(r["gb_por_camera"], 2376.0, places=2)
        self.assertAlmostEqual(r["gb_bruto"], 4752.0, places=2)
        self.assertAlmostEqual(r["gb_total"], 9504.0, places=2)

    def test_cartoes_arredondam_para_cima(self):
        """1.2 TB brutos não cabem em 1 cartão de 1 TB — precisa de 2."""
        r = storage.calcular(1000, 1, cameras=3, copias=1)  # 1350 GB
        self.assertEqual(int(r["cartoes_1tb"]), 2)

    def test_offload_10gbps(self):
        """450 GB = 3600 Gb; a 10 Gb/s = 360 s = 6 min."""
        r = storage.calcular(1000, 1)
        self.assertAlmostEqual(r["minutos_offload_10gbps"], 6.0, places=3)

    def test_zero_horas_nao_consome(self):
        r = storage.calcular(1000, 0)
        self.assertEqual(r["gb_total"], 0.0)

    def test_entradas_invalidas_falham_alto(self):
        for args in [(0, 1), (-5, 1), (1000, -1)]:
            with self.assertRaises(ValueError):
                storage.calcular(*args)
        with self.assertRaises(ValueError):
            storage.calcular(1000, 1, cameras=0)
        with self.assertRaises(ValueError):
            storage.calcular(1000, 1, copias=0)

    def test_tabela_de_codecs_coerente(self):
        for chave, (mbps, desc) in storage.CODECS.items():
            self.assertGreater(mbps, 0, f"{chave} com bitrate inválido")
            self.assertTrue(desc.strip(), f"{chave} sem descrição")
            self.assertEqual(chave, chave.lower(), "chave de codec deve ser minúscula")


class TestCLI(unittest.TestCase):

    def test_listar_funciona(self):
        self.assertEqual(storage.main(["--listar"]), 0)

    def test_codec_desconhecido_retorna_erro(self):
        self.assertEqual(storage.main(["--codec", "nao-existe"]), 2)

    def test_execucao_normal(self):
        self.assertEqual(
            storage.main(["--codec", "prores-422hq-4k", "--horas", "6", "--cameras", "2"]), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
