import requests
import json
import logging as log


class LastFM:
    """
    Wrapper class around the last fm api.
    """
    url_root = 'http://ws.audioscrobbler.com'

    def __init__(self, api_key):
        self.api_key = api_key

    def get_user_top_tracks(self, user, keys=None, **query_params):
        """
        Gets the top tracks for a specific user.

        :param user: The username
        :type user: str
        :param keys: Any specific keys to query for, defaults to None
        :param keys: list, optional
        :return: A list of tracks
        :rtype: list
        """

        method, head = 'user.gettoptracks', ('toptracks', 'track')
        user = user.lower().replace(' ', '')
        query_params.update({'user': user})
        return self._process_request(method, head, keys, **query_params)

    def get_top_artists(self, user, keys=None, **query_params):
        """
        Gets the top artists for a specific user.

        :param user: The username
        :type user: str
        :param keys: Any specific keys to query for, defaults to None
        :param keys: list, optional
        :return: A list of artists
        :rtype: list
        """

        method, head = 'user.gettopartists', ('topartists', 'artist')
        query_params.update({'user': user})
        return self._process_request(method, head, keys, **query_params)

    def get_similar_artists(self, artist, keys=None, **query_params):
        """
        Gets artists similar to a specific artist.

        :param user: The username
        :type user: str
        :param keys: Any specific keys to query for, defaults to None
        :param keys: list, optional
        :return: A list of artists
        :rtype: list
        """
        method, head = 'artist.getsimilar', ('similarartists', 'artist')
        artist = artist.replace(' ', '+')
        query_params.update({'artist': artist})
        return self._process_request(method, head, keys, **query_params)

    def get_top_tracks_by_artist(self, artist, keys=None, **query_params):
        """
        Gets the top tracks for a specific artist.

        :param user: The username
        :type user: str
        :param keys: Any specific keys to query for, defaults to None
        :param keys: list, optional
        :return: A list of artists
        :rtype: list
        """
        method, head = 'artist.gettoptracks', ('toptracks', 'track')
        artist = artist.replace(' ', '+')
        query_params.update({'artist': artist})
        return self._process_request(method, head, keys, **query_params)

    def _process_request(self, method, head, keys, **kwargs):
        query = self._build_query(**kwargs)
        url, data = self._get(method, query)
        error_message = None
        if head[0] in data:
            data = data[head[0]]
            if head[1] in data:
                data = data[head[1]]
            else:
                error_message = u'Unexpected response format. {} not the inner field.\n{}'.format(head[
                                                                                                  1], url)
                log.error(error_message)
            if keys:
                data = [{key: track[key] for key in keys if key in track}
                        for track in data]
        else:
            error_message = u'Unexpected response format. {} not the outer field.\n{}'.format(head[
                                                                                              0], url)
            log.error(error_message)
        if error_message:
            return {'error': error_message}
        return data

    def _build_query(self, **kwargs):
        if kwargs:
            query_params = [u'{key}={val}'.format(
                key=key, val=kwargs[key]) for key in kwargs]
            query_params.append('api_key={}&format=json'.format(self.api_key))
            return '&'.join(query_params)
        return ''

    def _get(self, method, query):
        url = u'{root}/2.0/?method={method}&{query}'.format(
            root=self.url_root,
            method=method,
            query=query)
        response = requests.get(url)
        if response.status_code == 200:
            return url, json.loads(response.content)
        raise Exception(
            'Status {} -> {}\n{}'.format(response.status_code, response.content, url))
