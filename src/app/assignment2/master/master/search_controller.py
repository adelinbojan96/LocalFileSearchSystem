import os

from django.http import JsonResponse, HttpResponse
from django.core.cache import cache
from datetime import datetime
import requests

SLAVE_URLS = [
    'http://localhost:8001/api/search/',
    'http://localhost:8002/api/search/',
    'http://localhost:8003/api/search/',
]
def home(request):
    return HttpResponse("Master Server. Write /search/?query=WORD.")

# splitting the work in 3 since we have 3 servers
def split_into_chunks(dir_path, num_chunks=3):
    all_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path)]
    chunk_size = len(all_files) // num_chunks
    return [all_files[i:i + chunk_size] for i in range(0, len(all_files), chunk_size)]

def aggregate_results(query, dir_path):

    file_chunks = split_into_chunks(dir_path)
    results = []
    for i, url in enumerate(SLAVE_URLS):
        payload = {
            'query': query,
            'files': file_chunks[i],
        }
        try:
            # here it should ask the slaves to search
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                slave_results = response.json().get('results', [])
                results.extend(slave_results)
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
    return results

# exact matches
def rank_results(results, query):
    matches = [r for r in results if query.lower() in r.get('name', '').lower()]
    sorted_results = sorted(matches, key=lambda r: r.get('name', '').lower() == query.lower(), reverse=True)
    return sorted_results

def search_files(request):
    query = request.GET.get('query', '').strip()

    if not query:
        return JsonResponse({'error': 'Query cannot be empty'}, status=400)

    cache_key = f"search_{query}"
    cached_results = cache.get(cache_key)
    if cached_results:
        return JsonResponse({'results': cached_results, 'cached': True})

    dir_path = r'D:\SoftwareDesign_Iteartion1_LocalFileSeachSystem\src\app\assignment2\documents_to_search'

    results = aggregate_results(query, dir_path)

    ranked_results = rank_results(results, query)

    cache.set(cache_key, ranked_results, timeout=300)

    response_data = {
        'results': ranked_results,
        'timestamp': datetime.now().isoformat(),
        'total_results': len(ranked_results),
    }
    return JsonResponse(response_data)