const gulp          = require('gulp')
const sass          = require('gulp-sass')
const uglify        = require('gulp-uglify')
const browserify    = require('browserify')
const source        = require('vinyl-source-stream')
const gutil         = require('gulp-util')
const buffer     	= require('vinyl-buffer')
const babelify      = require('babelify')
const vueify        = require('vueify')
const browserSync   = require('browser-sync')
const reload		= browserSync.reload

let bundler = browserify({ entries: 'assets/js/app.js', debug: true })
    .transform(vueify)
    .transform(babelify, { presets: ['es2015'] })

let bundleApp = () => {

    bundler.bundle()
    // listen for errors (and log them using gutil.log)
    .on('error', gutil.log)
    // then use the source function and pass it the path to the app.js file
    .pipe(source('app.js'))
    // Buffer (dunno why but that's the fix)
    .pipe(buffer())
    // uglify the output
    .pipe(gutil.env.type === "production" ? uglify() : gutil.noop())
    // then gulp.dest it
    .pipe(gulp.dest('./tings/static/js'))
    // finally reload the page
    .pipe(reload({stream: true}))

}


// BrowserSync
gulp.task('sync', () => {
    browserSync.init({
        proxy: "tings.dev"
    })
})

// Sass
gulp.task('sass', () => {
    let outputStyle = 'compressed'
    return gulp.src('./assets/sass/**/*.sass')
    .pipe( sass({ outputStyle }).on('error', sass.logError) )
    .pipe( gulp.dest('./tings/static/css'))
    .pipe( browserSync.reload( {stream: true} ) )
})

// Scripts
gulp.task('scripts', () => bundleApp() )

// Watch
gulp.task('watch', () => {

    gulp.watch('./assets/sass/**/*.sass', ['sass'])
    gulp.watch('./assets/js/**/*.js', ['scripts'])

})

// Default tasks
gulp.task('default', ['sync', 'scripts', 'sass', 'watch'])
gulp.task('build', ['scripts', 'sass'])
