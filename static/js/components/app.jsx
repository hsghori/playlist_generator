import React, {useState} from 'react';
import { ThemeProvider, makeStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import Carousel from 'react-material-ui-carousel'
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import CircularProgress from '@material-ui/core/CircularProgress';
import Button from '@material-ui/core/Button';
import Input from '@material-ui/core/Input';
import CssBaseline from '@material-ui/core/CssBaseline';
import axios from 'axios';
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
    inputField: {
        marginTop: '16px',
    },
    loadingSpinner: {
        marginTop: '-88px;',
    },
    media: {
        height: 140,
        marginBottom: '16px',
    },
    playlistSection: {
        width: '80%',
        marginTop: '32px',
    }
});

const App = (props) => {
    const classes = useStyles();
    const [loading, setLoading] = useState(false);
    const [lastFmUsername, setLastFmUsername] = useState();
    const [playlistTitle, setPlaylistTitle] = useState();
    const [generatedPlaylist, setGeneratedPlaylist] = useState([]);
    const [generatedPlaylistName, setGeneratedPlaylistName] = useState();
    const [generatedPlaylistUrl, setGeneratedPlaylistUrl] = useState();
    const isButtonEnabled = !loading && lastFmUsername && playlistTitle;

    const createPlaylist = () => {
        setLoading(true);
        axios.post(
            '/create_playlist/',
            {
                lastfm_username: lastFmUsername,
                playlist_name: playlistTitle,
            }
        ).then(({data}) => {
            setGeneratedPlaylist(data.playlist.track_info);
            setGeneratedPlaylistUrl(data.playlist.url);
            setGeneratedPlaylistName(data.playlist.name);
        }).finally(() => {
            setLoading(false);
        });
    };

    const renderPlaylist = () => {
        if (generatedPlaylist.length === 0) {
            return null;
        }
        const playlistCards = generatedPlaylist.map(({title, artists, link, image}) => {
            return (
                <Card>
                    <CardContent>
                        <CardMedia
                            className={classes.media}
                            image={image.url}
                        />
                        <Typography>
                            {title}
                        </Typography>
                        <Typography>
                            by {artists}
                        </Typography>
                    </CardContent>
                    <CardActions>
                        <Button
                            target='_blank'
                            variant='outlined'
                            href={link}
                        >
                            Listen on Spotify
                        </Button>
                    </CardActions>
                </Card>
            );
        })

        return (
            <div className={classes.playlistSection}>
                <Card>
                    <CardContent>
                        <Typography>
                           {generatedPlaylistName}
                        </Typography>
                    </CardContent>
                    <CardActions>
                        <Button
                            target='_blank'
                            href={generatedPlaylistUrl}
                            variant='outlined'
                        >
                            View on Spotify
                        </Button>
                    </CardActions>
                </Card>
                <Carousel
                    autoPlay={true}
                    indicators={false}
                    animation='slide'
                >
                    {playlistCards}
                </Carousel>
            </div>
        )
    }

    return (
        <ThemeProvider theme={appTheme}>
            <CssBaseline>
                <Container className={classes.root}>
                    <Card>
                        <CardContent>
                            <Typography>
                                Create a playlist
                            </Typography>
                            <Input
                                autoFocus={true}
                                fullWidth={true}
                                name='username'
                                id='id_username'
                                className={classes.inputField}
                                placeholder='LastFM username'
                                onChange={(e) => {
                                    setLastFmUsername(e.target.value);
                                }}
                            />
                            <Input
                                fullWidth={true}
                                name='playlist'
                                id='id_playlist'
                                className={classes.inputField}
                                placeholder='Playlist title'
                                onChange={(e) => {
                                    setPlaylistTitle(e.target.value);
                                }}
                            />
                        </CardContent>
                        <CardActions>
                            <Button
                                variant='outlined'
                                onClick={createPlaylist}
                                disabled={!isButtonEnabled}
                            >
                                Create playlist
                            </Button>
                        </CardActions>
                    </Card>
                    {loading && <CircularProgress className={classes.loadingSpinner} size={36} />}
                    {renderPlaylist()}
                </Container>
            </CssBaseline>
        </ThemeProvider>
    );
};

App.propTypes = {};

export { App };
