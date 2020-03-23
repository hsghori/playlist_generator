import React from 'react';
import { ThemeProvider, makeStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import { appTheme } from './theme';


const useStyles = makeStyles({
    root: {
        height: '100%',
        width: '80%',
        marginTop: '16px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
    card: {
        width: '50%',
        marginTop: '16px',
        padding: '8px',
    },
    title: {
        fontSize: 14,
    },
});

const Login = (props) => {
    const classes = useStyles();

    return (
        <ThemeProvider theme={appTheme}>
            <CssBaseline>
                <Container className={classes.root}>
                    <Card className={classes.card}>
                        <CardContent>
                            <Typography className={classes.title} gutterBottom>
                                Log in with Spotify
                            </Typography>
                            <Typography color='textSecondary'>
                                This application requires authentication with Spotify to create playlists.
                            </Typography>
                        </CardContent>
                        <CardActions>
                            <Button
                                variant='outlined'
                                href={props.authUrl}
                            >
                                Log in
                            </Button>
                        </CardActions>
                    </Card>
                </Container>
            </CssBaseline>
        </ThemeProvider>
    );
};

Login.propTypes = {
    authUrl: PropTypes.string.isRequired,
};

export { Login };
