from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'index.html'


class ProductionMapTests(unittest.TestCase):
    def test_site_has_map_candidates_and_external_sources(self):
        self.assertTrue(SITE.exists(), '배포용 index.html이 없습니다.')
        html = SITE.read_text(encoding='utf-8')
        for text in ['청주 사진관 입지지도', 'CJ-20260902-01', '공영주차장', '2024 기준 사업체조사']:
            self.assertIn(text, html)
        self.assertIn('https://www.cheongju.go.kr/stat/selectBbsNttView.do?key=1763&bbsNo=539&nttNo=268480', html)
        self.assertIn('https://www.cheongju.go.kr/downloadContentsFile.do?key=24132&fileNo=2123', html)


if __name__ == '__main__':
    unittest.main()
