var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');


module.exports = (env, options) => {
    return {
        context: __dirname,

        entry: {
            polyfill: 'babel-polyfill',
            main: path.resolve(__dirname, './static/js/main.js'),
            login: path.resolve(__dirname, './static/js/login.js'),
        },

        output: {
            path: path.resolve('./static/bundles/'),
            filename: '[name]-[hash].js',
        },

        plugins: [
            new CleanWebpackPlugin(),
            new BundleTracker({filename: './webpack-stats.json'}),
        ],

        module: {
            rules: [
                {
                    test: /\.(js|jsx)$/,
                    exclude: /node_modules/,
                    use: ['babel-loader'],
                },
                {
                    test: /\.css$/i,
                    use: ['style-loader', 'css-loader'],
                },

            ]
        },

        resolve: {
            extensions: ['*', '.js', '.jsx']
        }
    };
};
