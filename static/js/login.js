import React from 'react';
import ReactDOM from 'react-dom';
import Cookies from 'js-cookie';
import axios from 'axios';
import { Login } from './components/login';

axios.defaults.headers.common = {
    'X-CSRFToken': Cookies.get('csrftoken'),
};

ReactDOM.render(
    <Login authUrl={spotifyAuthUrl} />,
    document.getElementById('app'),
);
