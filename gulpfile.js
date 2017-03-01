const gulp          = require('gulp')
const babel         = require("babelify")
const browserify    = require("browserify")
const source        = require("vinyl-source-stream")
const buffer        = require("vinyl-buffer")
const sass          = require('gulp-sass')
const plumber       = require("gulp-plumber")
const history       = require("connect-history-api-fallback")
const uglify        = require('gulp-uglify')
const browserSync   = require('browser-sync')
const reload		= browserSync.reload

// BrowserSync
gulp.task('sync', () => {
    browserSync.init({
        proxy: "tings.dev",
        middleware: [ history() ]
    })
})

// Sass
gulp.task('sass', () => {
    let outputStyle = 'compressed'
    return gulp.src('./assets/sass/**/*.sass')
    .pipe( sass({ outputStyle }).on('error', sass.logError) )
    .pipe( gulp.dest('./tings/static/css/'))
    .pipe( browserSync.reload( {stream: true} ) )
})

// Scripts
gulp.task('scripts', () => {
    return browserify("assets/js/app.js")
        .transform("babelify", {
            presets: ["es2015", "react"]
        })
        .bundle()
        .pipe(source("app.js"))
        .pipe(buffer())
        .pipe(uglify())
        .pipe(gulp.dest("./tings/static/js/"))
        .pipe(reload({stream: true}))
})

// Watch
gulp.task('watch', () => {

    gulp.watch('./assets/sass/**/*.sass', ['sass'])
    gulp.watch('./assets/js/**/*.js', ['scripts'])

})

// Default tasks
gulp.task('default', ['sync', 'scripts', 'sass', 'watch'])
gulp.task('build', ['scripts', 'sass'])
