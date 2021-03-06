import React from 'react';
import ReactDOM from 'react-dom';
import Cookies from 'js-cookie';
import axios from 'axios';
import { App } from './components/app';

axios.defaults.headers.common = {
    'X-CSRFToken': Cookies.get('csrftoken'),
};

ReactDOM.render(
    <App />,
    document.getElementById('app'),
);
