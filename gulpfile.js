import gulp from "gulp";
import gulpSass from "gulp-sass";
import * as dartSass from "sass";
import postcss from "gulp-postcss";
import autoprefixer from "autoprefixer";
import cssnano from "cssnano";
import rename from "gulp-rename";
import { deleteAsync } from "del";

const { src, dest, watch, series } = gulp;
const sass = gulpSass(dartSass);

export function clean() {
  return deleteAsync([
    "static/css/bootstrap-overrides.css",
    "static/css/bootstrap-overrides.min.css",
  ]);
}

export function compileSass() {
  return src("static/scss/bootstrap-overrides.scss")
    .pipe(
      sass({
        includePaths: ["node_modules"],
        quietDeps: true,
        silenceDeprecations: ["import", "color-functions"],
      }).on("error", sass.logError),
    )
    .pipe(postcss([autoprefixer()]))
    .pipe(dest("static/css"))
    .pipe(postcss([cssnano({ preset: ["default", { svgo: false }] })]))
    .pipe(rename({ suffix: ".min" }))
    .pipe(dest("static/css"));
}

export function watchSass() {
  watch(["static/scss/**/*.scss"], compileSass);
}

export const build = series(clean, compileSass);
export default series(clean, compileSass, watchSass);
