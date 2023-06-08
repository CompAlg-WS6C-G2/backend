def calculate_weight(source, target):
    """
    Función para calcular el peso entre dos nodos

    Args:
        source : Nodo origen
        target : Nodo destino

    Returns:
        weight (int) : Peso de la arista entre los nodos
    """

    weight = 0
    source_genre = source['Genre'].split(',')
    target_genre = target['Genre'].split(',')

    common_genres = [_ for _ in source_genre if _ in target_genre]

    min_quantity_genres = min(len(source_genre), len(target_genre)) / 2

    if len(common_genres) > min_quantity_genres:
        source_country_availability = source['Country Availability'].split(',')
        target_country_availability = target['Country Availability'].split(',')

        common_countries = [
            _ for _ in source_country_availability if _ in target_country_availability]

        source_languages = source['Languages'].split(',')
        target_languages = target['Languages'].split(',')

        common_languages = [
            _ for _ in source_languages if _ in target_languages]

        # Values:
        genre_value = 1 - (len(common_genres) /
                           max(len(source_genre), len(target_genre)))
        country_availability_value = 1 - (len(common_countries) / max(
            len(source_country_availability), len(target_country_availability)))
        language_value = 1 - (len(common_languages) /
                              max(len(source_languages), len(target_languages)))
        type_value = 1 if source['Series or Movie'] != target['Series or Movie'] else 0

        weight = (genre_value + country_availability_value +
                  language_value + type_value) * 10

    return int(weight)
