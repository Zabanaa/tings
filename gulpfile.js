const gulp          = require('gulp')
const sass          = require('gulp-sass')
const uglify        = require('gulp-uglify')
const browserSync   = require('browser-sync')
const reload		= browserSync.reload

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
    .pipe( gulp.dest('./tings/static/css/'))
    .pipe( browserSync.reload( {stream: true} ) )
})

// Scripts
gulp.task('scripts', () => {

    return gulp.src("./assets/js/*.js")
        .pipe( uglify() )
        .pipe(gulp.dest("./tings/static/js/"))
        .pipe( browserSync.reload( {stream: true} ) )
})

// Watch
gulp.task('watch', () => {

    gulp.watch('./assets/sass/**/*.sass', ['sass'])
    gulp.watch('./assets/js/**/*.js', ['scripts'])

})

// Default tasks
gulp.task('default', ['sync', 'scripts', 'sass', 'watch'])
gulp.task('build', ['scripts', 'sass'])
