const { src, dest, watch, series } = require("gulp");
const sass = require("gulp-sass")(require("sass"));
const cleanCSS = require("gulp-clean-css");
const rename = require("gulp-rename");
const { deleteAsync } = require("del");

function clean() {
  return deleteAsync(["static/css/*"]);
}

function compileSass() {
  return src("static/scss/bootstrap-overrides.scss")
    .pipe(
      sass({
        includePaths: ["node_modules"],
        quietDeps: true,
        silenceDeprecations: ["import", "color-functions"],
      }).on("error", sass.logError)
    )
    .pipe(dest("static/css"))
    .pipe(cleanCSS())
    .pipe(rename({ suffix: ".min" }))
    .pipe(dest("static/css"));
}

function watchSass() {
  watch(["static/scss/**/*.scss"], compileSass);
}

exports.build = series(clean, compileSass);
exports.default = series(clean, compileSass, watchSass);
