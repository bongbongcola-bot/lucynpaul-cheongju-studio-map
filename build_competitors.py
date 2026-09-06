from pathlib import Path
import re, json

source = Path('/tmp/naver_cheongju_photo.html').read_text()
ids = re.findall(r'PlaceListBusinessesItem:(\d+):\1', source)
items = []
seen = set()
for business_id in ids:
    if business_id in seen:
        continue
    seen.add(business_id)
    start = source.find(f'PlaceListBusinessesItem:{business_id}:{business_id}')
    section = source[start:start + 18000]
    def field(key):
        match = re.search(rf'\\?"{key}\\?":\\?"(.*?)\\?"', section)
        return match.group(1).replace('\\u002F', '/').replace('\\u0026', '&') if match else ''
    route = field('routeUrl')
    coordinate = re.search(r'longitude%5E([0-9.]+)%3Blatitude%5E([0-9.]+)', route)
    name = field('name')
    if not name or not coordinate:
        continue
    lon, lat = coordinate.groups()
    items.append({
        'id': business_id,
        'name': name,
        'district': field('commonAddress'),
        'address': field('roadAddress'),
        'category': field('category'),
        'lat': float(lat),
        'lon': float(lon),
        'naver_url': f'https://map.naver.com/p/entry/place/{business_id}',
    })

out = Path(__file__).parent / 'data' / 'cheongju-photo-studios.json'
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps({
    'source_query': '청주 사진관',
    'retrieved': '2026-09-06',
    'source': 'https://search.naver.com/search.naver?query=%EC%B2%AD%EC%A3%BC%20%EC%82%AC%EC%A7%84%EA%B4%80',
    'scope_note': '검색 결과 첫 화면의 네이버 플레이스 7개이며 청주 전체 사업자 목록이 아닙니다. 영업 여부·가격·서비스는 방문 전 해당 업체 페이지에서 재확인해야 합니다.',
    'studios': items,
}, ensure_ascii=False, indent=2))
print(json.dumps(items, ensure_ascii=False, indent=2))
