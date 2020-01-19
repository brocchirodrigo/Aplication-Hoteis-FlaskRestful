def normalize_path_params(cidade=None,
                          estrelas_min = 0,
                          estrelas_max = 5,
                          diarias_min = 0,
                          diarias_max = 10000,
                          limit = 50,
                          offset = 0, **dados):
    if cidade:
        return {'estrelas_min': estrelas_min,
                'estrelas_max': estrelas_max,
                'diarias_min': diarias_min,
                'diarias_max': diarias_max,
                'cidade': cidade,
                'limit': limit,
                'offset': offset}
    return {'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diarias_min': diarias_min,
            'diarias_max': diarias_max,
            'limit': limit,
            'offset': offset}

consulta_sem_cidade = "SELECT * FROM hoteis \
WHERE (estrelas >= ? and estrelas <= ?) \
and (diarias >= ? and diarias <= ?) \
LIMIT ? OFFSET ?"

consulta_com_cidade = "SELECT * FROM hoteis \
WHERE (estrelas >= ? and estrelas <= ?) \
and (diarias >= ? and diarias <= ?) \
and cidade = ? \
LIMIT ? OFFSET ?"