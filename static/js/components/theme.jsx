import { createMuiTheme } from '@material-ui/core/styles';
import purple from '@material-ui/core/colors/purple';
import grey from '@material-ui/core/colors/grey';

const appTheme = createMuiTheme({
    palette: {
        type: 'dark',
        primary: purple,
        secondary: grey,
    },
});

export { appTheme };