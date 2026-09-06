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
        self.assertIn('https://unpkg.com/leaflet@1.9.4/dist/leaflet.js', html)
        self.assertIn("tile.openstreetmap.org", html)
        self.assertIn("const studios=[", html)
        for studio in ['에이블스튜디오 청주점', '시안사진관 청주점', '연희스튜디오 청주점', '명화사진관', '송절동사진관']:
            self.assertIn(studio, html)
        self.assertIn('https://search.naver.com/search.naver?query=%EC%B2%AD%EC%A3%BC%20%EC%82%AC%EC%A7%84%EA%B4%80', html)
        self.assertIn('https://www.cheongju.go.kr/stat/selectBbsNttView.do?key=1763&bbsNo=539&nttNo=268480', html)


if __name__ == '__main__':
    unittest.main()
