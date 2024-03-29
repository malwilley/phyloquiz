import svelte from 'rollup-plugin-svelte'
import commonjs from '@rollup/plugin-commonjs'
import resolve from '@rollup/plugin-node-resolve'
import livereload from 'rollup-plugin-livereload'
import { terser } from 'rollup-plugin-terser'
import css from 'rollup-plugin-css-only'
import preprocess from 'svelte-preprocess'
import copy from 'rollup-plugin-copy'
import { babel } from '@rollup/plugin-babel'
import smartAsset from 'rollup-plugin-smart-asset'
import replace from '@rollup/plugin-replace'

const production = !process.env.ROLLUP_WATCH

function serve() {
  let server

  function toExit() {
    if (server) server.kill(0)
  }

  return {
    writeBundle() {
      if (server) return
      server = require('child_process').spawn(
        'npm',
        ['run', 'start', '--', '--dev'],
        {
          stdio: ['ignore', 'inherit', 'inherit'],
          shell: true,
        },
      )

      process.on('SIGTERM', toExit)
      process.on('exit', toExit)
    },
  }
}

export default {
  input: 'src/index.js',
  output: {
    sourcemap: true,
    format: 'iife',
    name: 'app',
    file: 'dist/bundle.js',
  },
  plugins: [
    replace({
      preventAssignment: true,
      values: {
        'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV),
        'process.env.SENTRY_DSN': JSON.stringify(process.env.SENTRY_DSN),
        'process.env.SENTRY_TRACES_SAMPLE_RATE': JSON.stringify(
          process.env.SENTRY_TRACES_SAMPLE_RATE,
        ),
      },
    }),

    copy({
      targets: [{ src: 'public/**/*', dest: 'dist' }],
      hook: 'writeBundle',
    }),

    svelte({
      compilerOptions: {
        // enable run-time checks when not in production
        dev: !production,
      },
      preprocess: preprocess(),
    }),

    babel({
      extensions: ['.js', '.mjs', '.html', '.svelte'],
      presets: [
        [
          '@babel/preset-env',
          {
            useBuiltIns: 'usage',
            targets: 'defaults',
            corejs: { version: '3.9', proposals: true },
          },
        ],
      ],
      include: ['src/**', 'node_modules/svelte/**'],
      babelHelpers: 'bundled',
    }),

    smartAsset({
      url: 'copy',
      assetsPath: '/assets',
      publicPath: '/assets',
      useHash: true,
      keepName: true,
    }),

    // we'll extract any component CSS out into
    // a separate file - better for performance
    css({ output: 'bundle.css' }),

    // If you have external dependencies installed from
    // npm, you'll most likely need these plugins. In
    // some cases you'll need additional configuration -
    // consult the documentation for details:
    // https://github.com/rollup/plugins/tree/master/packages/commonjs
    resolve({
      browser: true,
      dedupe: ['svelte'],
    }),

    commonjs(),

    // In dev mode, call `npm run start` once
    // the bundle has been generated
    !production && serve(),

    // Watch the `dist` directory and refresh the
    // browser on changes when not in production
    !production && livereload('dist'),

    // If we're building for production (npm run build
    // instead of npm run dev), minify
    production && terser(),
  ],
  watch: {
    clearScreen: false,
  },
}
